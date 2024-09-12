from engine import *


class Volcanion(PokemonBase):
    _species='Volcanion'
    _types=['Fire','Water']
    _gender='Male'
    _ability=['Water Absorb']
    _move_1=('Steam Eruption',110,95,'Special','Water',0,[])
    _move_2=('Fire Blast',110,85,'Special','Fire',0,[])
    def __init__(self):
        super().__init__()

    def _take_damage_attack(self,x):
        if 'type_efc' in self.target['act'] and self.target['act']['type_efc']<0.1:
            self.logger.log('It is immune by %s.'%self._species)
            return
        self.register_act_taken()
        if self['act_taken']['type']=='Water':
            self.state['hp']=min(self['max_hp'],self['hp']+self['max_hp']//4)
            return
        self.state['hp']=max(0,self['hp']-x)
        self.log(script='attack',species=self._species,x=x,**self['act_taken'])
        if self['hp']>0 and self['act_taken']['type']=='Fire':
            self.set_condition('ERUPTION_BOOST',counter=0)

    def get_stat(self,key,boost=None):
        stat=self['stats'][key]
        boost=self['boosts'][key] if not boost else boost
        stat_ratio={0:1,1:1.5,2:2,3:2.5,4:3,5:3.5,6:4}[min(6,abs(boost))]
        if boost<0:
            stat_ratio=1/stat_ratio
        stat_ratio*=self.get_weather_stat_mult(key)
        if key=='spe' and self.isstatus('PAR'):
            stat_ratio*=0.5
        if key=='spa' and self['conditions'].get('ERUPTION_BOOST'):
            stat_ratio*=1.5
        return int(stat*stat_ratio)

    def endturn(self):
        if self['conditions'].get('ERUPTION_BOOST'):
            self['conditions']['ERUPTION_BOOST']['counter']+=1
            if self['conditions']['ERUPTION_BOOST']['counter']==2:
                del self['conditions']['ERUPTION_BOOST']

    def move_1(self): # Steam Eruption
        damage_ret=self.get_damage()
        if not damage_ret['miss']:
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            if self['conditions'].get('ERUPTION_BOOST'):
                damage=int(damage*1.3)
            self.target.take_damage(damage)
            if not self.target.isfaint() and rnd()<30/100: self.target.set_status('BRN')
            if self['status']=='FRZ': self.state['status']=None

    def move_2(self): # Fire Blast
        damage_ret=self.get_damage()
        if not damage_ret['miss']:
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            if not self.target.isfaint() and rnd()<10/100: self.target.set_status('BRN')
