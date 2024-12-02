import argparse
import os


def main(args):
    path: str = args.path
    target_extension: str = args.target_extension

    output_dir = "converted_output"

    works_dirs = os.listdir(path)
    print(f"found {len(works_dirs)}, processing...")

    if not os.path.exists(output_dir):
        os.mkdir(output_dir)

    for dir in os.listdir(path):
        print(f"processing {dir}...")

        input_path = os.path.join(path, dir, "index.html")
        output_path = os.path.join(output_dir, f"{dir}.{target_extension}")

        os.system(f"ebook-convert {input_path} {output_path}")

    print("done")


def get_args():
    parser = argparse.ArgumentParser()

    parser.add_argument("--path", required=True, type=str, help="path to exported works directory")
    parser.add_argument("--target_extension", type=str, default="azw3", help="format of converted works")

    opt = parser.parse_args()

    return opt


if __name__ == '__main__':
    main(get_args())