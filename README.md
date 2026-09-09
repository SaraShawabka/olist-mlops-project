# Olist MLOps Project

## Project Overview

An end-to-end Machine Learning Operations (MLOps) project built using the Brazilian E-Commerce Public Dataset by Olist.

The project focuses on predicting whether an e-commerce order will be delivered **late or on time**.

The project is developed progressively, from data ingestion and exploration to model development and a production-ready prediction service.

## Business Problem

Late deliveries can negatively affect customer satisfaction and the overall e-commerce experience.

The goal of this project is to build a machine learning solution that can predict potential delivery delays based on information available at the time of prediction.

## Objective

The main objective is to develop an end-to-end machine learning workflow that:

- Ingests and manages Olist e-commerce data
- Stores and queries data using PostgreSQL
- Performs data exploration and analysis
- Preprocesses and engineers features for machine learning
- Trains and evaluates a classification model
- Builds a reusable prediction pipeline
- Exposes the trained model through a REST API
- Validates prediction inputs before inference
- Follows MLOps practices for reproducibility, version control, and production readiness

## Dataset

The project uses the **Brazilian E-Commerce Public Dataset by Olist**.

The dataset contains information about:

- Orders
- Customers
- Sellers
- Products
- Payments
- Reviews
- Order items
- Geolocation
- Product categories

The raw dataset is not stored in this repository due to its size.

The data is processed and transformed throughout the project to prepare it for analysis and machine learning.

## Technologies

- Python
- Pandas
- NumPy
- Scikit-learn
- XGBoost
- PostgreSQL
- Docker
- FastAPI
- Great Expectations
- Joblib
- PyYAML
- Git
- GitHub
- Jupyter Notebook
## Project Structure

olist-mlops-project/
│
├── app/
│   └── main.py
│
├── artifacts/
│   ├── models/
│   └── ...
│
├── config/
│   └── config.yaml
│
├── data/
│   ├── raw/
│   └── processed/
│
├── great_expectations/
│   ├── expectations/
│   ├── validation_definitions/
│   └── great_expectations.yml
│
├── notebooks/
│
├── sql/
│
├── src/
│   ├── features.py
│   ├── predictor.py
│   ├── preprocessing.py
│   └── validation.py
│
├── tests/
│
├── requirements.txt
├── .gitignore
└── README.md


## Project Workflow

The project is developed through the following stages:

1. Data ingestion and database setup
2. Data exploration and analysis
3. Data preprocessing
4. Feature engineering
5. Model development
6. Model evaluation
7. Production prediction service
8. Input data validation
9. Testing
10. Containerization and deployment
11. CI/CD integration
12. Model monitoring

## Current Status

🚧 **Project in progress**

The following components have been completed:

- Data ingestion and database setup
- Data exploration and analysis
- Feature engineering
- Classification model development
- Model evaluation
- Production prediction API
- Single and batch prediction endpoints
- Input validation with Great Expectations
- Git/GitHub version control

The next stages focus on testing, containerization, CI/CD, deployment, and model monitoring.

## Future Improvements

Potential future improvements include:

- Automated testing
- Dockerized application deployment
- CI/CD integration
- Experiment and model tracking
- Model versioning
- Model monitoring
- Automated retraining workflows
- Cloud deployment
