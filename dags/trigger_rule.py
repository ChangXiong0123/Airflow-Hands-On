from airflow import DAG
from datetime import datetime
from airflow.operators.bash import BashOperator

default_args = {
    'start_date':datetime(2020,1,1)
}

with DAG('trigger_rule',schedule_interval = '@daily',
        default_args=default_args, catchup = False) as dag:
    
    task1 = BashOperator(
        task_id = 'task1',
        bash_command = 'exit 1', #exit 0 succeed, exit 1 fail
        do_xcom_push = False

    )

    task2 = BashOperator(
    task_id = 'task2',
    bash_command = 'sleep 30', #exit 0 succeed, exit 1 fail
    do_xcom_push = False

   )


    task3 = BashOperator(
    task_id = 'task3',
    bash_command = 'exit 0', #exit 0 succeed, exit 1 fail
    do_xcom_push = False,
    trigger_rule = 'one_failed'

    )


[task1,task2] >> task3 #task3 depends on both task1 and task2