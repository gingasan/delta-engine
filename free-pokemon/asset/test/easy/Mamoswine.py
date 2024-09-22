from engine import *


class Mamoswine(PokemonBase):
    _species='Mamoswine'
    _types=['Ice','Ground']
    _gender='Male'
    _ability=['Snow Cloak']
    _move_1=('Earthquake',100,100,'Physical','Ground',0,[])
    _move_2=('Icicle Crash',85,90,'Physical','Ice',0,[])
    def __init__(self):
        super().__init__()

    def get_evasion(self):
        if self.env.get('Snow'):
            return 0.2
        return 0

    def move_1(self): # Earthquake
        attack_ret=self.attack()
        if not (attack_ret['miss'] or attack_ret['immune']):
            damage_ret=self.get_damage()
            damage=damage_ret['damage']
            self.target.take_damage(damage)
    
    def move_2(self): # Icicle Crash
        attack_ret=self.attack()
        if not (attack_ret['miss'] or attack_ret['immune']):
            damage_ret=self.get_damage()
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            if not self.target.isfaint() and rnd()<30/100:
                self.target.set_condition('Flinch',counter=0)

# ----------

@Increment(Mamoswine,'_move_3')
def value():
    return ('Ice Shard',40,100,'Physical','Ice',1,[])

@Increment(Mamoswine)
def move_3(self): # Ice Shard
    attack_ret=self.attack()
    if not (attack_ret['miss'] or attack_ret['immune']):
        damage_ret=self.get_damage()
        damage=damage_ret['damage']
        self.target.take_damage(damage)
