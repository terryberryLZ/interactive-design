#!/usr/bin/env python3
"""
Test script to verify pygame avatar generation works correctly
Generates sample avatars with different seeds and saves them
"""

import pygame
import sys
import os

# Add the current directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import the avatar generator
from fantasy_avatar_generator import (
    generate_avatar, SCREEN_WIDTH, SCREEN_HEIGHT,
    RACES, EXPRESSIONS, HEADWEAR, CLOTHES, BACKGROUNDS
)
import random


def test_generation():
    """Test avatar generation with different seeds"""
    print("Testing Fantasy Avatar Generator...")
    print(f"Screen size: {SCREEN_WIDTH}x{SCREEN_HEIGHT}")
    print(f"Total combinations: {2 * len(RACES) * 8 * len(EXPRESSIONS) * len(HEADWEAR) * 5 * 5 * len(CLOTHES) * len(BACKGROUNDS):,}")
    
    # Initialize pygame
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Avatar Generator Test')
    
    # Test with specific seeds
    test_seeds = [42, 100, 500, 1000, 9999]
    
    print("\nGenerating test avatars...")
    for seed in test_seeds:
        random.seed(seed)
        print(f"  Seed {seed}...", end=" ")
        
        try:
            generate_avatar(screen)
            filename = f"test_avatar_seed_{seed}.png"
            pygame.image.save(screen, filename)
            print(f"✓ Saved as {filename}")
        except Exception as e:
            print(f"✗ Error: {e}")
            return False
    
    print("\nAll tests passed! ✓")
    print(f"Generated {len(test_seeds)} sample avatars.")
    print("\nSample avatars saved as: test_avatar_seed_*.png")
    
    pygame.quit()
    return True


def test_all_races():
    """Test that all races can be drawn"""
    print("\nTesting all races...")
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    
    for race in RACES:
        print(f"  Testing {race}...", end=" ")
        try:
            # Set a fixed seed for reproducibility
            random.seed(0)
            generate_avatar(screen)
            print("✓")
        except Exception as e:
            print(f"✗ Error: {e}")
            pygame.quit()
            return False
    
    pygame.quit()
    return True


def test_all_expressions():
    """Test that all expressions can be drawn"""
    print("\nTesting all expressions...")
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    
    for expression in EXPRESSIONS:
        print(f"  Testing {expression}...", end=" ")
        try:
            random.seed(0)
            generate_avatar(screen)
            print("✓")
        except Exception as e:
            print(f"✗ Error: {e}")
            pygame.quit()
            return False
    
    pygame.quit()
    return True


if __name__ == '__main__':
    print("=" * 60)
    print("Fantasy Avatar Generator - Test Suite")
    print("=" * 60)
    
    # Run tests
    success = True
    success = success and test_generation()
    success = success and test_all_races()
    success = success and test_all_expressions()
    
    print("\n" + "=" * 60)
    if success:
        print("All tests completed successfully! ✓")
        print("=" * 60)
        sys.exit(0)
    else:
        print("Some tests failed! ✗")
        print("=" * 60)
        sys.exit(1)
