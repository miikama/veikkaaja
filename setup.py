"""Setting up veikkaaja."""
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="veikkaaja",
    version="0.1.0",
    author="Miika Mäkelä",
    author_email="makelanmiika@gmail.com",
    description="A wrapper for Veikkaus (veikkaus.fi) betting API.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/miikama/veikkaaja",
    packages=setuptools.find_packages(exclude='test'),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'requests',
    ],
    extras_require= {
        'dev': [
            'pytest',
            'pylint',
            'yapf',
            'mypy',
            'responses',
        ]
    },
    python_requires='>=3.6',
    entry_points={
        'console_scripts': [
        ],
    },
)
