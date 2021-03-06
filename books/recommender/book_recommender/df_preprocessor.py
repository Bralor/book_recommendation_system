import os
import logging
import zipfile
import sqlite3

import requests

from recommender.book_recommender.df_utils import merge_two_dfs
from recommender.book_recommender.df_utils import load_dataframe_with_lowercase


class DatabaseCreator:
    """Create a new database if there is none."""

    def __init__(self, name: str, path: str):
        self.name = name
        self.path = path

    def is_db_available(self):
        return os.path.isfile(self.name)

    def create_new_table(self, db_table):
        """If there is no such table, create one."""
        conn = sqlite3.connect(self.name)
        c = conn.cursor()

        c.execute("""
        CREATE TABLE IF NOT EXISTS collection (
          id integer primary key,
          ISBN text,
          UserID text,
          BookRating text,
          BookTitle text,
          BookAuthor text,
          YearOfPublication text,
          Publisher text,
          ImageURLS text,
          ImageURLM text,
          ImageURLL text
        )
        """
        )
        conn.commit()

        db_table.to_sql(
            'collection', conn, if_exists='replace',
            index=True, index_label="id"
        )


class DataDownloader:
    """Get the csv dataset from the web."""

    def __init__(self, zip_name: str):
        self.zip_name = zip_name
        self.path: str = "recommender/book_recommender/data"
        self.url: str = \
           "http://www2.informatik.uni-freiburg.de/~cziegler/BX/BX-CSV-Dump.zip"

    def is_there_zip(self):
        return os.path.exists(
            os.path.join(self.path, self.zip_name)
        )

    def download_data(self):
        """Download the source zip file if there is none."""
        return requests.get(self.url)


class ZipManager:
    def __init__(self):
        self.zip_name: str = "books.zip"
        self.books: str = "BX-Books.csv"
        self.ratings: str = "BX-Book-Ratings.csv"
        self.path: str = "recommender/book_recommender/data"
        self.new_zip = os.path.join(self.path, self.zip_name)

    def write_zip_file(self, data: bytes) -> None:
        """Save the downloaded data as zip file."""
        with open(self.new_zip, "wb") as zip_f:
            zip_f.write(data)

    def open_zip_file(self):
        return zipfile.ZipFile(self.new_zip)

    def collect_csv_files(self, zfile):
        """Try to collect the csv files."""
        try:
            books = zfile.open(self.books)
            ratings = zfile.open(self.ratings)

        except Exception:
            print("Some error")
        else:
            return books, ratings


class Preprocessor:
    """Run the continuous preprocessor."""

    def run_preprocessing(self):
        fmt="[%(levelname)s] %(asctime)s - %(message)s"
        logging.basicConfig(level=logging.DEBUG, format=fmt)

        db = DatabaseCreator("ratings.sqlite3", ".")
        source = DataDownloader("books.zip")
        writer = ZipManager()

        if not db.is_db_available():
            logging.info("DB is not available..")

            if not source.is_there_zip():
                logging.info("Dataset is not available..")
                response = source.download_data()
                writer.write_zip_file(response.content)
                logging.info("Dataset downloaded..")

            logging.info("Dataset is available..")

            books, ratings = writer.collect_csv_files(writer.open_zip_file())
            logging.info(".csv file extracted..")

            books = load_dataframe_with_lowercase(books)
            ratings = load_dataframe_with_lowercase(ratings)
            logging.info("Dataframes created..")

            collection = merge_two_dfs(books, ratings)
            logging.info("Dataframes merged..")


            db.create_new_table(collection)
            logging.info("DB table created..")

        else:
            logging.info("DB already created..")
