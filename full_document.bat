@echo off
@echo Running PHP Documentor
call Article_Analytics\document.bat
@echo Running Python Documentor
call Article_Scrape_And_Parse\document.bat