# API Development and Documentation Final Project_Trivia App

## Introduction

This is an awesome game in which users can test their knowledge by answering some cool questions. It is one which can be easily set up with a local machine.

Let's Jump right in!!!

---
## Getting Started
The frontend of the application was developed with create-react-app; while the backend runs on flask. 

For the best experience, setup and start the backend before running the frontend.

### Prerequisites

To use this project, make sure that you have Python3, Pip, postgres, Npm and Node Js installed.

<br>

---
## Frontend

#### Dependencies
To start up the frontend, simply navigate to the /frontend directory and run this command in bash:

```bash
npm install
```

To run the application in development mode, run this command:

```` 
npm start
````

Open http://localhost:3000 to view the project in the browser.
> View the [Frontend README](./frontend/README.md) for more details.
---
## Backend

In the /backend directory, initialize and activate a virtual environment:

```
python -m virtualenv env

```

Then run this command to activate the virtual environment:

````
source env/bin/activate

````

>**Note** - In Windows OS, the `env` `bin` directory is absent; use this command instead:

````
env/Scripts/activate.bat
````

#### Dependencies
Then run this command to install the necessary dependencies.

```bash
pip install -r requirements.txt
```

>**Alternatively** You can install the dependencies manually:

````
pip install Flask
pip install psycopg2
pip install -U flask-cors
pip install Flask-SQLAlchemy
````

#### Set Up and Populate the Database
With Postgres running, create a trivia database:

````
createdb trivia
````

>**Note** For windows users, run this command instead:

````
CREATE DATABASE trivia;
````

Then, from the backend folder in the terminal, populate the database using the trivia.psql file that is provided. Run this command:

````
psql trivia < trivia.psql

````
#### Start the Server
In the backend directory, start the Flask server by running:

````
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
````
>**Note** For windows users, run this command instead:

````
set FLASK_APP=flaskr
set FLASK_ENV=development
flask run
````
> View the [Backend README](./backend/README.md) for more details.
<br>

---
## Testing

To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```
Omit the dropdb command the first time you run tests.

>**For Windows users, use `CREATE DATABASE` and `DROP DATABASE` clause instead.

<br>

---
## API Reference
---
### Getting Started

* Base URL: Currently this application is only hosted locally. The backend is hosted at `http://127.0.0.1:5000/`
* Authentication: This version does not require authentication or API keys.

### Error Handling

Errors are returned as JSON in the following format:
<br>

    {
        "success": False,
        "error": 404,
        "message": "resource not found"
    }

The API will return three types of errors:

* 400 – bad request
* 404 – resource not found
* 422 – unprocessable
* 500 - server error
<br>


---
### Expected endpoints and behaviors

`GET '/categories'`

- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, categories, that contains an object of id: category_string key:value pairs.

```json
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  }
}
```

---

`GET '/questions?page=${integer}'`

- Fetches a paginated set of questions, a total number of questions, all categories and current category string.
- Request Arguments: `page` - integer
- Returns: An object with 10 paginated questions, total questions, object including all categories, and current category string

```json
{
  "questions": [
    {
      "id": 1,
      "question": "This is a question",
      "answer": "This is an answer",
      "difficulty": 5,
      "category": 2
    }
  ],
  "totalQuestions": 100,
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "currentCategory": "History"
}
```

---

`GET '/categories/${id}/questions'`

- Fetches questions for a cateogry specified by id request argument
- Request Arguments: `id` - integer
- Returns: An object with questions for the specified category, total questions, and current category string

```json
{
  "questions": [
    {
      "id": 1,
      "question": "This is a question",
      "answer": "This is an answer",
      "difficulty": 5,
      "category": 4
    }
  ],
  "totalQuestions": 100,
  "currentCategory": "History"
}
```

---

`DELETE '/questions/${id}'`

- Deletes a specified question using the id of the question
- Request Arguments: `id` - integer
- Returns: Does not need to return anything besides the appropriate HTTP status code. Optionally can return the id of the question. If you are able to modify the frontend, you can have it remove the question using the id instead of refetching the questions.

---

`POST '/quizzes'`

- Sends a post request in order to get the next question
- Request Body:

```json
{
    'previous_questions': [1, 4, 20, 15]
    quiz_category': 'current category'
 }
```

- Returns: a single new question object

```json
{
  "question": {
    "id": 1,
    "question": "This is a question",
    "answer": "This is an answer",
    "difficulty": 5,
    "category": 4
  }
}
```

---

`POST '/questions'`

- Sends a post request in order to add a new question
- Request Body:

```json
{
  "question": "Heres a new question string",
  "answer": "Heres a new answer string",
  "difficulty": 1,
  "category": 3
}
```

- Returns: Does not return any new data

---

`POST '/questions'`

- Sends a post request in order to search for a specific question by search term
- Request Body:

```json
{
  "searchTerm": "this is the term the user is looking for"
}
```

- Returns: any array of questions, a number of totalQuestions that met the search term and the current category string

```json
{
  "questions": [
    {
      "id": 1,
      "question": "This is a question",
      "answer": "This is an answer",
      "difficulty": 5,
      "category": 5
    }
  ],
  "totalQuestions": 100,
  "currentCategory": "Entertainment"
}
```




