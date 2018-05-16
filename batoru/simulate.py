#!/usr/bin/python

import sys
from simulator.battle import Battle


fight = Battle()
fight.tournament_rounds = int(sys.argv[3])
fight.simulate(sys.argv[1], sys.argv[2])
