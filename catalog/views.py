from django.shortcuts import render
from django.http import HttpResponse
from .models import Book, Author, BookInstance, Genre, Language
from django.views import generic
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin



class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    """Generic class-based view listing books on loan to current user."""
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        member = self.request.user
        if  member.groups.filter(name="Librarians").exists():
            return (BookInstance.objects.all()
                    .filter(status__exact='o')
                    .order_by('due_back'))
        else:
            return (BookInstance.objects.filter(borrower = member)
                    .filter(status__exact='o')
                    .order_by('due_back'))

    def get_context_data(self, *args, **kwargs):
        context = super(LoanedBooksByUserListView, self).get_context_data(*args,**kwargs)
        context['islibrarian'] = self.request.user.groups.filter(name="Librarians").exists()
        return context




@login_required
def index(request):
    """View function for home page of site."""

    # Generate counts of some of the main objects
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()

    # Available books (status = 'a')
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()

    # The 'all()' is implied by default.
    num_authors = Author.objects.count()
    
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_visits': num_visits,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'catalog/index.html', context=context)


def dbmaint(request):
    num_visits_2 = request.session.get('num_visits_2', 0)
    request.session['num_visits_2'] = num_visits_2 + 1
    return render(request, 'catalog/dbmaint.html', {"num_visits_2": num_visits_2})


class BookListView(generic.ListView):
    model = Book
    context_object_name = 'book_list'
    queryset = Book.objects.all()[:20]
    template_name = "book/book_list"
    paginate_by = 10


class BookDetailView(generic.DetailView):
    model = Book


class GenreListView(LoginRequiredMixin, generic.ListView):
    model = Genre


class LanguageListView(generic.ListView):
    model = Language


def book_detail(request, pk):
    book = Book.objects.get(pk=pk)
    return HttpResponse(f"{book}, Under construction, be patient please ...")


class AuthorDetailView(generic.DetailView):
    model = Author


class AuthorListView(generic.ListView):
    model = Author
    paginate_by = 10



## forms tutorial

import datetime

from django.shortcuts import render, get_object_or_404
from django.http      import HttpResponseRedirect
from django.urls      import reverse
from catalog.forms    import RenewBookForm, RenewBookModelForm


@login_required
@permission_required('catalog.can_mark_returned', raise_exception=True)
def renew_book_librarian(request, pk):
    book_instance = get_object_or_404(BookInstance, pk=pk)

    # If this is a POST request then process the Form data
    if  request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = RenewBookModelForm(request.POST)

        # Check if the form is valid:
        if  form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            #book_instance.due_back = form.cleaned_data['renewal_date']    # use this one with regular form  
            book_instance.due_back = form.cleaned_data['due_back']         # use this one with ModelForm
            book_instance.save()

            # redirect to a new URL:
            return HttpResponseRedirect(reverse('catalog:my-borrowed'))

    # If this is a GET (or any other method) create the default form.
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        #form = RenewBookForm(initial={'renewal_date': proposed_renewal_date})   # use this one with regular form.Form
        form = RenewBookModelForm(initial={'due_back': proposed_renewal_date})   # use this one with ModelForm

    context = {'form'         : form,
               'book_instance': book_instance,}

    return render(request, 'catalog/renew-book-librarian.html', context)





from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from catalog.models import Author

class AuthorCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Author
    fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']
    initial = {'date_of_death': '11/06/2020'}
    permission_required = "catalog.add_author"

class AuthorUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Author
    fields = '__all__' # Not recommended (potential security issue if more fields added)
    permission_required = "catalog.change_author"

class AuthorDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Author
    success_url = reverse_lazy('catalog:authors')
    permission_required = "catalog.delete_author"

from catalog.models import Book

class BookCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    fields = "__all__"
    model = Book

class BookUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Book
    fields = '__all__' # Not recommended (potential security issue if more fields added)

class BookDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Book
    fields = "__all__"
    success_url = reverse_lazy('catalog:books')

