# converts legacy db (with text rows) to new one (last commit 9a075d3)

import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

import argparse
from migrations_stripts import common_utils
from ao3_web_reader import models


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

            common_utils.add_model(models.Chapter, session, chapter_data)


def write_data_to_new_models(new_session, db_data):
    models_to_copy = [models.User, models.Tag, models.UpdateMessage, models.Work]

    print("copying models...")
    for model in models_to_copy:
        print(f"writing data for {model.__name__}...")
        common_utils.copy_models(db_data[model.__name__], model, new_session)

    print(f"writing + converting data for chapters and textrows...")
    convert_chapters(db_data[models.Chapter.__name__], db_data["TextRow"], new_session)

    new_session.commit()


def main(args):
    new_db_path = args.new_db_path
    db_data_path = args.db_data_path

    if new_db_path and os.path.exists(db_data_path):
        print(f"Converting {db_data_path} -> {new_db_path}...")

        print(f"creating db session for {new_db_path}...")
        new_db_session = common_utils.init_db_session(new_db_path)

        with new_db_session() as new_session:
            print("db session created...")

            db_data = common_utils.load_db_data(db_data_path)
            db_data = common_utils.tweak_json_dates(db_data)

            write_data_to_new_models(new_session, db_data)

    print("process done...")


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--db_data_path", type=str, default=None, help="database dumped json data path", required=True)
    parser.add_argument("--new_db_path", type=str, default=None, help="new database path", required=True)
    opt = parser.parse_args()

    return opt


if __name__ == '__main__':
    main(get_args())
