#!/usr/bin/env python3
"""
ESPN Fantasy Football API - Intro Test Script

This script demonstrates how to get started with the ESPN Fantasy Football API.
It shows basic usage patterns for connecting to a league and retrieving data.

Requirements:
- A valid ESPN Fantasy Football league ID
- The year/season you want to access
- For private leagues: espn_s2 and SWID cookies (see instructions below)

Getting Private League Access:
1. Log into ESPN Fantasy Football in your browser
2. Open Developer Tools (F12)
3. Go to Application/Storage > Cookies > espn.com
4. Find and copy the values for 'espn_s2' and 'SWID' cookies
"""

from espn_api.football import League


def test_public_league():
    """Test connection to a public league (no authentication needed)"""
    print("=== Testing Public League Connection ===")
    
    try:
        # Example with a public league (replace with your league ID and year)
        # This is ESPN's example public league - you should replace with your own
        league_id = 222  # Replace with your league ID
        year = 2023      # Replace with your desired year
        
        print(f"Connecting to League ID: {league_id}, Year: {year}")
        
        # Initialize league (this will fetch basic league data)
        league = League(league_id=league_id, year=year)
        
        # Basic league information
        print(f"League Name: {league.settings.name}")
        print(f"Number of Teams: {len(league.teams)}")
        print(f"Current Week: {league.current_week}")
        print(f"NFL Week: {league.nfl_week}")
        
        # Show team names
        print("\nTeams in League:")
        for i, team in enumerate(league.teams, 1):
            print(f"  {i}. {team.team_name} (Owner: {team.owner})")
        
        # Show current standings
        print("\nCurrent Standings:")
        standings = league.standings()
        for i, team in enumerate(standings, 1):
            print(f"  {i}. {team.team_name} - {team.wins}-{team.losses} ({team.points_for:.1f} PF)")
        
        print("\n✅ Public league connection successful!")
        return True
        
    except Exception as e:
        print(f"❌ Error connecting to public league: {e}")
        print("Make sure the league ID is correct and the league is public.")
        return False


def test_private_league():
    """Test connection to a private league (requires authentication)"""
    print("\n=== Testing Private League Connection ===")
    
    # You'll need to provide these values for private leagues
    league_id = None      # Replace with your private league ID
    year = 2023           # Replace with your desired year
    espn_s2 = None        # Replace with your espn_s2 cookie value
    swid = None           # Replace with your SWID cookie value
    
    if not all([league_id, espn_s2, swid]):
        print("⚠️  Private league test skipped - missing credentials")
        print("To test private leagues, update the variables above with your:")
        print("- league_id: Your ESPN league ID")
        print("- espn_s2: Your espn_s2 cookie value")
        print("- swid: Your SWID cookie value")
        return False
    
    try:
        print(f"Connecting to Private League ID: {league_id}, Year: {year}")
        
        # Initialize league with authentication cookies
        league = League(
            league_id=league_id,
            year=year,
            espn_s2=espn_s2,
            swid=swid
        )
        
        # Basic league information
        print(f"League Name: {league.settings.name}")
        print(f"Number of Teams: {len(league.teams)}")
        
        # Show recent activity (private leagues only)
        print("\nRecent League Activity:")
        try:
            activities = league.recent_activity(size=5)
            for activity in activities:
                print(f"  - {activity}")
        except Exception as e:
            print(f"  Could not fetch recent activity: {e}")
        
        print("\n✅ Private league connection successful!")
        return True
        
    except Exception as e:
        print(f"❌ Error connecting to private league: {e}")
        print("Check your league ID and authentication cookies.")
        return False


def demonstrate_features():
    """Demonstrate various API features with a test league"""
    print("\n=== Demonstrating API Features ===")
    
    try:
        # Use a public league for demonstration
        league = League(league_id=222, year=2023)
        
        print("1. League Settings:")
        print(f"   - Roster Size: {league.settings.roster_size}")
        print(f"   - Playoff Teams: {league.settings.playoff_team_count}")
        print(f"   - Regular Season Matchup Periods: {league.settings.reg_season_count}")
        
        print("\n2. Top Scorer:")
        top_team = league.top_scorer()
        print(f"   {top_team.team_name}: {top_team.points_for:.1f} points")
        
        print("\n3. Least Scorer:")
        least_team = league.least_scorer()
        print(f"   {least_team.team_name}: {least_team.points_for:.1f} points")
        
        print("\n4. Current Week Scoreboard:")
        try:
            matchups = league.scoreboard()
            for matchup in matchups[:3]:  # Show first 3 matchups
                home_score = matchup.home_score if matchup.home_score else 0
                away_score = matchup.away_score if matchup.away_score else 0
                print(f"   {matchup.away_team.team_name} ({away_score:.1f}) @ {matchup.home_team.team_name} ({home_score:.1f})")
        except Exception as e:
            print(f"   Could not fetch scoreboard: {e}")
        
        print("\n✅ Feature demonstration complete!")
        
    except Exception as e:
        print(f"❌ Error demonstrating features: {e}")


def main():
    """Main function to run all tests"""
    print("ESPN Fantasy Football API - Intro Test")
    print("=" * 50)
    
    # Test public league connection
    public_success = test_public_league()
    
    # Test private league connection (if configured)
    private_success = test_private_league()
    
    # Demonstrate features if we have a working connection
    if public_success:
        demonstrate_features()
    
    print("\n" + "=" * 50)
    print("Test Summary:")
    print(f"Public League:  {'✅ Success' if public_success else '❌ Failed'}")
    print(f"Private League: {'✅ Success' if private_success else '⚠️ Skipped/Failed'}")
    
    if public_success or private_success:
        print("\n🎉 You're ready to use the ESPN Fantasy Football API!")
        print("\nNext steps:")
        print("- Replace the example league_id with your own league")
        print("- Explore more features like box_scores(), free_agents(), power_rankings()")
        print("- Check the wiki for detailed documentation: https://github.com/cwendt94/espn-api/wiki")
    else:
        print("\n❌ No successful connections. Check your league ID and network connection.")


if __name__ == "__main__":
    main()
