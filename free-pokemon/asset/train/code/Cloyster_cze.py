from engine import *


class Cloyster(PokemonBase):
    _species='Cloyster'
    _types=['Water','Ice']
    _gender='Female'
    _ability=['Skill Link']
    _move_1=('Rock Blast',25,90,'Physical','Rock',0,[])
    _move_2=('Icicle Spear',25,100,'Physical','Ice',0,[])
    def __init__(self):
        super().__init__()

    def move_1(self): # Rock Blast
        hit=True; i=0
        while hit and i<5:
            attack_ret=self.attack()
            if attack_ret['miss'] or attack_ret['immune']: break
            damage_ret=self.get_damage()
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            i+=1; hit=False if self.target.isfaint() else True

    def move_2(self): # Icicle Spear
        hit=True; i=0
        while hit and i<5:
            attack_ret=self.attack()
            if attack_ret['miss'] or attack_ret['immune']: break
            damage_ret=self.get_damage()
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            i+=1; hit=False if self.target.isfaint() else True

# ----------

@Increment(Cloyster,'_move_3')
def value():
    return ('Ice Spinner',80,100,'Physical','Ice',0,['contact'])

@Increment(Cloyster)
def move_3(self): # Ice Spinner
    attack_ret=self.attack()
    if not (attack_ret['miss'] or attack_ret['immune']):
        damage_ret=self.get_damage()
        damage=damage_ret['damage']
        self.target.take_damage(damage)
        for t in ['Psychic Terrain','Electric Terrain','Grassy Terrain','Misty Terrain']:
            if self.env.get(t):
                self.env.clr_terrain()
