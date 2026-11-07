from mcp.server import MCPServer

mcp = MCPServer("Happy Book Readonly Lab")

@mcp.tool()
def list_records() -> list[dict[str, str]]:
    """Return two fictional workshop records; no remote data is accessed."""
    return [
        {"id": "R01", "title": "整理器材", "owner": "小河", "status": "open"},
        {"id": "R02", "title": "確認投影", "owner": "小杉", "status": "done"},
    ]

if __name__ == "__main__":
    mcp.run(transport="stdio")