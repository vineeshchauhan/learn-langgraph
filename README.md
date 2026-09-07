# Project environment creation guide
## Install python version
    python --version
## A virtual environment is an isolated Python environment that allows you to manage dependencies for each project  separately. It prevents conflicts between projects and avoids affecting the system-wide Python installation. Tools like venv or virtualenv are commonly used to create them.
### 1- Avoid Dependency Conflicts
### 2- Isolate Project Environments
### 3- Simplifies Project Management
### 4- Prevents System Interference
### 5- Enables Reproducibility


## install virtualenv
    pip install virtualenv
## check virtualenv version
    virtualenv --version
## create virtual environment 
    virtualenv my_env
## activate virtual environment
    cd my_env
    Scripts\activate
## deactivate virtual environment
    cd my_env
    deactivate
## Install dependencies
    pip3 install -r requirements.txt
