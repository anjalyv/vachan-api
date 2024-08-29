# Makefile Explanation

## Variable Definitions:

- ENVPATH := vachan-ENV: Defines a variable named ENVPATH and assigns it the value "vachan-ENV". This variable will likely be used to reference the path to a virtual environment.
- ACTIVATE_VENV := . $(ENVPATH)/bin/activate &&: Defines another variable named ACTIVATE_VENV. The value assigned to it is a command that will activate the virtual environment located in the ENVPATH directory. It uses the . command to source the activate script in the virtual environment's bin directory, and the && operator ensures that the subsequent command (which will likely be used later in the Makefile) is only executed if the activation is successful.
- SHELL := /bin/bash: Sets the default shell to use for executing commands within the Makefile. In this case, it's set to /bin/bash.

## Phony Targets:

- PHONY: pre-requistite venv-configure venv-activate install-dependencies check-package into-database environmental-variables installing-usfmgrammar installing-docker kratosconfig: Declares several targets as "phony". Phony targets are not actual files but are used to represent specific actions within the Makefile. This line ensures that Make doesn't treat these targets as files and doesn't try to rebuild them.

## Make Targets:

- pre-requisite:: Checks if the python3-pip and python3-venv packages are installed. If not, it installs them using sudo apt install.
- venv-configure:: Creates a virtual environment in the directory specified by ENVPATH using the python3 -m venv command.
- venv-activate:: Activates the virtual environment using the ACTIVATE_VENV variable.
- install-dependencies:: Installs the dependencies listed in the requirements.txt file using pip install within the activated virtual environment.
- check-package:: Checks if all the packages listed in requirements.txt are installed. If any are missing, it installs them using pip install.
- installing-psql:: Checks if PostgreSQL version 15.3 is installed. If not, it prompts the user to install it and then installs it using sudo apt install.
- environmental-variables:: Makes a script named setup.sh executable and then runs it. This script likely sets certain environment variables needed for the project.
- installing-docker:: Checks if Docker version 24.0.1 or above is installed. If not, it prompts the user to install it and then installs it using the official Docker repository.
- run-app:: Navigates to the cd app folder and runs uvicorn main:app --port=7000 --debug --reload to start the app

## Default Target:

- setup:: The default target that is executed when you run make without specifying a specific target. It calls all the other targets in sequence, effectively setting up the entire project environment.