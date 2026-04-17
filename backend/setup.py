"""Setup script for CloseZap AI"""
from setuptools import setup, find_packages

setup(
    name="closezap-ai",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "fastapi>=0.109.0",
        "uvicorn[standard]>=0.27.0",
        "sqlalchemy>=2.0.25",
        "psycopg2-binary>=2.9.9",
        "python-dotenv>=1.0.0",
        "openai>=1.10.0",
        "pydantic>=2.5.3",
        "pydantic-settings>=2.1.0",
        "httpx>=0.26.0",
        "apscheduler>=3.10.4",
        "twilio>=8.12.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.4",
            "pytest-asyncio>=0.23.3",
            "pytest-cov>=4.1.0",
            "black>=24.1.1",
            "flake8>=7.0.0",
            "isort>=5.13.2",
            "mypy>=1.8.0",
        ],
    },
    python_requires=">=3.10",
)