#!/usr/bin/env python3
"""
Test script to validate the fantasy_avatar_generator.pyde code structure
This validates Python syntax and basic structure, but cannot test Processing-specific functions
"""

import ast
import sys

def test_pyde_structure():
    """Test the structure of the .pyde file"""
    print("Testing fantasy_avatar_generator.pyde structure...")
    
    # Read the file
    with open('fantasy_avatar_generator.pyde', 'r', encoding='utf-8') as f:
        code = f.read()
    
    # Test 1: Parse the code as valid Python
    try:
        tree = ast.parse(code)
        print("✓ Code is valid Python syntax")
    except SyntaxError as e:
        print(f"✗ Syntax error: {e}")
        return False
    
    # Test 2: Check for required global variables
    required_globals = [
        'GENDERS', 'RACES', 'SKIN_COLORS', 'EXPRESSIONS',
        'HEADWEAR', 'NECKLACES', 'EARRINGS', 'CLOTHES', 'BACKGROUNDS', 'PIXEL'
    ]
    
    defined_globals = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name):
                    defined_globals.add(target.id)
    
    for var in required_globals:
        if var in defined_globals:
            print(f"✓ Global variable '{var}' is defined")
        else:
            print(f"✗ Global variable '{var}' is missing")
            return False
    
    # Test 3: Check for required functions
    required_functions = [
        'setup', 'draw', 'mousePressed', 'keyPressed', 'generateAvatar', 'random_choice',
        'drawBackground', 'drawHead', 'drawExpression', 'drawHeadwear', 'drawNecklace',
        'drawEarrings', 'drawClothes'
    ]
    
    defined_functions = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            defined_functions.add(node.name)
    
    for func in required_functions:
        if func in defined_functions:
            print(f"✓ Function '{func}' is defined")
        else:
            print(f"✗ Function '{func}' is missing")
            return False
    
    # Test 4: Check list contents by analyzing AST
    print("\nChecking list contents:")
    
    list_checks = {
        'GENDERS': 2,
        'RACES': 5,  # Added human
        'SKIN_COLORS': 8,  # Added more human skin tones
        'EXPRESSIONS': 4,  # Changed to handsome, serious, cute, goofy
        'HEADWEAR': 6,  # Added headband
        'NECKLACES': 5,  # Added rune_pendant
        'EARRINGS': 5,  # Added stud
        'CLOTHES': 5,  # Added hoodie
        'BACKGROUNDS': 7  # New category
    }
    
    list_lengths = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id in list_checks:
                    if isinstance(node.value, ast.List):
                        list_lengths[target.id] = len(node.value.elts)
    
    for list_name, expected_count in list_checks.items():
        if list_name in list_lengths:
            actual_count = list_lengths[list_name]
            if actual_count >= expected_count:
                print(f"✓ {list_name} has {actual_count} items (expected at least {expected_count})")
            else:
                print(f"✗ {list_name} has only {actual_count} items (expected at least {expected_count})")
                return False
        else:
            print(f"⚠ {list_name} structure could not be verified (may use complex initialization)")
    
    # Test 5: Calculate total combinations (if we can)
    if len(list_lengths) == len(list_checks):
        total_combinations = 1
        for count in list_lengths.values():
            total_combinations *= count
        print(f"\n✓ Total possible avatar combinations: {total_combinations:,}")
    else:
        print(f"\n⚠ Could not calculate total combinations (some lists use complex initialization)")
    
    print("\n" + "="*50)
    print("All tests passed! ✓")
    print("="*50)
    print("\nNote: This script validates code structure only.")
    print("To actually run the avatar generator, use Processing with Python Mode.")
    return True

if __name__ == '__main__':
    success = test_pyde_structure()
    sys.exit(0 if success else 1)
