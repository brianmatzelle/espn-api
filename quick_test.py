#!/usr/bin/env python3
"""
Quick ESPN Fantasy Football API Test

A minimal script to quickly test your ESPN Fantasy Football API connection.
Just update the league_id and year below and run!
"""

import urllib.parse
from espn_api.football import League

# Configuration - UPDATE THESE VALUES
LEAGUE_ID = 1955253855     # Replace with your ESPN league ID
YEAR = 2025

# For private leagues, uncomment and fill these in:
ESPN_S2 = "AECQL%2B2AIQS6%2BFOAguA5%2FY5GjS1o4kyISmmKLURXFI%2FbQ8edOZAgD7UACXY5VTfhX1psgImU4yENKwzjbLxpN9wSjMItx%2B%2B7cWFtx7oDVSydXo%2Bhof5CAtVh%2Bu%2BjmSlEFrJ94GPx2TzJ2Ppq5WJO%2FvZAhAvv7hesHZBj%2FuJB6fHrl9AG%2FQyWEqj%2FPrYX6Gku5LdJeoojLcGrjplHVfvyKL3bhNJSUtT1W929yuXcG%2FtPTTUal6Y8AYOJXaG2jrYlCjYFMwjrlEwN3sRrV8Wlcl5xW9m7vPrbIy1uflqhaShpw4FqUqn%2B%2FPH7ohOvtlioQSHtATz6GxHBZpI4v%2FiYTjk0"
SWID = "{88C298DE-BEE1-401E-9D60-F92268A73179}"

def main():
    print(f"Testing ESPN Fantasy Football API connection...")
    print(f"League ID: {LEAGUE_ID}, Year: {YEAR}")
    print("-" * 40)
    
    # URL decode the ESPN_S2 cookie (it appears to be URL encoded)
    decoded_espn_s2 = urllib.parse.unquote(ESPN_S2)
    print(f"Using decoded ESPN_S2 cookie...")
    
    try:
        # For private leagues with decoded cookies
        league = League(league_id=LEAGUE_ID, year=YEAR, espn_s2=decoded_espn_s2, swid=SWID)
        
        # Basic info
        print(f"✅ Connected successfully!")
        print(f"League: {league.settings.name}")
        print(f"Teams: {len(league.teams)}")
        print(f"Current Week: {league.current_week}")
        
        # Show teams
        print(f"\nTeams:")
        for i, team in enumerate(league.teams[:5], 1):  # Show first 5 teams
            print(f"  {i}. {team.team_name} ({team.wins}-{team.losses})")
        
        if len(league.teams) > 5:
            print(f"  ... and {len(league.teams) - 5} more teams")
            
        print(f"\n🎉 Success! The API is working correctly.")
        
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        print(f"\nTroubleshooting:")
        print(f"- Check that league_id {LEAGUE_ID} is correct")
        print(f"- Verify the year {YEAR} is valid")
        print(f"- For private leagues, make sure you have the correct cookies")

if __name__ == "__main__":
    main()
