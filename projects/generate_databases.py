import json
import os
import random
import shutil

BASE_DIR = r"H:\boring\projects"
OPENSOURCE_DIR = os.path.join(BASE_DIR, "opensource-directory")

OPENSOURCE_URLS = [
    "https://github.com/microsoft/vscode",
    "https://github.com/torvalds/linux",
    "https://github.com/facebook/react",
    "https://github.com/vuejs/vue",
    "https://github.com/django/django",
    "https://github.com/pallets/flask",
    "https://github.com/fastapi/fastapi",
    "https://github.com/docker/docker-ce",
    "https://github.com/kubernetes/kubernetes",
    "https://github.com/ansible/ansible"
]

DATASETS_URLS = [
    "https://huggingface.co/datasets/imdb",
    "https://huggingface.co/datasets/squad",
    "https://huggingface.co/datasets/coco",
    "https://archive.ics.uci.edu/ml/index.php",
    "https://www.kaggle.com/datasets",
    "https://registry.opendata.aws/",
    "https://datasetsearch.research.google.com/",
    "https://www.data.gov/",
    "https://data.fivethirtyeight.com/",
    "https://earthdata.nasa.gov/"
]

TOOLS_URLS = [
    "https://1.1.1.1",
    "https://www.cloudflare.com",
    "https://regex101.com/",
    "https://jwt.io/",
    "https://gchq.github.io/CyberChef/",
    "https://carbon.now.sh/",
    "https://crontab.guru/",
    "https://gitignore.io/",
    "https://bundlephobia.com/",
    "https://caniuse.com/"
]

def generate_opensource():
    items = []
    for i in range(1, 51):
        url = random.choice(OPENSOURCE_URLS)
        items.append({
            "id": str(i),
            "slug": f"open-source-tool-{i}",
            "title": f"Open Source Project {i}",
            "url": url,
            "description": f"An amazing community-driven open-source alternative for Enterprise SaaS {i}.",
            "category": random.choice(["Analytics", "Automation", "Communication", "Database", "Design", "Productivity"]),
            "alternative_to": f"Proprietary App {i}",
            "github_repo": url,
            "license": random.choice(["MIT", "GPL-3.0", "Apache-2.0"])
        })
    return items

def generate_datasets():
    items = []
    for i in range(1, 51):
        url = random.choice(DATASETS_URLS)
        items.append({
            "id": str(i),
            "slug": f"data-archive-{i}",
            "title": f"Public Dataset Archive {i}",
            "url": url,
            "description": f"High quality verifiable public dataset #{i} tailored for machine learning pre-training loops.",
            "category": random.choice(["Climate", "Natural Language", "Computer Vision", "Finance", "Healthcare", "Economics"]),
            "format": random.choice(["CSV", "JSON", "Parquet", "Image Archive"]),
            "size": f"{random.randint(1, 100)} GB",
            "license": random.choice(["CC-BY-4.0", "Public Domain", "MIT"])
        })
    return items

def generate_tools():
    items = []
    for i in range(1, 51):
        url = random.choice(TOOLS_URLS)
        items.append({
            "id": str(i),
            "slug": f"web-utility-{i}",
            "title": f"Web Utility Instance {i}",
            "url": url,
            "description": f"A rapidly accessible zero-install browser-based network utility script #{i}.",
            "category": random.choice(["Network", "Formatting", "Generators", "Security", "SEO"]),
            "platform": "Web",
            "tool_type": "Utility",
            "pricing": "Free"
        })
    return items

def save_json(repo, data):
    path = os.path.join(BASE_DIR, repo, "data", "database.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)
        
def sync_check_links():
    src_script = os.path.join(OPENSOURCE_DIR, "scripts", "check_links.py")
    src_test = os.path.join(OPENSOURCE_DIR, "tests", "test_check_links.py")
    
    for dest_repo in ["datasets-directory", "tools-directory"]:
        print(f"Syncing scripts to {dest_repo}")
        dest_dir = os.path.join(BASE_DIR, dest_repo)
        try:
            shutil.copyfile(src_script, os.path.join(dest_dir, "scripts", "check_links.py"))
            shutil.copyfile(src_test, os.path.join(dest_dir, "tests", "test_check_links.py"))
        except Exception as e:
            print(f"Failed to copy to {dest_repo}: {e}")

if __name__ == "__main__":
    print("Regenerating 50 item databases...")
    save_json("opensource-directory", generate_opensource())
    save_json("datasets-directory", generate_datasets())
    save_json("tools-directory", generate_tools())
    sync_check_links()
    print("Done generating 50-item JSON objects across 3 repos.")
