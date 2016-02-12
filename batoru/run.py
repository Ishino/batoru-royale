#!/usr/bin/python

import sys
from simulator.battle import Battle


fight = Battle()
fight.simulate(sys.argv[1], sys.argv[2], sys.argv[3])
