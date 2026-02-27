#!/bin/bash

echo "🚀 Setting up Project Management CLI..."

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install requirements
if [ -f "requirements.txt" ]; then
    echo "Installing requirements..."
    pip install -r requirements.txt
else
    echo "Creating requirements.txt and installing packages..."
    cat > requirements.txt << 'REQ'
tabulate>=0.8.9
colorama>=0.4.4
pytest>=7.0.0
REQ
    pip install -r requirements.txt
fi

echo "✅ Setup complete!"
echo ""
echo "To run the application:"
echo "  source venv/bin/activate"
echo "  python3 main.py"
echo ""
echo "Or use this script with: ./run.sh"
