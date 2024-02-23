import setuptools


with open("README.md") as fp:
    long_description = fp.read()

setuptools.setup(
    name="simple-file-server",
    version="0.0.1",
    description="Woven take-home challenge",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="ct.ivanovich@gmail.com",
    install_requires=[
        "pytest"
,        "flask",
        "flask_session",
        "requests",
        "gunicorn"
    ],
    python_requires=">=3.9",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3.8",
        "Topic :: Software Development :: Code Generators",
        "Topic :: Utilities",
        "Typing :: Typed",
    ],
)