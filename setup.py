from setuptools import setup

setup(
    name="yape",
    description="Yet another pbuttons tool",
    url="https://github.com/murrayo/yape",
    author="Fabian,Murray",
    author_email="fabian@fabianhaupt.de",
    license="MIT",
    packages=["yape"],
    entry_points={
        "console_scripts": [
            "yape=yape.command_line:main",
            "yape-profile=yape.command_line:main_profile",
        ]
    },
    test_suite="nose.collector",
    tests_require=["nose"],
    install_requires=[
        "pytz==2018.5",
        "matplotlib==2.2.3",
        "numpy==1.15.1",
        "pandas==0.23.4",
        "setuptools_scm==3.1.0",
        "gitchangelog>=3.0.4",
        "pre-commit>=1.14.4",
        "black>=18",
        "pystache>=0.5.4",
    ],
    version="2.1.0",
    setup_requires=["setuptools_scm"],
    zip_safe=False,
)
