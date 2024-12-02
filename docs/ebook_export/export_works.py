import argparse
import os
import requests
import zipfile
from ao3_web_reader.utils import works_utils


def main(args):
    url: str = args.url
    unzip: bool = args.unzip

    print(f"login to {url}...")

    auth_token = input("auth token > ")
    headers = {"AUTHENTICATION": auth_token}

    tag_name = input("tag name > ")

    all_works_url = f"{url}/api/{tag_name}/all-works"
    works_for_tag_response = requests.get(all_works_url, headers=headers)

    if works_for_tag_response.status_code != 200 or works_for_tag_response.url != all_works_url:
        raise Exception(f"error while getting works for {tag_name}, status: {works_for_tag_response.status_code}")

    works = works_for_tag_response.json()

    print(f"got {len(works)}, processing...")

    current_dir = os.path.abspath(os.path.dirname(__file__))
    output_dir = os.path.join(current_dir, "works_output")

    if not os.path.exists(output_dir):
        os.mkdir(output_dir)

    for work in works:
        print(f"exporting {work['name']}...")
        res = requests.get(f"{url}/works/{work['work_id']}/download", headers=headers)
        work_name = works_utils.serialize_work_name(work['name'])

        with open(os.path.join(output_dir, f"{work_name}.zip"), "wb") as file:
            file.write(res.content)

    print("works export completed...")

    if unzip:
        unzip_output = os.path.join(output_dir, "archives")
        print(f"extracting archives to {unzip_output}")

        os.mkdir(unzip_output)

        for file in os.listdir(output_dir):
            archive_path = os.path.join(output_dir, file)

            if os.path.isfile(archive_path):
                file_name = file.split(".")[0]
                file_path = os.path.join(unzip_output, file_name)

                print(f"extracting {file_name}...")

                with zipfile.ZipFile(archive_path, "r") as zip_ref:
                    zip_ref.extractall(file_path)

        print(f"works have been extracted to {unzip_output}")

    print("done")


def get_args():
    parser = argparse.ArgumentParser()

    parser.add_argument("--url",
                        type=str,
                        help="app url, for example: http://127.0.0.1:8000",
                        required=True)

    parser.add_argument("--unzip", action="store_true", help="unzip exported archives", required=False)

    opt = parser.parse_args()

    return opt


if __name__ == '__main__':
    main(get_args())