from engine import *


class Suanyu(PokemonBase):
    _species='Suanyu'
    _types=['Dragon','Flying']
    _gender='Neutral'
    _ability=['Terrifying Presence']
    _move_1=('Jade Shard',90,100,'Special','Dragon',0,[])
    _move_2=('Serpent Dance',0,100000,'Status','Flying',0,[])
    def __init__(self):
        super().__init__()

    def onswitch(self):
        self.target.set_boost('atk',-1)

    def move_1(self): # Jade Shard
        attack_ret=self.attack()
        if not (attack_ret['miss'] or attack_ret['immune']):
            damage_ret=self.get_damage()
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            if not self.target.isfaint() and rnd()<0.2:
                self.target.set_boost('spd',-1)

    def move_2(self): # Serpent Dance
        self.set_boost('spe',+2,'self')

# ----------

@Increment(Suanyu,'_move_3')
def value():
    return ('Echoing Cry',100,90,'Special','Dragon',0,[])

@Increment(Suanyu)
def move_3(self): # Echoing Cry
    attack_ret=self.attack()
    if not (attack_ret['miss'] or attack_ret['immune']):
        damage_ret=self.get_damage()
        damage=damage_ret['damage']
        self.target.take_damage(damage)
        if not self.target.isfaint() and rnd()<0.3:
            self.target.set_condition('Confusion',counter=0)

@Increment(Suanyu)
def get_crit(self):
    if self['act']['id']=='Echoing Cry' and self.target['conditions'].get('Confusion'):
        return True
    crit_mult=[0,24,8,2,1]
    crit_ratio=self['boosts']['crit']
    crit=False
    if rnd()*crit_mult[crit_ratio+1]<1:
        crit=True
    return crit

# ----------

@Increment(Suanyu,'_ability')
def value():
    return ['Terrifying Presence','Mystic Cry']

@Increment(Suanyu)
def take_damage_attack(self,x):
    self.register_act_taken()
    self._set_hp(-x)
    if self['hp']==0:
        return
    if rnd()<0.3:
        self.target.set_condition('Confusion',counter=0)
