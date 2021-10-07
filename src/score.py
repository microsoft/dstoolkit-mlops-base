# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import os
import json
from pathlib import Path

import joblib
import pandas as pd
from azureml.contrib.services.aml_response import AMLResponse


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
