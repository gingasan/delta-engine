from engine import *


class Talonflame(PokemonBase):
    _species='Talonflame'
    _types=['Fire','Flying']
    _gender='Female'
    _ability=['Gale Wings']
    _move_1=('Brave Bird',120,100,'Physical','Flying',0,['contact'])
    _move_2=('Flamethrower',90,100,'Special','Fire',0,[])
    def __init__(self):
        super().__init__()

    def get_priority(self,move_id):
        if self['hp']==self['max_hp'] and self._moves[move_id]['type']=='Flying':
            return 1
        return self._moves[move_id]['priority']

    def move_1(self): # Brave Bird
        attack_ret=self.attack()
        if not (attack_ret['miss'] or attack_ret['immune']):
            damage_ret=self.get_damage()
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            self.take_damage(int(0.33*damage),'recoil')

    def move_2(self): # Flamethrower
        attack_ret=self.attack()
        if not (attack_ret['miss'] or attack_ret['immune']):
            damage_ret=self.get_damage()
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            if not self.target.isfaint() and rnd()<10/100:
                self.target.set_status('BRN')

# ----------

@Increment(Talonflame,'_move_3')
def value():
    return ('Will-O-Wisp',0,85,'Status','Fire',0,[])

@Increment(Talonflame)
def move_3(self): # Will-O-Wisp
    attack_ret=self.attack()
    if not (attack_ret['miss'] or attack_ret['immune']):
        self.target.set_status('BRN')

# ----------

@Increment(Talonflame,'_move_4')
def value():
    return ('Roost',0,100000,'Status','Flying',0,[])

@Increment(Talonflame)
def move_4(self): # Roost
    self.restore(self['max_hp']//2,'heal')
