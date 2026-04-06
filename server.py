from mcp.server.fastmcp import FastMCP
import math
import random
import datetime

mcp = FastMCP("My MCP Server")

# ─── CALCULATOR TOOLS ───────────────────────────────────────────────

@mcp.tool()
def calculate(expression: str) -> str:
    """
    Evaluate a math expression safely.
    Examples: "2 + 2", "10 * 5", "sqrt(144)", "2 ** 8"
    """
    try:
        allowed = {k: v for k, v in math.__dict__.items() if not k.startswith("_")}
        result = eval(expression, {"__builtins__": {}}, allowed)
        return f"Result: {result}"
    except Exception as e:
        return f"Error evaluating expression: {e}"


@mcp.tool()
def convert_units(value: float, from_unit: str, to_unit: str) -> str:
    """
    Convert between common units.
    Supported: km/miles, kg/lbs, celsius/fahrenheit, meters/feet
    """
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
        result = conversions[key](value)
        return f"{value} {from_unit} = {round(result, 4)} {to_unit}"
    return f"Conversion from {from_unit} to {to_unit} is not supported."


# ─── TEXT TOOLS ─────────────────────────────────────────────────────

@mcp.tool()
def word_count(text: str) -> str:
    """Count words, characters, and sentences in a block of text."""
    words = len(text.split())
    chars = len(text)
    chars_no_spaces = len(text.replace(" ", ""))
    sentences = text.count('.') + text.count('!') + text.count('?')
    return (
        f"Words: {words}\n"
        f"Characters (with spaces): {chars}\n"
        f"Characters (no spaces): {chars_no_spaces}\n"
        f"Sentences (approx): {sentences}"
    )


@mcp.tool()
def reverse_text(text: str) -> str:
    """Reverse a string of text."""
    return text[::-1]


@mcp.tool()
def generate_password(length: int = 16, include_symbols: bool = True) -> str:
    """
    Generate a random secure password.
    Args:
        length: Password length (default 16)
        include_symbols: Whether to include symbols like !@#$ (default True)
    """
    import string
    chars = string.ascii_letters + string.digits
    if include_symbols:
        chars += "!@#$%^&*"
    password = ''.join(random.choices(chars, k=length))
    return f"Generated password: {password}"


# ─── DATE & TIME TOOLS ──────────────────────────────────────────────

@mcp.tool()
def get_current_datetime() -> str:
    """Get the current date and time."""
    now = datetime.datetime.now()
    return now.strftime("Date: %A, %d %B %Y\nTime: %H:%M:%S")


@mcp.tool()
def days_until(target_date: str) -> str:
    """
    Calculate how many days until a future date.
    Date format: YYYY-MM-DD  e.g. "2025-12-25"
    """
    try:
        target = datetime.datetime.strptime(target_date, "%Y-%m-%d").date()
        today = datetime.date.today()
        delta = (target - today).days
        if delta > 0:
            return f"{delta} days until {target_date}"
        elif delta == 0:
            return "That's today!"
        else:
            return f"That date was {abs(delta)} days ago."
    except ValueError:
        return "Invalid date format. Please use YYYY-MM-DD."


# ─── FUN TOOLS ──────────────────────────────────────────────────────

@mcp.tool()
def roll_dice(sides: int = 6, count: int = 1) -> str:
    """
    Roll dice.
    Args:
        sides: Number of sides on the dice (default 6)
        count: Number of dice to roll (default 1)
    """
    rolls = [random.randint(1, sides) for _ in range(count)]
    total = sum(rolls)
    if count == 1:
        return f"🎲 Rolled a d{sides}: {rolls[0]}"
    return f"🎲 Rolled {count}d{sides}: {rolls} — Total: {total}"


@mcp.tool()
def flip_coin() -> str:
    """Flip a coin and return Heads or Tails."""
    result = random.choice(["Heads", "Tails"])
    return f"🪙 {result}!"


@mcp.tool()
def pick_random(options: str) -> str:
    """
    Pick a random item from a comma-separated list.
    Example: "pizza, sushi, tacos, burgers"
    """
    items = [item.strip() for item in options.split(",") if item.strip()]
    if not items:
        return "No options provided."
    chosen = random.choice(items)
    return f"🎯 Picked: {chosen}"


if __name__ == "__main__":
    mcp.run(transport="streamable-http")
