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
class Preprocessor:
    """Simple preprocessing representation."""

    def is_db_available(self):
        pass

    def download_data(self):
        pass

    def extract_data(self):
        pass


class DfProcessor:
    """Process dataframe operations."""

    def run_recommender(self):
        pass


class ResultParser:
    """From the given data, return the selected values."""

    def read_data(self):
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
    DB already available..
    Processing..
    """
```

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
     ├─test_processor.py
     ├─test_preprocessor.py
     ├─test_parser.py
     └─data/
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

Install the list of frameworks and packages (using pip):
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
"harry potter and the sorcerer's stone (book 1)"
...
```

The result will be books that appeal to users with a similar interest.
