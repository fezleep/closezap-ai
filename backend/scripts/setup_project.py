#!/usr/bin/env python3
"""Startup script to initialize and run the application"""
import os
import sys
import subprocess

def check_python_version():
    """Check Python version is 3.10+"""
    if sys.version_info < (3, 10):
        print("Error: Python 3.10 or higher is required")
        sys.exit(1)
    print(f"✓ Python {sys.version_info.major}.{sys.version_info.minor} detected")


def check_env_file():
    """Check if .env file exists"""
    env_file = os.path.join(os.path.dirname(__file__), ".env")
    env_example = os.path.join(os.path.dirname(__file__), ".env.example")

    if not os.path.exists(env_file):
        if os.path.exists(env_example):
            print("⚠ .env file not found. Copying .env.example to .env...")
            subprocess.run(["cp", env_example, env_file])
            print("✓ .env file created. Please edit it with your credentials.")
        else:
            print("⚠ No .env or .env.example found. Using defaults.")
    else:
        print("✓ .env file found")


def install_dependencies():
    """Install Python dependencies"""
    requirements = os.path.join(os.path.dirname(__file__), "requirements.txt")
    if os.path.exists(requirements):
        print("Installing dependencies...")
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", requirements])
        print("✓ Dependencies installed")
    else:
        print("⚠ requirements.txt not found")


def create_database():
    """Initialize database tables"""
    print("Creating database tables...")
    from app.database import engine, Base
    from app.models.lead import Lead  # Import models
    Base.metadata.create_all(bind=engine)
    print("✓ Database tables created")


def run_server():
    """Start the development server"""
    print("\n" + "=" * 50)
    print("Starting CloseZap AI server...")
    print("=" * 50 + "\n")

    subprocess.run([
        sys.executable, "-m", "uvicorn",
        "app.main:app",
        "--reload",
        "--host", "0.0.0.0",
        "--port", "8000"
    ])


def main():
    """Main entry point"""
    print("\n" + "=" * 50)
    print("CloseZap AI - Setup & Startup")
    print("=" * 50 + "\n")

    # Change to script directory
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    check_python_version()
    check_env_file()
    install_dependencies()
    create_database()
    run_server()


if __name__ == "__main__":
    main()