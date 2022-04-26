Gentle Garden

As an interactive gardening game, this game is meant to simulate growing and 
tending for plants with different terrains, from planting seeds all the way to 
harvesting fruits and vegetables. The changing weather and the user’s ability 
to properly water the plants influences each plant’s growth. As there are more 
plants planted, leveling up grants the user more space to grow more plants.

TO PLAY:
Run Python file main.py, and make sure that the other files 
(cmu_112_graphics,plant,pathfinding,etc.) are also placed in the same folder.
Pygame will have to be downloaded to play background music.

KEY COMMANDS:
To end the day early and show the quickest path home, press 'h'.

To plant a seed, select the seed from the planting window and press enter to
start planting.

When performing any action to a plant (watering, harvesting, removing, etc),
always click on the lower middle cell of the planting box.

HOW TO PLAY:
Users are given the option to load a new game with a blank/new terrain, or
load a saved game if they wish to. Every new terrain is generated randomly.

There are 3 types of terrains: the green terrain is grass, dark brown terrain is to 
plant trees, and the lighter brown is to plant other smaller plants

Plants must be a certain distance apart from each other and the edges of the terrain.
The daily temperature and the plant's water level affects its growth. The plant
goes through multiple stages: sprout, small growth, medium growth, mature growth,
flowering, unripe fruiting, and fruiting. When the fruits are ripe the user can
harvest them and store them in their inventory. Plants can also be removed.

The plant will still grow (albeit slowly) when it is overwatered/dry, or when
the temperature is too hot or too cold. The plant's water state is shown in its
soil color. 

All actions to the plant must be done on the lowest center cell of the plant's
planting box.

The day will end naturally, but if the user wishes to end it early, they may press 'h'
and the most energy efficient path to return home will be highlighted and the 
day will end. Terrains are ordered from most tedious to easiest to travel across.

With every 5 additional plants, the terrain levels up and expands with more land
to grow plants on. 