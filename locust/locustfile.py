from locust import HttpUser, task, between
from requests.auth import HTTPBasicAuth
import uuid
import xmltodict
import random

class User(HttpUser):
    DAV_PATH = "/remote.php/dav/files/"
    wait_time = between(1, 2)  # Simulate wait time between 1 and 2 seconds

    def on_start(self):
        self.user_uuid = "loc" + str(uuid.uuid4()).replace("-", "")[:8] # Generate a random user name
        self.password = self.user_uuid
        headers = {
            "OCS-APIRequest": "true",
            "Content-Type": "application/x-www-form-urlencoded"
        }

        payload = {
            "userid": self.user_uuid,
            "password": self.password
        }
        self.client.post("/ocs/v2.php/cloud/users", data=payload, headers=headers, auth=HTTPBasicAuth("admin", "admin"))
        self.list_test_files()
       
    @task(20)
    def list_test_files(self):
        xml_content = self.client.request("PROPFIND", f"{self.DAV_PATH}{self.user_uuid}/", auth=(self.user_uuid, self.password), name="list_files")
        response_dict = xmltodict.parse(xml_content.content)
        self.list_test_files = [elem["d:href"] for elem in response_dict["d:multistatus"]["d:response"] if "testfile" in elem["d:href"]]

    @task(5)
    def read_random_file(self):
        if len(self.list_test_files) == 0:
            rnd_href = f"{self.DAV_PATH}{self.user_uuid}/Readme.md"
            self.client.get(rnd_href, auth=(self.user_uuid, self.password), name="read_file")
        else:
            rnd_href = random.choice(self.list_test_files)
            filesize = rnd_href.split("_")[-1]
            self.client.get(rnd_href, auth=(self.user_uuid, self.password), name=f"read_file_{filesize}")

    @task(15)
    def upload_file_1kb(self):
        self.upload_file("/locust/testfile_1kb")

    @task(6)
    def upload_file_1mb(self):
        self.upload_file("/locust/testfile_1mb")

    @task(1)
    def upload_file_1gb(self):
        self.upload_file("/locust/testfile_1gb")

    @task(12)
    def delete_random_file(self):
        if len(self.list_test_files) == 0:
            return
        rnd_href = random.choice(self.list_test_files)
        self.client.delete(rnd_href, auth=(self.user_uuid, self.password), name="delete_file")
        self.list_test_files.remove(rnd_href) # avoid deleting the same file twice

    def upload_file(self, filepath):
        filesize = filepath.split("_")[-1]
        with open(filepath, "rb") as file:
            remote_path = f"{self.DAV_PATH}{self.user_uuid}/testfile_{str(uuid.uuid4()):8}_{filesize}"
            self.client.put(remote_path, data=file, auth=(self.user_uuid, self.password), name=f"upload_file_{filesize}")