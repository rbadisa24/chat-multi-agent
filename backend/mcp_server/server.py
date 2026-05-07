from mcp.server.fastmcp import FastMCP

mcp = FastMCP("utility-tools")

@mcp.tool()
def reverse_string(text: str) -> str:
    """Reverse the characters in a string"""
    return text[::-1]

@mcp.tool()
def word_count(text: str) -> int:
    """Count the number of words in a string"""
    return len(text.split())


if __name__ == "__main__":
    mcp.run(transport="stdio")