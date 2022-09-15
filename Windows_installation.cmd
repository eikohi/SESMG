@echo ################################
@echo Building the Virtual Enviroment
@echo File path: %~dp0
@echo ################################

@echo off
set /p PYVERSION="Enter your Python Version here:"

py -%PYVERSION% -m venv .

cd Scripts/
start /b activate.bat

pip install pipwin
pipwin install gdal 
pipwin install fiona 

@echo #############################################
@echo download and install required python packages
@echo #############################################

pip install -r ..\requirements.txt

@echo ######################
@echo Installation completed
@echo Starting SESMG
@echo ######################
cd ..
Scripts\python.exe start_script.py
