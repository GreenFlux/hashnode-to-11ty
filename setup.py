from setuptools import setup, find_packages

setup(
    name="hashnode-to-11ty",
    version="1.0.0",
    description="Convert Hashnode blog exports to 11ty static site format",
    author="GitNode",
    packages=find_packages(),
    install_requires=[
        "requests>=2.28.0",
        "jinja2>=3.1.0",
        "python-dotenv>=0.19.0",
        "click>=8.0.0",
        "rich>=12.0.0",
    ],
    entry_points={
        "console_scripts": [
            "h2e=h2e:cli",
        ],
    },
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)