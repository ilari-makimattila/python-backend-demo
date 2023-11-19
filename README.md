Python Backend Server Demo Project
==================================

This project demoes how I would develop a Python backend server project.

Notable Things
--------------

Most decisions made are documented in Git commit messages. I suggest you to
follow through them in order to understand the project and to experience my
typical development workflow.

### Package management with poetry

Python Poetry is a modern take on package management. It is significantly
easier than using pip for example.

### Static type checking with mypy

Type checking is an important part of the development process. It makes the
software easier to work with in the long run and increases overall correctness.

### Linting with ruff

Ruff is a modern and fast linter that supports most rules and features of other
Python linters out of the box.

### Testing with pytest

Pytest is in my opinion the most powerful testing framework. Not only for Python
but it's better than any other framework I've seen for any language.

Requirements and Architecture
-----------------------------

1. A RESTful API with two endpoints:
    * `POST /measurements/:room_id` to store temperature measurements
    * `GET /measurements/:room_id/average/:duration` to retrieve an average of
      temperature measurements per room
2. A database to store temperature measurements
3. App is dockerized
4. A CI/CD pipeline is set up

The app is built using the [FastAPI](https://fastapi.tiangolo.com/) framework.
It is a lightweight and fast REST API framework that offers many things such as
request validation and API docs out of the box.

Development
-----------

Run the app in development mode:
```
make dev
```

Run tests:
```
make test
```

Run checks:
```
make lint
make typecheck

# or both at the same time:
make check
```
