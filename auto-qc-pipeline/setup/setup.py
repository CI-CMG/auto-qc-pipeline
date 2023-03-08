import setuptools

with open("README.md", "r") as fh:
  long_description = fh.read()

with open('requirements.txt') as f:
  requirements = f.read().splitlines()

setuptools.setup(
  name="autoqc-pipeline",
  version="${wheel.version}",
  description="Runs AutoQC in a multiprocessing EIP pipeline",
  long_description=long_description,
  long_description_content_type="text/markdown",
  url="https://github.com/ci-cmg/auto-qc-pipeline",
  package_dir={'': 'src'},
  packages=setuptools.find_packages('src'),
  classifiers=[
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
  ],
  python_requires='>=3.9',
  install_requires=[req for req in requirements if req[:2] != "# " and not req.startswith("git")]
)