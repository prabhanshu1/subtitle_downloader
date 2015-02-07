@echo off
set par1=%%a
for /f "tokens=*" %%a in ("%*") do (

    set therest=%%a
)

python "F:\holiday\scripts\sub_downloader\subtitle_downloader_win.py" %therest%
