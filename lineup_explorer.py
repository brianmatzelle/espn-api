#!/usr/bin/env python3
"""
ESPN Fantasy Lineup Explorer

This script helps discover the API endpoints used for making lineup changes
by providing tools to inspect your current roster and generate curl commands
for making changes.

Based on reverse engineering ESPN's internal APIs.
"""

import urllib.parse
import json
import requests
from espn_api.football import League

# Your league credentials
LEAGUE_ID = 1955253855
YEAR = 2025
ESPN_S2 = "AECQL%2B2AIQS6%2BFOAguA5%2FY5GjS1o4kyISmmKLURXFI%2FbQ8edOZAgD7UACXY5VTfhX1psgImU4yENKwzjbLxpN9wSjMItx%2B%2B7cWFtx7oDVSydXo%2Bhof5CAtVh%2Bu%2BjmSlEFrJ94GPx2TzJ2Ppq5WJO%2FvZAhAvv7hesHZBj%2FuJB6fHrl9AG%2FQyWEqj%2FPrYX6Gku5LdJeoojLcGrjplHVfvyKL3bhNJSUtT1W929yuXcG%2FtPTTUal6Y8AYOJXaG2jrYlCjYFMwjrlEwN3sRrV8Wlcl5xW9m7vPrbIy1uflqhaShpw4FqUqn%2B%2FPH7ohOvtlioQSHtATz6GxHBZpI4v%2FiYTjk0"
SWID = "{88C298DE-BEE1-401E-9D60-F92268A73179}"

def get_league_info():
    """Get basic league and team info"""
    decoded_espn_s2 = urllib.parse.unquote(ESPN_S2)
    league = League(league_id=LEAGUE_ID, year=YEAR, espn_s2=decoded_espn_s2, swid=SWID)
    return league

def find_my_team(league):
    """Find which team belongs to the authenticated user"""
    # This is tricky - we need to identify which team is "yours"
    # For now, let's just show all teams and let user choose
    print("Available teams in your league:")
    for i, team in enumerate(league.teams):
        # Handle different ways owner info might be stored
        owner_info = ""
        if hasattr(team, 'owner'):
            owner_info = f" (Owner: {team.owner})"
        elif hasattr(team, 'owners') and team.owners:
            owner_info = f" (Owner: {team.owners[0] if team.owners else 'Unknown'})"
        
        print(f"  {i+1}. {team.team_name}{owner_info}")
    
    while True:
        try:
            choice = int(input("\nWhich team is yours? Enter number: ")) - 1
            if 0 <= choice < len(league.teams):
                return league.teams[choice]
            else:
                print("Invalid choice. Please try again.")
        except ValueError:
            print("Please enter a valid number.")

def show_roster_details(team, week=None):
    """Show detailed roster information including lineup slots"""
    print(f"\n=== {team.team_name} Roster Details ===")
    
    if week:
        # Load specific week roster
        team.league.load_roster_week(week)
    
    print(f"Team ID: {team.team_id}")
    print(f"Current Week: {team.league.current_week}")
    
    print("\nCurrent Roster:")
    for i, player in enumerate(team.roster):
        slot_name = get_slot_name(player.slot_position)
        print(f"  {i+1}. {player.name} ({player.position}) - Slot: {slot_name} (ID: {player.slot_position})")
        print(f"      Player ID: {player.playerId}")
        if hasattr(player, 'injuryStatus') and player.injuryStatus:
            print(f"      Injury: {player.injuryStatus}")

def get_slot_name(slot_id):
    """Convert slot ID to human readable name"""
    slot_map = {
        0: 'QB',
        2: 'RB', 
        4: 'WR',
        6: 'TE',
        16: 'D/ST',
        17: 'K',
        20: 'BENCH',
        21: 'IR',
        23: 'FLEX'
    }
    return slot_map.get(slot_id, f'UNKNOWN({slot_id})')

def generate_lineup_change_curl(team, player_id, from_slot, to_slot, week=None):
    """Generate a curl command to change a player's lineup position"""
    
    if not week:
        week = team.league.current_week
    
    decoded_espn_s2 = urllib.parse.unquote(ESPN_S2)
    
    # Based on reverse engineering, lineup changes likely use PUT/POST to roster endpoints
    # Common ESPN API patterns suggest something like:
    base_url = f"https://lm-api-writes.fantasy.espn.com/v3/games/ffl/seasons/{YEAR}/segments/0/leagues/{LEAGUE_ID}"
    
    # Potential endpoints for roster changes:
    endpoints_to_try = [
        f"{base_url}/teams/{team.team_id}/roster",
        f"{base_url}/teams/{team.team_id}/roster?scoringPeriodId={week}",
        f"{base_url}/roster",
        f"{base_url}/transactions"
    ]
    
    # Roster change payload (educated guess based on typical ESPN API structure)
    roster_payload = {
        "teams": [{
            "teamId": team.team_id,
            "roster": {
                "entries": [{
                    "playerId": player_id,
                    "lineupSlotId": to_slot
                }]
            }
        }]
    }
    
    transaction_payload = {
        "teamId": team.team_id,
        "type": "LINEUP",
        "memberId": team.team_id,  # might need actual member ID
        "scoringPeriodId": week,
        "executionType": "EXECUTE",
        "items": [{
            "playerId": player_id,
            "type": "MOVE",
            "fromLineupSlotId": from_slot,
            "toLineupSlotId": to_slot
        }]
    }
    
    print(f"\n=== Generated Curl Commands ===")
    print("Try these endpoints in order until one works:\n")
    
    for i, endpoint in enumerate(endpoints_to_try, 1):
        payload = roster_payload if 'roster' in endpoint else transaction_payload
        
        curl_cmd = f'''curl -X PUT "{endpoint}" \\
  -H "Content-Type: application/json" \\
  -H "Cookie: espn_s2={decoded_espn_s2}; SWID={SWID}" \\
  -H "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36" \\
  -d '{json.dumps(payload, indent=2)}'
'''
        
        print(f"Option {i}:")
        print(curl_cmd)
        print("-" * 80)

def interactive_lineup_change(team):
    """Interactive helper to build lineup change commands"""
    print(f"\n=== Interactive Lineup Change for {team.team_name} ===")
    
    show_roster_details(team)
    
    print("\nTo move a player:")
    try:
        player_num = int(input("Enter player number to move: ")) - 1
        if player_num < 0 or player_num >= len(team.roster):
            print("Invalid player number")
            return
            
        player = team.roster[player_num]
        current_slot = player.slot_position
        
        print(f"\nSelected: {player.name} (currently in {get_slot_name(current_slot)})")
        print("\nAvailable slots:")
        print("  0 = QB, 2 = RB, 4 = WR, 6 = TE, 16 = D/ST, 17 = K, 20 = BENCH, 21 = IR, 23 = FLEX")
        
        new_slot = int(input("Enter new slot ID: "))
        
        generate_lineup_change_curl(team, player.playerId, current_slot, new_slot)
        
    except ValueError:
        print("Please enter valid numbers")

def main():
    """Main function"""
    print("ESPN Fantasy Lineup Explorer")
    print("=" * 50)
    
    try:
        print("Connecting to your league...")
        league = get_league_info()
        print(f"✅ Connected to: {league.settings.name}")
        
        my_team = find_my_team(league)
        print(f"✅ Selected team: {my_team.team_name}")
        
        while True:
            print("\nOptions:")
            print("1. Show roster details")
            print("2. Generate lineup change curl command")
            print("3. Test raw API endpoint")
            print("4. Exit")
            
            choice = input("\nChoose option (1-4): ").strip()
            
            if choice == "1":
                week = input("Enter week number (or press Enter for current): ").strip()
                week = int(week) if week else None
                show_roster_details(my_team, week)
                
            elif choice == "2":
                interactive_lineup_change(my_team)
                
            elif choice == "3":
                test_api_endpoints(my_team)
                
            elif choice == "4":
                print("Goodbye!")
                break
                
            else:
                print("Invalid choice")
                
    except Exception as e:
        print(f"❌ Error: {e}")

def test_api_endpoints(team):
    """Test various API endpoints to find the right one for roster changes"""
    print("\n=== Testing API Endpoints ===")
    
    decoded_espn_s2 = urllib.parse.unquote(ESPN_S2)
    cookies = {'espn_s2': decoded_espn_s2, 'SWID': SWID}
    
    # Test GET endpoints first to understand the data structure
    base_url = f"https://lm-api-reads.fantasy.espn.com/v3/games/ffl/seasons/{YEAR}/segments/0/leagues/{LEAGUE_ID}"
    
    test_endpoints = [
        f"{base_url}/teams/{team.team_id}/roster",
        f"{base_url}/teams/{team.team_id}",
        f"{base_url}/roster",
        f"{base_url}"
    ]
    
    for endpoint in test_endpoints:
        try:
            print(f"\nTesting: {endpoint}")
            response = requests.get(endpoint, cookies=cookies, timeout=10)
            print(f"Status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                print(f"Response keys: {list(data.keys()) if isinstance(data, dict) else 'Not a dict'}")
                
                # Save response for analysis
                filename = f"api_response_{endpoint.split('/')[-1] or 'root'}.json"
                with open(filename, 'w') as f:
                    json.dump(data, f, indent=2)
                print(f"Saved response to: {filename}")
            else:
                print(f"Error: {response.text[:200]}...")
                
        except Exception as e:
            print(f"Failed: {e}")

if __name__ == "__main__":
    main()
