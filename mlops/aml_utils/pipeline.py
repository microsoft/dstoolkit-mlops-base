# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from azureml.pipeline.core import Pipeline, PublishedPipeline, PipelineEndpoint


def publish_pipeline(ws, name, steps, description=None, version=None):

    # Create the pipeline
    pipeline = Pipeline(workspace=ws, steps=steps)
    pipeline.validate()

    # Publish pipeline
    old_pipelines = get_existing_pipelines(ws, name)
    published_pipeline = pipeline.publish(
        name=name,
        description=description,
        version=version,
        continue_on_step_failure=False
    )

    # Publish or update pipeline endpoint
    pipeline_endpoint_name = f'{name}-endpoint'
    try:
        published_endpoint = PipelineEndpoint.get(workspace=ws, name=pipeline_endpoint_name)
        published_endpoint.add_default(published_pipeline)
    except:
        published_endpoint = PipelineEndpoint.publish(
            workspace=ws,
            name=pipeline_endpoint_name,
            pipeline=published_pipeline,
            description=f'{description} - Endpoint'
        )

    for pipeline in old_pipelines:
        pipeline.disable()

    return published_endpoint, published_pipeline


def disable_existing_pipelines(ws, name):
    for pipeline in PublishedPipeline.list(ws):
        if pipeline.name == name:
            pipeline.disable()


def get_existing_pipelines(ws, name):
    return [pipeline for pipeline in PublishedPipeline.list(ws) if pipeline.name == name]
