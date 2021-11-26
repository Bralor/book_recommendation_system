### Books

---

It is a web-project that creates a relation database system of book evaluations
from the obtained source and recommends works according to the evaluations.

<br>

#### Parts of project

---

1. `SQLite` - data storage,
2. `Django` - web framework,
3. `book_recommender` - Python book recommendation package.

<br>

#### Project scheme

---

```
┌──────┐    ┌─────────────────────────┐    ┌────────────────┐
| User |<──>| HTML+Bootstrap:frontend |<──>| Django:backend |
└──────┘    └─────────────────────────┘    └────────────────┘
                                              |           |
                                              |           |
                                              |           |
                                              V           V
                           ┌──────────────────────┐    ┌──────────────────────────┐
                           |        SQLite        |<───| Python: book_recommender |
                           └──────────────────────┘    └──────────────────────────┘
```

<br>

#### Junior's solution

---

```
/root
  ├─book.py
  └─book_recommender
     ├─df_preprocessor.py  # data preparation module
     ├─df_processor.py     # book_rec.py
     ├─df_utils.py         # some useful utilities
     ├─test_preprocessor.py
     ├─test_utils.py
     └─data/
```

<br>

##### Pros and cons

---

+ ✅ ready2run,
+ ✅ a lot of `pandas` utilities (but some obsolete),
- ❌ hard-coded solution,
- ❌ no room for:
    - ❌ testing,
    - ❌ documentation (docstrings -> sphinx),
    - ❌ improvements,
    - ❌ upgrades.

<br>

#### Updated solution

---

Used pattern: structural design pattern **facade**. See the simple example:
```python
class DataframePreprocessor:
    """Check database, prepare it if it is not available."""

    def is_db_available(self, db_name: str) -> bool:
        pass

    def download_data(self, url: str) -> requests.model.Response:
        pass

    def extract_data(self, filename: str) -> zipfile.ZipFile:
        pass


class DataframeProcessor:
    """Process dataframe operations with specific users and ratings."""

    def run_recommender(self, df) -> pandas.core.frame.DataFrame:
        pass


class ResultParser:
    """From the given data, return the selected values."""

    def read_data(self, df) -> list:
        return f"Suggestions {}"


class RecommenderFacade:
    """Represents a facade for various computer parts."""

    def __init__(self):
        self.prep = Preprocessor()
        self.proc = DfProcessor()
        self.reader = ResultParser()

    def start(self):
        if not self.prep.is_db_available():
           self.prep.extract_data(
               self.prep.download_data()
           )

        self.proc.run_recommender()
        self.reader.read_data()


def main():
    """
    >>> recommender = RecommenderFacade()
    >>> recommender.start()
    [INFO] DB already available..
    [INFO] Processing..
    """
```

<br>

Better solution of module `book_rec.py`:
```python
def load_dataframe_with_lowercase(name: str) -> pandas.core.frame.DataFrame:
    """Load dataframe from .csv file as a lowecase strings."""
    return pandas.read_csv(
        name,
        encoding="cp1251",
        sep=";",
        on_bad_lines="skip",
        index_col=False,
        dtype='unicode'
    ).apply(lambda x: x.astype(str).str.lower())


def merge_two_dfs(
    df1: pandas.core.frame.DataFrame,
    df2: pandas.core.frame.DataFrame,
    key: str ="ISBN"):
    return pandas.merge(df1, df2, on=[key])


def select_all_readers_of_one_author_and_book(
      title: str,
      author: str,
      col: pandas.core.frame.DataFrame
   ) -> pandas.core.frame.DataFrame:

    return col["User-ID"][
        (col["Book-Title"] == title)
        & filter_dataframe(col, "Book-Author", author)
    ]


def filter_dataframe(col: pandas.core.frame.DataFrame, key: str, val: str):
    return col[key].str.contains(val)


def all_books_from_readers(col, key, filtered):
    return col[col[key].isin(filtered)]


def sum_of_ratings_of_each_book(other_books, column):
    return other_books.groupby([column]).agg("count").reset_index()


def filter_titles_with_threshold(sum_ratings, title, threshold):
    return sum_ratings[title][sum_ratings["User-ID"] >= threshold].tolist()


def create_new_dataframe_from_values(col, columns, filtered):
    return col[columns][col["Book-Title"].isin(filtered)]


def calculate_the_mean_val(new_df, vals, key):
    return new_df.groupby(vals)[key].mean().to_frame().reset_index()
```
Short but useful functions can provide a testable solution.

<br>

Package structure:
```
/root
  ├─book.py
  └─book_recommender
     ├─facade.py
     ├─processor.py
     ├─preprocessor.py
     ├─data_parser.py
     ├─data/
     └─tests/
        ├─test_preprocessor.py
        ├─test_processor.py
        └─test_parser.py
```

<br>

#### Installation
Clone the repository:
```
$ git clone https://github.com/Bralor/book_recommender_system
```

Create a virtual enviroment:
```
$ python -m venv env
```

Install the given list of frameworks and packages (using pip):
```
$ pip install -r requirements.txt
```

Run the localhost:
```
cd books/
python manage.py runserver
[INFO] DB is not available ..
[INFO] Dataset downloading ..
...
```

#### Usage
Write the name of the book you like:
```
harry potter and the sorcerer's stone (book 1)
the fellowship of the ring (the lord of the rings, part 1)
...
```

The result will be books that appeal to users with a similar interest.
