from engine import *


class Dragapult(PokemonBase):
    _species='Dragapult'
    _types=['Dragon','Ghost']
    _gender='Female'
    _ability=['Ghostly Boost']
    _move_1=('Dragon Darts',50,100,'Physical','Dragon',0,[])
    _move_2=('Phantom Force',90,100,'Physical','Ghost',0,['contact'])
    def __init__(self):
        super().__init__()
    
    def get_evasion(self):
        if self['conditions'].get('PHANTOM_FORCE'):
            return 0
        return 1
    
    def endturn(self):
        if rnd()<0.3:
            self.set_boost(rndc(['atk','def','spa','spd','spe']),+1)
    
    def move_1(self): # Dragon Darts
        hit=True; i=0
        while hit and i<2:
            damage_ret=self.get_damage()
            if damage_ret['miss']: break
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            i+=1; hit=False if self.target.isfaint() else True
    
    def move_2(self): # Phantom Force
        if not self['conditions'].get('PHANTOM_FORCE'):
            self.set_condition('PHANTOM_FORCE',counter=0)
            self.state['canact']='Phantom Force'
        else:
            del self['conditions']['PHANTOM_FORCE']
            self.state['canact']=True
            damage_ret=self.get_damage()
            if not damage_ret['miss']:
                damage=damage_ret['damage']
                self.target.take_damage(damage)
