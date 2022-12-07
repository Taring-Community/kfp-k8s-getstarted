import kfp
from kfp import dsl
from kfp.v2.dsl import (
    component,
    Input,
    Output,
    Dataset,
    Metrics,
)

# Connect to Kubeflow Pipelines
client = kfp.Client( host='http://3.34.205.245:80' )
print( client.list_pipelines() )

#===================== COMPONENT =====================
# First component
@component
def add( a: float, b: float ) -> float:
    print( 'Adding two numbers' )
    return a + b

#===================== PIPELINE =====================
# Pipeline definition
@dsl.pipeline(
    name='addition-pipeline',
    description='A toy pipeline that performs addition calculations.'
    # pipeline_root='gs://kubeflow-pipeline-data/addition-pipeline',
)
def add_pipeline(
    a: float = 1,
    b: float = 7,
):
    first_add_task = add( a, 4 )

    second_add_task = add( first_add_task.output, b )

# Specify pipeline argument values
arguments = { 'a': '7', 'b': 8 }

# Submit a pipeline run using the v2 compatible mode
client.create_run_from_pipeline_func(
    add_pipeline,
    arguments=arguments
)