#!/usr/bin/python

import sys
from combat.battle import Battle


fight = Battle()
fight.engage(sys.argv[1], sys.argv[2], sys.argv[3])
