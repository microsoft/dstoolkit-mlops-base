# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import os
import json
import joblib
from pathlib import Path

import pandas as pd


# from inference_schema.schema_decorators import input_schema, output_schema
# from inference_schema.parameter_types.numpy_parameter_type import NumpyParameterType

model = None


def preprocessing(X):
    """
    Create Week_number from WeekStarting
    Drop two unnecessary columns: WeekStarting, Revenue
    """
    X['WeekStarting'] = pd.to_datetime(X['WeekStarting'])
    X['week_number'] = X['WeekStarting'].apply(lambda x: x.strftime("%U"))
    # Drop 'WeekStarting','Revenue' columns if it exist
    X = X.drop(['WeekStarting', 'Revenue', 'Quantity'], axis=1, errors='ignore')
    return X


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
        result = model.predict(data_input)
        # You can return any data type, as long as it is JSON serializable.
        return result.tolist()
    except Exception as e:
        result = str(e)
        # return error message back to the client
        return json.dumps({"error": result})
