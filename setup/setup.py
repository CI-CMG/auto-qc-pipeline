import setuptools

with open("README.md", "r") as fh:
  long_description = fh.read()

with open('requirements.txt') as f:
  requirements = f.read().splitlines()

setuptools.setup(
  name="auto-qc-pipeline",
  version="${wheel.version}",
  description="Runs AutoQC in a queue with multiple processors",
  long_description=long_description,
  long_description_content_type="text/markdown",
  url="https://github.com/ci-cmg/auto-qc-pipeline",
  package_dir={'tests': ''},
  packages=setuptools.find_packages(exclude=['tests']),
  classifiers=[
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: Implementation :: CPython",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
  ],
  python_requires='>=3.9',
  install_requires=[req for req in requirements if req[:2] != "# "]
)