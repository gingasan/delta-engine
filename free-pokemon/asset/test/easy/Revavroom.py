from engine import *


class Revavroom(PokemonBase):
    _species='Revavroom'
    _types=['Steel','Poison']
    _gender='Male'
    _ability=['Filter']
    _move_1=('Shift Gear',0,100000,'Status','Steel',0,[])
    _move_2=('Gunk Shot',120,80,'Physical','Poison',0,[])
    def __init__(self):
        super().__init__()

    def _take_damage_attack(self,x):
        if 'type_efc' in self.target['act'] and self.target['act']['type_efc']<0.1:
            self.logger.log('It is immune by %s.'%self._species)
            return
        self.register_act_taken()
        if self['act_taken'].get('type_efc',0)>1:
            x=int(x*0.75)
        self.state['hp']=max(0,self['hp']-x)
        self.log(script='attack',species=self._species,x=x,**self['act_taken'])

    def move_1(self): # Shift Gear
        self.set_boost('spe',2,'self')
        self.set_boost('atk',1,'self')

    def move_2(self): # Gunk Shot
        damage_ret=self.get_damage()
        if not damage_ret['miss']:
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            if not self.target.isfaint() and rnd()<30/100:
                self.target.set_status('PSN')

# ----------

@Increment(Revavroom,'_move_3')
def value():
    return ('High Horsepower',95,95,'Physical','Ground',0,['contact'])

@Increment(Revavroom)
def move_3(self): # High Horsepower
    damage_ret=self.get_damage()
    if not damage_ret['miss']:
        damage=damage_ret['damage']
        self.target.take_damage(damage)

# ----------

@Increment(Revavroom,'_move_4')
def value():
    return ('Iron Head',80,100,'Physical','Steel',0,['contact'])

@Increment(Revavroom)
def move_4(self): # Iron Head
    damage_ret=self.get_damage()
    if not damage_ret['miss']:
        damage=damage_ret['damage']
        self.target.take_damage(damage)
        if not self.target.isfaint() and rnd()<30/100:
            self.target.set_condition('FLINCH',counter=0)
