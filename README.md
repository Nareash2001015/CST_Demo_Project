

# Flask-RESTful

[![Build Status](https://travis-ci.org/flask-restful/flask-restful.svg?branch=master)](http://travis-ci.org/flask-restful/flask-restful)
[![Coverage Status](http://img.shields.io/coveralls/flask-restful/flask-restful/master.svg)](https://coveralls.io/r/flask-restful/flask-restful)
[![PyPI Version](http://img.shields.io/pypi/v/Flask-RESTful.svg)](https://pypi.python.org/pypi/Flask-RESTful)

Flask-RESTful provides the building blocks for creating a great REST API.

## Project goals

1) Rest Endpoint to filter the customer details
	- Operation
		 - The customer details are returned as the list of objects and joined to refer the repository name.
2) Rest Endpoint to trigger the Azure Devops pipeline 
	 - operation: 
		 - The Request pushes the repository to the github and Azure Devops pipeline is triggered automatically.
		 - The pipeline checkouts the repositories filtered through the first API.
3) Rest Endpoint to check the status of the jobs running through the Azure Devops pipeline.

## Technologies used

1) Azure Devops
2) Python Flask
3) MySQL DBMS

## Steps

### Way 1
1) Install python
2) Install flask
3) Clone Repository
	-  ` git clone https://github.com/Nareash20010150/CST_Demo_Project.git`
	-  ` cd CST_Demo_Project/`
	- `  flask -app flakr run `

### Way 2
1) Install Docker
2) Start docker daemon
3) Use the commands
	- `docker build -t flask_cst_app .`
	-  `docker run -p 5000:5000 --name flask_cst_app flask_cst_app:latest` 
