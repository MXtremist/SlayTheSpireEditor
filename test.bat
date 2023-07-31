@echo off
@REM if not defined bflag (
@REM     set bflag=1
@REM     start wt --title "SlayTheSpire Editor" %0
@REM     exit
@REM )

cd /d %~dp0
python ./Editor.py
pause