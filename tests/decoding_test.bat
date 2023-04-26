@ECHO OFF
REM https://stackoverflow.com/a/4580120/20785734
setlocal
set PYTHONPATH=%~dp0
python tests/decoding_test.py
endlocal


