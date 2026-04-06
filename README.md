# 🔧 My MCP Server

A remote MCP server built with Python and FastMCP, deployable to Render.

## Tools Included

| Tool | What it does |
|---|---|
| `calculate` | Evaluate math expressions |
| `convert_units` | Convert km↔miles, kg↔lbs, etc. |
| `word_count` | Count words, chars, sentences |
| `reverse_text` | Reverse any string |
| `generate_password` | Generate a secure password |
| `get_current_datetime` | Get today's date and time |
| `days_until` | Days until a future date |
| `roll_dice` | Roll any dice (d6, d20, etc.) |
| `flip_coin` | Heads or tails |
| `pick_random` | Pick from a list of options |

---

## 🚀 Deploy to Render

### Step 1 — Push to GitHub
```bash
git init
git add .
git commit -m "Initial MCP server"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
git push -u origin main
```

### Step 2 — Deploy on Render
1. Go to [render.com](https://render.com) → **New → Web Service**
2. Connect your GitHub repo
3. Render auto-detects `render.yaml` — just click **Deploy**
4. Wait ~2 minutes for the build to finish
5. Your URL will be: `https://my-mcp-server.onrender.com`

### Step 3 — Connect to Claude Desktop App
1. Open Claude Desktop App → Settings → Connectors
2. Click **Add custom connector**
3. Name: `My MCP Server`
4. URL: `https://my-mcp-server.onrender.com/mcp`
5. Click **Add** ✅

---

## 🧪 Run Locally (Optional)

```bash
pip install -r requirements.txt
python -m mcp run server.py --transport streamable-http
```

Server runs at `http://localhost:8000/mcp`

---

## ➕ Adding Your Own Tools

In `server.py`, add a new function with the `@mcp.tool()` decorator:

```python
@mcp.tool()
def say_hello(name: str) -> str:
    """Say hello to someone."""
    return f"Hello, {name}! 👋"
```

That's it — Claude can now use this tool in chat!
