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
     ├─test_processor.py
     ├─test_processor.py
     ├─test_utils.py
     └─data/
```

<br>

##### Pros and cons

---

+ ready2run,
+ a lot of `pandas` utilities (but some obsolete),
- hard-coded solution,
- no room for:
    - testing,
    - documentation (docstrings -> sphinx),
    - improvements,
    - upgrades.

<br>

#### Updated solution

---


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

Collect the remote data:
```
$ ./collector
> Getting books...
> Getting ratings...
> Completed!
```

Run the localhost:
```
cd books/
python manage.py runserver
```

#### Usage
Write the name of the book you like:
```
"harry potter and the sorcerer's stone (book 1)"
...
```

The result will be books that appeal to users with a similar interest.
