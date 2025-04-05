from setuptools import setup, find_packages

setup(
    name="scout_tracking",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        # List of dependencies (e.g., pytest, pandas, etc.)
        "pytest>=6.0"
    ],
    test_suite="tests",  # Points to the tests directory
)

