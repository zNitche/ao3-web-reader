import sys
import os
import importlib

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

import argparse
from migrations_stripts import common_utils


def main(args):
    old_db_path = args.old_db_path
    output_path = args.output_path
    models_path = args.models_path
    models_names = args.models

    if output_path and os.path.exists(old_db_path) and models_path and len(models_names) > 0:
        print(f"getting data from {old_db_path}...")

        print(f"creating db session for {old_db_path}...")
        db_session = common_utils.init_db_session(old_db_path)

        with db_session() as session:
            print("db session created...")

            print("importing models...")
            legacy_models = importlib.import_module(models_path)

            models = [getattr(legacy_models, model_name) for model_name in dir(legacy_models)
                                if model_name in models_names]

            db_data = common_utils.get_data_from_models(session, models)

            print(f"writing data to {output_path}...")
            common_utils.write_data(db_data, output_path)

    print("process done...")


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--old_db_path", type=str, default=None, help="old database path", required=True)
    parser.add_argument("--output_path", type=str, default=None, help="output json path", required=True)
    parser.add_argument("--models-path", type=str, default=None, help="old models path", required=True)
    parser.add_argument("--models", nargs="+", default=[], help="old models names", required=True)
    opt = parser.parse_args()

    return opt


if __name__ == '__main__':
    main(get_args())
