# converts legacy db (with text rows) to new one

import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

import argparse
import json
from datetime import datetime
from scripts import common_utils
from ao3_web_reader import models


def copy_models(model_db_data, model, session):
    models_ids_in_db = [model.id for model in session.query(model).all()]

    for data in model_db_data:
        model_id = data["id"]
        if model_id not in models_ids_in_db:
            new_model = model(**data)
            session.add(new_model)


def get_textrows_content_for_chapter(textrows_data, chapter_id):
    rows = [row["content"] for row in textrows_data if row["chapter_id"] == chapter_id]

    return rows


def convert_chapters(chapters_data, textrows_data, session):
    chapters_ids_in_db = [model.id for model in session.query(models.Chapter).all()]

    for chapter_data in chapters_data:
        chapter_id = chapter_data["id"]
        print(f"processing: {chapter_data['title']}...")

        if chapter_id not in chapters_ids_in_db:
            textrows_content_for_chapter = get_textrows_content_for_chapter(textrows_data, chapter_id)
            chapter_data["text"] = "\n".join([textrow for textrow in textrows_content_for_chapter])

            new_chapter = models.Chapter(**chapter_data)
            session.add(new_chapter)


def write_data_to_new_models(new_session, db_data):
    models_to_copy = [models.User, models.Tag, models.UpdateMessage, models.Work]

    for model in models_to_copy:
        print(f"writing data for {model.__name__}...")
        copy_models(db_data[model.__name__], model, new_session)

    print(f"writing + converting data for chapters and textrows...")
    convert_chapters(db_data[models.Chapter.__name__], db_data["TextRow"], new_session)

    new_session.commit()


def tweak_json_dates(data):
    for model_name in data:
        for model in data[model_name]:
            for model_key in model:
                if "date" in model_key:
                    model[model_key] = datetime.fromisoformat(model[model_key])

    return data


def load_db_data(data_path):
    with open(data_path, "r") as file:
        data = json.loads(file.read())

    return data


def main(args):
    new_db_path = args.new_db_path
    db_data_path = args.db_data_path

    if new_db_path and os.path.exists(db_data_path):
        print(f"Converting {db_data_path} -> {new_db_path}...")

        print(f"creating db session for {new_db_path}...")
        new_db_session = common_utils.init_db_session(new_db_path)

        with new_db_session() as new_session:
            print("db session created...")

            db_data = load_db_data(db_data_path)
            db_data = tweak_json_dates(db_data)

            write_data_to_new_models(new_session, db_data)

    print("process done...")


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--db_data_path", type=str, default=None, help="database dumped json data path")
    parser.add_argument("--new_db_path", type=str, default=None, help="new database path")
    opt = parser.parse_args()

    return opt


if __name__ == '__main__':
    main(get_args())
