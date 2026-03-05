from pathlib import Path

import typer
import uvicorn
import yaml
from src.settings import settings

app = typer.Typer()


@app.command()
def http_server():
    print("Starting HTTP server...")
    uvicorn.run(
        "src.http_server:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.RELOAD,
        log_level=settings.LOG_LEVEL,
    )


@app.command()
def export_openapi():
    from src.http_server import app as fastapi_app

    schema = fastapi_app.openapi()
    output = Path("contracts/api/openapi.yml")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(yaml.dump(schema, sort_keys=False, allow_unicode=True))
    print(f"OpenAPI spec exported to {output}")


@app.command()
def mcp_server():
    print("Starting MCP server...")


if __name__ == "__main__":
    app()
