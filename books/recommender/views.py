from django.db.models import Q
from django.views.generic import TemplateView, ListView

from .models import Collection
from recommender.books import run_recommender
from recommender.book_recommender.df_preprocessor import Preprocessor


class HomePageView(TemplateView):
    template_name: str = "home.html"


class SearchResultsView(ListView):
    model = Collection
    template_name: str = "search_results.html"

    prep = Preprocessor()
    prep.run_preprocessing()

    def get_queryset(self):
        """
        Get query from the given form. Then process the input and render
        the ResultView.
        """
        query = self.request.GET.get('q')
        object_list = Collection.objects.all()

        result = run_recommender(
            query,
            object_list,
        )

        return result

