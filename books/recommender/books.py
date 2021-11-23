from recommender.df_processor import FrameProcessor


def run_recommender(query: str, df) -> list:
    """
    With this script, run the recommendation system.

    :query: str -> "the fellowship of the ring",
    :df: pandas.data.frame.DataFrame
    :return: list -> [{}, {}, {}]
    """
    books = FrameProcessor(query, df)
    return books.start_session()

