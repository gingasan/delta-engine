from engine import *


class Velkhana(PokemonBase):
    _species='Velkhana'
    _types=['Ice','Dragon']
    _gender='Male'
    _ability=['Frost Armor']
    _move_1=('Flash Freeze Breath',90,95,'Special','Ice',0,[])
    _move_2=('Icy Wall',0,100000,'Status','Ice',0,[])
    def __init__(self):
        super().__init__()

    def onswitch(self):
        self.set_condition('ICE_ARMOR',counter=0)
    
    def _take_damage_attack(self,x):
        if 'type_efc' in self.target['act'] and self.target['act']['type_efc']<0.1:
            self.logger.log('It is immune by %s.'%self._species)
            return
        self.register_act_taken()
        if self['conditions'].get('ICE_ARMOR'):
            if self['act_taken']['category']=='Physical':
                x=int(x*0.75)
                del self['conditions']['ICE_ARMOR']
                self.target.take_damage(self['max_hp']//8,'loss')
        if self['conditions'].get('ICY_WALL'):
            x=int(x*0.5)
            self['conditions']['ICY_WALL']['counter']+=1
            if self['conditions']['ICY_WALL']['counter']==3:
                del self['conditions']['ICY_WALL']
        self.state['hp']=max(0,self['hp']-x)
        self.log(script='attack',species=self._species,x=x,**self['act_taken'])

    def move_1(self): # Flash Freeze Breath
        damage_ret=self.get_damage()
        if not damage_ret['miss']:
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            if not self.target.isfaint() and rnd()<30/100:
                self.target.set_status('FRZ')
    
    def move_2(self): # Icy Wall
        self.set_condition('ICY_WALL',counter=0)

# ----------

@Increment(Velkhana,'_move_3')
def value():
    return ('Tail Lance',70,100,'Physical','Dragon',0,[])

@Increment(Velkhana)
def move_3(self): # Tail Lance
    damage_ret=self.get_damage()
    if not damage_ret['miss']:
        damage=damage_ret['damage']
        self.target.take_damage(damage)
        for key in ['atk','def','spa','spd','spe','crit','accuracy']:
            self['boosts'][key]=0

# ----------

@Increment(Velkhana,'_ability')
def value():
    return ['Frost Armor','Frozen Surge']

@Increment(Velkhana)
def move_1(self): # Flash Freeze Breath
    damage_ret=self.get_damage()
    if not damage_ret['miss']:
        damage=damage_ret['damage']
        self.target.take_damage(damage)
        if not self.target.isfaint() and rnd()<30/100:
            self.target.set_status('FRZ')
        self.set_condition('FREEZING_CLOUD',counter=0)

@Increment(Velkhana)
def get_other_mult(self):
    mult=1
    if self.isstatus('BRN') and self['act']['category']=='Physical':
        mult*=0.5
    if self['act']['type']=='Ice' and self['conditions'].get('FREEZING_CLOUD'):
        mult*=2
        del self['conditions']['FREEZING_CLOUD']
    return mult
