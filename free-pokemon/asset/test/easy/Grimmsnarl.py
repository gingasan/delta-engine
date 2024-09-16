from engine import *


class Grimmsnarl(PokemonBase):
    _species='Grimmsnarl'
    _types=['Dark','Fairy']
    _gender='Male'
    _ability=['Prankster']
    _move_1=('Bulk Up',0,100000,'Status','Fighting',0,[])
    _move_2=('Spirit Break',75,100,'Physical','Fairy',0,['contact'])
    def __init__(self):
        super().__init__()

    def get_priority(self,move_id):
        if self._moves[move_id]['category']=='Status':
            return 1
        return self._moves[move_id]['priority']

    def move_1(self): # Bulk Up
        self.set_boost('atk',+1,'self')
        self.set_boost('def',+1,'self')
    
    def move_2(self): # Spirit Break
        damage_ret=self.get_damage()
        if not damage_ret['miss']:
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            if not self.target.isfaint():
                self.target.set_boost('spa',-1)

# ----------

@Increment(Grimmsnarl,'_move_3')
def value():
    return ('Substitute',0,100000,'Status','Normal',0,[])

@Increment(Grimmsnarl)
def move_3(self): # Substitute
    if self['hp']>self['max_hp']//4 and not self['conditions'].get('SUBSTITUTE'):
        self.take_damage(self['max_hp']//4,'loss')
        self.set_condition('SUBSTITUTE',hp=self['max_hp']//4)

@Increment(Grimmsnarl)
def _take_damage_attack(self,x):
    if 'type_effect' in self.target['act'] and self.target['act']['type_effect']<0.1:
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
