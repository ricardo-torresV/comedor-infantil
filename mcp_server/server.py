import sys
import json
from mcp.server import Server, NotificationOptions
from mcp.server.models import InitializationOptions
from mcp.types import (
    Tool,
    TextContent,
    LoggingLevel,
)
from mcp.server.stdio import stdio_server
from pydantic import BaseModel, Field

from mcp_server.database import db


server = Server("comedor-db")


class QueryArgs(BaseModel):
    query: str = Field(description="SQL query to execute (SELECT only)")


class InsertArgs(BaseModel):
    table: str = Field(description="Table name")
    data: str = Field(description="JSON string with column:value pairs to insert")


@server.list_tools()
async def handle_list_tools() -> list[Tool]:
    return [
        Tool(
            name="list_tables",
            description="List all tables in the database",
            inputSchema={
                "type": "object",
                "properties": {},
            },
        ),
        Tool(
            name="describe_table",
            description="Get schema information for a specific table",
            inputSchema={
                "type": "object",
                "properties": {
                    "table_name": {
                        "type": "string",
                        "description": "Name of the table",
                    }
                },
                "required": ["table_name"],
            },
        ),
        Tool(
            name="query",
            description="Execute a SELECT query on the database",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "SQL SELECT query",
                    }
                },
                "required": ["query"],
            },
        ),
        Tool(
            name="insert",
            description="Insert a row into a table",
            inputSchema={
                "type": "object",
                "properties": {
                    "table": {
                        "type": "string",
                        "description": "Table name",
                    },
                    "data": {
                        "type": "string",
                        "description": "JSON with column:value pairs",
                    },
                },
                "required": ["table", "data"],
            },
        ),
    ]


@server.call_tool()
async def handle_call_tool(name: str, arguments: dict | None) -> list[TextContent]:
    if not arguments:
        arguments = {}

    if name == "list_tables":
        tables = await db.get_tables()
        return [
            TextContent(
                type="text",
                text=json.dumps(tables, indent=2, default=str),
            )
        ]

    elif name == "describe_table":
        table_name = arguments.get("table_name", "")
        schema = await db.get_table_schema(table_name)
        return [
            TextContent(
                type="text",
                text=json.dumps(schema, indent=2, default=str),
            )
        ]

    elif name == "query":
        query = arguments.get("query", "")
        result = await db.execute_query(query)
        return [
            TextContent(
                type="text",
                text=json.dumps(result, indent=2, default=str),
            )
        ]

    elif name == "insert":
        table = arguments.get("table", "")
        data = json.loads(arguments.get("data", "{}"))
        columns = ", ".join(data.keys())
        placeholders = ", ".join(f"${i+1}" for i in range(len(data)))
        values = list(data.values())
        query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders}) RETURNING *"
        result = await db.execute_insert(query, *values)
        return [
            TextContent(
                type="text",
                text=json.dumps({"result": result}, indent=2, default=str),
            )
        ]

    raise ValueError(f"Unknown tool: {name}")


@server.list_prompts()
async def handle_list_prompts():
    return []


@server.list_resources()
async def handle_list_resources():
    return []


async def main():
    await db.connect()

    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="comedor-db",
                server_version="0.1.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
