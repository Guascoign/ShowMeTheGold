@echo off
echo Reading ItemStrings...
python ExportItemStrings.py
echo Reading Names...
python ExportNames.py
echo ExportItemDB...
python ExportItemDB.py
pause
