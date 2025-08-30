# ESPN Fantasy Football API - Reverse Engineered

A Python library for programmatically managing ESPN Fantasy Football lineups using reverse-engineered write APIs.

## 🚨 Important Disclaimers

- **Unofficial & Unsupported**: These APIs are not officially documented by ESPN and may break without notice
- **Terms of Service**: Usage may violate ESPN's ToS - use at your own risk
- **Educational Purpose**: This project is primarily for learning reverse engineering techniques
- **No Guarantees**: ESPN can change or disable these endpoints at any time

## 🔍 Reverse Engineering Process

This library was created by analyzing real browser network requests (HAR files) to understand ESPN's internal API structure.

### Key Discoveries

1. **Correct Endpoint Structure**:
   ```
   https://lm-api-writes.fantasy.espn.com/apis/v3/games/ffl/seasons/{year}/segments/0/leagues/{league_id}/transactions/
   ```

2. **Critical Headers** (discovered through HAR analysis):
   ```
   X-Fantasy-Source: kona
   X-Fantasy-Platform: kona-PROD-ee817b5eea5e3f12efb5185ee8c626ec21f7c3d8
   ```

3. **Authentication**: Uses `espn_s2` and `SWID` cookies from authenticated browser sessions

4. **Payload Format**: Uses `"type": "ROSTER"` with `"items"` array containing `"type": "LINEUP"` moves

5. **Slot IDs**: Integer-based lineup positions:
   - `0` = QB
   - `2` = RB  
   - `4` = WR
   - `6` = TE
   - `16` = D/ST
   - `17` = K
   - `20` = BENCH
   - `21` = IR
   - `23` = FLEX

## 🛠️ Technical Implementation

### Core Components

- **`ESPNLineupManager`**: Main class handling API communication
- **`LineupMove`**: Data class representing individual player moves
- **`LineupSlot`**: Enum for lineup position constants

### Authentication Requirements

You need two cookies from an authenticated ESPN session:

1. **`espn_s2`**: ESPN authentication token
2. **`SWID`**: ESPN user identifier

#### Getting Your Cookies

1. Log into ESPN Fantasy Football in your browser
2. Open Developer Tools (F12) 
3. Go to Application/Storage → Cookies → espn.com
4. Copy the values for `espn_s2` and `SWID`

**Note**: The `espn_s2` cookie may be URL-encoded and need to be decoded.

## 📚 Usage Examples

### Basic Setup

```python
from espn_lineup_manager import ESPNLineupManager, LineupMove, LineupSlot

# Initialize the manager
manager = ESPNLineupManager(
    league_id=1955253855,
    year=2025,
    team_id=12,
    espn_s2="your_espn_s2_cookie_here",
    swid="{your-swid-here}"
)
```

### Making Lineup Changes

```python
# Swap two players
manager.swap_players(
    player1_id=4685415, player1_slot=LineupSlot.BENCH,
    player2_id=4372016, player2_slot=LineupSlot.FLEX
)

# Move player to bench
manager.move_player_to_bench(
    player_id=4685415, 
    current_slot=LineupSlot.WR
)

# Move player from bench to starting position
manager.move_player_from_bench(
    player_id=4685415,
    target_slot=LineupSlot.FLEX
)

# Multiple moves in one transaction
moves = [
    LineupMove(4685415, LineupSlot.BENCH, LineupSlot.WR),
    LineupMove(4372016, LineupSlot.FLEX, LineupSlot.BENCH)
]
manager.make_lineup_changes(moves)
```

## 🔧 API Reverse Engineering Notes

### HAR Analysis Process

1. **Captured Real Request**: Used browser dev tools to capture lineup change
2. **Analyzed Headers**: Identified required `X-Fantasy-*` headers  
3. **Studied Payload**: Discovered exact JSON structure ESPN expects
4. **Cookie Analysis**: Found authentication requirements
5. **Endpoint Discovery**: Located correct write API URL with `/apis/` path

### Failed Attempts & Lessons Learned

- **403 Forbidden Errors**: Missing critical headers and wrong endpoint paths
- **Wrong Base URLs**: Tried `lm-api-writes` without `/apis/` path
- **Header Requirements**: Standard browser headers aren't sufficient
- **Payload Structure**: ESPN expects specific nested JSON format

### Success Factors

- **Exact Header Matching**: Using identical headers from working browser request
- **Proper Authentication**: Correctly formatted cookies from active session
- **Precise Payload Format**: Matching ESPN's expected JSON structure exactly
- **Correct HTTP Method**: POST to transactions endpoint (not PUT to roster)

## 🚀 Getting Started

1. **Install Dependencies**:
   ```bash
   pip install requests
   ```

2. **Get Your Credentials**:
   - League ID (from your ESPN fantasy URL)
   - Team ID (your team number in the league)  
   - ESPN cookies (`espn_s2` and `SWID`)

3. **Run the Example**:
   ```bash
   python espn_lineup_manager.py
   ```

## ⚠️ Error Handling

The library handles common error scenarios:

- **401 Unauthorized**: Invalid or expired cookies
- **403 Forbidden**: Insufficient permissions
- **422 Unprocessable Entity**: Invalid request data
- **Network Errors**: Connection timeouts and failures

## 🔄 Future Enhancements

Potential areas for expansion:

- **Roster Management**: Add/drop players, waiver claims
- **Trade Proposals**: Programmatic trade offers
- **League Settings**: Modify league configuration (if permissions allow)
- **Multi-Team Support**: Manage multiple teams/leagues
- **Schedule Integration**: Automated lineup optimization

## 🤝 Contributing

This is a learning project focused on reverse engineering techniques. Contributions welcome for:

- Additional API endpoint discovery
- Error handling improvements  
- Code organization and structure
- Documentation enhancements

## 📄 License

This project is for educational purposes. Use responsibly and in accordance with ESPN's terms of service.

---

**Created by**: Brian Matzelle  
**Date**: August 30, 2025  
**Method**: Browser HAR analysis and API reverse engineering
