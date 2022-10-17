from datetime import datetime, timezone
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.utils.task_group import TaskGroup
from src.api_call import get_symbol_data
from src.populate_and_remove import remove, populate
from src.create_table import create_table
from src.config import CONN_URL, NEW_TABLE_NAME, ROOT_DIR, SYMBOLS

default_args = {
    "owner": "Daniela",
    "retries": 0,
    "start_date": datetime(2022, 9, 30, 22, tzinfo=timezone.utc),
    "depends_on_past": True,
    "wait_for_downstream": True,
}

with DAG(
    dag_id="etl-cryptos-dag",
    default_args=default_args,
    schedule_interval="@daily",
    catchup=True,
    max_active_runs=1,  # to avoid API restrictions
) as dag:
    create_table_task = PythonOperator(
        task_id="create_table_task",
        python_callable=create_table,
        op_args=[CONN_URL, NEW_TABLE_NAME],
    )
    with TaskGroup(group_id=f"get_daily_data") as get_daily_data_task_group:
        for symbol in SYMBOLS:
            call_api = PythonOperator(
                task_id=f"get_{symbol}_daily_data",
                python_callable=get_symbol_data,
                op_args=[symbol, ROOT_DIR],
                provide_context=True,
            )
    populate_table = PythonOperator(
        task_id="populate_table_task",
        python_callable=populate,
        op_args=[NEW_TABLE_NAME, ROOT_DIR, CONN_URL],
    )
    remove_files = PythonOperator(
        task_id="remove_tmp_file", python_callable=remove, op_args=[ROOT_DIR]
    )


create_table_task >> get_daily_data_task_group >> populate_table >> remove_files
