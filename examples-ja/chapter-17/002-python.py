from mcp.server import MCPServer

mcp = MCPServer("Happy Book Readonly Lab")

@mcp.tool()
def list_records() -> list[dict[str, str]]:
    """架空のワークショップ記録を2件返す。外部データにはアクセスしない。"""
    return [
        {"id": "R01", "title": "備品の整理", "owner": "小河", "status": "open"},
        {"id": "R02", "title": "プロジェクターの確認", "owner": "小杉", "status": "done"},
    ]

if __name__ == "__main__":
    mcp.run(transport="stdio")
