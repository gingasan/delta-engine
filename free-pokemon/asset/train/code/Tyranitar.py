from engine import *


class Tyranitar(PokemonBase):
    _species='Tyranitar'
    _types=['Rock','Dark']
    _gender='Male'
    _ability=['Sand Stream']
    _move_1=('Rock Slide',75,90,'Physical','Rock',0,[])
    _move_2=('Crunch',80,100,'Physical','Dark',0,['contact'])
    def __init__(self):
        super().__init__()

    def onswitch(self):
        self.env.set_weather('Sandstorm',from_=self._species)

    def move_1(self): # Rock Slide
        attack_ret=self.attack()
        if not (attack_ret['miss'] or attack_ret['immune']):
            damage_ret=self.get_damage()
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            if not self.target.isfaint() and rnd()<30/100:
                self.target.set_condition('Flinch',counter=0)
    
    def move_2(self): # Crunch
        attack_ret=self.attack()
        if not (attack_ret['miss'] or attack_ret['immune']):
            damage_ret=self.get_damage()
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            if not self.target.isfaint() and rnd()<20/100: self.target.set_boost('def',-1)
