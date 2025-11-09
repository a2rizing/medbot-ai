@echo off
REM Quick evaluation script for Windows
REM Run this from the backend directory

echo ========================================
echo MedBot-AI Model Evaluation
echo ========================================
echo.

REM Check if virtual environment exists
if not exist "venv\" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Install requirements if needed
echo Installing/updating dependencies...
pip install -q --upgrade pip
pip install -q torch torchvision numpy matplotlib seaborn scikit-learn pandas pillow tqdm

echo.
echo Starting evaluation...
echo.
python evaluate_model.py

echo.
echo ========================================
echo Evaluation complete!
echo Check the evaluation_results folder for outputs
echo ========================================
pause
