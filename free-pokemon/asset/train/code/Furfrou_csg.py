from engine import *


class Furfrou(PokemonBase):
    _species='Furfrou'
    _types=['Normal']
    _gender='Male'
    _ability=['Fur Coat']
    _move_1=('Thunder Fang',65,95,'Physical','Electric',0,['contact'])
    _move_2=('Ice Fang',65,95,'Physical','Ice',0,['contact'])
    def __init__(self):
        super().__init__()

    def _take_damage_attack(self,x):
        if 'type_effect' in self.target['act'] and self.target['act']['type_effect']<0.1:
            self.logger.log('It is immune by %s.'%self._species)
            return
        self.register_act_taken()
        if self['act_taken']['category']=='Physical':
            x//=2
        self.state['hp']=max(0,self['hp']-x)
        self.log(script='attack',species=self._species,x=x,**self['act_taken'])

    def move_1(self): # Thunder Fang
        damage_ret=self.get_damage()
        if not damage_ret['miss']:
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            if not self.target.isfaint() and rnd()<10/100: 
                self.target.set_status('PAR')
            if not self.target.isfaint() and rnd()<10/100:
                self.target.set_condition('Flinch',counter=0)

    def move_2(self): # Ice Fang
        damage_ret=self.get_damage()
        if not damage_ret['miss']:
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            if not self.target.isfaint() and rnd()<10/100:
                self.target.set_status('FRZ')
            if not self.target.isfaint() and rnd()<10/100:
                self.target.set_condition('Flinch',counter=0)
