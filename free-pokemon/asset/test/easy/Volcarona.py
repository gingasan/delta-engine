from engine import *


class Volcarona(PokemonBase):
    _species='Volcarona'
    _types=['Bug','Fire']
    _gender='Female'
    _ability=['Flame Body']
    _move_1=('Quiver Dance',0,100000,'Status','Bug',0,[])
    _move_2=('Flamethrower',90,100,'Special','Fire',0,[])
    def __init__(self):
        super().__init__()

    def _take_damage_attack(self,x):
        if 'type_effect' in self.target['act'] and self.target['act']['type_effect']<0.1:
            self.logger.log('It is immune by %s.'%self._species)
            return
        self.register_act_taken()
        self.state['hp']=max(0,self['hp']-x)
        self.log(script='attack',species=self._species,x=x,**self['act_taken'])
        if self['hp']==0:
            return
        if self['act_taken'] and 'property' in self['act_taken'] and 'contact' in self['act_taken']['property']:
            if rnd()<0.3:
                self.target.set_status('BRN')

    def move_1(self): # Quiver Dance
        self.set_boost('spa',+1,'self')
        self.set_boost('spd',+1,'self')
        self.set_boost('spe',+1,'self')

    def move_2(self): # Flamethrower
        damage_ret=self.get_damage()
        if not damage_ret['miss']:
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            if not self.target.isfaint() and rnd()<0.1:
                self.target.set_status('BRN')

# ----------

@Increment(Volcarona,'_move_3')
def value():
    return ('Morning Sun',0,100000,'Status','Normal',0,[])

@Increment(Volcarona)
def move_3(self): # Morning Sun
    if not any([self.env.get(x) for x in ['Sunlight','Rain','Sandstorm','Snow']]):
        self.restore(self['max_hp']//2,'heal')
    elif self.env.get('Sunlight'):
        self.restore(self['max_hp']//3*2,'heal')
    else:
        self.restore(self['max_hp']//4,'heal')

# ----------

@Increment(Volcarona,'_move_4')
def value():
    return ('Will-O-Wisp',0,85,'Status','Fire',0,[])

@Increment(Volcarona)
def move_4(self): # Will-O-Wisp
    damage_ret=self.get_damage()
    if not damage_ret['miss']:
        self.target.set_status('BRN')
