# Product API — Serverless REST API with AWS CDK

A serverless REST API built with **Python**, **AWS Lambda**, **Amazon API Gateway**, and **AWS CDK**.

This project was created as a practical implementation of Infrastructure as Code (IaC), demonstrating how to define, deploy, and manage a simple REST API entirely from code.

---

## Overview

The API exposes product information through a REST endpoint.

A client sends an HTTP request to Amazon API Gateway. API Gateway invokes an AWS Lambda function, which processes the request and returns the corresponding product as a JSON response.

### Request flow

```text

Client

  │

  │ GET /products/{id}

  ▼

Amazon API Gateway

  │

  ▼

AWS Lambda

  │

  ▼

Product Data

  │

  ▼

JSON Response

```

The infrastructure is defined using **AWS CDK with Python**, allowing the complete AWS environment to be created and updated from source code.

---

## Architecture

The project currently provisions the following AWS resources:

- **Amazon API Gateway**

  - REST API

  - `/products/{id}` resource

  - `GET` method

- **AWS Lambda**

  - Python 3.12 runtime

  - Handles product retrieval

- **AWS IAM**

  - Execution role generated and managed by AWS CDK

- **Amazon CloudWatch**

  - Lambda execution logs

- **AWS CloudFormation**

  - Infrastructure deployment and lifecycle management

---

## Technologies

| Technology | Purpose |

|---|---|

| Python | Lambda application logic |

| AWS Lambda | Serverless compute |

| Amazon API Gateway | REST API exposure |

| AWS CDK | Infrastructure as Code |

| AWS CloudFormation | Infrastructure provisioning |

| AWS IAM | Permissions and execution roles |

| Amazon CloudWatch | Logging and monitoring |

| Git | Version control |

---

## Project Structure

```text

product-api/

│

├── lambda_code/

│   ├── get_product.py

│   ├── productos.py

│   └── responses.py

│

├── product_api/

│   ├── __init__.py

│   └── product_api_stack.py

│

├── tests/

│   ├── __init__.py

│   └── unit/

│       ├── __init__.py

│       └── test_product_api_stack.py

│

├── app.py

├── cdk.json

├── requirements.txt

├── requirements-dev.txt

├── .gitignore

└── README.md

```

### `lambda_code/`

Contains the application code executed by AWS Lambda.

**`get_product.py`**

Contains the Lambda handler responsible for receiving the API Gateway event, extracting the product ID, searching for the product, and returning the appropriate HTTP response.

**`productos.py`**

Contains the sample product dataset used by the API.

**`responses.py`**

Provides a reusable function for generating HTTP responses with JSON serialization, status codes, headers, and CORS configuration.

### `product_api/`

Contains the AWS infrastructure definition.

**`product_api_stack.py`**

Defines the AWS resources using CDK:

```text

API Gateway

      │

      ▼

/products/{id}

      │

     GET

      │

      ▼

AWS Lambda

```

---

## API Endpoint

### Get product by ID

```http

GET /products/{id}

```

Example:

```http

GET /products/1

```

Example response:

```json

{

  "id": "1",

  "nombre": "Laptop Lenovo",

  "precio": 2500000,

  "stock": 10,

  "categoria": "Computadores"

}

```

### Possible responses

#### `200 OK`

The product exists and is returned successfully.

```json

{

  "id": "1",

  "nombre": "Laptop Lenovo",

  "precio": 2500000,

  "stock": 10,

  "categoria": "Computadores"

}

```

#### `400 Bad Request`

The request does not contain a product ID.

#### `404 Not Found`

No product exists with the requested ID.

---

## Lambda Handler

The Lambda function follows the standard AWS handler structure:

```python

def handler(event, context):

    ...

```

API Gateway sends an event containing the request information.

For the endpoint:

```http

GET /products/1

```

the product ID is obtained from:

```python

event["pathParameters"]["id"]

```

The Lambda function then searches the product dataset and returns an HTTP response.

---

## Infrastructure as Code

The infrastructure is defined with AWS CDK instead of manually creating resources from the AWS Console.

For example, the Lambda function is defined using:

```python

get_product = lambda_.Function(

    self,

    "GetProductFunction",

    runtime=lambda_.Runtime.PYTHON_3_12,

    handler="get_product.handler",

    code=lambda_.Code.from_asset("lambda_code"),

)

```

API Gateway is also created through CDK:

```python

api = apigw.RestApi(

    self,

    "ProductsApi",

    rest_api_name="Products API",

)

```

The route is connected to the Lambda function:

```python

products = api.root.add_resource("products")

product_by_id = products.add_resource("{id}")

product_by_id.add_method(

    "GET",

    apigw.LambdaIntegration(get_product)

)

```

This makes the infrastructure reproducible and version-controlled.

---

## Local Setup

### 1. Clone the repository

```bash

git clone <repository-url>

cd product-api

```

### 2. Create a Python virtual environment

```bash

python3 -m venv .venv

```

Activate it on macOS/Linux:

```bash

source .venv/bin/activate

```

### 3. Install dependencies

```bash

pip install -r requirements.txt

```

---

## AWS Authentication

Before deploying, make sure the AWS CLI is authenticated.

Check the current identity:

```bash

aws sts get-caller-identity

```

If authentication is required:

```bash

aws login

```

Check the configured region:

```bash

aws configure get region

```

You can change it with:

```bash

aws configure set region <aws-region>

```

> AWS credentials, tokens, account IDs, `.env` files, and local AWS configuration should never be committed to the repository.

---

## AWS CDK Deployment

### Synthesize the infrastructure

```bash

cdk synth

```

This converts the CDK application into an AWS CloudFormation template.

### Review infrastructure changes

```bash

cdk diff

```

This shows the resources that will be created, modified, or removed.

### Bootstrap the AWS environment

CDK requires a bootstrap stack before the first deployment to an AWS account and region.

```bash

cdk bootstrap aws://<account-id>/<region>

```

The account ID should **not** be hardcoded into the repository.

You can obtain your current AWS account information locally using:

```bash

aws sts get-caller-identity

```

### Deploy

```bash

cdk deploy

```

CDK will:

```text

Python CDK Code

      │

      ▼

cdk synth

      │

      ▼

CloudFormation Template

      │

      ▼

AWS CloudFormation

      │

      ├── IAM Role

      ├── Lambda

      ├── API Gateway

      └── CloudWatch Logs

```

After deployment, CDK outputs the API Gateway base URL.

---

## Testing the API

After deployment, call the endpoint using the generated API Gateway URL:

```bash

curl https://<api-id>.execute-api.<region>.amazonaws.com/prod/products/1

```

Example response:

```json

{

  "id": "1",

  "nombre": "Laptop Lenovo",

  "precio": 2500000,

  "stock": 10,

  "categoria": "Computadores"

}

```

The endpoint can also be tested using tools such as Postman.

---

## Updating the API

After modifying the Lambda code or CDK infrastructure, review the changes:

```bash

cdk diff

```

Then deploy the new version:

```bash

cdk deploy

```

AWS CDK detects the changes and updates the corresponding resources through CloudFormation.

---

## Removing the Infrastructure

To remove the AWS resources created by this project:

```bash

cdk destroy

```

Always review the resources before deleting a stack.

---

## Security

Sensitive AWS information is intentionally excluded from version control.

The repository ignores local and generated files such as:

```text

.venv/

venv/

cdk.out/

.cdk.staging/

.env

.env.*

.aws/

.DS_Store

.vscode/

.idea/

```

AWS credentials should be managed through the AWS CLI or another supported AWS authentication mechanism rather than stored in source code.

---

## Current Scope

The current version focuses on a simple read operation:

```http

GET /products/{id}

```

The product data is currently stored in memory for learning and demonstration purposes.

Possible future improvements include:

- `GET /products`

- `POST /products`

- `PUT /products/{id}`

- `DELETE /products/{id}`

- Amazon DynamoDB persistence

- Request validation

- Automated tests

- API authentication

- CI/CD with GitHub Actions

- Multiple deployment environments (`dev`, `staging`, `prod`)

---

## What This Project Demonstrates

This project demonstrates practical experience with:

- Building serverless APIs

- AWS Lambda handlers

- REST API design

- API Gateway and Lambda integration

- Infrastructure as Code

- AWS CDK

- CloudFormation deployments

- IAM execution roles

- CloudWatch logging

- AWS CLI authentication

- Infrastructure deployment and updates

- Git-based infrastructure versioning

---

## Author

**Alberto Duque**

Backend & Automation Developer

GitHub: `AlbertoDuque1006`

---

## License

This project is intended for educational and portfolio purposes.