@echo off
set SCRIPT=%~dp0launcher.py
set SHORTCUT="%USERPROFILE%\Desktop\Launcher.lnk"
set VBS=%TEMP%\create_shortcut.vbs

:: Crear acceso directo con VBScript que usa pythonw.exe
echo Set oWS = WScript.CreateObject("WScript.Shell") > %VBS%
echo sLinkFile = %SHORTCUT% >> %VBS%
echo Set oLink = oWS.CreateShortcut(sLinkFile) >> %VBS%
echo oLink.TargetPath = "pythonw.exe" >> %VBS%
echo oLink.Arguments = Chr(34) ^& "%SCRIPT%" ^& Chr(34) >> %VBS%
echo oLink.WorkingDirectory = "%~dp0" >> %VBS%
echo oLink.WindowStyle = 0 >> %VBS%
echo oLink.IconLocation = "python.exe, 0" >> %VBS%
echo oLink.Save >> %VBS%

:: Ejecutar script para crear acceso directo
cscript //nologo %VBS%
del %VBS%

:: Ejecutar launcher.py sin consola
start "" pythonw "%SCRIPT%"
