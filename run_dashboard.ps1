# Sales Analytics Dashboard Launcher
Write-Host "🚀 Starting Sales Analytics Dashboard..." -ForegroundColor Green
Write-Host ""

# Check if Python is available
try {
    $pythonVersion = python --version
    Write-Host "✅ Python found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Python not found. Please install Python first." -ForegroundColor Red
    exit 1
}

# Install dependencies
Write-Host "📦 Installing dependencies..." -ForegroundColor Yellow
pip install -r requirements.txt

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Dependencies installed successfully!" -ForegroundColor Green
} else {
    Write-Host "❌ Failed to install dependencies." -ForegroundColor Red
    exit 1
}

# Start the dashboard
Write-Host ""
Write-Host "🌐 Starting Streamlit dashboard..." -ForegroundColor Yellow
Write-Host "Dashboard will be available at: http://localhost:8501" -ForegroundColor Cyan
Write-Host "Press Ctrl+C to stop the dashboard" -ForegroundColor Gray
Write-Host ""

streamlit run streamlit_dashboard.py --server.port 8501
