if __name__ == "__main__":
    import argparse
    import os
    import re
    from zipfile import ZipFile

    parser = argparse.ArgumentParser(
        description="Package and zip LLM provided solutions"
    )
    parser.add_argument("--root", type=str, help="Root directory of solutions")
    parser.add_argument(
        "--output", type=str, required=True, help="Output directory of zip files"
    )
    args = parser.parse_args()

    # [model_name]_temp_[temp] (without -sanitized)
    directory_pattern = re.compile(r"(.*)_temp_(?:\d*\.?\d+)$")

    assert os.path.isdir(args.root)
    os.makedirs(args.output, exist_ok=True)

    for directory in os.listdir(args.root):
        match = directory_pattern.match(directory)
        if not match:
            continue
        directory_name = match.group(0)
        full_dir_path = os.path.join(args.root, directory_name)
        assert os.path.isdir(full_dir_path)
        print(f"Processing {full_dir_path}")

        zip_file_path = os.path.join(args.output, f"{directory_name}.zip")
        if os.path.exists(zip_file_path):
            print(f"Skipping -- {zip_file_path} already exists")
            continue

        with ZipFile(zip_file_path, "w") as zip_file:
            # directory_name/${TASK_ID}/${SAMPLE_ID}.py
            for task_id in os.listdir(full_dir_path):
                task_dir = os.path.join(full_dir_path, task_id)
                if not os.path.isdir(task_dir):
                    continue
                for sample_id in os.listdir(task_dir):
                    sample_file = os.path.join(task_dir, sample_id)
                    if not sample_file.endswith(".py"):
                        continue
                    zip_file.write(
                        sample_file, os.path.join(directory_name, task_id, sample_id)
                    )
