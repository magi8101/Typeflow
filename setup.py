from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="typeflow",
    version="0.1.0",
    author="Magi Sharma",
    author_email="sharmamagi0@gmail.com",
    description="Seamlessly handle type conversion during operations in Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/magi8101/typeflow",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.7",
    install_requires=[],  # Add any dependencies your package needs
)