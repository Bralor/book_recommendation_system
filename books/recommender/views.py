from django.db.models import Q
from django.views.generic import TemplateView, ListView

from .models import Collection


class HomePageView(TemplateView):
    template_name: str = "home.html"


class SearchResultsView(ListView):
    model = Collection
    template_name: str = "search_results.html"

    def get_queryset(self):
        query = self.request.GET.get('q')
        object_list = Collection.objects.filter(
            Q(book_title__icontains=query)
        )

        # return get_recommendations(
            # object_list = Collection.objects.filter(
                # Q(book_title__icontains=query)
            # )
        # )

        # pandas.DataFrame(list(object_list))


        return object_list

