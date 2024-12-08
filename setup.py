from setuptools import setup, find_packages

setup(
    name="gameboy-py",               # Replace with your project name
    version="0.1",                  # Initial version
    packages=find_packages(where="src"),  # Discover all packages in src/
    package_dir={"": "src"},         # Map the root package to src/
    python_requires=">=3.6",         # Specify the minimum Python version
)