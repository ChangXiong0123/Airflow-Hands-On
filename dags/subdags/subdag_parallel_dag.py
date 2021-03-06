from airflow import DAG
from airflow.operators.bash import BashOperator

def subdag_parallel_dag(parent_dag_id, child_dag_id, default_args):
    
     #default_args need to be consistent with the whole airflow

     with DAG(dag_id = f'{parent_dag_id}.{child_dag_id}', 
            default_args = default_args) as dag:
        
        task2 = BashOperator(
        task_id = 'task2',
        bash_command= 'sleep 3'
        )

        task3 = BashOperator(
            task_id = 'task3',
            bash_command= 'sleep 3'
        )

        return dag

