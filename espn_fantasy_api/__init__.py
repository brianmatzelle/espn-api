"""
ESPN Fantasy Football API - Reverse Engineered

A Python library for programmatically managing ESPN Fantasy Football lineups
using reverse-engineered write APIs discovered through browser HAR analysis.

Author: Brian Matzelle
Created: 2025-08-30

⚠️  DISCLAIMER: This library uses unofficial ESPN APIs that may break without notice.
    Use at your own risk and in accordance with ESPN's terms of service.
"""

from .espn_lineup_manager import (
    ESPNLineupManager,
    LineupMove,
    LineupSlot
)

__version__ = "0.1.0"
__author__ = "Brian Matzelle"

__all__ = [
    "ESPNLineupManager",
    "LineupMove", 
    "LineupSlot"
]

# Quick reference for lineup slots
LINEUP_SLOTS = {
    "QB": 0,
    "RB": 2,
    "WR": 4,
    "TE": 6,
    "D/ST": 16,
    "K": 17,
    "BENCH": 20,
    "IR": 21,
    "FLEX": 23
}
