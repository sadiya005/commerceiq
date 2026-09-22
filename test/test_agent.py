import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

sys.path.insert(
    0,
    str(PROJECT_ROOT)
)

from src.agent import commerceiq_agent


result = commerceiq_agent(
    "Compare customer 12346's revenue "
    "with the overall CommerceIQ revenue."
)


print("Agent answer:")
print(result["answer"])

print("\nTools used:")

for tool_call in result["tool_calls"]:
    print(
        "-",
        tool_call["tool"],
        tool_call["arguments"]
    )


assert result["answer"] is not None

assert len(
    result["tool_calls"]
) >= 1

tool_names = [
    call["tool"]
    for call in result["tool_calls"]
]

assert "lookup_customer" in tool_names
assert "revenue_summary" in tool_names

print("\nAgent validation: PASS")