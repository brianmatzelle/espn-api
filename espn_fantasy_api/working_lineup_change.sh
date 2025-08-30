#!/bin/bash
# ESPN Fantasy Football Lineup Change - WORKING VERSION
# Based on real HAR capture from browser

# Your credentials
LEAGUE_ID="1955253855"
YEAR="2025" 
TEAM_ID="12"
ESPN_S2="AEAtP8bWFwzl3v6tye0ICdqdzT1gXJbC28j7dgl4bjP6KGYJ/QRT3n1Vu+jVxIvgwnOhY2nFs4uGWt5QeP4ZoaaL7FeKLzuyVXZvbtHBSVUmKq0w1lB7UQ6qc09vxrlqxeolhZYTHyNpc2YUbP1VdOVNI1tjIfkmXt8fPVYg2NHjP8Cn32WMbB1f73sljFj4hwANVOJ0cXbn2u0HhB5kCqSURIRVfNDGqfttCA2egQYe9CzBgrJu33cVY83pLyhgNhVA6Ai4Hs0JeclDxSPwIJhkVkOAnrLexx7luQXhY6ApXkdV5QFrhXW2kR/xs/gsgmLe+d3NILQh3tPf0CcXxipk"
SWID="{88C298DE-BEE1-401E-9D60-F92268A73179}"

echo "🚀 ESPN Fantasy Lineup Change - Using Real Browser Format"
echo "=========================================================="

# Example 1: Move Travis Hunter from BENCH (20) to FLEX (23)
# and move Jaylen Waddle from FLEX (23) to BENCH (20)
echo -e "\n📋 Moving Travis Hunter to starting lineup (BENCH → FLEX)"
curl -X POST "https://lm-api-writes.fantasy.espn.com/apis/v3/games/ffl/seasons/${YEAR}/segments/0/leagues/${LEAGUE_ID}/transactions/" \
  -H "Host: lm-api-writes.fantasy.espn.com" \
  -H "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:142.0) Gecko/20100101 Firefox/142.0" \
  -H "Accept: application/json" \
  -H "Accept-Language: en-US,en;q=0.5" \
  -H "Accept-Encoding: gzip, deflate, br, zstd" \
  -H "Content-Type: application/json" \
  -H "X-Fantasy-Source: kona" \
  -H "X-Fantasy-Platform: kona-PROD-ee817b5eea5e3f12efb5185ee8c626ec21f7c3d8" \
  -H "Origin: https://fantasy.espn.com" \
  -H "Connection: keep-alive" \
  -H "Referer: https://fantasy.espn.com/" \
  -H "Cookie: SWID=${SWID}; espn_s2=${ESPN_S2}" \
  -H "Sec-Fetch-Dest: empty" \
  -H "Sec-Fetch-Mode: cors" \
  -H "Sec-Fetch-Site: same-site" \
  -d '{
    "isLeagueManager": false,
    "teamId": 12,
    "type": "ROSTER",
    "memberId": "{88C298DE-BEE1-401E-9D60-F92268A73179}",
    "scoringPeriodId": 1,
    "executionType": "EXECUTE",
    "items": [
      {
        "playerId": 4685415,
        "type": "LINEUP",
        "fromLineupSlotId": 20,
        "toLineupSlotId": 23
      },
      {
        "playerId": 4372016,
        "type": "LINEUP", 
        "fromLineupSlotId": 23,
        "toLineupSlotId": 20
      }
    ]
  }'

echo -e "\n\n📋 SLOT ID REFERENCE:"
echo "0=QB, 2=RB, 4=WR, 6=TE, 16=D/ST, 17=K, 20=BENCH, 21=IR, 23=FLEX"

echo -e "\n💡 PLAYER ID REFERENCE (from your roster):"
echo "4262921 = Justin Jefferson (WR)"
echo "4361307 = Trey McBride (TE)" 
echo "4426348 = Jayden Daniels (QB)"
echo "4241416 = Chuba Hubbard (RB)"
echo "4429615 = Zay Flowers (WR)"
echo "4372016 = Jaylen Waddle (WR) - currently in FLEX"
echo "4360516 = Tyrone Tracy Jr. (RB)"
echo "4685415 = Travis Hunter (WR) - currently on BENCH"
echo "4361579 = Javonte Williams (RB)"
echo "4362887 = Justin Fields (QB)"
echo "4723086 = Colston Loveland (TE)"
echo "4569587 = Wan'Dale Robinson (WR)"
echo "3046779 = Jared Goff (QB)"
echo "4695883 = Jalen Coker (WR)"
echo "-16034 = Texans D/ST"
echo "4249087 = Matt Gay (K)"

echo -e "\n🎯 EXAMPLE: Move Justin Fields from BENCH to QB (benching Jayden Daniels)"
echo "Uncomment and modify the curl below:"

curl -X POST "https://lm-api-writes.fantasy.espn.com/apis/v3/games/ffl/seasons/2025/segments/0/leagues/1955253855/transactions/" \
  -H "Content-Type: application/json" \
  -H "X-Fantasy-Source: kona" \
  -H "X-Fantasy-Platform: kona-PROD-ee817b5eea5e3f12efb5185ee8c626ec21f7c3d8" \
  -H "Cookie: SWID={88C298DE-BEE1-401E-9D60-F92268A73179}; espn_s2=AEAtP8bWFwzl3v6tye0ICdqdzT1gXJbC28j7dgl4bjP6KGYJ/QRT3n1Vu+jVxIvgwnOhY2nFs4uGWt5QeP4ZoaaL7FeKLzuyVXZvbtHBSVUmKq0w1lB7UQ6qc09vxrlqxeolhZYTHyNpc2YUbP1VdOVNI1tjIfkmXt8fPVYg2NHjP8Cn32WMbB1f73sljFj4hwANVOJ0cXbn2u0HhB5kCqSURIRVfNDGqfttCA2egQYe9CzBgrJu33cVY83pLyhgNhVA6Ai4Hs0JeclDxSPwIJhkVkOAnrLexx7luQXhY6ApXkdV5QFrhXW2kR/xs/gsgmLe+d3NILQh3tPf0CcXxipk" \
  -H "Referer: https://fantasy.espn.com/" \
  -H "Origin: https://fantasy.espn.com" \
  -d '{
    "isLeagueManager": false,
    "teamId": 12,
    "type": "ROSTER",
    "memberId": "{88C298DE-BEE1-401E-9D60-F92268A73179}",
    "scoringPeriodId": 1,
    "executionType": "EXECUTE",
    "items": [
      {
        "playerId": 4362887,
        "type": "LINEUP",
        "fromLineupSlotId": 20,
        "toLineupSlotId": 0
      },
      {
        "playerId": 4426348,
        "type": "LINEUP",
        "fromLineupSlotId": 0,
        "toLineupSlotId": 20
      }
    ]
  }'


echo -e "\n✅ This script uses the EXACT format ESPN's website uses!"
echo "The first command should work to move Travis Hunter to your starting lineup."
