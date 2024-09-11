from engine import *


class Alomomola(PokemonBase):
    _species='Alomomola'
    _types=['Water']
    _gender='Male'
    _ability=['Hydration']
    _move_1=('Scald',80,100,'Special','Water',0,[])
    _move_2=('Protect',0,100000,'Status','Normal',4,[])
    def __init__(self):
        super().__init__()

    def endturn(self):
        if self.get_env('Rain'):
            self.state['status']=None
        if self['conditions'].get('PROTECT'):
            del self['conditions']['PROTECT']

    def move_1(self): # Scald
        damage_ret=self.get_damage()
        if not damage_ret['miss']:
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            if not self.target.isfaint() and rnd()<30/100:
                self.target.set_status('BRN')
                if self.target['status']=='FRZ':
                    self.target.state['status']=None

    def move_2(self): # Protect
        if self['last_act'] and self['last_act']['id']=='Protect':
            return
        self.set_condition('PROTECT',counter=0)
    
    def _take_damage_attack(self,x):
        if 'type_efc' in self.target['act'] and self.target['act']['type_efc']<0.1:
            self.logger.log('It is immune by %s.'%self._species)
            return
        if self['conditions'].get('PROTECT'):
            del self['conditions']['PROTECT']
            return
        self.register_act_taken()
        self.state['hp']=max(0,self['hp']-x)
        self.log('{} loses {} HP.'.format(self._species,x),act_taken=self['act_taken'])
