"""
Setup script for Screen Time Monitor.
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="screen-time-monitor",
    version="1.0.0",
    author="Screen Time Monitor",
    description="Camera-based screen time monitoring using computer vision",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/screen-time-monitor",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[
        "opencv-python>=4.8.0",
        "ultralytics>=8.0.0",
        "torch>=2.0.0",
        "torchvision>=0.15.0",
        "numpy>=1.24.0",
        "PyYAML>=6.0",
        "pillow>=10.0.0",
        "matplotlib>=3.7.0",
    ],
    entry_points={
        "console_scripts": [
            "screen-time-monitor=src.main:main",
            "screen-time-stats=src.stats:main",
        ],
    },
)
