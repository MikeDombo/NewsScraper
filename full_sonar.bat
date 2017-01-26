@echo off
@echo Running PHP SonarQube
call %~dp0%Article_Analytics\sonarqube.bat
@echo Running Python SonarQube
call %~dp0%Article_Scrape_And_Parse\sonarqube.bat