@echo off
rem Startet die automatische Auswertung aller Bilder (braucht Python).
cd /d "%~dp0"
where py >nul 2>nul
if %errorlevel%==0 (
  py bilder_auswerten.py %*
  goto ende
)
python --version >nul 2>nul
if %errorlevel%==0 (
  python bilder_auswerten.py %*
  goto ende
)
echo Python ist auf diesem Rechner nicht installiert.
echo Download: https://www.python.org/downloads/windows/
:ende
pause
