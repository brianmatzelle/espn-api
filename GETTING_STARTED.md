# Getting Started with ESPN Fantasy Football API

This directory contains simple scripts to help you get started with the ESPN Fantasy Football API.

## Quick Start

1. **For a minimal test**: Use `quick_test.py`
   ```bash
   python quick_test.py
   ```

2. **For comprehensive examples**: Use `intro_test.py`
   ```bash
   python intro_test.py
   ```

## Configuration

### Public Leagues
Simply update the `LEAGUE_ID` and `YEAR` in the scripts:
```python
LEAGUE_ID = 222     # Your ESPN league ID
YEAR = 2023         # Your desired year
```

### Private Leagues
For private leagues, you'll need authentication cookies:

1. **Get your cookies**:
   - Log into ESPN Fantasy Football in your browser
   - Open Developer Tools (F12)
   - Go to Application/Storage > Cookies > espn.com
   - Copy the values for `espn_s2` and `SWID`

2. **Update the script**:
   ```python
   league = League(
       league_id=LEAGUE_ID,
       year=YEAR,
       espn_s2="your_espn_s2_value",
       swid="your_swid_value"
   )
   ```

## What These Scripts Do

### `quick_test.py`
- Minimal connection test
- Shows basic league info
- Lists first few teams
- Perfect for verifying your setup

### `intro_test.py`
- Comprehensive demonstration
- Tests both public and private league connections
- Shows various API features:
  - League settings
  - Team standings
  - Top/bottom scorers
  - Current week matchups
- Includes detailed error handling and troubleshooting

## Next Steps

Once you have a working connection:

1. **Explore the API**: Check out the [official wiki](https://github.com/cwendt94/espn-api/wiki)
2. **Try more features**:
   - `league.box_scores()` - Detailed matchup data
   - `league.free_agents()` - Available players
   - `league.power_rankings()` - Power rankings
   - `league.recent_activity()` - League transactions
3. **Build your own tools**: Use these scripts as a foundation for your fantasy football projects

## Troubleshooting

- **"Connection failed"**: Check your league ID and year
- **"Private league access denied"**: Verify your espn_s2 and SWID cookies
- **"No data found"**: The league might not have started yet for that year
- **Import errors**: Make sure you've installed the package (`pip install espn_api`)

## Example League IDs

The scripts use league ID `222` as a default (ESPN's public example league). Replace this with your own league ID, which you can find in your ESPN Fantasy Football URL.
