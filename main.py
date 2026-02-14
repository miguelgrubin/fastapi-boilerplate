import typer
import uvicorn
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
def mcp_server():
    print("Starting MCP server...")


if __name__ == "__main__":
    app()
