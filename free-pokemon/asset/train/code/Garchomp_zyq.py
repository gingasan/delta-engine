from engine import *


class Garchomp(PokemonBase):
    _species='Garchomp'
    _types=['Dragon','Ground']
    _gender='Female'
    _ability=['Arena Trap']
    _move_1=('Sand Tomb',35,85,'Physical','Ground',0,[])
    _move_2=('Dragon Claw',80,100,'Physical','Dragon',0,['contact'])
    def __init__(self):
        super().__init__()

    def move_effect(self,type_efc):
        if type_efc>1:
            self.target.set_boost('def',-1)
            self.target.set_boost('spd',-1)

    def endturn(self):
        if self.target['conditions'].get('TRAP'):
            if self.target['conditions']['TRAP']['counter']<5:
                self.target.take_damage(self.target['max_hp']//8,'loss')
                self.target['conditions']['TRAP']['counter']+=1
            else:
                del self.target['conditions']['TRAP']

    def move_1(self): # Sand Tomb
        damage_ret=self.get_damage()
        if not damage_ret['miss']:
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            if not self.target.isfaint():
                self.move_effect(damage_ret['type_efc'])
                if rnd()<30/100:
                    self.target.set_condition('TRAP',counter=0)

    def move_2(self): # Dragon Claw
        damage_ret=self.get_damage()
        if not damage_ret['miss']:
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            if not self.target.isfaint():
                self.move_effect(damage_ret['type_efc'])

# ----------

@Increment(Garchomp,'_move_3')
def value():
    return ('Protect',0,100000,'Status','Normal',4,[])

@Increment(Garchomp)
def move_3(self): # Protect
    if self['last_act'] and self['last_act']['id']=='Protect':
        return
    self.set_condition('PROTECT',counter=0)

@Increment(Garchomp)
def _take_damage_attack(self,x):
    if 'type_efc' in self.target['act'] and self.target['act']['type_efc']<0.1:
        self.logger.log('It is immune by %s.'%self._species)
        return
    if self['conditions'].get('PROTECT'):
        del self['conditions']['PROTECT']
        return
    self.register_act_taken()
    self.state['hp']=max(0,self['hp']-x)
    self.log(script='attack',species=self._species,x=x,**self['act_taken'])

@Increment(Garchomp)
def endturn(self):
    if self.target['conditions'].get('TRAP'):
        if self.target['conditions']['TRAP']['counter']<5:
            self.target.take_damage(self.target['max_hp']//8,'loss')
            self.target['conditions']['TRAP']['counter']+=1
        else:
            del self.target['conditions']['TRAP']
    if self['conditions'].get('PROTECT'):
        del self['conditions']['PROTECT']
