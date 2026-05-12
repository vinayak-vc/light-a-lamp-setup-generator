import json
import sys
from pathlib import Path
import os
import subprocess
from PySide6.QtCore import QProcess
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QTextEdit,
    QLineEdit,
    QFileDialog,
    QMessageBox,
    QComboBox,
    QPlainTextEdit,
    QSpinBox,
    QCheckBox,
    QProgressBar
    )
from storage import Storage
from builder import Builder
class MainWindow(QWidget):
        def __init__(self):
            super().__init__()
            self.process = None
            self.current_json = {}
            self.setWindowTitle("Installer Builder")
            self.resize(1200, 700)
            self.root_path = (
                self.get_default_root_path()
            )
            self.setup_ui()
            self.load_projects()
        def setup_ui(self):
            root = QHBoxLayout(self)
            
            self.logs = QTextEdit()
            self.logs.setReadOnly(True)

            self.root_label = QLabel()
            
            # LEFT
            left = QVBoxLayout()
            self.project_dropdown = QComboBox()
            self.project_dropdown.currentTextChanged.connect(
            self.on_project_selected
            )
            
            left.addWidget(QLabel("Projects"))
            left.addWidget(self.project_dropdown)
            self.project_name = QLineEdit()
            left.addWidget(QLabel("Project Name"))
            left.addWidget(self.project_name)
            path_btn = QPushButton("Select Root Folder")
            path_btn.clicked.connect(self.select_root)
            left.addWidget(self.root_label)
            left.addWidget(path_btn)
            self.json_text = QTextEdit()
            self.json_text.textChanged.connect(self.validate_json)
            left.addWidget(QLabel("JSON"))
            left.addWidget(self.json_text)
            self.validate_btn = QPushButton("Validate")
            self.validate_btn.clicked.connect(self.validate_json)
            left.addWidget(self.validate_btn)
            # RIGHT
            right = QVBoxLayout()
            right.addWidget(QLabel("screenURL_List"))
            self.url_list = QPlainTextEdit()
            right.addWidget(self.url_list)
            self.api_url = QLineEdit()
            right.addWidget(QLabel("APIBaseURL"))
            right.addWidget(self.api_url)
            self.socket_url = QLineEdit()
            right.addWidget(QLabel("SocketBaseURL"))
            right.addWidget(self.socket_url)
            self.scene_index = QSpinBox()
            self.scene_index.setMinimum(-1)
            self.scene_index.setMaximum(999)
            right.addWidget(QLabel("AutoLoadSceneIndex"))
            right.addWidget(self.scene_index)
            self.auto_reset = QCheckBox("AutoReset")
            right.addWidget(self.auto_reset)
            time_layout = QHBoxLayout()
            
            self.reset_hour = QSpinBox()
            self.reset_hour.setRange(0, 23)
            self.reset_minute = QSpinBox()
            self.reset_minute.setRange(0, 59)
            time_layout.addWidget(QLabel("Hour"))
            time_layout.addWidget(self.reset_hour)
            time_layout.addWidget(QLabel("Minute"))
            time_layout.addWidget(self.reset_minute)
            right.addLayout(time_layout)
            self.build_btn = QPushButton("Build")
            self.build_btn.clicked.connect(self.build_project)
            right.addWidget(self.build_btn)
            root.addLayout(left, 1)
            root.addLayout(right, 1)
            
            # Progress
            self.progress_bar = QProgressBar()
            self.progress_bar.setValue(0)

            right.addWidget(self.progress_bar)
            right.addWidget(self.logs)

            # Output Path
            output_layout = QHBoxLayout()

            self.output_path = QLineEdit()
            self.output_path.setReadOnly(True)

            self.open_output_btn = QPushButton("Open in Explorer")
            self.open_output_btn.clicked.connect(
                self.open_output_folder
            )

            output_layout.addWidget(self.output_path)
            output_layout.addWidget(self.open_output_btn)

            right.addLayout(output_layout)
            
            self.api_url.textChanged.connect(
                self.refresh_json_text
            )

            self.socket_url.textChanged.connect(
                self.refresh_json_text
            )
            
            self.scene_index.valueChanged.connect(
                self.refresh_json_text
            )

            self.reset_hour.valueChanged.connect(
                self.refresh_json_text
            )

            self.reset_minute.valueChanged.connect(
                self.refresh_json_text
            )
            
            self.auto_reset.stateChanged.connect(
                self.refresh_json_text
            )
            
            self.root_label.setText(
                self.root_path
            )
            
        def select_root(self):
            folder = QFileDialog.getExistingDirectory(
            self,
            "Select Build Root Folder"
            )
            if folder:
              self.root_path = folder
              
            self.root_label.setText(
                self.root_path
            )
        def validate_json(self):
            text = self.json_text.toPlainText().strip()
            if not text:
               return
            try:
                data = json.loads(text)
                self.current_json = data
                screen_urls = data.get("screenURL_List", [])
                api = data.get("APIBaseURL", "")
                socket = data.get("SocketBaseURL", "")
                
                auto_scene = data.get("AutoLoadSceneIndex", -1)
                auto_reset = data.get("AutoReset", False)
                reset_hour = data.get("AutoResetHour", 2)
                reset_minute = data.get("AutoResetMinute", 0)
                self.url_list.setPlainText(
                    "\n".join(screen_urls)
                )
                self.api_url.setText(api)
                self.socket_url.setText(socket)
                self.scene_index.setValue(auto_scene)
                self.auto_reset.setChecked(auto_reset)
                self.reset_hour.setValue(reset_hour)
                self.reset_minute.setValue(reset_minute)
                self.validate_btn.setText("Valid JSON")
            except Exception as e:
                self.validate_btn.setText("Invalid JSON")
                
        def build_project(self):

            try:

                project_name = (
                    self.project_name.text().strip()
                )

                if not project_name:

                    QMessageBox.warning(
                        self,
                        "Error",
                        "Project name required"
                    )

                    return

                config = self.collect_current_config()
                
                Storage.save_project(
                project_name,
                    {
                        "project_name": project_name,
                        "root_path": str(
                            self.root_path
                        ),
                        "config": config
                    }
                )

                self.load_projects()

                self.builder = Builder(
                    self.root_path
                )

                # Write config.json
                self.builder.write_config(config)

                # Create temp iss
                temp_iss = self.builder.modify_iss(
                    project_name
                )

                self.log(f"Temp ISS: {temp_iss}")

                self.process = QProcess(self)

                self.process.readyReadStandardOutput.connect(
                    self.handle_stdout
                )

                self.process.readyReadStandardError.connect(
                    self.handle_stderr
                )

                self.process.finished.connect(
                    lambda: self.build_finished(
                        project_name,
                        temp_iss
                    )
                )

                self.process.errorOccurred.connect(
                    self.process_error
                )

                # IMPORTANT
                iscc_path = (
                    r"C:\Program Files (x86)"
                    r"\Inno Setup 6\ISCC.exe"
                )

                self.log(f"Using ISCC: {iscc_path}")

                self.process.start(
                    iscc_path,
                    [str(temp_iss)]
                )

                started = self.process.waitForStarted()

                if not started:

                    self.log(
                        "FAILED TO START PROCESS"
                    )

                    QMessageBox.critical(
                        self,
                        "Error",
                        "Failed to start ISCC.exe"
                    )

                    return

                self.progress_bar.setValue(20)

                self.build_btn.setEnabled(False)

            except Exception as e:

                QMessageBox.critical(
                    self,
                    "Exception",
                    str(e)
                )

                print(e)
            
        def build_finished(
            self,
            project_name,
            temp_iss
        ):

            self.progress_bar.setValue(95)

            output_path = (
                self.builder.finalize_build(
                    project_name
                )
            )

            if output_path:

                self.output_path.setText(
                    output_path
                )

                self.progress_bar.setValue(100)

                self.log(
                    f"Build Success:\n{output_path}"
                )

            else:

                self.log(
                    "FAILED TO LOCATE OUTPUT"
                )

            if Path(temp_iss).exists():

                Path(temp_iss).unlink()

            self.build_btn.setEnabled(True)       
            
        def handle_stderr(self):

            data = self.process.readAllStandardError()

            stderr = bytes(data).decode(
                "utf-8",
                errors="ignore"
            )

            self.log(stderr)
            
        def handle_stdout(self):

            data = self.process.readAllStandardOutput()

            stdout = bytes(data).decode(
                "utf-8",
                errors="ignore"
            )

            self.log(stdout)

            if "Parsing [Setup]" in stdout:
                self.progress_bar.setValue(30)

            elif "Compressing" in stdout:
                self.progress_bar.setValue(60)

            elif "Successful compile" in stdout:
                self.progress_bar.setValue(90)
        
        def load_projects(self):
            projects = Storage.load_projects()
            self.project_dropdown.blockSignals(True)
            self.project_dropdown.clear()
            self.project_dropdown.addItem("")
            self.project_dropdown.addItems(
                sorted(set(projects.keys()))
            )
            self.project_dropdown.blockSignals(False)
            
        def on_project_selected(self, name):
            
            if not name:
              return
            projects = Storage.load_projects()
            if name not in projects:
               return
            data = projects[name]
            self.project_name.setText(data.get("project_name", ""))
            #self.root_path = data.get("root_path", "")
            json_text = json.dumps(
                data.get("config", {}),
                indent=4
            )
            self.json_text.blockSignals(True)
            self.json_text.setText(json_text)
            self.json_text.blockSignals(False)
            self.validate_json()
    
        def open_output_folder(self):

                path = self.output_path.text().strip()

                if not path:
                    return

                if not os.path.exists(path):
                    return

                normalized = os.path.normpath(path)

                subprocess.Popen([
                    "explorer",
                    "/select,",
                    normalized
                ])
        def refresh_json_text(self):
            config = self.collect_current_config()
            self.json_text.blockSignals(True)
            self.json_text.setText(
                json.dumps(config, indent=4)
            )
            self.json_text.blockSignals(False)
        
        def collect_current_config(self):
            return {
                 "screenURL_List": [
                    line.strip()
                    for line in self.url_list
                        .toPlainText()
                        .splitlines()
                    if line.strip()
                ],
                "APIBaseURL": self.api_url.text(),
                "SocketBaseURL": self.socket_url.text(),
                "AutoLoadSceneIndex":
                    self.scene_index.value(),
                "AutoReset":
                    self.auto_reset.isChecked(),
                "AutoResetHour":
                    self.reset_hour.value(),
                "AutoResetMinute":
                    self.reset_minute.value(),
            }
            
        def log(self, text):
            self.logs.append(text)
            print(text)
            
        def process_error(self, error):
            self.log(
                f"QProcess Error: {error}"
            )
            QMessageBox.critical(
                self,
                "Build Error",
                str(error)
            )
        def get_default_root_path(self):
            # EXE mode
            if getattr(sys, "frozen", False):

                base_path = Path(
                    sys.executable
                ).parent

            # Python mode
            else:
                base_path = Path(
                    __file__
                ).resolve().parent

            target_path = (
                base_path / "target"
            )
            if not Path(target_path).exists():
                QMessageBox.warning(
                    self,
                    "Target Missing",
                    f"Could not find:\n\n"
                    f"{target_path}"
                )
            return str(target_path)