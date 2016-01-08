batoru-royale
=============

[![Build Status](https://travis-ci.org/Ishino/batoru-royale.svg?branch=master)](https://travis-ci.org/Ishino/batoru-royale)
[![Gitter](https://badges.gitter.im/Ishino/batoru-royale.svg)](https://gitter.im/Ishino/batoru-royale)

Heroku URL: https://intense-anchorage-9323.herokuapp.com

Code coverage report: http://ishino.github.io/batoru-royale/cover/index.html

Learning Python the fun way.

## prerequisites ##

- Python 3.x


## Kibana ##

You can use Kibana to visualize the charater creation and fight statistics. In the kibana folder are JSON exports
to use in Kibana 4.3

To use all the saved objects add the following indices:

- creation
- fights

To the fights filter, add a scripted field

name: level_difference
script: doc['fighter_level'].value - doc['opponent_level'].value
