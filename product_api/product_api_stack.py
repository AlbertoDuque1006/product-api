from aws_cdk import (
    Stack,
    aws_lambda as lambda_,
    aws_apigateway as apigw,
)

from constructs import Construct


class ProductApiStack(Stack):

    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        **kwargs
    ):
        super().__init__(scope, construct_id, **kwargs)

        # Lambda que ejecuta get_product.py
        get_product = lambda_.Function(
            self,
            "GetProductFunction",
            runtime=lambda_.Runtime.PYTHON_3_12,
            handler="get_product.handler",
            code=lambda_.Code.from_asset("lambda_code"),
        )

        # API Gateway
        api = apigw.RestApi(
            self,
            "ProductsApi",
            rest_api_name="Products API",
        )

        # /products
        products = api.root.add_resource("products")

        # /products/{id}
        product_by_id = products.add_resource("{id}")

        # GET /products/{id}
        product_by_id.add_method(
            "GET",
            apigw.LambdaIntegration(get_product)
        )