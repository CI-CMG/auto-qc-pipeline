# auto-qc-pipeline

## Setting up the Python Environment

# MacOS
  1. Install pyenv (https://github.com/pyenv/pyenv#set-up-your-shell-environment-for-pyenv)
     1. ```brew update```
     2. ```brew install pyenv```
     3. In ~/.bashrc add
        1. ```export PYENV_ROOT="$HOME/.pyenv"```
        2. ```export PATH="$PYENV_ROOT/bin:$PATH"```
        3. ```eval "$(pyenv init -)"```
     4. ```brew install openssl readline sqlite3 xz zlib tcl-tk```
  2. Install pyenv-virtualenv (https://github.com/pyenv/pyenv-virtualenv)
     1. ```brew install pyenv-virtualenv```
     2. In ~/.bashrc add
         1. ```eval "$(pyenv virtualenv-init -)"```
  3. Open a new terminal
  4. Install Python version
     1. ```env PYTHON_CONFIGURE_OPTS="--enable-shared" pyenv install 3.9.2```
     2. Optional: set global version of Python ```env PYTHON_CONFIGURE_OPTS="--enable-shared" pyenv global 3.9.2```
  5. Create virtual env
     1. ```pyenv virtualenv 3.9.2 auto-qc-pipeline-1.0.0-SNAPSHOT```
  6. Set local version of python (if not done already)
     1. change directory to root of project
     2. ```pyenv local auto-qc-pipeline-1.0.0-SNAPSHOT```

# Other OS
  1. TODO

## Setting up IntelliJ

  1. Install the IntelliJ Python plugin
  2. Set up pyenv
     1. File -> Project Structure or CMD + ;
     2. SDKs -> + -> Add Python SDK -> Virtual Environment
     3. Select Existing Environment
     4. Choose ~/.pyenv/versions/uscg-split-survey-1.0.0-SNAPSHOT/bin/python
  3. Set up Python Facet (not sure if this is required)
     1. File -> Project Structure or CMD + ;
     2. Facets -> + -> Python 
     3. Set interpreter 

## Installing Dependencies

  1. Add dependencies with versions to requirements.txt
  2. ```pip install --upgrade pip && pip install -r requirements_dev.txt```

## Maven
This project can use Apache Maven to easily build this project.  However, this is not required, but recommended.
Maven can be easily installed by downloading it from the Maven site or using sdkman.

## Build with Maven
After setting up your pyenv run:
```mvn clean package```

## Executable
This project uses pyinstaller to build a system native application.  The application will be located at dist/split_survey.

Run the application:
```split_survey/split_survey <input_csv_file> <output_directory> <max_time_seconds> <max_distance_km>```
Ex.
```split_survey/split_survey AllData_3col.xyz AllData_3col_split 86400 1000```