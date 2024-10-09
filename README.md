## Job Scheduler API [Django]

Job Scheduler API documentation

## Installation

```python

On development environment
pip install -r requirements.txt

```

## Initialize the database

On all operating systems, these is a need to run database migrations and create the first user account.

``` To do this, run.

docker compose up airflow-init

```

## Running Api and Airflow

```

docker compose up

```

All environment variables are to be set in the `.env` file.
