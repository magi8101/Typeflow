from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="typeflow",
    version="0.13.6",
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
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">3.0",
    install_requires=[],
    entry_points={
        "console_scripts": [
            "typeflow=typeflow.__main__:main",
        ],
    },
)