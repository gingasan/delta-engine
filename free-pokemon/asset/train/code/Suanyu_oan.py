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
        damage_ret=self.get_damage()
        if not damage_ret['miss']:
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            if not self.target.isfaint() and rnd()<0.2:
                self.target.set_boost('spd',-1)

    def move_2(self): # Serpent Dance
        self.set_boost('spe',+2,'self')

# -------------------------------------------------------------

@Increment(Suanyu,'_move_3')
def value():
    return ('Echoing Cry',100,90,'Special','Dragon',0,[])

@Increment(Suanyu)
def move_3(self): # Echoing Cry
    damage_ret=self.get_damage()
    if not damage_ret['miss']:
        damage=damage_ret['damage']
        self.target.take_damage(damage)
        if not self.target.isfaint() and rnd()<0.3:
            self.target.set_condition('CONFUSION',counter=0)

@Increment(Suanyu)
def get_crit(self):
    if self['act']['id']=='Echoing Cry' and self.target['conditions'].get('CONFUSION'):
        return True
    crit_mult=[0,24,8,2,1]
    crit_ratio=self['boosts']['crit']
    crit=False
    if rnd()*crit_mult[crit_ratio+1]<1:
        crit=True
    return crit

# -------------------------------------------------------------

@Increment(Suanyu,'_ability')
def value():
    return ['Terrifying Presence','Mystic Cry']

@Increment(Suanyu)
def _take_damage_attack(self,x):
    if 'type_efc' in self.target['act'] and self.target['act']['type_efc']<0.1:
        self.logger.log('It is immune by %s.'%self._species)
        return
    self.register_act_taken()
    self.state['hp']=max(0,self['hp']-x)
    if rnd()<0.3:
        self.target.set_condition('CONFUSION',counter=0)
    self.log('{} loses {} HP.'.format(self._species,x),act_taken=self['act_taken'])
