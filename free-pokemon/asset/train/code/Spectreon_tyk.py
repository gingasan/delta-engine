from engine import *


class Spectreon(PokemonBase):
    _species='Spectreon'
    _types=['Ghost','Dark']
    _gender='Male'
    _ability=['Spectral Aura']
    _move_1=('Shadow Ball',80,100,'Special','Ghost',0,[])
    _move_2=('Void Pulse',90,100,'Special','Dark',0,[])
    def __init__(self):
        super().__init__()

    def _take_damage_attack(self,x):
        if 'type_efc' in self.target['act'] and self.target['act']['type_efc']<0.1:
            self.logger.log('It is immune by %s.'%self._species)
            return
        self.register_act_taken()
        if self['boosts']['def']>=0:
            x=int(x*(1-0.1*self['boosts']['def']))
        self.state['hp']=max(0,self['hp']-x)
        self.log(script='attack',species=self._species,x=x,**self['act_taken'])

    def move_1(self): # Shadow Ball
        damage_ret=self.get_damage()
        if not damage_ret['miss']:
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            if not self.target.isfaint() and rnd()<20/100:
                self.target.set_boost('spd',-1)

    def move_2(self): # Void Pulse
        damage_ret=self.get_damage()
        if not damage_ret['miss']:
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            if not self.target.isfaint() and rnd()<30/100:
                self.target.set_boost('atk',-1)
