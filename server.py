import os
import math
import random
import datetime
from mcp.server.fastmcp import FastMCP
from mcp.server.transport_security import TransportSecuritySettings
from starlette.types import ASGIApp, Receive, Scope, Send
from starlette.requests import Request
from starlette.responses import PlainTextResponse
from starlette.routing import Route
from starlette.applications import Starlette

# Debug app to show what headers are coming in
async def debug(request: Request):
    headers = dict(request.headers)
    return PlainTextResponse(f"Headers received:\n" + "\n".join(f"{k}: {v}" for k, v in headers.items()))

class TrustAllHostsMiddleware:
    def __init__(self, app: ASGIApp):
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send):
        if scope["type"] in ("http", "websocket"):
            scope["headers"] = [
                (b"host", b"localhost") if k == b"host" else (k, v)
                for k, v in scope["headers"]
            ]
        await self.app(scope, receive, send)

mcp = FastMCP(
    "My MCP Server",
    transport_security=TransportSecuritySettings(
        enable_dns_rebinding_protection=True,
        allowed_hosts=["localhost"],
        allowed_origins=[]
    )
)

@mcp.tool()
def flip_coin() -> str:
    """Flip a coin."""
    return f"🪙 {random.choice(['Heads', 'Tails'])}!"

if __name__ == "__main__":
    import uvicorn
    mcp_app = mcp.streamable_http_app()
    
    # Add debug route
    debug_app = Starlette(routes=[Route("/debug", debug)])
    
    # Combined app
    class CombinedApp:
        def __init__(self):
            self.mcp = TrustAllHostsMiddleware(mcp_app)
            self.debug = debug_app
        
        async def __call__(self, scope, receive, send):
            if scope.get("path", "").startswith("/debug"):
                await self.debug(scope, receive, send)
            else:
                await self.mcp(scope, receive, send)
    
    uvicorn.run(
        CombinedApp(),
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 8000)),
        forwarded_allow_ips="*",
        proxy_headers=True
    )
