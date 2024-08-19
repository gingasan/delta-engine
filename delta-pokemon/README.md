# Delta-Pokemon

Delta-Pokemon is a self-made game developed based on *Delta-Engine*. Players can craft their own pokemons by issuing natural language scripts and battle with others.



Our delta-engine paper: https://arxiv.org/pdf/2408.05842

Our video: https://www.bilibili.com/video/BV1FtYkehEHF



This project is only for research purposes. Any commercial usage is not allowed.



## Overview

Code of our engine is in `engine.py`. It can be split into two modules: role engine (PokemonBase) and battle engine (Battle).

To get SFT data, use `proc.ipynb`.

To see our prompts used in the paper, see `prompt`.



## Data

Our data in `asset` contains two parts: **role script** and **role code**.

* role script: a json file of the pokemon's ability, moves, etc.
* role code: python implementation of the pokemon

Here is example for Aerodactyl.

role script:

```json
{
  "species": "Aerodactyl",
  "types": [
    "Rock",
    "Flying"
  ],
  "gender": "Male",
  "ability": {
    "Tough Claws": "This Pokemon's contact moves have their power multiplied by 1.3.",
    "Rock Head": "This Pokemon does not take recoil damage."
  },
  "moves": {
    "Head Smash": {
      "power": 150,
      "accuracy": 80,
      "category": "Physical",
      "type": "Rock",
      "effect": "If the target lost HP, the user takes recoil damage equal to 1/2 the HP lost by the target.",
      "property": [
        "contact"
      ]
    },
    "Brave Bird": {
      "power": 120,
      "accuracy": 100,
      "category": "Physical",
      "type": "Flying",
      "effect": "If the target lost HP, the user takes recoil damage equal to 33% the HP lost by the target.",
      "property": [
        "contact"
      ]
    },
    "Dragon Claw": {
      "power": 80,
      "accuracy": 100,
      "category": "Physical",
      "type": "Dragon",
      "effect": "No additional effect.",
      "property": [
        "contact"
      ]
    },
    "Dragon Dance": {
      "power": 0,
      "accuracy": 100000,
      "category": "Status",
      "type": "Dragon",
      "effect": "Raises the user's Attack and Speed by 1 stage."
    },
    "Earthquake": {
      "power": 100,
      "accuracy": 100,
      "category": "Physical",
      "type": "Ground",
      "effect": "No additional effect."
    }
  }
}
```

role code:

```python
from engine import *


class Aerodactyl(PokemonBase):
    _species='Aerodactyl'
    _types=['Rock','Flying']
    _gender='Male'
    _ability=['Tough Claws']
    _move_1=('Head Smash',150,80,'Physical','Rock',0,['contact'])
    _move_2=('Dual Wingbeat',40,90,'Physical','Flying',0,['contact'])
    def __init__(self):
        super().__init__()

    def get_power(self):        
        power=self['act']['power']
        if 'contact' in self['act']['property']:
            power*=1.3
        return int(power*self.get_weather_power_mult())

    def move_1(self): # Head Smash
        damage_ret=self.get_damage()
        if not damage_ret['miss']:
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            self.take_damage(damage//2,'recoil')

    def move_2(self): # Brave Bird
        damage_ret=self.get_damage()
        if not damage_ret['miss']:
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            self.take_damage(int(0.33*damage),'recoil')

# -------------------------------------------------------------

@Increment(Aerodactyl,'_move_3')
def value():
    return ('Dragon Claw',80,100,'Physical','Dragon',0,['contact'])

@Increment(Aerodactyl)
def move_3(self): # Dragon Claw
    damage_ret=self.get_damage()
    if not damage_ret['miss']:
        damage=damage_ret['damage']
        self.target.take_damage(damage)

# -------------------------------------------------------------

@Increment(Aerodactyl,'_move_4')
def value():
    return ('Dragon Dance',0,100000,'Status','Dragon',0,[])

@Increment(Aerodactyl)
def move_4(self): # Dragon Dance
    self.set_boost('atk',1,'self')
    self.set_boost('spe',1,'self')

# -------------------------------------------------------------

@Increment(Aerodactyl,'_ability')
def value():
    return ['Tough Claws','Rock Head']

@Increment(Aerodactyl)
def move_1(self): # Head Smash
    damage_ret=self.get_damage()
    if not damage_ret['miss']:
        damage=damage_ret['damage']
        self.target.take_damage(damage)

@Increment(Aerodactyl)
def move_2(self): # Brave Bird
    damage_ret=self.get_damage()
    if not damage_ret['miss']:
        damage=damage_ret['damage']
        self.target.take_damage(damage)

# -------------------------------------------------------------

@Increment(Aerodactyl,'_move_5')
def value():
    return ('Earthquake',100,100,'Physical','Ground',0,[])

@Increment(Aerodactyl)
def move_5(self): # Earthquake
    damage_ret=self.get_damage()
    if not damage_ret['miss']:
        damage=damage_ret['damage']
        self.target.take_damage(damage)
```



## Quick Play

We are working on the real game. Now, we provide a quick play to test the pokemon roles.

First, make a new dir in `assset` named with anything (default `user`). Then, place your role code in `asset/user`.

```bash
python test.py --user [YOUR USER NAME/DIR NAME, e.g. user] --role [YOUR POKEMON, e.g. Graphal] --oppo [OPPONENT POKEMON, e.g. Aerodactyl]
```

Sample output:

```bash
**
V.S.:   Aerodactyl
Type:   Rock & Flying
**
Choose your move from:
{'1': 'Dark Rainbow', '2': 'Shadow Ball', '3': 'Dark Dealings', '4': 'Flash Cannon', '5': 'Dark World'}
3
**
Graphal used Dark Dealings!
Aerodactyl used Head Smash!
Graphal|202/404||atk+2 spa+2 spe+2||DARK_WORLD
Aerodactyl|404/404||||
**
```

