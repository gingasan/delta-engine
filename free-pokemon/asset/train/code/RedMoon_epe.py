from engine import *


class RedMoon(PokemonBase):
    _species='Red-Moon'
    _types=['Dragon','Flying']
    _gender='Male'
    _ability=['Pressure']
    _move_1=('Dragon Pulse',85,100,'Special','Dragon',0,[])
    _move_2=('Sky Attack',140,90,'Physical','Flying',0,['contact'])
    def __init__(self):
        super().__init__()

    def onswitch(self):
        self.target.set_boost('def',-1)
        self.target.set_boost('spd',-1)

    def move_1(self): # Dragon Pulse
        damage_ret=self.get_damage()
        if not damage_ret['miss']:
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            if not self.target.isfaint() and rnd()<20/100:
                self.target.set_condition('CONFUSION',counter=0)

    def move_2(self): # Sky Attack
        if not self['conditions'].get('SKY_ATTACK'):
            self.set_condition('SKY_ATTACK',counter=0)
            self.state['canact']=False
            self.set_boost('def',+1,'self')
            self.set_boost('spd',+1,'self')
        else:
            del self['conditions']['SKY_ATTACK']
            self.state['canact']='Sky Attack'
            damage_ret=self.get_damage()
            if not damage_ret['miss']:
                damage=damage_ret['damage']
                self.target.take_damage(damage)
                if not self.target.isfaint() and rnd()<30/100:
                    self.target.set_condition('Flinch',counter=0)
