import os
import math
import random
import datetime
from mcp.server.fastmcp import FastMCP

from mcp.server.transport_security import TransportSecuritySettings

mcp = FastMCP(
    "My MCP Server",
    transport_security=TransportSecuritySettings(
        enable_dns_rebinding_protection=False
    )
)

mcp = FastMCP("My MCP Server")

# ─── CALCULATOR TOOLS ───────────────────────────────────────────────

@mcp.tool()
def calculate(expression: str) -> str:
    """Evaluate a math expression. Examples: '2 + 2', 'sqrt(144)', '2 ** 8'"""
    try:
        allowed = {k: v for k, v in math.__dict__.items() if not k.startswith("_")}
        result = eval(expression, {"__builtins__": {}}, allowed)
        return f"Result: {result}"
    except Exception as e:
        return f"Error: {e}"

@mcp.tool()
def convert_units(value: float, from_unit: str, to_unit: str) -> str:
    """Convert between km/miles, kg/lbs, celsius/fahrenheit, meters/feet"""
    conversions = {
        ("km", "miles"): lambda x: x * 0.621371,
        ("miles", "km"): lambda x: x * 1.60934,
        ("kg", "lbs"): lambda x: x * 2.20462,
        ("lbs", "kg"): lambda x: x * 0.453592,
        ("celsius", "fahrenheit"): lambda x: x * 9/5 + 32,
        ("fahrenheit", "celsius"): lambda x: (x - 32) * 5/9,
        ("meters", "feet"): lambda x: x * 3.28084,
        ("feet", "meters"): lambda x: x * 0.3048,
    }
    key = (from_unit.lower(), to_unit.lower())
    if key in conversions:
        return f"{value} {from_unit} = {round(conversions[key](value), 4)} {to_unit}"
    return f"Conversion from {from_unit} to {to_unit} not supported."

@mcp.tool()
def word_count(text: str) -> str:
    """Count words, characters, and sentences in text."""
    return (f"Words: {len(text.split())}\n"
            f"Characters: {len(text)}\n"
            f"Sentences: {text.count('.') + text.count('!') + text.count('?')}")

@mcp.tool()
def reverse_text(text: str) -> str:
    """Reverse a string of text."""
    return text[::-1]

@mcp.tool()
def generate_password(length: int = 16, include_symbols: bool = True) -> str:
    """Generate a random secure password."""
    import string
    chars = string.ascii_letters + string.digits
    if include_symbols:
        chars += "!@#$%^&*"
    return f"Password: {''.join(random.choices(chars, k=length))}"

@mcp.tool()
def get_current_datetime() -> str:
    """Get the current date and time."""
    return datetime.datetime.now().strftime("Date: %A, %d %B %Y\nTime: %H:%M:%S")

@mcp.tool()
def days_until(target_date: str) -> str:
    """Days until a date. Format: YYYY-MM-DD"""
    try:
        delta = (datetime.datetime.strptime(target_date, "%Y-%m-%d").date() - datetime.date.today()).days
        if delta > 0: return f"{delta} days until {target_date}"
        elif delta == 0: return "That's today!"
        else: return f"That was {abs(delta)} days ago."
    except ValueError:
        return "Invalid date format. Use YYYY-MM-DD."

@mcp.tool()
def roll_dice(sides: int = 6, count: int = 1) -> str:
    """Roll dice. E.g. roll_dice(20) for a d20."""
    rolls = [random.randint(1, sides) for _ in range(count)]
    return f"🎲 Rolled {count}d{sides}: {rolls} — Total: {sum(rolls)}"

@mcp.tool()
def flip_coin() -> str:
    """Flip a coin."""
    return f"🪙 {random.choice(['Heads', 'Tails'])}!"

@mcp.tool()
def pick_random(options: str) -> str:
    """Pick randomly from a comma-separated list. E.g. 'pizza, sushi, tacos'"""
    items = [i.strip() for i in options.split(",") if i.strip()]
    return f"🎯 Picked: {random.choice(items)}" if items else "No options provided."

if __name__ == "__main__":
    import uvicorn
    app = mcp.streamable_http_app()
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8000)), forwarded_allow_ips="*")