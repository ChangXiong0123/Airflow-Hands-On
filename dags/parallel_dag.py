from airflow import DAG
from datetime import datetime

from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from airflow.operators.subdag import SubDagOperator
#subdag is a dag inside another dag
from airflow.utils.task_group import TaskGroup

from subdags.subdag_parallel_dag import subdag_parallel_dag


default_args = {
    'start_date': datetime(2020,1,1)
}

with DAG('parallel_dag', schedule_interval ='@daily', 
        default_args = default_args, catchup = False ) as dag:
            # change the catch up to true in order to run multiple dag runs

    
    task1 = BashOperator(
        task_id = 'task1',
        bash_command= 'sleep 3'
    )

##############group tasks together using TaskGroup & Sub task groups #################
    with TaskGroup('processing_tasks') as processing_tasks:
        task2 = BashOperator(
        task_id = 'task2',
        bash_command= 'sleep 3'
    )

        with TaskGroup('spark_tasks') as soark_tasks:
            task3 = BashOperator(
            task_id = 'task3', # here under the task group, you will get 'spark_tasks.task3' by default
            bash_command= 'sleep 3'
        )

        with TaskGroup('flink_tasks') as flink_tasks:
            task3 = BashOperator(
            task_id = 'task3',# here under the task group, you will get 'flink_tasks.task3' by default
            bash_command= 'sleep 3'
        )
        #####uder a task group/sub taskgroup, the task id will be given by default with the prefix




##############group tasks together using TaskGroup
    # with TaskGroup('processing_tasks') as processing_tasks:
    #     task2 = BashOperator(
    #     task_id = 'task2',
    #     bash_command= 'sleep 3'
    # )

    #     task3 = BashOperator(
    #     task_id = 'task3',
    #     bash_command= 'sleep 3'
    # )


##############group task 2 and task 3 together using Subdags####################

    # processing = SubDagOperator(
    #     task_id = 'processing_tasks',
    #     subdag = subdag_parallel_dag('parallel_dag','processing_tasks', default_args)
    #     #parent dag id, then the child dag id(the subdag id, which is  processing_tasks)
    # )

#################No group ###############################
    # task2 = BashOperator(
    #     task_id = 'task2',
    #     bash_command= 'sleep 3'
    # )

    # task3 = BashOperator(
    #     task_id = 'task3',
    #     bash_command= 'sleep 3'
    # )

    task4 = BashOperator(
        task_id = 'task4',
        bash_command= 'sleep 3'
    )

################Dependency#####################
# task1 >> task2 >> task4
# task1 >> task3 >> task4
# or can use task1 >> [task2, task3] >> task4

task1 >> processing_tasks >> task4

