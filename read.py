

import requests

def read_github_file(owner, repo, path,branch="main"):
    url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}?ref={branch}"
    headers = {
        "Accept": "application/vnd.github.v3.raw"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.text
    else:
        raise Exception(f"Error: {response.status_code} - {response.text}")

# Replace these variables with your own values
owner = "code360Pro"
repo = "github-action"
path = "test.hcl"

file_content = read_github_file(owner, repo, path)
print(file_content)
