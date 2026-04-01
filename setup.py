from pathlib import Path

from setuptools import setup


README = Path(__file__).with_name("README.md").read_text(encoding="utf-8")


setup(
    name="pygsm7",
    version="1.0.6",
    py_modules=["pygsm7"],
    description="pygsm7 is a Python package that provides functions for encoding and decoding messages using GSM 7-bit encoding. It is designed to facilitate the processing of text messages in the context of SMS and mobile communication.",
    long_description=README,
    long_description_content_type="text/markdown",
    author="Alvin Mayende",
    author_email="alvinmayende@gmail.com",
    python_requires=">=3.5",
)
