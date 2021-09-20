# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from azureml.pipeline.core import Pipeline, PublishedPipeline


def publish_pipeline(ws, name, steps, description=None, version=None):

    # Create the pipeline
    pipeline = Pipeline(workspace=ws, steps=steps)
    pipeline.validate()

    # Publish it replacing old pipeline
    disable_old_pipelines(ws, name)
    published_pipeline = pipeline.publish(
        name=name,
        description=description,
        version=version,
        continue_on_step_failure=False
    )

    return published_pipeline


def disable_old_pipelines(ws, name):
    for pipeline in PublishedPipeline.list(ws):
        if pipeline.name == name:
            pipeline.disable()
