#!/usr/bin/env python3
"""
Setup script for Patent Partners Assistant
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="patent-partners-assistant",
    version="0.1.0",
    author="Team 4 Patent Partners",
    author_email="team4@patentpartners.com",
    description="Offline Patent Assistant MVP - Team 4 Patent Partners",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/nandanpabolu/Capstone-Project-Team-4",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Legal Industry",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.9",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "patent-assistant=patent_assistant.cli:main",
        ],
    },
)
