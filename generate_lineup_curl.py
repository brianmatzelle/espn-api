#!/usr/bin/env python3
"""
Generate Curl Commands for ESPN Fantasy Lineup Changes

This script creates curl commands to modify your fantasy football lineup
using ESPN's internal write APIs.
"""

import urllib.parse
import json
from espn_api.football import League

# Your league credentials
LEAGUE_ID = 1955253855
YEAR = 2025
ESPN_S2 = "AECQL%2B2AIQS6%2BFOAguA5%2FY5GjS1o4kyISmmKLURXFI%2FbQ8edOZAgD7UACXY5VTfhX1psgImU4yENKwzjbLxpN9wSjMItx%2B%2B7cWFtx7oDVSydXo%2Bhof5CAtVh%2Bu%2BjmSlEFrJ94GPx2TzJ2Ppq5WJO%2FvZAhAvv7hesHZBj%2FuJB6fHrl9AG%2FQyWEqj%2FPrYX6Gku5LdJeoojLcGrjplHVfvyKL3bhNJSUtT1W929yuXcG%2FtPTTUal6Y8AYOJXaG2jrYlCjYFMwjrlEwN3sRrV8Wlcl5xW9m7vPrbIy1uflqhaShpw4FqUqn%2B%2FPH7ohOvtlioQSHtATz6GxHBZpI4v%2FiYTjk0"
SWID = "{88C298DE-BEE1-401E-9D60-F92268A73179}"
YOUR_TEAM_ID = 12  # Brian's Best Team

def get_roster_info():
    """Get your current roster information"""
    decoded_espn_s2 = urllib.parse.unquote(ESPN_S2)
    league = League(league_id=LEAGUE_ID, year=YEAR, espn_s2=decoded_espn_s2, swid=SWID)
    
    # Find your team
    your_team = None
    for team in league.teams:
        if team.team_id == YOUR_TEAM_ID:
            your_team = team
            break
    
    if not your_team:
        print("❌ Could not find your team!")
        return None, None
    
    print(f"=== {your_team.team_name} Current Roster ===")
    print(f"Team ID: {your_team.team_id}")
    print(f"Current Week: {league.current_week}")
    
    print("\nCurrent Lineup:")
    for i, player in enumerate(your_team.roster):
        # Try different possible attribute names for lineup slot
        slot_id = None
        for attr in ['lineupSlot', 'slot_position', 'lineupSlotId', 'lineup_slot_id', 'slotId', 'slot_id']:
            if hasattr(player, attr):
                slot_id = getattr(player, attr)
                break
        
        if slot_id is None:
            # Debug: show all player attributes
            print(f"  {i+1:2d}. {player.name:25} {player.position:4} | UNKNOWN SLOT | ID: {player.playerId}")
            if i == 0:  # Only show for first player to avoid spam
                print(f"       Available attributes: {[attr for attr in dir(player) if not attr.startswith('_')]}")
        else:
            slot_name = get_slot_name(slot_id)
            status = ""
            if hasattr(player, 'injuryStatus') and player.injuryStatus:
                status = f" [{player.injuryStatus}]"
            
            print(f"  {i+1:2d}. {player.name:25} {player.position:4} | {slot_name:8} | ID: {player.playerId}{status}")
    
    return league, your_team

def get_slot_name(slot_id):
    """Convert slot ID to human readable name"""
    slot_map = {
        0: 'QB',      # Quarterback
        2: 'RB',      # Running Back  
        4: 'WR',      # Wide Receiver
        6: 'TE',      # Tight End
        16: 'D/ST',   # Defense/Special Teams
        17: 'K',      # Kicker
        20: 'BENCH',  # Bench
        21: 'IR',     # Injured Reserve
        23: 'FLEX'    # Flex (RB/WR/TE)
    }
    return slot_map.get(slot_id, f'SLOT_{slot_id}')

def generate_curl_commands(team, player_id, from_slot, to_slot, week=None):
    """Generate curl commands for lineup changes"""
    
    if not week:
        week = team.league.current_week
    
    decoded_espn_s2 = urllib.parse.unquote(ESPN_S2)
    
    print(f"\n🚀 Generated Curl Commands to Move Player {player_id}")
    print(f"   From: {get_slot_name(from_slot)} → To: {get_slot_name(to_slot)}")
    print("=" * 80)
    
    # Method 1: Direct roster update (most likely to work)
    base_url = f"https://lm-api-writes.fantasy.espn.com/v3/games/ffl/seasons/{YEAR}/segments/0/leagues/{LEAGUE_ID}"
    
    # Build roster entries - we need to send the entire roster with the change
    roster_entries = []
    for player in team.roster:
        entry = {
            "playerId": player.playerId,
            "lineupSlotId": to_slot if player.playerId == player_id else player.lineupSlot
        }
        roster_entries.append(entry)
    
    roster_payload = {
        "teams": [{
            "teamId": YOUR_TEAM_ID,
            "roster": {
                "entries": roster_entries
            }
        }]
    }
    
    print("METHOD 1: Full Roster Update")
    curl_1 = f'''curl -X PUT "{base_url}/teams/{YOUR_TEAM_ID}/roster?scoringPeriodId={week}" \\
  -H "Content-Type: application/json" \\
  -H "Cookie: espn_s2={decoded_espn_s2}; SWID={SWID}" \\
  -H "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36" \\
  -H "Accept: application/json" \\
  -H "Referer: https://fantasy.espn.com/" \\
  -H "Origin: https://fantasy.espn.com" \\
  -d '{json.dumps(roster_payload)}'
'''
    print(curl_1)
    print("\n" + "-" * 80)
    
    # Method 2: Transaction-based approach
    transaction_payload = {
        "teamId": YOUR_TEAM_ID,
        "type": "LINEUP_CHANGE",
        "memberId": SWID.strip('{}'),
        "scoringPeriodId": week,
        "executionType": "EXECUTE",
        "items": [{
            "playerId": player_id,
            "type": "MOVE",
            "fromLineupSlotId": from_slot,
            "toLineupSlotId": to_slot
        }]
    }
    
    print("METHOD 2: Transaction-based")
    curl_2 = f'''curl -X POST "{base_url}/transactions" \\
  -H "Content-Type: application/json" \\
  -H "Cookie: espn_s2={decoded_espn_s2}; SWID={SWID}" \\
  -H "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36" \\
  -H "Accept: application/json" \\
  -H "Referer: https://fantasy.espn.com/" \\
  -H "Origin: https://fantasy.espn.com" \\
  -d '{json.dumps(transaction_payload)}'
'''
    print(curl_2)
    print("\n" + "-" * 80)
    
    # Method 3: Simple roster entry update
    simple_payload = {
        "playerId": player_id,
        "lineupSlotId": to_slot
    }
    
    print("METHOD 3: Simple Player Move")
    curl_3 = f'''curl -X PUT "{base_url}/teams/{YOUR_TEAM_ID}/roster/entries/{player_id}" \\
  -H "Content-Type: application/json" \\
  -H "Cookie: espn_s2={decoded_espn_s2}; SWID={SWID}" \\
  -H "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36" \\
  -H "Accept: application/json" \\
  -H "Referer: https://fantasy.espn.com/" \\
  -H "Origin: https://fantasy.espn.com" \\
  -d '{json.dumps(simple_payload)}'
'''
    print(curl_3)
    print("\n" + "=" * 80)
    
    print("💡 TESTING TIPS:")
    print("1. Try Method 1 first - it's most likely to work")
    print("2. If you get a 401 error, your cookies might have expired")
    print("3. If you get a 403 error, the endpoint might be wrong")
    print("4. If you get a 422 error, the payload format might be incorrect")
    print("5. Look for any error messages in the response JSON")
    
    # Save to file for easy testing
    with open('lineup_change_curls.sh', 'w') as f:
        f.write('#!/bin/bash\n')
        f.write('# ESPN Fantasy Football Lineup Change Commands\n')
        f.write('# Generated automatically - test these one by one\n\n')
        f.write('echo "Testing Method 1: Full Roster Update"\n')
        f.write(curl_1 + '\n\n')
        f.write('echo "Testing Method 2: Transaction-based"\n') 
        f.write(curl_2 + '\n\n')
        f.write('echo "Testing Method 3: Simple Player Move"\n')
        f.write(curl_3 + '\n\n')
    
    print(f"\n💾 Commands saved to: lineup_change_curls.sh")
    print("   Make it executable: chmod +x lineup_change_curls.sh")

def main():
    """Main function"""
    print("ESPN Fantasy Lineup Curl Generator")
    print("=" * 50)
    
    league, team = get_roster_info()
    if not team:
        return
    
    print(f"\n📋 Available Slot IDs:")
    print("   0=QB, 2=RB, 4=WR, 6=TE, 16=D/ST, 17=K, 20=BENCH, 21=IR, 23=FLEX")
    
    try:
        # Get player to move
        player_num = int(input(f"\n🎯 Enter player number to move (1-{len(team.roster)}): ")) - 1
        if player_num < 0 or player_num >= len(team.roster):
            print("❌ Invalid player number")
            return
            
        player = team.roster[player_num]
        current_slot = player.lineupSlot
        
        print(f"\n✅ Selected: {player.name} ({player.position})")
        print(f"   Currently in: {get_slot_name(current_slot)} (ID: {current_slot})")
        
        # Get destination slot
        new_slot = int(input(f"🎯 Enter new slot ID: "))
        
        if new_slot == current_slot:
            print("⚠️  Player is already in that slot!")
            return
        
        # Generate the curl commands
        generate_curl_commands(team, player.playerId, current_slot, new_slot)
        
    except ValueError:
        print("❌ Please enter valid numbers")
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")

if __name__ == "__main__":
    main()
