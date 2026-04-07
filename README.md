# 🔧 My MCP Server

A remote MCP (Model Context Protocol) server built with Python and FastMCP, deployed on Render and connected to Claude Desktop App.

> **MCP** is an open standard by Anthropic that lets AI assistants like Claude call external tools and services in real time.

---

## 🛠️ Tools Available

| Tool | What it does |
|---|---|
| `calculate` | Evaluate math expressions e.g. `sqrt(144)`, `2 ** 16` |
| `convert_units` | Convert km↔miles, kg↔lbs, celsius↔fahrenheit, meters↔feet |
| `word_count` | Count words, characters and sentences in text |
| `reverse_text` | Reverse any string |
| `generate_password` | Generate a secure random password |
| `get_current_datetime` | Get today's date and time |
| `days_until` | Count days until a future date |
| `roll_dice` | Roll any dice (d6, d20, etc.) |
| `flip_coin` | Heads or tails |
| `pick_random` | Pick randomly from a comma-separated list |

---

## 🚀 Deploy Your Own

### Step 1 — Clone & push to GitHub
```bash
git clone https://github.com/MungManBaoIsan/mcp-server.git
cd mcp-server
git remote set-url origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git push -u origin main
```

### Step 2 — Deploy on Render
1. Go to [render.com](https://render.com) → **New → Web Service**
2. Connect your GitHub repo
3. **Build Command:** `pip install -r requirements.txt`
4. **Start Command:** `python server.py`
5. Click **Deploy** and wait ~2 minutes

### Step 3 — Connect to Claude Desktop App
1. Open Claude Desktop App → Settings → Connectors
2. Click **Add custom connector**
3. **Name:** `My MCP Server`
4. **URL:** `https://your-service-name.onrender.com/mcp`
5. Click **Add** ✅

---

## ➕ Adding Your Own Tools

In `server.py`, add a new function with the `@mcp.tool()` decorator:

```python
@mcp.tool()
def say_hello(name: str) -> str:
    """Say hello to someone."""
    return f"Hello, {name}! 👋"
```

Push to GitHub and Render redeploys automatically!

---

## 🗺️ My Journey

This project was my first time building and deploying a remote MCP server. Here's an honest account of how it went — including the hard parts.

### What I set out to do
I wanted to connect a real Python server to Claude Desktop App so Claude could call my own custom tools in chat. MCP (Model Context Protocol) is brand new, so there weren't many tutorials to follow.

### The tech stack I used
- **Python** with the `FastMCP` library to write the server
- **Git & GitHub** to version control and store the code
- **Render** (free tier) to host the server in the cloud
- **Claude Desktop App** to connect and test the tools

### The journey
Getting the server running locally was straightforward. Deploying to Render was also smooth. The real challenge was a persistent **"Invalid Host header"** error — Render's proxy was sending a host header that the MCP library's security check was rejecting with a 421 error.

After a lot of debugging, the fix involved:
- Pinning the MCP library version to `1.24.0` to match my local environment
- Adding a `/debug` endpoint to inspect the exact headers Render was sending
- Setting `allowed_hosts` to the exact Render domain
- Wrapping the app in a custom `TrustAllHostsMiddleware` class

Once that was sorted, I added the connector URL in Claude Desktop App and typed *"flip a coin"* in chat. Claude responded with `🪙 Heads!` — calling my Python server live. That was a great moment.

### What I learned
- Always `cd` into your project folder before running git commands
- Cloud deployments behave differently to local — a debug endpoint is your best friend
- Pinning library versions prevents surprises between environments
- MCP is very new — problem-solving matters more than following tutorials
- Persistence is the most important skill in development

### What's next
- Add more tools (weather, notes, news)
- Add this to my portfolio with a writeup
- Explore MCP connectors for Gmail and Google Calendar

---

## 📋 Requirements

```
mcp[cli]==1.24.0
```

---

*Built by [MungManBaoIsan](https://github.com/MungManBaoIsan) — April 2026*