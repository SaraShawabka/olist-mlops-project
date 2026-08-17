# Olist MLOps Project

## Project Overview

An end-to-end Machine Learning Operations (MLOps) project built using the Brazilian E-Commerce Public Dataset by Olist.

The project focuses on predicting whether an e-commerce order will be delivered late or on time.

## Business Problem

Late deliveries can negatively affect customer satisfaction and the overall e-commerce experience.

The goal of this project is to build a machine learning solution that can predict delivery delays based on information available about an order.

## Objective

The main objective is to develop an end-to-end machine learning pipeline that:

* Ingests the Olist e-commerce data
* Stores and manages the data using PostgreSQL
* Performs data exploration and preprocessing
* Engineers features for machine learning
* Trains a classification model
* Evaluates model performance
* Follows MLOps practices for reproducibility and version control

## Dataset

The project uses the **Brazilian E-Commerce Public Dataset by Olist**.

The dataset contains information about:

* Orders
* Customers
* Sellers
* Products
* Payments
* Reviews
* Order items
* Geolocation
* Product categories

The raw dataset is not stored in this repository.

## Technologies

* Python
* Pandas
* NumPy
* Scikit-learn
* PostgreSQL
* Docker
* Git
* GitHub
* Jupyter Notebook

Additional tools and technologies will be added as the project evolves.

## Project Structure

```text
olist-mlops-project/
│
├── data/
│   ├── raw/
│   └── processed/
│
├── sql/
│
├── notebooks/
│
├── src/
│
├── tests/
│
├── docs/
│
├── .gitignore
└── README.md
```

## Project Workflow

The project will be developed through the following stages:

1. Data ingestion
2. Database setup
3. Data exploration
4. Data preprocessing
5. Feature engineering
6. Model development
7. Model evaluation
8. ML pipeline development
9. Testing
10. Documentation and deployment

## Current Status

🚧 Project in progress.

Currently, the project structure and Git/GitHub version control setup have been completed.

More components will be added as development progresses.

## Future Improvements

Potential future improvements include:

* Automated data pipelines
* Model tracking
* Model versioning
* Automated testing
* Model deployment
* API development
* CI/CD integration
* Model monitoring
