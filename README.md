# uPy-OTA  
OTA updater for MicroPython boards  
uPy-OTA works with private and public Github repos. It expects a flat file structure without any folders. Keep all files in the root directory.  
A Github Personal Access Token is needed to use this with a private repo.  
---
## Class `OTA`  
The OTA class handles all operations  
## method `__init__(self, user: str, repo: str, branch: str="main", access_token: str|None=None, headers: dict={})`  
- user: The repo's username
- repo: The repo's name
- branch: The branch name you want to target. Default "main"
- access_token: Optional. Personal Access Token needed for private repos. This is added as a bearer token to request headers
- headers: Optional. Dict of additional headers to supply in requests

## method `list_files(self)`
Calls `https://api.github.com/repos/{self.user}/{self.repo}/git/trees/{self.branch}?recursive=1` to get a list of files in the repo.  
Returns a dict of file names with values of [file hash, file length]  
i.e. {"boot.py": [76ad815df364682fe01ecd6f4e1bf6f8c2308d06, 621], "main.py": [ad549568108dcbaf9e911cb9bf6e20f4e3c5836c, 4072]}  

## method `check_for_updates(self)`
Compares hashes of local files against Github files.  
Returns list of file names who's hashes did not match. These files should be updated.  

## method `sha1(self, file)`  
returns a sha1 hash of a file in HEX.  

## method `github_sha1(self, file)`  
returns a file hash in Github's format: `blob {len(file)}\x00{file}`  

## method `dl_file(self, file_name, retries=1)`  
Attempts to download the file from `https://raw.githubusercontent.com/{user}/{repo}/{branch}/{file_name}`.  
Returns file as a string or None if it fails.  

## method `update(self)`  
Iterates through each file in the repo, checking if it's hash matched the local files hash. If the hashes mismatch then the Github file is downloaded and the local file overwritten.  
Returns the number of files updated. The user should reset the board with `machine.reset()` accordingly.



