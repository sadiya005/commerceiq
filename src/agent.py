import json

from dotenv import load_dotenv
from groq import Groq

from src.config import (
    GROQ_API_KEY,
    TEXT_MODEL
)

from src.tools import (
    TOOL_SCHEMAS,
    AVAILABLE_FUNCTIONS
)


load_dotenv()


client = Groq(
    api_key=GROQ_API_KEY
)


SYSTEM_PROMPT = """
You are CommerceIQ, an e-commerce analytics agent.

Use the available CommerceIQ business tools to answer
questions using actual dataset evidence.

Rules:
- Use tools whenever business data is required.
- You may call multiple tools when necessary.
- Do not invent numbers or business facts.
- Revenue values are in British pounds (£).
- Do not claim profitability unless profitability data
  is explicitly provided.
- Do not invent customer motivations or future behavior.
- If the available data is insufficient, say so.
- Only use the tools provided.
- Do not create or call unavailable tools.
- Stop using tools when enough evidence is available.
"""


def commerceiq_agent(
    question,
    max_steps=5
):
    """Run the CommerceIQ multi-step agent."""

    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        },
        {
            "role": "user",
            "content": question
        }
    ]

    tool_calls_log = []

    for _ in range(max_steps):

        response = client.chat.completions.create(
            model=TEXT_MODEL,
            messages=messages,
            tools=TOOL_SCHEMAS,
            tool_choice="auto",
            temperature=0
        )

        assistant_message = (
            response.choices[0].message
        )

        if not assistant_message.tool_calls:
            return {
                "answer": assistant_message.content,
                "tool_calls": tool_calls_log
            }

        messages.append(
            assistant_message
        )

        for tool_call in (
            assistant_message.tool_calls
        ):

            function_name = (
                tool_call.function.name
            )

            arguments = json.loads(
                tool_call.function.arguments
            )

            if function_name not in AVAILABLE_FUNCTIONS:
                raise ValueError(
                    f"Unknown tool requested: "
                    f"{function_name}"
                )

            function = AVAILABLE_FUNCTIONS[
                function_name
            ]

            if function_name == "revenue_summary":
                result = function()
                arguments = {}
            else:
                result = function(
                    **arguments
                )

            tool_calls_log.append({
                "tool": function_name,
                "arguments": arguments
            })

            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": json.dumps(result)
            })

    return {
        "answer": (
            "The agent could not complete the "
            "analysis within the allowed number "
            "of steps."
        ),
        "tool_calls": tool_calls_log
    }