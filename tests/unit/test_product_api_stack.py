import aws_cdk as core
import aws_cdk.assertions as assertions

from product_api.product_api_stack import ProductApiStack

# example tests. To run these tests, uncomment this file along with the example
# resource in product_api/product_api_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = ProductApiStack(app, "product-api")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
