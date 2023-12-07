# 1. About this repository

		This repo has a script for open movie database management like POST, GET, and DELETE movies from the application

clone repo: git clone {repositary URL}

# 2. Prerequisites

	* Install any one IDE for Python(Visual studio code, PyCharm)
		* Link for Visual Studio Code(Python extensions needs to install separately)
			https://code.visualstudio.com/docs/?dv=win64user
		* Link for Pycharm Installation
			https://www.jetbrains.com/help/pycharm/installation-guide.html#toolbox

	* Install pip from the below link
		https://phoenixnap.com/kb/install-pip-windows

	* Install python 3.X
		https://www.python.org/downloads/

* Install the required modules of the application
		requests
		flask==2.1.3
		flask-restplus
		Werkzeug==2.0.3
		python-dotenv
		jinja2==3.0.3
		itsdangerous==2.1.2
		flask-sqlalchemy==2.5.1

# 3. Module/Library Explanations

Python:
=======
	Python is a general programming language. Downloading and Installing Python is free and easy.

Flask:
======
    Flask is a popular web framework, meaning it is a third-party Python library used for developing web applications and API’s.

Flask Rest Plus and Werkzeug:
========================
	Flask-RESTPlus and Werkzeug is an extension for Flask that encourages best practices with minimal setup. It provides a collection of decorators and tools to describe API and expose its documentation using Swagger.

Flask-SQLAlchemy:
================
    Flask-SQLAlchemy is an extension for Flask that adds support for SQLAlchemy to your application. It aims to simplify using SQLAlchemy with Flask by providing useful defaults and extra helpers that make it easier to accomplish common tasks.

# 4. Folders and Files:
Secret files:
=============
	you should create a .env file to store the secret variables(It should be below the variable).
		*apikey" = "omdp app apikey"
		*user" = "username"
		*password" = "password"
	helpers ----->  Start app file will use the methods or functions from this folder.
	models  ----->  This folder has all the request models of the APIs
		* What are the request parameters
		* What type of parameter it is like string, list, and dropdown?
	start_app.py   ----->  Start app file will start the application with the host URL and Port.
	authorizations.py--->  Basic Auth enabled for delete movies API
	tests          -----> This folder performs unit testing of all APIs.
	Dockerfile   ----->  Dockerfile of application with all installation commands.

# 5. Application Details (How to start the application in Locally)

	After installing all the pre requisites, you can start the application with the below command

		-------python start_app.py

Once start the application, you will see below output

PS C:\QlikAssignment> python .\start_app.py
		* Serving Flask app "start_app" (lazy loading)
		* Environment: production
		WARNING: This is a development server. Do not use it in a production deployment.
		Use a production WSGI server instead.
		* Debug mode: on
		* Restarting with stat
		* Debugger is active!
		* Debugger PIN: 271-357-746
		* Running on http://127.0.0.1:5002/ (Press CTRL+C to quit)

Application URL: http://127.0.0.1:5002/

# 6.Deploy a Flask app in GCP
	We can deploy the flask application in different approaches.

	* To use Google App Engine
	* To create Google cloud Run
		1.Create a docker container
		 	This way is very useful for setting up a continuous deployment to deploy whenever the code is pushed to Source(Github).
			By Connecting the GitHub repositories to Cloud Run.
				* Once configured Github repository, we need to fill the options in the Build Configuration Step.
				* Select Branch(Github branch name Ex:main) and Branch type(Ex:Dockerfile and Google Cloud Buildpacks)
				* After the continuous build step, the push to the branch we configure will trigger the new version to deploy in the Cloud Run.
		2.Directly from the source
			When we deploy the cloud project from the source, the cloud tool identifies the application type and sets up the cloud build to build the container and deploy it in Google Cloud Run.
			Deploy from source using the following command.
			* gcloud run deploys order-service --source .
			* This approach does not have Dockerfile.Buildpacks automatically determines that this is a Python application. It know how to run the python application and how to start the python server from Procfile. Buildpacks build a docker container image for the application, so we don't need to worry about managing the base image - as it's all managed by Google and tooling to build the container image locally or how to containerize your app.

HTTP Methods:
=============
* GET - (Retrieve) Get the data from the Database in encrypted form.
* POST - (Create) Used to send data in an encrypted format to Database.
* DELETE - Delete all current records of the target resource.