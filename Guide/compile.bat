@echo off
setlocal
REM ── Compile main.tex → PDF outputs ───────────────────────
REM   All aux/log/toc/out files go into build\
REM   Final PDFs are copied to:
REM     - Guide\main.pdf
REM     - Repo root\YARP_RV32I_Guide.pdf
REM   Run: compile.bat
REM ─────────────────────────────────────────────────────────

cd /d "%~dp0"
for %%I in ("%~dp0..") do set "REPO_ROOT=%%~fI"
set "GUIDE_DIR=%CD%"

if not exist build mkdir build

echo [1/2] Compiling (pass 1)...
pdflatex -interaction=nonstopmode -file-line-error -output-directory=build --include-directory="%GUIDE_DIR%" main.tex
if errorlevel 1 goto :fail

echo [2/2] Compiling (pass 2 - TOC/refs)...
pdflatex -interaction=nonstopmode -file-line-error -output-directory=build --include-directory="%GUIDE_DIR%" main.tex
if errorlevel 1 goto :fail

if exist build\main.pdf (
    copy /Y build\main.pdf main.pdf >nul
    copy /Y build\main.pdf "%REPO_ROOT%\YARP_RV32I_Guide.pdf" >nul
    echo.
    echo  ✓  PDFs generated successfully.
    echo     - %CD%\main.pdf
    echo     - %REPO_ROOT%\YARP_RV32I_Guide.pdf
    exit /b 0
)

:fail
echo.
echo  ✗  Compilation failed. Check build\main.log for details.
exit /b 1
