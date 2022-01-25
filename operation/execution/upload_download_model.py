"""
Script to upload/download a model to/from an AML WS
"""

import os
import sys
import argparse

from azureml.core import Model

from aml_utils import workspace


def main(model_name, pipeline_version, job_type, model_path):

    ws = workspace.retrieve_workspace()

    if job_type == 'download':
        print("Download Model")

        model = Model(ws, name=model_name)
        download_path = os.path.join(model_path, model_name)
        print(download_path)
        model.download(target_dir=download_path,
                       exist_ok=True)

    elif job_type == 'upload':
        print(f"Uploading Model: {model_path}")
        local_model_path = os.path.join(model_path, model_name)
        print(local_model_path)

        # TODO - extend tagging for traceability across environments
        model = Model.register(model_path=local_model_path,
                               model_name=model_name,
                               tags={'buildid': str(pipeline_version)},
                               workspace=ws)

    else:
        print(f'Unkown Job Type: {job_type}')
        print('Please Set to either upload or download')
        sys.exit(-1)


def parse_args(args_list=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('--model-name', type=str, required=True)
    parser.add_argument('--job-type', type=str, required=True)
    # TODO set tags argument and make optional
    parser.add_argument('--pipeline-version', type=str, required=True)
    parser.add_argument('--local-model-path', type=str, required=True)
    return parser.parse_args(args_list)


if __name__ == "__main__":
    args = parse_args()

    main(
        model_name=args.model_name,
        pipeline_version=args.pipeline_version,
        job_type=args.job_type,
        model_path=args.local_model_path
    )
