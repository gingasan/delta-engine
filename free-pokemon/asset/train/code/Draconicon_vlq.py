from engine import *


class Draconicon(PokemonBase):
    _species='Draconicon'
    _types=['Dragon','Poison']
    _gender='Female'
    _ability=['Poisonous Skin']
    _move_1=('Draconic Beam',80,100,'Special','Dragon',0,[])
    _move_2=('Venoshock',65,100,'Special','Poison',0,[])
    def __init__(self):
        super().__init__()

    def _take_damage_attack(self,x):
        if 'type_effect' in self.target['act'] and self.target['act']['type_effect']<0.1:
            self.logger.log('It is immune by %s.'%self._species)
            return
        self.register_act_taken()
        self.state['hp']=max(0,self['hp']-x)
        self.log(script='attack',species=self._species,x=x,**self['act_taken'])
        if self['hp']==0:
            return
        if self['act_taken'] and 'property' in self['act_taken'] and 'contact' in self['act_taken']['property']:
            if rnd()<20/100:
                self.target.set_condition('Confusion',counter=0)
    
    def get_power(self):
        power=self['act']['power']
        if self.target.isstatus('PSN') or self.target.isstatus('TOX'):
            power*=2
        return int(power*self.get_weather_power_mult())

    def move_1(self): # Draconic Beam
        damage_ret=self.get_damage()
        if not damage_ret['miss']:
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            if not self.target.isfaint() and rnd()<10/100:
                self.target.set_boost('def',-1)
                self.target.set_boost('spd',-1)
    
    def move_2(self): # Venoshock
        damage_ret=self.get_damage()
        if not damage_ret['miss']:
            damage=damage_ret['damage']
            self.target.take_damage(damage)
