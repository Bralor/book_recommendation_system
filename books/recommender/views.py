from django.db.models import Q
from django.shortcuts import render
from django.views.generic import TemplateView, ListView

from .models import Collection


class HomePageView(TemplateView):
    template_name = "home.html"


class SearchResultsView(ListView):
    model = Collection
    template_name = "search_results.html"

    def get_queryset(self):
        query = self.request.GET.get('q')
        object_list = Collection.objects.filter(
            Q(book_title__icontains=query)
        )
        # object_list = [
            # {'book_author': 'george orwell',
             # 'isbn': '0451524934',
             # 'book_rating': 8.73,
             # 'book_title': '1984'},
            # {'book_author': 'john grisham',
             # 'isbn': '0440211727',
             # 'book_rating': 8.56,
             # 'book_title': 'a time to kill'},
            # {'book_author': 'john grisham',
              # 'isbn': '038550120x',
             # 'book_rating': 8.44,
             # 'book_title': 'a painted house'},
            # {'book_author': "madeleine l'engle",
             # 'isbn': '0440498058',
             # 'book_rating': 8.36,
             # 'book_title': 'a wrinkle in time'},
            # {'book_author': 'dan brown',
             # 'isbn': '0743486226',
             # 'book_rating': 8.3,
             # 'book_title': 'angels &amp; demons'},
            # {'book_author': 'james patterson',
             # 'isbn': '0446610038',
             # 'book_rating': 8.0,
             # 'book_title': '1st to die: a novel'},
        # ]
        return object_list


# def index(request):
    # books = Collection.objects.all()
    # context = {
        # "books": books
    # }
    # return render(request, 'index.html', context)

