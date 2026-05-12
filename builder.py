import json
import subprocess
import zipfile
import shutil
import os
from pathlib import Path
import re

class Builder:

    def __init__(self, root_path):

        self.root_path = Path(root_path)

        # Automatically detect *_Data folder
        self.data_folder = self.find_data_folder()

        if not self.data_folder:
            raise Exception(
                "No *_Data folder found"
            )

        self.config_path = (
            self.data_folder /
            "StreamingAssets" /
            "config.json"
        )

        self.iss_path = (
            self.root_path /
            "InnoSetupScript_prod.iss"
        )

        self.bat_path = (
            self.root_path /
            "BuildInstaller.bat"
        )

    def find_data_folder(self):

        for folder in self.root_path.iterdir():

            if (
                folder.is_dir() and
                folder.name.lower().endswith("_data")
            ):
                return folder

        return None

    def get_project_info(self):

        data_folder_name = self.data_folder.name

        # Example:
        # Light a Lamp-4.0.0-9_Data

        # Remove _Data
        clean_name = re.sub(
            r"_Data$",
            "",
            data_folder_name,
            flags=re.IGNORECASE
        )

        # Split version
        # Result:
        # project_name = Light a Lamp
        # version = 4.0.0-9

        match = re.match(
            r"(.+)-([0-9].+)",
            clean_name
        )

        if not match:

            return {
                "project_name": clean_name,
                "version": "Unknown"
            }

        return {
            "project_name": match.group(1),
            "version": match.group(2)
        }


    def write_config(self, config_data):

        self.config_path.parent.mkdir(parents=True, exist_ok=True)

        with open(self.config_path, "w", encoding="utf-8") as f:
            json.dump(config_data, f, indent=4)

    def modify_iss(self):

        info = self.get_project_info()

        project_name = (
            info["project_name"]
            .replace(" ", "_")
        )

        version = info["version"]

        output_name = (
            f"{project_name}"
            f"_prod_Setup_"
            f"{version}"
        )

        build_root = str(self.root_path)

        output_dir = str(
            self.root_path /
            "InstallerOutput"
        )

        original_iss = self.iss_path

        temp_iss = (
            self.root_path /
            "temp_build.iss"
        )

        with open(
            original_iss,
            "r",
            encoding="utf-8"
        ) as f:

            lines = f.readlines()

        new_lines = []

        for line in lines:

            stripped = line.strip()

            # BuildRoot
            if stripped.startswith("#define BuildRoot"):

                line = (
                    f'#define BuildRoot '
                    f'"{build_root}"\n'
                )

            # OutputDir
            elif stripped.startswith("OutputDir="):

                line = (
                    f"OutputDir="
                    f"{output_dir}\n"
                )

            # OutputBaseFilename
            elif stripped.startswith(
                "OutputBaseFilename="
            ):

                line = (
                    f"OutputBaseFilename="
                    f"{output_name}\n"
                )

            new_lines.append(line)

        with open(
            temp_iss,
            "w",
            encoding="utf-8"
        ) as f:

            f.writelines(new_lines)

        return temp_iss
    
    def finalize_build(self, project_name):
            exe_files = list(
                self.root_path.rglob("*.exe")
            )
            filtered = []
            for file in exe_files:
                name = file.name.lower()
                if "setup" in name:
                    filtered.append(file)
            if not filtered:
                return None
            latest_exe = max(
                filtered,
                key=lambda f: f.stat().st_mtime
            )
            self.create_zip(latest_exe)
            return str(latest_exe)
        
    def create_zip(self, setup_path):
            setup_path = Path(setup_path)
            zip_path = setup_path.with_suffix(".zip")
            with zipfile.ZipFile(
                zip_path,
                "w",
                zipfile.ZIP_DEFLATED
            ) as zipf:
                zipf.write(
                    setup_path,
                    arcname=setup_path.name
                )
            return zip_path