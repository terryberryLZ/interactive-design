#!/usr/bin/env python3
"""
Test script to validate the fantasy_avatar_generator.py (Pygame version) code structure
This validates Python syntax, pygame integration, and basic structure
"""

import ast
import sys
import os

def test_pygame_version():
    """Test the structure of the Pygame version"""
    print("Testing fantasy_avatar_generator.py (Pygame version) structure...")
    
    # Read the file
    with open('fantasy_avatar_generator.py', 'r', encoding='utf-8') as f:
        code = f.read()
    
    # Test 1: Parse the code as valid Python
    try:
        tree = ast.parse(code)
        print("✓ Code is valid Python syntax")
    except SyntaxError as e:
        print(f"✗ Syntax error: {e}")
        return False
    
    # Test 2: Check for required imports
    required_imports = ['pygame', 'random', 'sys']
    found_imports = set()
    
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                found_imports.add(alias.name)
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                found_imports.add(node.module)
    
    for imp in required_imports:
        if imp in found_imports:
            print(f"✓ Import '{imp}' found")
        else:
            print(f"✗ Import '{imp}' is missing")
            return False
    
    # Test 3: Check for required global variables
    required_globals = [
        'GENDERS', 'RACES', 'SKIN_COLORS', 'EXPRESSIONS',
        'HEADWEAR', 'NECKLACES', 'EARRINGS', 'CLOTHES', 'PIXEL',
        'WINDOW_WIDTH', 'WINDOW_HEIGHT', 'BACKGROUND_COLOR'
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
    
    # Test 4: Check for required functions
    required_functions = [
        'setup', 'generate_avatar', 'draw_avatar', 'main',
        'draw_head', 'draw_expression', 'draw_headwear', 'draw_necklace',
        'draw_earrings', 'draw_clothes'
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
    
    # Test 5: Check that Processing-specific imports are NOT used
    has_processing_import = False
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                if 'processing' in alias.name.lower():
                    has_processing_import = True
        elif isinstance(node, ast.ImportFrom):
            if node.module and 'processing' in node.module.lower():
                has_processing_import = True
    
    if has_processing_import:
        print("✗ Code still contains Processing imports")
        return False
    else:
        print("✓ No Processing imports found")
    
    # Test 6: Check for Pygame-specific patterns
    pygame_patterns = [
        'pygame.init',
        'pygame.display',
        'pygame.draw.rect',
        'pygame.MOUSEBUTTONDOWN',
        'pygame.quit'
    ]
    
    for pattern in pygame_patterns:
        if pattern in code:
            print(f"✓ Pygame pattern '{pattern}' found")
        else:
            print(f"✗ Pygame pattern '{pattern}' is missing")
            return False
    
    # Test 7: Check list contents by analyzing AST
    print("\nChecking list contents:")
    
    list_checks = {
        'GENDERS': 2,
        'RACES': 4,
        'SKIN_COLORS': 6,
        'EXPRESSIONS': 4,
        'HEADWEAR': 5,
        'NECKLACES': 4,
        'EARRINGS': 4,
        'CLOTHES': 4
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
            print(f"⚠ {list_name} structure could not be verified")
    
    # Test 8: Calculate total combinations
    if len(list_lengths) == len(list_checks):
        total_combinations = 1
        for count in list_lengths.values():
            total_combinations *= count
        print(f"\n✓ Total possible avatar combinations: {total_combinations:,}")
    
    # Test 9: Verify the file can be imported without errors
    print("\nTesting import...")
    try:
        # Set environment for headless testing
        os.environ['SDL_VIDEODRIVER'] = 'dummy'
        import fantasy_avatar_generator
        print("✓ Module can be imported successfully")
    except Exception as e:
        print(f"✗ Import error: {e}")
        return False
    
    print("\n" + "="*50)
    print("All tests passed! ✓")
    print("="*50)
    print("\nThe Pygame version is ready to use!")
    print("Run it with: python3 fantasy_avatar_generator.py")
    return True

if __name__ == '__main__':
    success = test_pygame_version()
    sys.exit(0 if success else 1)
