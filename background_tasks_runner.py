from ao3_web_reader.modules.background_processes import WorksUpdaterProcess


def main():
    processes = [WorksUpdaterProcess]

    for process in processes:
        try:
            instance = process()

            print(f"starting {instance.get_process_name()}...")
            instance.start_process()

            print(f"{instance.get_process_name()} has been started")

        except Exception as e:
            print(f"failed to start background process: {str(e)}")


if __name__ == '__main__':
    main()
