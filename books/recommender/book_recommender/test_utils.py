import pytest

import pandas

from recommender.book_recommender.df_utils import merge_two_dfs
from recommender.book_recommender.df_utils import load_dataframe_with_lowercase


class TestLoadingNewDataframes:

    def setup(self):
        self.df1: str = "recommender/book_recommender/test_csv_1.csv"
        self.df2: str = "recommender/book_recommender/test_csv_2.csv"


    def test_correct_loading_of_the_first_dataframe(self):
        df1 = load_dataframe_with_lowercase(self.df1)
        assert len(df1.values.tolist()[0]) == 8

    def test_correct_loading_of_the_second_dataframe(self):
        df2 = load_dataframe_with_lowercase(self.df2)
        assert len(df2.values.tolist()[0]) == 3

    def test_incorrect_loading_the_dataframes(self):
        with pytest.raises(FileNotFoundError):
            load_dataframe_with_lowercase("foo/bar/test.csv")

    def test_merging_two_existing_dataframes(self):
        a = pandas.DataFrame({'id': [1], 'ISBN': ["1234"], "name": ["Matous"]})
        b = pandas.DataFrame({'ISBN': ["1234"], "surname": ["Svatous"]})
        merged = merge_two_dfs(a, b)
        assert len(merged.values.tolist()[0]) == 4

