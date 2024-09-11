from engine import *


class Cyclorax(PokemonBase):
    _species='Cyclorax'
    _types=['Rock','Steel']
    _gender='Neutral'
    _ability=['Giants Craft']
    _move_1=('Titanic Strike',120,85,'Physical','Rock',0,[])
    _move_2=('Forged Fist',90,95,'Physical','Steel',0,[])
    def __init__(self):
        super().__init__()

    def get_power(self):
        power=self['act']['power']
        if self['act']['type'] in ['Rock','Steel']:
            power*=1.5
        return int(power*self.get_weather_power_mult())
    
    def _take_damage_attack(self,x):
        if 'type_efc' in self.target['act'] and self.target['act']['type_efc']<0.1:
            self.logger.log('It is immune by %s.'%self._species)
            return
        self.register_act_taken()
        self.state['hp']=max(0,self['hp']-x)
        self.log('{} loses {} HP.'.format(self._species,x),act_taken=self['act_taken'])
        if self['hp']==0:
            return
        if self['act_taken'] and self['act_taken']['type']=='Rock':
            self.set_boost('def',1,'self')

    def move_1(self): # Titanic Strike
        damage_ret=self.get_damage()
        if not damage_ret['miss']:
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            if not self.target.isfaint() and rnd()<20/100:
                self.target.set_boost('def',-1)

    def move_2(self): # Forged Fist
        damage_ret=self.get_damage()
        if not damage_ret['miss']:
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            if not self.target.isfaint() and rnd()<30/100:
                self.target.set_condition('FLINCH',counter=0)

# -------------------------------------------------------------

@Increment(Cyclorax,'_move_3')
def value():
    return ('Stubborn Stare',0,100,'Status','Steel',0,[])

@Increment(Cyclorax)
def move_3(self): # Stubborn Stare
    self.set_boost('atk',+1,'self')
    self.set_boost('def',+1,'self')
    self.target.set_boost('atk',-1)

# -------------------------------------------------------------

@Increment(Cyclorax,'_move_4')
def value():
    return ('Counter',0,100,'Physical','Fighting',-5,['contact'])

@Increment(Cyclorax)
def move_4(self): # Counter
    if self['act_taken'] and self['act_taken']['category']=='Physical' and self['act_taken'].get('damage'):
        self.target.take_damage(self['act_taken']['damage']*2)

# -------------------------------------------------------------

@Increment(Cyclorax,'_ability')
def value():
    return ['Giants Craft','One-Eyed Stubbornness']

@Increment(Cyclorax)
def _take_damage_attack(self,x):
    if 'type_efc' in self.target['act'] and self.target['act']['type_efc']<0.1:
        self.logger.log('It is immune by %s.'%self._species)
        return
    self.register_act_taken()
    self.state['hp']=max(0,self['hp']-x)
    if self['hp']==0:
        if rnd()<30/100:
          self.state['hp']=1
        else:
          self.state['status']='FNT'
          return
    if self['act_taken'] and self['act_taken']['type']=='Rock':
        self.set_boost('def',1,'self')
