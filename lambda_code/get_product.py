from productos import productos
from responses import create_response


def handler(event, context):

    path_parameters = event.get("pathParameters") or {}

    product_id = path_parameters.get("id")

    if not product_id:
        return create_response(
            400,
            {"error": "Product ID required"}
        )

    product = productos.get(product_id)

    if not product:
        return create_response(
            404,
            {"error": "Product not found"}
        )

    return create_response(
        200,
        product
    )



