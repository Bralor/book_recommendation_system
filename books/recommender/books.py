from recommender.book_recommender.df_processor import FrameProcessor
from recommender.book_recommender.df_preprocessor import Preprocessor


def run_recommender(query: str, df) -> list:
    """
    With this script, run the recommendation system.

    :query: str -> "the fellowship of the ring",
    :df: pandas.data.frame.DataFrame
    :return: list -> [{}, {}, {}]
    """
    prep = Preprocessor()
    prep.run_preprocessing()

    books = FrameProcessor(query, df)
    return books.start_session()

