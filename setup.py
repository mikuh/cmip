import setuptools

with open("README.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name="cmip",
    version="0.0.5",
    author="geb",
    author_email="853934146@qq.com",
    description="An efficient information processing program.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mikuh/cmip",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    package_data={'': ['data/*.txt', "data/*.tsv"]},
    install_requires=['numpy', 'pandas', 'nltk', 'validators'],
    python_requires='>=3.8',
)
