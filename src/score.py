# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import os
import json
import joblib
from pathlib import Path


def init():
    global model
    
    models_root_path = Path(os.environ('AZUREML_MODEL_DIR'))
    models_files = [f for f in models_root_path.glob('**/*') if f.is_file()]
    if len(models_files) > 1:
        raise RuntimeError(f'Found more than one model:\n\t{models_files}')
    
    model_path = models_files[0]
    model = joblib.load(model_path)
    print("Loaded model:",model_path)


def run(data):
    try:
        data_input = json.loads(data)
        data_input = pd.DataFrame.from_dict(data_input["data"])
        result = model.predict(data_input)
        # You can return any data type, as long as it is JSON serializable.
        return result.tolist()
    except Exception as e:
        result = str(e)
        # return error message back to the client
        return json.dumps({"error": result})
