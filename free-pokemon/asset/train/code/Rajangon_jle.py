from engine import *


class Rajangon(PokemonBase):
    _species='Rajangon'
    _types=['Electric','Fighting']
    _gender='Male'
    _ability=['Rage Mode']
    _move_1=('Thunder Beam',120,70,'Special','Electric',0,[])
    _move_2=('Rampage',80,100,'Physical','Fighting',0,[])
    def __init__(self):
        super().__init__()

    def get_stat(self,key,boost=None):
        stat=self['stats'][key]
        boost=self['boosts'][key] if not boost else boost
        stat_ratio={0:1,1:1.5,2:2,3:2.5,4:3,5:3.5,6:4}[min(6,abs(boost))]
        if boost<0:
            stat_ratio=1/stat_ratio
        stat_ratio*=self.get_weather_stat_mult(key)
        if key=='spe' and self.isstatus('PAR'):
            stat_ratio*=0.5
        if key in ['atk','spe'] and self['hp']<self['max_hp']//2:
            stat_ratio*=1.5
        if key in ['def','spd'] and self['hp']<self['max_hp']//2:
            stat_ratio*=0.75
        return int(stat*stat_ratio)

    def move_1(self): # Thunder Beam
        damage_ret=self.get_damage()
        if not damage_ret['miss']:
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            if not self.target.isfaint() and rnd()<30/100:
                self.target.set_status('PAR')

    def move_2(self): # Rampage
        damage_ret=self.get_damage()
        if not damage_ret['miss']:
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            self.set_boost('atk',+1,'self')

# ----------

@Increment(Rajangon,'_move_3')
def value():
    return ('Deflect',0,100000,'Status','Fighting',4,[])

@Increment(Rajangon)
def move_3(self): # Deflect
    if self['last_act'] and self['last_act']['id']=='Deflect':
        return
    self.set_condition('Protected',counter=0)

@Increment(Rajangon)
def _take_damage_attack(self,x):
    if 'type_efc' in self.target['act'] and self.target['act']['type_efc']<0.1:
        self.logger.log('It is immune by %s.'%self._species)
        return
    if self['conditions'].get('Protected'):
        del self['conditions']['Protected']
        self.set_boost('atk',+1,'self')
        return
    self.register_act_taken()
    self.state['hp']=max(0,self['hp']-x)
    self.log(script='attack',species=self._species,x=x,**self['act_taken'])

@Increment(Rajangon)
def endturn(self):
    if self['conditions'].get('Protected'):
        del self['conditions']['Protected']

# ----------

@Increment(Rajangon,'_move_4')
def value():
    return ('Blazing Fists',90,100,'Physical','Fire',0,[])

@Increment(Rajangon)
def move_4(self): # Blazing Fists
    damage_ret=self.get_damage()
    if not damage_ret['miss']:
        damage=damage_ret['damage']
        self.target.take_damage(damage)
        if not self.target.isfaint() and rnd()<20/100:
            self.target.set_status('BRN')

# ----------

@Increment(Rajangon,'_ability')
def value():
    return ['Rage Mode','Deflecting Arms']

@Increment(Rajangon)
def _take_damage_attack(self,x):
    if 'type_efc' in self.target['act'] and self.target['act']['type_efc']<0.1:
        self.logger.log('It is immune by %s.'%self._species)
        return
    if self['conditions'].get('Protected'):
        del self['conditions']['Protected']
        self.set_boost('atk',+1,'self')
        return
    self.register_act_taken()
    if self['act_taken']['category']=='Physical' and rnd()<0.3:
        x//=2
    self.state['hp']=max(0,self['hp']-x)
    self.log(script='attack',species=self._species,x=x,**self['act_taken'])

# ----------

@Increment(Rajangon,'_move_5')
def value():
    return ('Rage Blast',100,100,'Special','Normal',0,[])

@Increment(Rajangon)
def move_5(self): # Rage Blast
    damage_ret=self.get_damage()
    if not damage_ret['miss']:
        damage=damage_ret['damage']
        self.target.take_damage(damage)

@Increment(Rajangon)
def get_power(self):
    power=self['act']['power']
    if self['act']['id'] in ['Rage Blast']:
        for key in ['atk','def','spa','spd','spe']:
            if self['boosts'][key]<0:
                power*=2
                break
    return int(power*self.get_weather_power_mult())
