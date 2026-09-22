from src.analytics import (
    lookup_customer,
    lookup_product,
    revenue_summary,
    top_revenue_products
)


AVAILABLE_FUNCTIONS = {
    "lookup_customer": lookup_customer,
    "lookup_product": lookup_product,
    "revenue_summary": revenue_summary,
    "top_revenue_products": top_revenue_products
}


TOOL_SCHEMAS = [
    {
        "type": "function",
        "function": {
            "name": "lookup_customer",
            "description": (
                "Look up business information "
                "for a CommerceIQ customer."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "customer_id": {
                        "type": "integer",
                        "description": (
                            "CommerceIQ customer ID."
                        )
                    }
                },
                "required": ["customer_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "lookup_product",
            "description": (
                "Look up business information "
                "for a CommerceIQ product."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "stock_code": {
                        "type": "string",
                        "description": (
                            "CommerceIQ product stock code."
                        )
                    }
                },
                "required": ["stock_code"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "revenue_summary",
            "description": (
                "Return overall CommerceIQ "
                "revenue and business summary."
            ),
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "top_revenue_products",
            "description": (
                "Return the highest-revenue "
                "CommerceIQ merchandise products."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "top_k": {
                        "type": "integer",
                        "description": (
                            "Number of top products to return."
                        )
                    }
                },
                "required": ["top_k"]
            }
        }
    }
]


def execute_tool(
    function_name,
    arguments=None
):
    """Execute a CommerceIQ business tool."""

    if function_name not in AVAILABLE_FUNCTIONS:
        raise ValueError(
            f"Unknown CommerceIQ tool: "
            f"{function_name}"
        )

    arguments = arguments or {}

    function = AVAILABLE_FUNCTIONS[
        function_name
    ]

    return function(**arguments)