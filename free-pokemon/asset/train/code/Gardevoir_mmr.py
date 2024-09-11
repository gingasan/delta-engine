from engine import *


class Gardevoir(PokemonBase):
    _species='Gardevoir'
    _types=['Psychic','Fairy']
    _gender='Female'
    _ability=['Synchronize']
    _move_1=('Psychic',90,100,'Special','Psychic',0,[])
    _move_2=('Moon Blast',95,100,'Special','Fairy',0,[])
    def __init__(self):
        super().__init__()

    def set_status(self,x):
        if self['status'] or self.get_env('Misty Terrain'):
            return
        if x=='BRN':
            if not self.istype('Fire'):
                self.state['status']={x:{'counter':0}}
                self.log('%s is burned.'%self._species)
                self.target.set_status(x)
        elif x=='PAR':
            if not self.istype('Electric'):
                self.state['status']={x:{'counter':0}}
                self.log('%s is paralyzed.'%self._species)
                self.target.set_status(x)
        elif x=='PSN':
            if not self.istype('Poison') and not self.istype('Steel'):
                self.state['status']={x:{'counter':0}}
                self.log('%s is poisoned.'%self._species)
                self.target.set_status(x)
        elif x=='TOX':
            if not self.istype('Poison') and not self.istype('Steel'):
                self.state['status']={x:{'counter':0}}
                self.log('%s is badly poisoned.'%self._species)
                self.target.set_status(x)
        elif x=='FRZ':
            if not self.istype('Ice'):
                self.state['status']={x:{'counter':0}}
                self.log('%s is frozen.'%self._species)
                self.target.set_status(x)
        elif x=='SLP':
            if not self.env.get("Electric Terrain"):
                self.state['status']={x:{'counter':0}}
                self.log('%s falls asleep.'%self._species)
                self.target.set_status(x)

    def move_1(self): # Psychic
        damage_ret=self.get_damage()
        if not damage_ret['miss']:
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            if not self.target.isfaint() and rnd()<10/100: self.target.set_boost('spd',-1)

    def move_2(self): # Moon Blast
        damage_ret=self.get_damage()
        if not damage_ret['miss']:
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            if not self.target.isfaint() and rnd()<30/100: self.target.set_boost('spa',-1)

# -------------------------------------------------------------

@Increment(Gardevoir,'_move_3')
def value():
    return ('Thunderbolt',90,100,'Special','Electric',0,[])

@Increment(Gardevoir)
def move_3(self): # Thunderbolt
    damage_ret=self.get_damage()
    if not damage_ret['miss']:
        damage=damage_ret['damage']
        self.target.take_damage(damage)
        if not self.target.isfaint() and rnd()<10/100: self.target.set_status('PAR')

# -------------------------------------------------------------

@Increment(Gardevoir,'_move_4')
def value():
    return ('Shadow Ball',80,100,'Special','Ghost',0,[])

@Increment(Gardevoir)
def move_4(self): # Shadow Ball
    damage_ret=self.get_damage()
    if not damage_ret['miss']:
        damage=damage_ret['damage']
        self.target.take_damage(damage)
        if not self.target.isfaint() and rnd()<20/100: self.target.set_boost('spd',-1)

# -------------------------------------------------------------

@Increment(Gardevoir,'_ability')
def value():
    return ['Synchronize','Mind Shield']

@Increment(Gardevoir)
def _take_damage_attack(self,x):
    if 'type_efc' in self.target['act'] and self.target['act']['type_efc']<0.1:
        self.logger.log('It is immune by %s.'%self._species)
        return
    self.register_act_taken()
    if self['act_taken']['category']=='Special':
        x//=2
    self.state['hp']=max(0,self['hp']-x)
    self.log('{} loses {} HP.'.format(self._species,x),act_taken=self['act_taken'])

# -------------------------------------------------------------

@Increment(Gardevoir,'_move_5')
def value():
    return ('Ethereal Shield',0,100000,'Status','Psychic',0,[])

@Increment(Gardevoir)
def move_5(self): # Ethereal Shield
    self.set_boost('spd',+2)
