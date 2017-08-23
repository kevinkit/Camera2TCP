FOR /F "tokens=* USEBACKQ" %%F IN (`python --version`) DO (
SET var=%%F
)
ECHO %var%
ECHO %var%
ECHO %var%
ECHO %var%

REM for %%a in (%var%) do echo %%a