import os
from pathlib import Path

import typer
import uvicorn
import yaml
from src.settings import settings

app = typer.Typer()


def _init_debugger() -> None:
    """Initialize debugpy if DEBUG environment variable is set."""
    if os.getenv("DEBUG", "false").lower() == "true":
        try:
            import debugpy

            debugpy.listen(("0.0.0.0", 5678))
            print("⏸️  Debugger listening on 0.0.0.0:5678")
            print("   Connect your IDE debugger to proceed...")
            # Uncomment the line below if you want to wait for debugger
            # before starting the application
            # debugpy.wait_for_client()
        except ImportError:
            print("⚠️  DEBUG=true but debugpy not installed. Run: uv pip install debugpy")


@app.command()
def http_server() -> None:
    """Start the HTTP server."""
    print("Starting HTTP server...")
    uvicorn.run(
        "src.http_server:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.RELOAD,
        log_level=settings.LOG_LEVEL,
    )


@app.command()
def export_openapi() -> None:
    """Export OpenAPI schema to YAML file."""
    from src.http_server import app as fastapi_app

    schema = fastapi_app.openapi()
    output = Path("contracts/api/openapi.yml")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(yaml.dump(schema, sort_keys=False, allow_unicode=True))
    print(f"OpenAPI spec exported to {output}")


@app.command()
def mcp_server() -> None:
    """Start the MCP server."""
    print("Starting MCP server...")


if __name__ == "__main__":
    _init_debugger()
    app()
