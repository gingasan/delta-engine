from engine import *


class Araquanid(PokemonBase):
    _species='Araquanid'
    _types=['Water','Bug']
    _gender='Female'
    _ability=['Water Bubble']
    _move_1=('Liquidation',85,100,'Physical','Water',0,['contact'])
    _move_2=('Leech Life',80,100,'Physical','Bug',0,['contact'])
    def __init__(self):
        super().__init__()

    def get_power(self):
        power=self['act']['power']
        if self['act']['type']=='Water':
            power*=2
        return int(power*self.get_weather_power_mult())

    def set_status(self,x):
        if self['hp']<=self['max_hp']//3:
            return
        if self['status'] or self.get_env('Misty Terrain'):
            return
        if x=='BRN':
            return
        elif x=='PAR':
            if not self.istype('Electric'):
                self.state['status']={x:{'counter':0}}
                self.log('%s is paralyzed.'%self._species)
        elif x=='PSN':
            if not self.istype('Poison') and not self.istype('Steel'):
                self.state['status']={x:{'counter':0}}
                self.log('%s is poisoned.'%self._species)
        elif x=='TOX':
            if not self.istype('Poison') and not self.istype('Steel'):
                self.state['status']={x:{'counter':0}}
                self.log('%s is badly poisoned.'%self._species)
        elif x=='FRZ':
            if not self.istype('Ice'):
                self.state['status']={x:{'counter':0}}
                self.log('%s is frozen.'%self._species)
        elif x=='SLP':
            if not self.env.get("Electric Terrain"):
                self.state['status']={x:{'counter':0}}
                self.log('%s falls asleep.'%self._species)

    def _take_damage_attack(self,x):
        if 'type_efc' in self.target['act'] and self.target['act']['type_efc']<0.1:
            self.logger.log('It is immune by %s.'%self._species)
            return
        self.register_act_taken()
        if self['act_taken']['type']=='Fire':
            x=int(x*0.5)
        self.state['hp']=max(0,self['hp']-x)
        self.log('{} loses {} HP.'.format(self._species,x),act_taken=self['act_taken'])

    def move_1(self): # Liquidation
        damage_ret=self.get_damage()
        if not damage_ret['miss']:
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            if not self.target.isfaint() and rnd()<20/100:
                self.target.set_boost('def',-1)

    def move_2(self): # Leech Life
        damage_ret=self.get_damage()
        if not damage_ret['miss']:
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            self.restore(int(1/2*damage),'drain')
