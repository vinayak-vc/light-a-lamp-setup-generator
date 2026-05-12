import json
import os
from pathlib import Path


APP_DIR = Path(os.getenv("APPDATA")) / "InstallerBuilder"
APP_DIR.mkdir(parents=True, exist_ok=True)

PROJECTS_FILE = APP_DIR / "projects.json"


class Storage:

    @staticmethod
    def load_projects():
        if not PROJECTS_FILE.exists():
            return {}

        try:
            with open(PROJECTS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return {}

    @staticmethod
    def save_project(project_name, data):
        projects = Storage.load_projects()
        projects[project_name] = data

        with open(PROJECTS_FILE, "w", encoding="utf-8") as f:
            json.dump(projects, f, indent=4)