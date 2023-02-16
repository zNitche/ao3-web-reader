import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

import argparse
import json
from scripts import common_utils
from scripts.convert_legacy_db_to_new import legacy_models


def get_data_from_old_models(old_session):
    data = {}
    models = [legacy_models.User,
              legacy_models.UpdateMessage,
              legacy_models.Work,
              legacy_models.Tag,
              legacy_models.Chapter,
              legacy_models.TextRow]

    for base_model in models:
        print(f"getting data for {base_model.__name__}...")
        data[base_model.__name__] = [model.__dict__ for model in old_session.query(base_model).all()]

    return data


def clear_db_data(db_data):
    for model_name in db_data:
        for model in db_data[model_name]:
            del model["_sa_instance_state"]

    return db_data


def write_data(db_data, file_path):
    with open(file_path, "w") as file:
        file.write(json.dumps(db_data, indent=4, sort_keys=True, default=str))


def main(args):
    old_db_path = args.old_db_path
    output_path = args.output_path

    if output_path and os.path.exists(old_db_path):
        print(f"Getting data from {old_db_path}...")

        print(f"creating db session for {old_db_path}...")
        old_db_session = common_utils.init_db_session(old_db_path)

        with old_db_session() as old_session:
            print("db session created...")
            db_data = get_data_from_old_models(old_session)

            print("clearing db data...")
            db_data = clear_db_data(db_data)

            print(f"writing data to {output_path}...")
            write_data(db_data, output_path)

    print("process done...")


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--old_db_path", type=str, default=None, help="old database path")
    parser.add_argument("--output_path", type=str, default=None, help="output json path")
    opt = parser.parse_args()

    return opt


if __name__ == '__main__':
    main(get_args())
