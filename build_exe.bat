@echo off

pyinstaller ^
--noconfirm ^
--windowed ^
--onefile ^
--icon=assets/icon.ico ^
main.py

pause