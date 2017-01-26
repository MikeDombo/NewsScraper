@echo off
SET loc=%~dp0%
sphinx-apidoc -f -o %loc%docs %loc%
%loc%docs\make.bat html