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
        self.env.set_side_condition('Lunar Aura',self.side_id,from_=self._species,counter=0,max_count=3)

    def move_1(self): # Lunar Slash
        attack_ret=self.attack()
        if not (attack_ret['miss'] or attack_ret['immune']):
            damage_ret=self.get_damage()
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            if not self.target.isfaint():
                if self.env.get_side_condition('Lunar Aura',self.side_id):
                    self.target.set_boost('spe',-1)
                elif rnd()<20/100:
                    self.target.set_boost('spe',-1)

    def move_2(self): # Moonlit Flight
        attack_ret=self.attack()
        if not (attack_ret['miss'] or attack_ret['immune']):
            damage_ret=self.get_damage()
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            if self.env.get_side_condition('Lunar Aura',self.side_id):
                self.set_boost('spe',+1,'self')
            elif rnd()<10/100:
                self.set_boost('spe',+1,'self')

# ----------

@Increment(RedMoon,'_move_3')
def value():
    return ('Zen Headbutt',80,90,'Physical','Psychic',0,['contact'])

@Increment(RedMoon)
def move_3(self): # Zen Headbutt
    attack_ret=self.attack()
    if not (attack_ret['miss'] or attack_ret['immune']):
        damage_ret=self.get_damage()
        damage=damage_ret['damage']
        self.target.take_damage(damage)
        if not self.target.isfaint() and rnd()<20/100:
            self.target.set_condition('Flinch',counter=0)
