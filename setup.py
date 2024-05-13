from setuptools import setup, find_packages

__title__ = 'gptgitassist'
__version__ = '0.0.5'
__author__ = 'FLHCore'
__email__ = 'operation@flh.com.tw'


def read_files(files):
    data = []
    for file in files:
        with open(file, encoding='utf-8') as f:
            data.append(f.read())
    return "\n".join(data)


long_description = read_files(['README.md'])

with open('requirements.txt') as f:
    install_requires = f.read().split('\n')

setup(
    name=__title__,
    version=__version__,
    description="FLH CoreTech Team Assistant CLI Python Package.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    url="https://www.flh.com.tw",
    author=__author__,
    author_email=__email__,
    license="MIT",
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=install_requires,
    python_requires='>=3.7',
    entry_points={
        "console_scripts": [
            "gdiff-pr=gptassist.create_git_pr_diff_for_gpt:main",
            "gdiff-unstaged=gptassist.create_git_unstaged_diff:log_git_changes",
        ],
    },
)
