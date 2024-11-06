import os
import requests
from dotenv import load_dotenv
from langchain_core.documents import Document

load_dotenv()

github_token = os.getenv("GITHUB_TOKEN")

def fetch_github(owner, repo, endpoint):
    url = f"https://api.github.com/repos/{owner}/{repo}/{endpoint}"
    headers = {
        "Authorization": f"Bearer {github_token}"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
    else:
        print("Failed with status code:", response.status_code)
        return []
    print(data)
    return data

def fetch_github_issues(owner, repo):
    data = fetch_github(owner, repo, "issues")
    return load_issues(data)

def load_issues(issues):
    docs = []
    for doc in issues:
        metadata = {
            "author": doc["user"]["login"],
            "comments": doc["comments"],
            "body": doc["body"],
            "labels": doc["labels"],
            "created_at": doc["created_at"],
        }
        data = doc["title"]
        if doc["body"]:
            data += " " + doc["body"]
        doc = Document(page_content=data, metadata=metadata)
        docs.append(doc)
    return docs