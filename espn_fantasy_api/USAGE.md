# ESPN Fantasy API - Usage Guide

## Quick Start

1. **Install dependencies**:
   ```bash
   pip install requests
   # or
   pip install -r requirements.txt
   ```

2. **Get your ESPN credentials**:
   - League ID (from your ESPN fantasy URL)
   - Team ID (your team number in the league)
   - ESPN cookies (`espn_s2` and `SWID` from browser dev tools)

3. **Basic usage**:
   ```python
   from espn_fantasy_api import ESPNLineupManager, LineupSlot
   
   manager = ESPNLineupManager(
       league_id=1955253855,
       year=2025,
       team_id=12,
       espn_s2="your_cookie_here",
       swid="{your-swid-here}"
   )
   
   # Swap two players
   manager.swap_players(
       player1_id=4685415, player1_slot=LineupSlot.BENCH,
       player2_id=4372016, player2_slot=LineupSlot.FLEX
   )
   ```

4. **Run the example**:
   ```bash
   python example.py
   ```

## Key Features

- ✅ **Swap Players**: Exchange positions between two players
- ✅ **Bench Players**: Move players to/from bench
- ✅ **Multiple Moves**: Execute multiple changes in one transaction
- ✅ **Error Handling**: Proper error messages and validation
- ✅ **Type Safety**: Enum-based slot IDs and dataclasses

## Reverse Engineering Success

This implementation works because we:

1. **Captured real browser requests** using HAR files
2. **Identified critical headers** (`X-Fantasy-Source`, `X-Fantasy-Platform`)
3. **Found the correct endpoint** with `/apis/` path
4. **Matched exact payload format** ESPN expects
5. **Used proper authentication** with decoded cookies

The 403 errors from our first attempts were solved by using the exact same format as ESPN's website!
