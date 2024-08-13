from engine import *


class Scizor(PokemonBase):
    _species='Scizor'
    _types=['Bug','Steel']
    _gender='Female'
    _ability=['Tough Armor']
    _move_1=('Steel Wing',70,90,'Physical','Steel',0,['contact'])
    _move_2=('Bug Rush',10,100,'Physical','Bug',0,[])
    def __init__(self):
        super().__init__()

    def onswitch(self):
        self.set_condition('STEEL_WING',counter=0)

    def get_power(self):
        power=self['act']['power']
        if power<=75:
            power=int(power*1.2)
        return int(power*self.get_weather_power_mult())
    
    def take_damage(self,x,from_='attack'):
        if from_=='attack':
            self._take_damage_attack(x)
        elif from_=='loss':
            self._take_damage_loss(x)
        elif from_=='recoil':
            self._take_damage_recoil(x)
        if self['hp']>0 and x>=150:
            self.restore(int(x*0.25),'heal')
    
    def move_1(self): # Steel Wing
        damage_ret=self.get_damage()
        if not damage_ret['miss']:
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            self['conditions']['STEEL_WING']['counter']+=1
            if self['conditions']['STEEL_WING']['counter']>=3:
                self.set_boost('def',1,'self')
    
    def move_2(self): # Bug Rush
        hit=True; i=0
        while hit and i<5:
            damage_ret=self.get_damage()
            if damage_ret['miss']: break
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            i+=1; hit=False if self.target.isfaint() else True
