$ErrorActionPreference = "Stop"

Write-Host "Creating minimal Virtual Environment..." -ForegroundColor Cyan
python -m venv .venv_test
& .\.venv_test\Scripts\python.exe -m pip install --upgrade pip -q

Write-Host "`nRunning Pytest on OPENSOURCE..." -ForegroundColor Yellow
cd H:\boring\projects\opensource-directory
& H:\boring\projects\.venv_test\Scripts\python.exe -m pip install -r requirements.txt pytest pytest-cov aiohttp -q
& H:\boring\projects\.venv_test\Scripts\python.exe -m pytest --cov=scripts

Write-Host "`nRunning Link Checker on OPENSOURCE..." -ForegroundColor Yellow
& H:\boring\projects\.venv_test\Scripts\python.exe scripts\check_links.py --output-report link_report.md

Write-Host "`nRunning Pytest on DATASETS..." -ForegroundColor Yellow
cd H:\boring\projects\datasets-directory
& H:\boring\projects\.venv_test\Scripts\python.exe -m pip install -r requirements.txt pytest pytest-cov aiohttp -q
& H:\boring\projects\.venv_test\Scripts\python.exe -m pytest --cov=scripts

Write-Host "`nRunning Link Checker on DATASETS..." -ForegroundColor Yellow
& H:\boring\projects\.venv_test\Scripts\python.exe scripts\check_links.py --output-report link_report.md

Write-Host "`nRunning Pytest on TOOLS..." -ForegroundColor Yellow
cd H:\boring\projects\tools-directory
& H:\boring\projects\.venv_test\Scripts\python.exe -m pip install -r requirements.txt pytest pytest-cov aiohttp -q
& H:\boring\projects\.venv_test\Scripts\python.exe -m pytest --cov=scripts

Write-Host "`nRunning Link Checker on TOOLS..." -ForegroundColor Yellow
& H:\boring\projects\.venv_test\Scripts\python.exe scripts\check_links.py --output-report link_report.md

Write-Host "`nDone!" -ForegroundColor Green
