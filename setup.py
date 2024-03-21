from setuptools import setup, find_packages

setup(
    name="metric-tree",
    version="0.1",
    packages=find_packages(),
    python_requires=">=3.11",
    install_requires=[
        "numpy",
        "polars"
    ],
    entry_points={
        'console_scripts': [
            # Add your console scripts here if any
        ],
    },
    extras_require={
        'dev': [
            'pytest',
            'black',
            'flake8',
            'isort'
            # Add other development dependencies here
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
