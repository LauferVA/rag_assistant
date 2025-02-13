from setuptools import setup, find_packages

setup(
    name='rag_assistant',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        "transformers",
        "torch",
        "sentence-transformers",
        "numpy",
        "tqdm",
        "bitsandbytes",
        "python-docx",
        "PyMuPDF",
        "PyPDF2",
        "openpyxl",
        "odfpy",
        # add any other parsing libraries you’re using
    ],
    author="Your Name",
    description="A retrieval-augmented generation assistant for local text files.",
    long_description=open('README.md', encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/rag_assistant",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
