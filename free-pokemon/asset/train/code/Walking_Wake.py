from engine import *


class Walking_Wake(PokemonBase):
    _species='Walking Wake'
    _types=['Dragon','Water']
    _gender='Male'
    _ability=['Protosynthesis']
    _move_1=('Hydro Steam',80,100,'Special','Water',0,[])
    _move_2=('Draco Meteor',130,90,'Special','Dragon',0,[])
    def __init__(self):
        super().__init__()

    def onswitch(self):
        if self.get_env('Sunlight'):
            t=max([(k,v) for k,v in self['stats'].items()],key=lambda x:x[1])[0]
            self.set_stat(t,1.5 if t=='spe' else 1.3)

    def get_weather_power_mult(self):
        if self.get_env('Sunlight'):
            if self['act']['id']=='Hydro Steam':
                return 1.5
            if self['act']['type'] in ['Fire','Water']:
                return {'Fire':1.5,'Water':0.5}[self['act']['type']]
        if self.get_env('Rain'):
            if self['act']['type'] in ['Fire','Water']:
                return {'Fire':0.5,'Water':1.5}[self['act']['type']]
        if self.get_env('Electric Terrain'):
            if self['act']['type']=='Electric':
                return 1.3
        if self.get_env('Grassy Terrain'):
            if self['act']['type']=='Grass':
                return 1.3
        if self.get_env('Psychic Terrain'):
            if self['act']['type']=='Psychic':
                return 1.3
        if self.get_env('Misty Terrain'):
            if self['act']['type']=='Dragon':
                return 0.5
        return 1.

    def move_1(self): # Hydro Steam
        damage_ret=self.get_damage()
        if not damage_ret['miss']:
            damage=damage_ret['damage']
            self.target.take_damage(damage)

    def move_2(self): # Draco Meteor
        damage_ret=self.get_damage()
        if not damage_ret['miss']:
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            self.set_boost('spa',-2,'self')

# ----------

@Increment(Walking_Wake,'_move_3')
def value():
    return ('Flamethrower',90,100,'Special','Fire',0,[])

@Increment(Walking_Wake)
def move_3(self): # Flamethrower
    damage_ret=self.get_damage()
    if not damage_ret['miss']:
        damage=damage_ret['damage']
        self.target.take_damage(damage)
        if not self.target.isfaint() and rnd()<10/100:
            self.target.set_status('BRN')

# ----------

@Increment(Walking_Wake,'_move_4')
def value():
    return ('Substitute',0,100000,'Status','Normal',0,[])

@Increment(Walking_Wake)
def move_4(self): # Substitute
    if self['hp']>self['max_hp']//4 and not self['conditions'].get('SUBSTITUTE'):
        self.take_damage(self['max_hp']//4,'loss')
        self.set_condition('SUBSTITUTE',hp=self['max_hp']//4)

@Increment(Walking_Wake)
def _take_damage_attack(self,x):
    if 'type_efc' in self.target['act'] and self.target['act']['type_efc']<0.1:
        self.logger.log('It is immune by %s.'%self._species)
        return
    self.register_act_taken()
    if self['conditions'].get('SUBSTITUTE'):
        self['conditions']['SUBSTITUTE']['hp']-=x
        if self['conditions']['SUBSTITUTE']['hp']<1:
            del self['conditions']['SUBSTITUTE']
    else:
        self.state['hp']=max(0,self['hp']-x)
        self.log(script='attack',species=self._species,x=x,**self['act_taken'])
