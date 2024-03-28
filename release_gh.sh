#!/bin/bash

# clear previous build files
rm -rf build/ dist/ *.egg-info

# build the package
python setup.py sdist bdist_wheel

# read version from setup.py
version=$(grep "__version__" setup.py | awk -F\' '{print $2}' | tr -d '\n')

# create github release with gh
gh release create "${version}" "dist/gptgitassist-${version}-py3-none-any.whl"
