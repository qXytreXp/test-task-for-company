FROM python:3.9.5

RUN mkdir /usr/src/testtask/
WORKDIR /usr/src/testtask/

COPY . /usr/src/testtask/

RUN pip install pipenv
RUN pipenv install --system --deploy --ignore-pipfile


CMD ["uvicorn", "src.main:app", "--reload"]
