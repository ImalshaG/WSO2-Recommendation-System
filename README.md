# AI based Recommendation System for the API Store

## What is WSO2 API Manager?

WSO2 API Manager is a full lifecycle API Management solution which has an API Gateway and a Microgateway. See more on https://wso2.com/api-management/


## What is API Recommendation System?

WSO2 API Manager Store Portal is a marketplace for APIs. Developers can login to the portal to choose and subscribe which APIs to leverage in their applications. Currently, the developer has to pick the APIs of interest by browsing through the APIs or searching with a particular information associated with the API. API Recommendation System recommends APIs which can be beneficial for the developer using AI technologies. 


# Quick Start Guide

## Prerequisites

1. Install Java 7 or 8 (https://www.oracle.com/technetwork/java/javase/downloads/index.html).
2. Download and install WSO2 API Manager version 3.0.0 (https://wso2.com/api-management/).
3. Install Python 3.6 or higher.
4. Install pip if not already installed.
5. Install virtualenv and start a virtual environment using the following commands.
    ```
    $ pip install virtualenv
    $ cd <project-home-directory>
    $ virtualenv venv
    $ source venv/bin/activate
    ```
6. Install the required python packages in the above created virtual environment, by running the following command in the project home directory.
    ```
    $ pip install -r requirements.txt
    ```
7. Create a mongodb instance at the ports: 27017-27019
8. Add the following configurations to the `<API-M_HOME>/repository/conf.deployment.toml` file.
    ```
    [apim.devportal.recommendation]
    url = "https://localhost:8082/"
    username = "admin"
    password = "admin"
    ```
9. To start the recommendation server, run `<project-home-directory>/bin/recommendation-server.sh`
    

   
