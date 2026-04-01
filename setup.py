from pathlib import Path

from setuptools import setup


README = Path(__file__).with_name("README.md").read_text(encoding="utf-8")


setup(
    name="pygsm7",
    version="1.0.5",
    py_modules=["pygsm7"],
    description="Unicode hex and GSM 7-bit encoding helpers",
    long_description=README,
    long_description_content_type="text/markdown",
    author="Alvin Mayende",
    author_email="alvinmayende@gmail.com",
    python_requires=">=3.5",
)
