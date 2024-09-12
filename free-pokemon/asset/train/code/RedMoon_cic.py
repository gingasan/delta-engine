from engine import *


class RedMoon(PokemonBase):
    _species='Red-Moon'
    _types=['Dragon','Flying']
    _gender='Male'
    _ability=['Lunar Aura']
    _move_1=('Lunar Slash',85,100,'Physical','Dragon',0,['contact'])
    _move_2=('Lunar Flight',90,100,'Physical','Flying',0,[])
    def __init__(self):
        super().__init__()

    def onswitch(self):
        self.set_env('Lunar Aura',side='self',counter=0,max_count=3)

    def move_1(self): # Lunar Slash
        damage_ret=self.get_damage()
        if not damage_ret['miss']:
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            if not self.target.isfaint():
                if self.get_env('Lunar Aura',side='self'):
                    self.target.set_boost('spe',-1)
                elif rnd()<20/100:
                    self.target.set_boost('spe',-1)

    def move_2(self): # Moonlit Flight
        damage_ret=self.get_damage()
        if not damage_ret['miss']:
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            if self.get_env('Lunar Aura',side='self'):
                self.set_boost('spe',+1,'self')
            elif rnd()<10/100:
                self.set_boost('spe',+1,'self')

# ----------

@Increment(RedMoon,'_move_3')
def value():
    return ('Zen Headbutt',80,90,'Physical','Psychic',0,['contact'])

@Increment(RedMoon)
def move_3(self): # Zen Headbutt
    damage_ret=self.get_damage()
    if not damage_ret['miss']:
        damage=damage_ret['damage']
        self.target.take_damage(damage)
        if not self.target.isfaint() and rnd()<20/100:
            self.target.set_condition('FLINCH',counter=0)
