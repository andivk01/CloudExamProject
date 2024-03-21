import os

def create_testfile(filesize, filepath):
    file_content = b'A' * filesize
    with open(filepath, "wb") as file:
        file.write(file_content)
        file.close()
    return filepath

if not os.path.exists("./locust/testfile_1kb"):
    create_testfile(1024, "./locust/testfile_1kb")

if not os.path.exists("./locust/testfile_1mb"):
    create_testfile(1024 * 1024, "./locust/testfile_1mb")

if not os.path.exists("./locust/testfile_1gb"):
    create_testfile(1024 * 1024 * 1024, "./locust/testfile_1gb")