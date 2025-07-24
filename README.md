# Pokemon Battle MCP Server

A Model Context Protocol (MCP) server that simulates Pokemon battles using type effectiveness and stats. This server provides tools for battling Pokemon, listing available Pokemon, checking type effectiveness, and getting detailed Pokemon information.

## Features

- **Pokemon Battles**: Simulate battles between any two Pokemon with type effectiveness calculations
- **Type Effectiveness**: Complete type chart with super effective, normal, not very effective, and no effect relationships
- **Pokemon Database**: 10 popular Pokemon with realistic stats
- **Battle Analysis**: Detailed battle results including damage calculations and winner determination

## Available Tools

- `battle_pokemon(pokemon1_name, pokemon2_name)` - Battle two Pokemon and determine the winner
- `list_pokemon()` - List all available Pokemon with their stats
- `get_type_chart()` - Get the complete type effectiveness chart
- `pokemon_info(pokemon_name)` - Get detailed information about a specific Pokemon

## Setup Instructions

### 1. Create Virtual Environment

```bash
# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate
```

### 2. Install Dependencies

```bash
# Install dependencies from requirements.txt
pip install -r requirements.txt
```

### 3. Run the MCP Server

```bash
# Run the Pokemon Battle MCP server
python pokemon_battle_mcp.py
```

## Adding to Claude Code MCP Client

### Method 1: Using MCP Configuration File

1. Create or edit your MCP configuration file (usually `~/.config/mcp/config.json` or similar)
2. Add the following configuration:

(replace with your own path)

```json
{
  "mcpServers": {
    "pokemon-battle": {
      "type": "stdio",
      "command": "/Volumes/extraSpace/code/mcp-pokemon/venv/bin/python",
      "args": ["/Volumes/extraSpace/code/mcp-pokemon/pokemon_battle_mcp.py"],
      "env": {}
    }
  }
}
```

### Method 2: Using Claude Desktop

1. Open Claude Desktop
2. Go to Settings → MCP Servers
3. Click "Add Server"
4. Configure the server:
   - **Name**: Pokemon Battle
   - **Command**: `python`
   - **Arguments**: `["/path/to/your/mcp-pokemon/pokemon_battle_mcp.py"]`
   - **Working Directory**: `/path/to/your/mcp-pokemon`

### Method 3: Using Claude Web

1. Go to Claude Web interface
2. Open the MCP panel
3. Add a new server configuration with the same settings as above

## Usage Examples

Once connected, you can use the Pokemon Battle MCP server with commands like:

- "Battle Pikachu against Charizard"
- "List all available Pokemon"
- "Show me the type effectiveness chart"
- "Get information about Gengar"

## Available Pokemon

The server includes 10 Pokemon with realistic stats:

- Pikachu (Electric)
- Charizard (Fire)
- Blastoise (Water)
- Venusaur (Grass)
- Alakazam (Psychic)
- Machamp (Fighting)
- Gengar (Ghost)
- Golem (Rock)
- Lapras (Water)
- Dragonite (Dragon)

## Type Effectiveness

The server includes a complete type effectiveness chart with all 18 Pokemon types:

- Normal, Fire, Water, Electric, Grass, Ice, Fighting, Poison, Ground, Flying
- Psychic, Bug, Rock, Ghost, Dragon, Dark, Steel, Fairy

## Requirements

- Python 3.7+
- FastMCP library
- Virtual environment (recommended)

## License

This project is open source and available under the MIT License.
