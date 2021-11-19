### Books
It is a web-project that creates a relation database system of book evaluations
from the obtained source and recommends works according to the evaluations.

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
lord of the rings
```

The result will be books that appeal to users with a similar interest.
