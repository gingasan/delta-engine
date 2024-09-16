from engine import *


class Ceruledge(PokemonBase):
    _species='Ceruledge'
    _types=['Fire','Ghost']
    _gender='Male'
    _ability=['Ghost Armor']
    _move_1=('Soul Stealer',90,100,'Physical','Ghost',0,['contact'])
    _move_2=('Bitter Blade',90,100,'Physical','Fire',0,['contact'])
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
        if self['act_taken'] and self['act_taken']['category']=='Physical':
            self.set_condition('GHOST_ARMOR',counter=0)

    def onswitch(self):
        if rnd()<30/100: 
            self.set_condition('GHOST_ARMOR',counter=0)

    def get_stat(self,key,boost=None):
        stat=self['stats'][key]
        boost=self['boosts'][key] if not boost else boost
        stat_ratio={0:1,1:1.5,2:2,3:2.5,4:3,5:3.5,6:4}[min(6,abs(boost))]
        if boost<0:
            stat_ratio=1/stat_ratio
        stat_ratio*=self.get_weather_stat_mult(key)
        if key=='def' and self['conditions'].get('GHOST_ARMOR'):
            stat_ratio*=1.5
        return int(stat*stat_ratio)
        
    def endturn(self):
        if self['conditions'].get('GHOST_ARMOR'):
            self['conditions']['GHOST_ARMOR']['counter']+=1
            if self['conditions']['GHOST_ARMOR']['counter']==2:
                del self['conditions']['GHOST_ARMOR']

    def move_1(self): # Soul Stealer  
        damage_ret=self.get_damage()
        if not damage_ret['miss']:
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            if damage>0: 
                self.restore(int(1/3*damage),'drain')
                self.target.take_damage(int(1/6*damage),'loss')
    
    def move_2(self): # Bitter Blade
        damage_ret=self.get_damage()
        if not damage_ret['miss']:
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            self.restore(int(1/2*damage),'drain')
