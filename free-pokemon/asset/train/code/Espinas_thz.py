from engine import *


class Espinas(PokemonBase):
    _species='Espinas'
    _types=['Poison','Fire']
    _gender='Male'
    _ability=['Toxic Shield']
    _move_1=('Thorned Assault',90,100,'Physical','Poison',0,['contact'])
    _move_2=('Horn Charge',120,75,'Physical','Normal',0,['contact'])
    def __init__(self):
        super().__init__()

    def _take_damage_attack(self,x):
        if 'type_effect' in self.target['act'] and self.target['act']['type_effect']<0.1:
            self.logger.log('It is immune by %s.'%self._species)
            return
        self.register_act_taken()
        if self['act_taken']['category']=='Physical':
            x=int(x*0.7)
        self.state['hp']=max(0,self['hp']-x)
        self.log(script='attack',species=self._species,x=x,**self['act_taken'])
        if self['hp']==0:
            return
        if 'contact' in self['act_taken']['property'] and rnd()<20/100:
            self.target.set_condition('PSN')

    def set_status(self,x):
        if self['status'] or self.env.get('Misty Terrain'):
            return
        if x=='BRN':
            if not self.istype('Fire'):
                self.state['status']={x:{'counter':0}}
                self.log('%s is burned.'%self._species)
        elif x=='FRZ':
            if not self.istype('Ice'):
                self.state['status']={x:{'counter':0}}
                self.log('%s is frozen.'%self._species)
        elif x=='SLP':
            if not self.env.get("Electric Terrain"):
                self.state['status']={x:{'counter':0}}
                self.log('%s falls asleep.'%self._species)

    def move_1(self): # Thorned Assault
        damage_ret=self.get_damage()
        if not damage_ret['miss']:
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            if not self.target.isfaint() and rnd()<50/100:
                self.target.set_condition('BRN')

    def move_2(self): # Horn Charge
        damage_ret=self.get_damage()
        if not damage_ret['miss']:
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            if not self.target.isfaint() and rnd()<30/100:
                self.target.set_boost('def',-1)

# ----------

@Increment(Espinas,'_move_3')
def value():
    return ('Flame Rush',80,100,'Physical','Fire',0,['contact'])

@Increment(Espinas)
def move_3(self): # Flame Rush
    damage_ret=self.get_damage()
    if not damage_ret['miss']:
        damage=damage_ret['damage']
        self.target.take_damage(damage)
        if rnd()<50/100:
            self.set_boost('spe',+1,'self')

# ----------

@Increment(Espinas,'_ability')
def value():
    return ['Toxic Shield','Blazing Surge']

@Increment(Espinas)
def move_3(self): # Flame Rush
    damage_ret=self.get_damage()
    if not damage_ret['miss']:
        damage=damage_ret['damage']
        self.target.take_damage(damage)
        if rnd()<50/100:
            self.set_boost('spe',+1,'self')
        if not self.target.isfaint() and rnd()<50/100:
            self.target.set_condition('PAR')
