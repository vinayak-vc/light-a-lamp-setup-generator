@echo off

rmdir /s /q build
rmdir /s /q dist

pyinstaller ^
--noconfirm ^
--clean ^
--onefile ^
--windowed ^
--icon=assets/icon.ico ^
--name InstallerBuilder ^
--hidden-import PySide6.QtCore ^
--hidden-import PySide6.QtGui ^
--hidden-import PySide6.QtWidgets ^
main.py

pause