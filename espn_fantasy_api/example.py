#!/usr/bin/env python3
"""
ESPN Fantasy Football API - Example Usage

This example demonstrates how to use the reverse-engineered ESPN API
to make programmatic lineup changes.

Make sure to update the configuration section with your actual credentials!
"""

import sys
import os

# Add the parent directory to Python path so we can import our module
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from espn_fantasy_api import ESPNLineupManager, LineupMove, LineupSlot, LINEUP_SLOTS


def main():
    """Example usage of the ESPN Fantasy API"""
    
    print("🏈 ESPN Fantasy Football API - Example Usage")
    print("=" * 55)
    
    # ========================================
    # CONFIGURATION - UPDATE THESE VALUES!
    # ========================================
    
    LEAGUE_ID = 1955253855  # Your ESPN league ID
    YEAR = 2025             # Fantasy season year
    TEAM_ID = 12            # Your team ID in the league
    
    # Your ESPN authentication cookies (get from browser dev tools)
    ESPN_S2 = "AEAtP8bWFwzl3v6tye0ICdqdzT1gXJbC28j7dgl4bjP6KGYJ/QRT3n1Vu+jVxIvgwnOhY2nFs4uGWt5QeP4ZoaaL7FeKLzuyVXZvbtHBSVUmKq0w1lB7UQ6qc09vxrlqxeolhZYTHyNpc2YUbP1VdOVNI1tjIfkmXt8fPVYg2NHjP8Cn32WMbB1f73sljFj4hwANVOJ0cXbn2u0HhB5kCqSURIRVfNDGqfttCA2egQYe9CzBgrJu33cVY83pLyhgNhVA6Ai4Hs0JeclDxSPwIJhkVkOAnrLexx7luQXhY6ApXkdV5QFrhXW2kR/xs/gsgmLe+d3NILQh3tPf0CcXxipk"
    SWID = "{88C298DE-BEE1-401E-9D60-F92268A73179}"
    
    # Example player IDs (replace with your actual player IDs)
    PLAYERS = {
        "Travis Hunter": 4685415,    # WR - currently on bench
        "Jaylen Waddle": 4372016,    # WR - currently in flex
        "Justin Fields": 4362887,    # QB - currently on bench
        "Jayden Daniels": 4426348,   # QB - currently starting
        "Justin Jefferson": 4262921,  # WR - currently starting
    }
    
    # ========================================
    # INITIALIZE THE API MANAGER
    # ========================================
    
    try:
        manager = ESPNLineupManager(
            league_id=LEAGUE_ID,
            year=YEAR,
            team_id=TEAM_ID,
            espn_s2=ESPN_S2,
            swid=SWID
        )
        
        print(f"✅ Initialized ESPN API Manager")
        print(f"   League: {LEAGUE_ID}")
        print(f"   Team: {TEAM_ID}")
        print(f"   Year: {YEAR}")
        
    except Exception as e:
        print(f"❌ Failed to initialize manager: {e}")
        return
    
    # ========================================
    # SHOW LINEUP SLOT REFERENCE
    # ========================================
    
    print(f"\n📋 Lineup Slot Reference:")
    for position, slot_id in LINEUP_SLOTS.items():
        print(f"   {position:5} = {slot_id}")
    
    # ========================================
    # EXAMPLE LINEUP CHANGES
    # ========================================
    
    print(f"\n🎯 Example Lineup Changes:")
    print(f"Choose an option to test:")
    print(f"1. Move Travis Hunter from BENCH to FLEX (swap with Waddle)")
    print(f"2. Swap QBs (Fields ↔ Daniels)")
    print(f"3. Move Travis Hunter to BENCH (if he's starting)")
    print(f"4. Custom moves")
    print(f"0. Exit without making changes")
    
    try:
        choice = input(f"\nEnter your choice (0-4): ").strip()
        
        if choice == "0":
            print("👋 Exiting without changes.")
            return
            
        elif choice == "1":
            print(f"\n🔄 Swapping Travis Hunter (BENCH) ↔ Jaylen Waddle (FLEX)")
            result = manager.swap_players(
                PLAYERS["Travis Hunter"], LineupSlot.BENCH,
                PLAYERS["Jaylen Waddle"], LineupSlot.FLEX
            )
            print(f"✅ Success! Transaction ID: {result.get('id', 'N/A')}")
            
        elif choice == "2":
            print(f"\n🔄 Swapping Justin Fields (BENCH) ↔ Jayden Daniels (QB)")
            result = manager.swap_players(
                PLAYERS["Justin Fields"], LineupSlot.BENCH,
                PLAYERS["Jayden Daniels"], LineupSlot.QB
            )
            print(f"✅ Success! Transaction ID: {result.get('id', 'N/A')}")
            
        elif choice == "3":
            print(f"\n📤 Moving Travis Hunter to BENCH")
            result = manager.move_player_to_bench(
                PLAYERS["Travis Hunter"], 
                LineupSlot.WR  # Assuming he's in a WR slot
            )
            print(f"✅ Success! Transaction ID: {result.get('id', 'N/A')}")
            
        elif choice == "4":
            print(f"\n🛠️ Custom moves example:")
            print(f"Making multiple moves in one transaction...")
            
            moves = [
                LineupMove(PLAYERS["Travis Hunter"], LineupSlot.BENCH, LineupSlot.WR),
                LineupMove(PLAYERS["Justin Jefferson"], LineupSlot.WR, LineupSlot.FLEX),
                LineupMove(PLAYERS["Jaylen Waddle"], LineupSlot.FLEX, LineupSlot.BENCH)
            ]
            
            result = manager.make_lineup_changes(moves)
            print(f"✅ Success! Transaction ID: {result.get('id', 'N/A')}")
            
        else:
            print(f"❌ Invalid choice: {choice}")
            
    except ValueError as e:
        print(f"❌ API Error: {e}")
    except KeyboardInterrupt:
        print(f"\n👋 Cancelled by user.")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        print(f"   This might indicate that your cookies have expired or the API has changed.")


if __name__ == "__main__":
    main()
