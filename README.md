# Installer Builder

A lightweight Windows desktop tool built with Python and PySide6 to automate Unity build configuration, JSON management, and Inno Setup installer generation.

Designed specifically for Unity Windows builds that require rapid project-specific configuration and automated installer packaging workflows.

---

# Features

## Project Management

- Save and load multiple project configurations
- Persistent project history using AppData
- Automatic project dropdown population
- Runtime configuration switching

---

## JSON Configuration System

- Live JSON validation
- Automatic fallback/default values
- Two-way synchronization between UI and JSON
- Runtime editing support

Supported config parameters:

```json
{
    "screenURL_List": [],
    "APIBaseURL": "",
    "SocketBaseURL": "",
    "AutoLoadSceneIndex": -1,
    "AutoReset": false,
    "AutoResetHour": 2,
    "AutoResetMinute": 0
}
```

---

## Unity Build Integration

Automatically detects:

```text
*_Data
```

folders from Unity Windows builds.

Supports:

- `StreamingAssets/config.json`
- Runtime config injection
- Dynamic version extraction
- Automatic project name parsing

---

## Inno Setup Automation

Automatically:

- Creates temporary `.iss` file
- Injects runtime paths
- Updates output names
- Compiles installers
- Generates ZIP packages

Output example:

```text
Light_a_Lamp_Kunj_prod_Setup_4.0.0-9.exe
Light_a_Lamp_Kunj_prod_Setup_4.0.0-9.zip
```

---

## Build System

- Non-blocking asynchronous build pipeline using `QProcess`
- Real-time progress tracking
- Build logs panel
- Automatic output discovery
- Explorer integration

---

## Windows Administrator Support

- UAC elevation enabled
- Admin manifest support
- Safe modification of protected directories
- Installer generation inside system locations

---

# Tech Stack

| Component | Technology |
|---|---|
| Language | Python 3 |
| UI | PySide6 |
| Packaging | PyInstaller |
| Installer | Inno Setup |
| Platform | Windows |

---

# Project Structure

```text
InstallerBuilder/
│
├── main.py
├── ui.py
├── builder.py
├── storage.py
│
├── assets/
│   └── icon.ico
│
├── target/
│   ├── UnityBuild.exe
│   ├── *_Data/
│   ├── BuildInstaller.bat
│   └── InnoSetupScript_prod.iss
│
├── build_exe.bat
├── admin.manifest
│
└── README.md
```

---

# Default Runtime Behavior

On startup, the application automatically searches for:

```text
./target
```

next to the executable.

Example:

```text
InstallerBuilder/
 ├── InstallerBuilder.exe
 └── target/
```

---

# Building the Application

## Install Dependencies

```bash
pip install PySide6
pip install pyinstaller
```

---

## Generate EXE

Run:

```bash
build_exe.bat
```

Generated output:

```text
dist/InstallerBuilder.exe
```

---

# Administrator Elevation

The application is compiled with:

```text
requireAdministrator
```

manifest privileges.

Windows will automatically request elevation on startup.

---

# AppData Storage

Project configurations are stored at:

```text
C:\Users\<USER>\AppData\Roaming\InstallerBuilder\projects.json
```

---

# Supported Workflow

1. Launch Installer Builder
2. Select or create project
3. Paste JSON configuration
4. Edit runtime values
5. Build installer
6. Automatically generate:
   - Updated config.json
   - Installer EXE
   - ZIP package

---

# Automatic Runtime Parsing

The tool dynamically extracts:

| Source | Extracted Value |
|---|---|
| `Light a Lamp-4.0.0-9_Data` | Project Name |
| `4.0.0-9` | Runtime Version |

Used for automatic installer naming.

---

# Generated Installer Example

```text
Light_a_Lamp_Chevron_prod_Setup_4.0.0-9.exe
```

---

# Key Advantages

- No manual ISS editing
- No repetitive Unity config updates
- Fast multi-project workflow
- Automatic installer packaging
- Portable deployment structure
- Production-ready Windows pipeline

---

# Future Improvements

Planned enhancements:

- Dark theme UI
- Drag & drop JSON support
- Build queue system
- Automatic Unity build detection
- Installer signing support
- Cloud config synchronization
- Build templates/profiles
- CI/CD integration

---

# License

Internal tooling / proprietary project.

---

# Author

Developed for automated Unity deployment and installer generation workflows.
