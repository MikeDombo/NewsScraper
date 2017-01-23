@echo off
@echo Running PHP SonarQube
call %~dp0%PHP\sonarqube.bat
@echo Running Python SonarQube
call %~dp0%Python\sonarqube.bat