#!/usr/bin/env python3
"""
ESPN Fantasy Football Lineup Manager

A Python implementation for programmatically managing ESPN Fantasy Football lineups
using reverse-engineered API endpoints. Based on real browser HAR capture analysis.

Author: Brian Matzelle
Created: 2025-08-30
"""

import requests
import json
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass
from enum import IntEnum


class LineupSlot(IntEnum):
    """ESPN Fantasy Football lineup slot IDs"""
    QB = 0
    RB = 2
    WR = 4
    TE = 6
    DST = 16  # Defense/Special Teams
    K = 17    # Kicker
    BENCH = 20
    IR = 21   # Injured Reserve
    FLEX = 23 # RB/WR/TE Flex


@dataclass
class LineupMove:
    """Represents a single player lineup move"""
    player_id: int
    from_slot: int
    to_slot: int
    
    def to_dict(self) -> Dict:
        """Convert to ESPN API format"""
        return {
            "playerId": self.player_id,
            "type": "LINEUP",
            "fromLineupSlotId": self.from_slot,
            "toLineupSlotId": self.to_slot
        }


class ESPNLineupManager:
    """
    ESPN Fantasy Football Lineup Manager
    
    Handles programmatic lineup changes using ESPN's internal write APIs.
    Based on reverse engineering of browser network requests.
    """
    
    # ESPN API endpoints and constants
    BASE_URL = "https://lm-api-writes.fantasy.espn.com"
    API_PATH = "/apis/v3/games/ffl/seasons/{year}/segments/0/leagues/{league_id}/transactions/"
    
    # Required headers discovered through HAR analysis
    REQUIRED_HEADERS = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "X-Fantasy-Source": "kona",
        "X-Fantasy-Platform": "kona-PROD-ee817b5eea5e3f12efb5185ee8c626ec21f7c3d8",
        "Origin": "https://fantasy.espn.com",
        "Referer": "https://fantasy.espn.com/",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:142.0) Gecko/20100101 Firefox/142.0",
        "Accept-Language": "en-US,en;q=0.5",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-site"
    }
    
    def __init__(self, league_id: int, year: int, team_id: int, espn_s2: str, swid: str):
        """
        Initialize the lineup manager
        
        Args:
            league_id: ESPN league ID
            year: Fantasy season year
            team_id: Your team ID within the league
            espn_s2: ESPN authentication cookie (espn_s2)
            swid: ESPN user identifier cookie (SWID)
        """
        self.league_id = league_id
        self.year = year
        self.team_id = team_id
        self.espn_s2 = espn_s2
        self.swid = swid
        
        # Build the API endpoint URL
        self.api_url = self.BASE_URL + self.API_PATH.format(
            year=year, 
            league_id=league_id
        )
        
        # Setup cookies for authentication
        self.cookies = {
            "espn_s2": espn_s2,
            "SWID": swid
        }
    
    def make_lineup_changes(self, moves: List[LineupMove], scoring_period: int = 1) -> Dict:
        """
        Execute multiple lineup changes in a single transaction
        
        Args:
            moves: List of LineupMove objects representing the changes
            scoring_period: Week/scoring period (default: 1)
            
        Returns:
            Dict containing the API response
            
        Raises:
            requests.exceptions.RequestException: If the API request fails
            ValueError: If the response indicates an error
        """
        
        # Build the payload using the exact format ESPN expects
        payload = {
            "isLeagueManager": False,
            "teamId": self.team_id,
            "type": "ROSTER",
            "memberId": self.swid,
            "scoringPeriodId": scoring_period,
            "executionType": "EXECUTE",
            "items": [move.to_dict() for move in moves]
        }
        
        print(f"🚀 Making {len(moves)} lineup change(s)...")
        print(f"📋 API URL: {self.api_url}")
        
        # Log the moves for debugging
        for i, move in enumerate(moves, 1):
            from_name = self._slot_id_to_name(move.from_slot)
            to_name = self._slot_id_to_name(move.to_slot)
            print(f"   {i}. Player {move.player_id}: {from_name} → {to_name}")
        
        try:
            response = requests.post(
                self.api_url,
                headers=self.REQUIRED_HEADERS,
                cookies=self.cookies,
                json=payload,
                timeout=30
            )
            
            print(f"📡 Response Status: {response.status_code}")
            
            # Handle different response scenarios
            if response.status_code == 200:
                result = response.json()
                print("✅ Lineup changes executed successfully!")
                print(f"🆔 Transaction ID: {result.get('id', 'N/A')}")
                return result
                
            elif response.status_code == 401:
                raise ValueError("❌ Authentication failed. Check your espn_s2 and SWID cookies.")
                
            elif response.status_code == 403:
                raise ValueError("❌ Access forbidden. You may not have permission to modify this team.")
                
            elif response.status_code == 422:
                error_text = response.text
                raise ValueError(f"❌ Invalid request data: {error_text}")
                
            else:
                response.raise_for_status()
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Network error: {e}")
            raise
        except json.JSONDecodeError as e:
            print(f"❌ Invalid JSON response: {e}")
            print(f"Raw response: {response.text}")
            raise ValueError("Invalid JSON response from ESPN API")
    
    def swap_players(self, player1_id: int, player1_slot: int, 
                    player2_id: int, player2_slot: int, 
                    scoring_period: int = 1) -> Dict:
        """
        Swap two players between lineup positions
        
        Args:
            player1_id: First player's ID
            player1_slot: First player's current slot
            player2_id: Second player's ID  
            player2_slot: Second player's current slot
            scoring_period: Week/scoring period
            
        Returns:
            Dict containing the API response
        """
        moves = [
            LineupMove(player1_id, player1_slot, player2_slot),
            LineupMove(player2_id, player2_slot, player1_slot)
        ]
        return self.make_lineup_changes(moves, scoring_period)
    
    def move_player_to_bench(self, player_id: int, current_slot: int, 
                           scoring_period: int = 1) -> Dict:
        """
        Move a player to the bench
        
        Args:
            player_id: Player's ID
            current_slot: Player's current lineup slot
            scoring_period: Week/scoring period
            
        Returns:
            Dict containing the API response
        """
        move = LineupMove(player_id, current_slot, LineupSlot.BENCH)
        return self.make_lineup_changes([move], scoring_period)
    
    def move_player_from_bench(self, player_id: int, target_slot: int,
                             scoring_period: int = 1) -> Dict:
        """
        Move a player from bench to a starting position
        
        Args:
            player_id: Player's ID
            target_slot: Target lineup slot
            scoring_period: Week/scoring period
            
        Returns:
            Dict containing the API response
        """
        move = LineupMove(player_id, LineupSlot.BENCH, target_slot)
        return self.make_lineup_changes([move], scoring_period)
    
    @staticmethod
    def _slot_id_to_name(slot_id: int) -> str:
        """Convert slot ID to human-readable name"""
        slot_names = {
            0: "QB",
            2: "RB", 
            4: "WR",
            6: "TE",
            16: "D/ST",
            17: "K",
            20: "BENCH",
            21: "IR",
            23: "FLEX"
        }
        return slot_names.get(slot_id, f"SLOT_{slot_id}")
    
    @staticmethod
    def get_slot_reference() -> Dict[str, int]:
        """Get a reference of all lineup slot IDs"""
        return {
            "QB": LineupSlot.QB,
            "RB": LineupSlot.RB,
            "WR": LineupSlot.WR,
            "TE": LineupSlot.TE,
            "D/ST": LineupSlot.DST,
            "K": LineupSlot.K,
            "BENCH": LineupSlot.BENCH,
            "IR": LineupSlot.IR,
            "FLEX": LineupSlot.FLEX
        }


def main():
    """Example usage of the ESPN Lineup Manager"""
    
    # Your league configuration (replace with your actual values)
    LEAGUE_ID = 1955253855
    YEAR = 2025
    TEAM_ID = 12
    ESPN_S2 = "AEAtP8bWFwzl3v6tye0ICdqdzT1gXJbC28j7dgl4bjP6KGYJ/QRT3n1Vu+jVxIvgwnOhY2nFs4uGWt5QeP4ZoaaL7FeKLzuyVXZvbtHBSVUmKq0w1lB7UQ6qc09vxrlqxeolhZYTHyNpc2YUbP1VdOVNI1tjIfkmXt8fPVYg2NHjP8Cn32WMbB1f73sljFj4hwANVOJ0cXbn2u0HhB5kCqSURIRVfNDGqfttCA2egQYe9CzBgrJu33cVY83pLyhgNhVA6Ai4Hs0JeclDxSPwIJhkVkOAnrLexx7luQXhY6ApXkdV5QFrhXW2kR/xs/gsgmLe+d3NILQh3tPf0CcXxipk"
    SWID = "{88C298DE-BEE1-401E-9D60-F92268A73179}"
    
    # Player IDs from your roster
    TRAVIS_HUNTER = 4685415   # Currently on bench
    JAYLEN_WADDLE = 4372016   # Currently in flex
    JUSTIN_FIELDS = 4362887   # Currently on bench  
    JAYDEN_DANIELS = 4426348  # Currently starting QB
    
    # Initialize the lineup manager
    manager = ESPNLineupManager(
        league_id=LEAGUE_ID,
        year=YEAR, 
        team_id=TEAM_ID,
        espn_s2=ESPN_S2,
        swid=SWID
    )
    
    print("ESPN Fantasy Lineup Manager - Python Edition")
    print("=" * 50)
    
    # Show slot reference
    print("\n📋 Lineup Slot Reference:")
    for name, slot_id in manager.get_slot_reference().items():
        print(f"   {name}: {slot_id}")
    
    try:
        # Example 1: Swap Travis Hunter from bench to flex, Waddle to bench
        print("\n🎯 Example 1: Moving Travis Hunter to starting lineup")
        result1 = manager.swap_players(
            TRAVIS_HUNTER, LineupSlot.BENCH,
            JAYLEN_WADDLE, LineupSlot.FLEX
        )
        print(f"✅ Transaction completed: {result1.get('status', 'Unknown')}")
        
        # Example 2: Swap QBs (commented out - uncomment to test)
        # print("\n🎯 Example 2: Swapping QBs")
        # result2 = manager.swap_players(
        #     JUSTIN_FIELDS, LineupSlot.BENCH,
        #     JAYDEN_DANIELS, LineupSlot.QB
        # )
        # print(f"✅ Transaction completed: {result2.get('status', 'Unknown')}")
        
    except ValueError as e:
        print(f"❌ Error: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")


if __name__ == "__main__":
    main()
