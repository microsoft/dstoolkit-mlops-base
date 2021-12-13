# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import os
import json
from pathlib import Path

import joblib
import pandas as pd
from azureml.contrib.services.aml_response import AMLResponse

from inference_schema.schema_decorators import input_schema, output_schema
from inference_schema.parameter_types.standard_py_parameter_type import StandardPythonParameterType

model = None

def init():
    global model

    models_root_path = Path(os.getenv('AZUREML_MODEL_DIR'))
    models_files = [f for f in models_root_path.glob('**/*') if f.is_file()]
    if len(models_files) > 1:  # TODO: support for more than one?
        raise RuntimeError(f'Found more than one model:\n\t{models_files}')

    model_path = models_files[0]
    model = joblib.load(model_path)
    print(f"Loaded model: '{model_path}'")

# Define your API input/output schema here using StandardPythonParameterType library.
# In below sample, API input is list of coordinates and its predicted output is string.

standard_sample_input = { "input": [1.0, 1.0, 1.0] }
standard_sample_output = { "output": "class_a" }

@input_schema('data', StandardPythonParameterType(standard_sample_input))
@output_schema(StandardPythonParameterType(standard_sample_output))

def run(data):
    try:
        data_input = json.loads(data)
        data_input = pd.DataFrame.from_dict(data_input["data"])
        data_input = preprocessing(data_input)
        result = predict(model, data_input)
        return result
    except Exception as ex:
        return AMLResponse(f'Error: {str(ex)}', 400)


def preprocessing(data):
    # Do your preprocessing here
    return data


def predict(model, data):
    # Generate your prediction here
    return []
