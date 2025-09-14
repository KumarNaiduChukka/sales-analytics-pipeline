# PowerShell script to set up the virtual environment

# Create virtual environment
Write-Host "Creating virtual environment..."
python -m venv venv

# Activate virtual environment
Write-Host "Activating virtual environment..."
.\venv\Scripts\Activate.ps1

# Install required packages
Write-Host "Installing required packages..."
pip install -r requirements.txt

Write-Host "Environment setup complete!"