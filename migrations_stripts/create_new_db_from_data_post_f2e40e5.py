# converts legacy db to new one (last commit f2e40e5)

import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

import argparse
from migrations_stripts import common_utils
from ao3_web_reader import models
from ao3_web_reader.utils import works_utils
from ao3_web_reader.consts import ChaptersConsts, UpdateMessagesConsts
import time


def get_chapters_struct_for_work_db_id(chapters_structs, work_id):
    struct = None

    for chapter_struct in chapters_structs:
        if chapter_struct.get("work_db_id") == work_id:
            struct = chapter_struct["chapters_struct"]
            break

    return struct

def get_chapter_struct(chapters_struct, chapter_title):
    struct = None

    for chapter_struct in chapters_struct:
        if chapter_struct.get("name") == chapter_title:
            struct = chapter_struct
            break

    return struct

def convert_chapters(chapters_data, chapters_structs, session):
    chapters_ids_in_db = [model.id for model in session.query(models.Chapter).all()]

    for chapter_data in chapters_data:
        print(f"processing: {chapter_data['title']}...")

        chapter_id = chapter_data["id"]
        chapters_struct = get_chapters_struct_for_work_db_id(chapters_structs, chapter_data["work_id"])

        if chapter_id not in chapters_ids_in_db and chapters_struct:
            chapter_struct = get_chapter_struct(chapters_struct, chapter_data["title"])

            if chapter_struct:
                chapter_data["chapter_id"] = chapter_struct[ChaptersConsts.ID]
                chapter_data["chapter_order_id"] = chapter_struct[ChaptersConsts.ORDER_ID]
                chapter_data["date"] = chapter_struct[ChaptersConsts.DATE]
                chapter_data["was_removed"] = False

                common_utils.add_model(models.Chapter, session, chapter_data)

            else:
                print(f"no data for {chapter_data['title']}, work_id: {chapter_data['work_id']}...")


def convert_update_messages(update_messages_data, session):
    update_messages_ids_in_db = [model.id for model in session.query(models.UpdateMessage).all()]

    for update_message_data in update_messages_data:
        print(f"processing: {update_message_data['id']}...")

        message_id = update_message_data["id"]

        if message_id not in update_messages_ids_in_db:
            update_message_data["type"] = UpdateMessagesConsts.MESSAGE_ADDED_TYPE

            common_utils.add_model(models.UpdateMessage, session, update_message_data)


def convert_works(works_data, session):
    works_ids_in_db = [model.id for model in session.query(models.Work).all()]

    for work_data in works_data:
        print(f"processing: {work_data['id']}...")

        work_id = work_data["id"]

        if work_id not in works_ids_in_db:
            work_data["was_removed"] = False

            common_utils.add_model(models.Work, session, work_data)


def get_chapters_structs(works_data):
    chapters_structs = []

    for id, work_data in enumerate(works_data):
        work_id = work_data.get("work_id")
        work_db_id = work_data.get("id")

        print(f"getting chapters struct for {work_id}... {id + 1}/{len(works_data)}")

        time.sleep(1)

        chapters_structs.append({
            "work_db_id": work_db_id,
            "work_id": work_id,
            "chapters_struct": works_utils.get_chapters_struct(work_id)
        })

    return chapters_structs

def write_data_to_new_models(new_session, db_data):
    models_to_copy = [models.User, models.Tag, models.Work]

    print("copying models...")
    for model in models_to_copy:
        print(f"writing data for {model.__name__}...")
        common_utils.copy_models(db_data[model.__name__], model, new_session)

    print("getting chapters structs...")

    works_data = [work_data for work_data in db_data[models.Work.__name__]]
    chapters_structs = get_chapters_structs(works_data)

    print("writing + converting data for chapters...")
    convert_chapters(db_data[models.Chapter.__name__], chapters_structs, new_session)

    print("writing + converting data for update messages...")
    convert_update_messages(db_data[models.UpdateMessage.__name__], new_session)

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
