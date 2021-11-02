# test-task-for-company
Test Task For Company

Python v3.9.5
Need to run redis and mysql.

First Terminal run:
```
pip install pipenv
```
```
pipenv shell
```
```
pipenv install
```
```
uvicorn src.main:app --reload
```

Second Terminal run:
```
pip install pipenv
```
```
pipenv shell
```
```
celery -A src.celery_ worker --loglevel=DEBUG
```
