import urequests
import uhashlib
import time

# Inspired by https://github.com/RangerDigital/senko
class OTA:
    raw    = "https://raw.githubusercontent.com"

    def __init__(self, user: str, repo: str, branch: str="main", access_token: str|None=None, headers: dict={}):
        self.url = f"{self.raw}/{user}/{repo}/{branch}"
        if access_token:
            headers["Authorization"] = f"Bearer {access_token}"
        headers["User-Agent"] = "uPy-OTA"
        self.headers = headers
        self.user = user
        self.repo = repo
        self.branch = branch

    def list_files(self) -> dict[str, tuple[str, int]]:
        url = f"https://api.github.com/repos/{self.user}/{self.repo}/git/trees/{self.branch}?recursive=1"
        print("API: ", url)
        resp = urequests.get(url, headers=self.headers)
        print("Resp: ",  resp.status_code)
        results = {}
        files = resp.json()["tree"]
        for file in files:
            print(file["path"])
            results[file["path"]] = [file["sha"], file["size"]]
        return results
    
    def check_for_updates(self) -> list:
        print("Checking for updates...")
        mismatches = []
        for f_name, file in self.list_files().items():
            try:
                with open(f_name) as f:
                    text = f.read()
            except:
                text = "" # incase file does not exist

            h = self.github_sha1(text)
            print(f"{f_name} {len(text)}:\t{h}")
            print(f"{f_name} {file[1]}:\t{file[0]}")
            if h != file[0]:
                mismatches += [f_name]
        return mismatches

    def sha1(self, file) -> str:
        _hash = uhashlib.sha1(file.encode())
        return _hash.digest().hex()
    
    def github_sha1(self, file) -> str:
        file = f"blob {len(file)}\x00{file}"
        return self.sha1(file)

    def dl_file(self, file_name, retries=1) -> str | None:
        url = f"{self.url}/{file_name}"
        for i in range(1, retries+1):
            resp = urequests.get(url, headers=self.headers)
            code = resp.status_code

            if code == 200:
                return resp.text
            time.delay_ms(2000*i)
        return None

    def update(self) -> int:
        to_update = self.check_for_updates()
        if to_update == []:
            print("Nothing to update.")
            return 0
        
        i = 0
        for file_name in to_update:
            print(f"Updating {file_name}...", end="")
            new_file = self.dl_file(file_name, retries=3)

            if new_file is None:
                raise Exception(f"Failed to DL {file_name}.")
            
            with open(file_name, "w") as f:
                f.write(new_file)
            print(" Done.")
            i += 1
        
        return i