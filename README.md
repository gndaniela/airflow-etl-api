# Building a Data System with Airflow & Docker

### About:

This repo creates a data system to collect and display data from some chosen crypto coins' prices.

### Steps:

- [x] Setup Airflow using the official `docker-compose` YAML file.

- [x] Create another database in the Postgres used by Airflow to store the stocks data:

➲ The `docker_postgres_init.sql` script was added into the original `docker-compose.yml` file to create a new database inside the same Postgres service used by Airflow. 

![ETL DAG](/documentation/db.PNG "ETL DAG")

- [x] Develop the data model to store the daily stock data (symbol, date, open, high, low, close) using SQLAlchemy's declarative base. Then create the tables in the DB.

➲ The developed model stores cryptocurrency prices for three chosen coins (BTC, ETH and ADA). SQLAlchemy's declarative base was used in `create_table.py` to determine the new table's fields and constraints. 
Once the script is run, it checks if the table exists. In case it doesn't, it gets created. 

![ETL DAG](/documentation/table.PNG "ETL DAG")


- [x] Develop a DAG that obtains the price information of Bitcoin (BTC), Ethereum (ETH) and Cardano (ADA) and then inserts the data in the database using SQLAlchemy insert method.

➲ The developed DAG checks/creates cryptos' table, then requests the price for that particular day to the API (filtering by execution date), and stores the retrieved data inside the table. A temporary file is created for each day, and its deletion takes place in the last step. 

![ETL DAG](/documentation/dag.PNG "ETL DAG")

- [x] Create a Python class, in order to connect with the Postgres DB. 

➲ A class called `PostgresCli` was created in order to query the database with different methods, and generate the base for the plots needed to analyze and display data. It is stored inside `postgres_cli.py`.

- [x] Fetch data from the Postgres DB and create a dashboard to display some plots

➲ A [Streamlit dashboard](http://localhost:8501/) is available to use and filter dynamically once the data is stored inside the DB. The user can choose the period or N days to be plotted.

![Streamlit](/documentation/streamlit.PNG "Streamlit")

- [x] Add two unit tests runnable with [pytest](https://docs.pytest.org/) that can be run from the command line:

➲ Inside `test_app.py`, two tests are available:

- The first one checks that the connection status of the DB is OK.
- The second one tests the extraction. It compares some parametrized values to the response coming from the API.

![Pytest](/documentation/pytest_local.PNG "Pytest")
   
- [x] Implement a CI step using [GitHub Actions](https://docs.github.com/en/actions) to run the unit tests using `pytest` each time a commit is pushed to a branch in a PR. In case of failure the result should be visible in GitHub's merge request UI.

➲ Inside `.github/workflows` a CI for testing was created. It runs on push or PRs to the main branch, using a Poetry environment. If a test fails, GitHub bot leaves a comment:

![Pytest](/documentation/pytest_GA.PNG "Pytest")

![Pytest](/documentation/ga_comment.PNG "Pytest")

## Bonus points

- [x] A CI step for Black was added. Files are formatted and auto fixes are done every time there's a commit or PR to the main branch.

![Black](/documentation/black-auto-fix.PNG "Black")

- [x] Pylint config file `.pylintrc` was created to state that only warnings and errors should show when checking the files.
In addition, a new CI step was created to make a comment with the linting results each time a commit is pushed to the main branch.

![Pylint comment](/documentation/pylint-comment.PNG "Pylint comment")


---

## Deploy and test

- Clone the repository
- Inside the main directory run `docker-compose up -d`
- Login to [Airflow UI](http://localhost:8080) _(user: airflow, password: airflow)_
- Activate etl_cryptos_dag and wait until the backfill process is finished
- Open [Cryptos Dashboard](http://localhost:8501) to get data rendered and choose the plots you want to see
           