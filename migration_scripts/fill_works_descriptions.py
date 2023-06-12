import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from ao3_web_reader.models import Work
from ao3_web_reader.utils import works_utils
from migration_scripts import common_utils


def main():
    print("creating db session...")
    db_session = common_utils.init_db_session()

    with db_session() as session:
        print("db session created...")

        print("fetching works with empty description...")
        works = [work for work in session.query(Work).all() if not work.description]

        print(f"got {len(works)} works...")

        for work in works:
            print(f"processing {work.name}...")

            work.description = works_utils.get_work_description(work.work_id)
            session.commit()

        print("process done...")


if __name__ == '__main__':
    main()
