import requests
from datetime import datetime

def get_file_sha(owner, repo, path, token, branch='main'):
    url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}?ref={branch}"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()['sha']
    else:
        raise Exception(f"Error: {response.status_code} - {response.text}")

def get_latest_commit_sha(owner, repo, token, branch='main'):
    url = f"https://api.github.com/repos/{owner}/{repo}/git/refs/heads/{branch}"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()['object']['sha']
    else:
        raise Exception(f"Error: {response.status_code} - {response.text}")

def update_files(owner, repo, files, token, branch, content):
    url = f"https://api.github.com/repos/{owner}/{repo}/git/trees"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    #content = base64.b64encode(content.encode()).decode()

    # Create a new tree with the updated files
    tree = []
    for file in files:
        tree.append({
            "path": file,
            "mode": "100644",
            "type": "blob",
            "content": content
        })

    # Get the latest commit SHA
    base_tree =  get_latest_commit_sha(owner, repo, token, branch)

    # Create the tree
    data = {
        "base_tree": base_tree,
        "tree": tree
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 201:
        tree_sha = response.json()['sha']
    else:
        raise Exception(f"Error1: {response.status_code} - {response.text}")

    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S") 
    commit_message = f"Update app version based on develop branches - {current_time}"
    # Create a new commit
    url = f"https://api.github.com/repos/{owner}/{repo}/git/commits"
    data = {
        "message": commit_message,
        "tree": tree_sha,
        "parents": [base_tree]
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 201:
        commit_sha = response.json()['sha']
    else:
        raise Exception(f"Error2: {response.status_code} - {response.text}")

    # Update the reference to point to the new commit
    url = f"https://api.github.com/repos/{owner}/{repo}/git/refs/heads/{branch}"
    data = {
        "sha": commit_sha
    }
    response = requests.patch(url, headers=headers, json=data)
    if response.status_code == 200:
        print("Files updated successfully")
    else:
        raise Exception(f"Error3: {response.status_code} - {response.text}")

# Replace these variables with your own values
owner = "code360Pro"
repo = "cloudbuild"
files = ["dev-01.hcl", "dev-02.hcl"]
content = "coreloggingversion = \"2.0.0\"\nrulesEditor = \"3.87.0\"\nplato = \"4.87.0\""
token = "fools"
branch = "main"  # Specify the branch name here

update_files(owner, repo, files, token, branch, content)
