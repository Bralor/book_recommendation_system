import os
import pytest

from pytest_mock import mocker

from recommender.book_recommender.df_preprocessor import ZipManager
from recommender.book_recommender.df_preprocessor import DataDownloader
from recommender.book_recommender.df_preprocessor import DatabaseCreator


class TestDatabaseCreator:

    def setup(self):
        """Setup a new testing instance."""
        db_name: str = "ratings.sqlite3"
        db_path: str = "recommender/book_recommender/data"
        self.test = DatabaseCreator(db_name, db_path)

    def test_if_the_sql_exist(self):
        """Check if the .sqlite3 file exists on the given path."""
        assert self.test.is_db_available()

    def test_if_the_sql_does_not_exist(self):
        self.test.name = "foo.sqlite3"

        with pytest.raises(AssertionError):  # incorrect file name
            assert self.test.is_db_available()


class TestDataDownloader:

    def setup(self):
        zip_file: str = "books.zip"
        self.test = DataDownloader(zip_file)

    def test_the_correct_class_attribute_url(self):
        assert self.test.url == \
            "http://www2.informatik.uni-freiburg.de/~cziegler/BX/BX-CSV-Dump.zip"

    def test_if_there_is_no_zip_file(self):
        with pytest.raises(AssertionError):  # no archive downloaded yet
            assert self.test.is_there_zip()

    def test_the_downloading_the_data(self, mocker):
        """Mock the method 'download_data' and test the output."""
        mocker.patch(
            "recommender.book_recommender.df_preprocessor.DataDownloader.download_data",
            return_value='<Response [200]>'
        )
        assert self.test.download_data() == '<Response [200]>'


class TestZipManager:

    def setup(self):
        self.test = ZipManager()

    def test_the_correct_class_attribute(self):
        assert self.test.zip_name == "books.zip"

    def test_the_incorrect_class_attribute(self):
        assert self.test.zip_name != "foo.zip"

    def test_the_correct_class_attribute_file_zip(self):
        assert self.test.new_zip == "recommender/book_recommender/data/books.zip"

    def test_the_incorrect_class_attribute_file_zip(self):
        assert self.test.new_zip != "foo/bar/data/books.zip"

    def test_is_the_source_folder_empty(self):
        assert not os.path.exists(self.test.new_zip)


class TestZipManagerArchive:

    def setup(self):
        self.test = ZipManager()

    def test_the_writting_of_the_zip_file(self):
        self.test.write_zip_file(b"1234")
        assert os.path.exists(self.test.new_zip)

    def test_the_zip_file_is_not_available(self):
        os.remove(self.test.new_zip)
        assert not os.path.exists(self.test.new_zip)

