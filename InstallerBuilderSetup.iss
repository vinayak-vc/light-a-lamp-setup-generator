; =========================================================
; InstallerBuilder Setup Script
; =========================================================

#define AppName "Light a Lamp InstallerBuilder"
#define AppVersion "1.0.0"
#define ExeName "Light a Lamp InstallerBuilder.exe"

[Setup]

AppId={{9E0F2F89-0C55-4B52-9D0D-6E0B95E7B1AA}

AppName={#AppName}
AppVersion={#AppVersion}

AppPublisher=ViitorCloud

DefaultDirName={autopf}\{#AppName}
DefaultGroupName={#AppName}

OutputDir=Output
OutputBaseFilename=InstallerBuilderSetup

Compression=lzma2/max
SolidCompression=yes

WizardStyle=modern

PrivilegesRequired=admin

ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64

SetupIconFile=icon.ico

UninstallDisplayIcon={app}\{#ExeName}

DisableProgramGroupPage=yes

; =========================================================
; FILES
; =========================================================

[Files]

; Main EXE
Source: "{#ExeName}"; DestDir: "{app}"; Flags: ignoreversion

; Entire target folder
Source: "target\*"; DestDir: "{app}\target"; Flags: ignoreversion recursesubdirs createallsubdirs

; =========================================================
; SHORTCUTS
; =========================================================

[Icons]

Name: "{group}\{#AppName}"; Filename: "{app}\{#ExeName}"

Name: "{commondesktop}\{#AppName}"; Filename: "{app}\{#ExeName}"

; =========================================================
; RUN AFTER INSTALL
; =========================================================

[Run]

Filename: "{app}\{#ExeName}";Description: "Launch {#AppName}";Flags: nowait postinstall skipifsilent runascurrentuser

; =========================================================
; UNINSTALL CLEANUP
; =========================================================

[UninstallDelete]

Type: filesandordirs; Name: "{app}\target"