#!/usr/bin/env python3
"""
Pokemon Battle MCP Server using FastMCP
A simple server that determines battle winners based on type effectiveness
"""

from fastmcp import FastMCP
from typing import Dict, List, Optional
import json

# Initialize FastMCP server
mcp = FastMCP("Pokemon Battle Server")

# Pokemon type effectiveness chart (simplified)
TYPE_EFFECTIVENESS = {
    "water": {"fire": 2.0, "ground": 2.0, "rock": 2.0, "grass": 0.5, "electric": 0.5},
    "fire": {"grass": 2.0, "ice": 2.0, "bug": 2.0, "steel": 2.0, "water": 0.5, "rock": 0.5, "ground": 0.5},
    "grass": {"water": 2.0, "ground": 2.0, "rock": 2.0, "fire": 0.5, "ice": 0.5, "bug": 0.5, "flying": 0.5},
    "electric": {"water": 2.0, "flying": 2.0, "grass": 0.5, "ground": 0.0},
    "ice": {"grass": 2.0, "ground": 2.0, "flying": 2.0, "dragon": 2.0, "fire": 0.5, "water": 0.5, "ice": 0.5, "steel": 0.5},
    "fighting": {"normal": 2.0, "ice": 2.0, "rock": 2.0, "dark": 2.0, "steel": 2.0, "flying": 0.5, "poison": 0.5, "bug": 0.5, "psychic": 0.5, "fairy": 0.5, "ghost": 0.0},
    "poison": {"grass": 2.0, "fairy": 2.0, "poison": 0.5, "ground": 0.5, "rock": 0.5, "ghost": 0.5, "steel": 0.0},
    "ground": {"fire": 2.0, "electric": 2.0, "poison": 2.0, "rock": 2.0, "steel": 2.0, "grass": 0.5, "bug": 0.5, "flying": 0.0},
    "flying": {"grass": 2.0, "fighting": 2.0, "bug": 2.0, "electric": 0.5, "rock": 0.5, "steel": 0.5},
    "psychic": {"fighting": 2.0, "poison": 2.0, "psychic": 0.5, "steel": 0.5, "dark": 0.0},
    "bug": {"grass": 2.0, "psychic": 2.0, "dark": 2.0, "fire": 0.5, "fighting": 0.5, "poison": 0.5, "flying": 0.5, "ghost": 0.5, "steel": 0.5, "fairy": 0.5},
    "rock": {"fire": 2.0, "ice": 2.0, "flying": 2.0, "bug": 2.0, "water": 0.5, "grass": 0.5, "fighting": 0.5, "poison": 0.5, "ground": 0.5, "steel": 0.5},
    "ghost": {"psychic": 2.0, "ghost": 2.0, "dark": 0.5, "normal": 0.0},
    "dragon": {"dragon": 2.0, "steel": 0.5, "fairy": 0.0},
    "dark": {"psychic": 2.0, "ghost": 2.0, "fighting": 0.5, "dark": 0.5, "fairy": 0.5},
    "steel": {"ice": 2.0, "rock": 2.0, "fairy": 2.0, "fire": 0.5, "water": 0.5, "electric": 0.5, "steel": 0.5},
    "fairy": {"fighting": 2.0, "dragon": 2.0, "dark": 2.0, "fire": 0.5, "poison": 0.5, "steel": 0.5},
    "normal": {"rock": 0.5, "ghost": 0.0, "steel": 0.5}
}

# Sample Pokemon database
POKEMON_DB = {
    "pikachu": {"type": "electric", "hp": 100, "attack": 80},
    "charizard": {"type": "fire", "hp": 120, "attack": 100},
    "blastoise": {"type": "water", "hp": 130, "attack": 90},
    "venusaur": {"type": "grass", "hp": 125, "attack": 85},
    "alakazam": {"type": "psychic", "hp": 90, "attack": 110},
    "machamp": {"type": "fighting", "hp": 140, "attack": 120},
    "gengar": {"type": "ghost", "hp": 100, "attack": 95},
    "golem": {"type": "rock", "hp": 135, "attack": 105},
    "lapras": {"type": "water", "hp": 160, "attack": 75},
    "dragonite": {"type": "dragon", "hp": 145, "attack": 115}
}

def get_type_effectiveness(attacker_type: str, defender_type: str) -> float:
    """Get type effectiveness multiplier"""
    if attacker_type in TYPE_EFFECTIVENESS:
        return TYPE_EFFECTIVENESS[attacker_type].get(defender_type, 1.0)
    return 1.0

def calculate_damage(attacker: Dict, defender: Dict) -> int:
    """Calculate damage dealt by attacker to defender"""
    base_damage = attacker["attack"]
    type_multiplier = get_type_effectiveness(attacker["type"], defender["type"])
    return int(base_damage * type_multiplier)

@mcp.tool()
def battle_pokemon(pokemon1_name: str, pokemon2_name: str) -> Dict:
    """
    Battle two Pokemon and determine the winner based on type effectiveness and stats.
    
    Args:
        pokemon1_name: Name of the first Pokemon (lowercase)
        pokemon2_name: Name of the second Pokemon (lowercase)
    
    Returns:
        Dictionary containing battle results and winner information
    """
    # Normalize names
    pokemon1_name = pokemon1_name.lower().strip()
    pokemon2_name = pokemon2_name.lower().strip()
    
    # Check if Pokemon exist in database
    if pokemon1_name not in POKEMON_DB:
        return {"error": f"Pokemon '{pokemon1_name}' not found in database"}
    
    if pokemon2_name not in POKEMON_DB:
        return {"error": f"Pokemon '{pokemon2_name}' not found in database"}
    
    # Get Pokemon data
    pokemon1 = POKEMON_DB[pokemon1_name].copy()
    pokemon2 = POKEMON_DB[pokemon2_name].copy()
    
    # Add names for reference
    pokemon1["name"] = pokemon1_name.capitalize()
    pokemon2["name"] = pokemon2_name.capitalize()
    
    # Calculate damage each Pokemon would deal
    damage1_to_2 = calculate_damage(pokemon1, pokemon2)
    damage2_to_1 = calculate_damage(pokemon2, pokemon1)
    
    # Get type effectiveness descriptions
    effectiveness1 = get_type_effectiveness(pokemon1["type"], pokemon2["type"])
    effectiveness2 = get_type_effectiveness(pokemon2["type"], pokemon1["type"])
    
    def get_effectiveness_description(multiplier: float) -> str:
        if multiplier == 0.0:
            return "No effect"
        elif multiplier == 0.5:
            return "Not very effective"
        elif multiplier == 1.0:
            return "Normal effectiveness"
        elif multiplier == 2.0:
            return "Super effective"
        else:
            return f"{multiplier}x effectiveness"
    
    # Determine winner based on damage potential and HP
    # Simple calculation: turns to defeat = defender_hp / damage_per_turn
    turns_to_defeat_pokemon2 = max(1, pokemon2["hp"] // max(1, damage1_to_2))
    turns_to_defeat_pokemon1 = max(1, pokemon1["hp"] // max(1, damage2_to_1))
    
    if turns_to_defeat_pokemon2 < turns_to_defeat_pokemon1:
        winner = pokemon1["name"]
        winner_advantage = "faster defeat"
    elif turns_to_defeat_pokemon1 < turns_to_defeat_pokemon2:
        winner = pokemon2["name"]
        winner_advantage = "faster defeat"
    else:
        # If equal turns, higher damage wins
        if damage1_to_2 > damage2_to_1:
            winner = pokemon1["name"]
            winner_advantage = "higher damage output"
        elif damage2_to_1 > damage1_to_2:
            winner = pokemon2["name"]
            winner_advantage = "higher damage output"
        else:
            # If damage is equal, higher HP wins
            if pokemon1["hp"] > pokemon2["hp"]:
                winner = pokemon1["name"]
                winner_advantage = "higher HP"
            elif pokemon2["hp"] > pokemon1["hp"]:
                winner = pokemon2["name"]
                winner_advantage = "higher HP"
            else:
                winner = "Tie"
                winner_advantage = "equal stats"
    
    return {
        "battle_result": {
            "winner": winner,
            "winner_advantage": winner_advantage,
            "pokemon1": {
                "name": pokemon1["name"],
                "type": pokemon1["type"],
                "hp": pokemon1["hp"],
                "attack": pokemon1["attack"],
                "damage_to_opponent": damage1_to_2,
                "type_effectiveness": get_effectiveness_description(effectiveness1),
                "turns_to_win": turns_to_defeat_pokemon2
            },
            "pokemon2": {
                "name": pokemon2["name"],
                "type": pokemon2["type"],
                "hp": pokemon2["hp"],
                "attack": pokemon2["attack"],
                "damage_to_opponent": damage2_to_1,
                "type_effectiveness": get_effectiveness_description(effectiveness2),
                "turns_to_win": turns_to_defeat_pokemon1
            }
        }
    }

@mcp.tool()
def list_pokemon() -> Dict:
    """
    List all available Pokemon in the database with their stats.
    
    Returns:
        Dictionary containing all Pokemon and their information
    """
    return {
        "available_pokemon": {
            name.capitalize(): {
                "type": stats["type"],
                "hp": stats["hp"], 
                "attack": stats["attack"]
            }
            for name, stats in POKEMON_DB.items()
        }
    }

@mcp.tool()
def get_type_chart() -> Dict:
    """
    Get the type effectiveness chart showing which types are effective against others.
    
    Returns:
        Dictionary containing type effectiveness information
    """
    return {
        "type_effectiveness_chart": TYPE_EFFECTIVENESS,
        "legend": {
            "2.0": "Super effective (2x damage)",
            "1.0": "Normal effectiveness (1x damage)", 
            "0.5": "Not very effective (0.5x damage)",
            "0.0": "No effect (0x damage)"
        }
    }

@mcp.tool()
def pokemon_info(pokemon_name: str) -> Dict:
    """
    Get detailed information about a specific Pokemon.
    
    Args:
        pokemon_name: Name of the Pokemon to look up
        
    Returns:
        Dictionary containing Pokemon information and type matchups
    """
    pokemon_name = pokemon_name.lower().strip()
    
    if pokemon_name not in POKEMON_DB:
        return {"error": f"Pokemon '{pokemon_name}' not found in database"}
    
    pokemon = POKEMON_DB[pokemon_name]
    pokemon_type = pokemon["type"]
    
    # Find what this Pokemon is strong/weak against
    strong_against = []
    weak_against = []
    immune_to = []
    immune_against = []
    
    # What this Pokemon's attacks are effective against
    if pokemon_type in TYPE_EFFECTIVENESS:
        for target_type, effectiveness in TYPE_EFFECTIVENESS[pokemon_type].items():
            if effectiveness == 2.0:
                strong_against.append(target_type)
            elif effectiveness == 0.0:
                immune_against.append(target_type)
    
    # What is effective against this Pokemon
    for attacker_type, matchups in TYPE_EFFECTIVENESS.items():
        if pokemon_type in matchups:
            effectiveness = matchups[pokemon_type]
            if effectiveness == 2.0:
                weak_against.append(attacker_type)
            elif effectiveness == 0.0:
                immune_to.append(attacker_type)
    
    return {
        "pokemon": {
            "name": pokemon_name.capitalize(),
            "type": pokemon_type,
            "hp": pokemon["hp"],
            "attack": pokemon["attack"],
            "matchups": {
                "strong_against": strong_against,
                "weak_against": weak_against,
                "immune_to": immune_to,
                "immune_against": immune_against
            }
        }
    }

if __name__ == "__main__":
    mcp.run()