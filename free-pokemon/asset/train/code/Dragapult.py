from engine import *


class Dragapult(PokemonBase):
    _species='Dragapult'
    _types=['Dragon','Ghost']
    _gender='Female'
    _ability=['Clear Body']
    _move_1=('Dragon Darts',50,100,'Physical','Dragon',0,[])
    _move_2=('Phantom Force',90,100,'Physical','Ghost',0,['contact'])
    def __init__(self):
        super().__init__()

    def set_boost(self,key,x,from_='target'):
        if x<0 and from_=='target':
            self.log('Due to Clear Body, Dragapult is immune to stat-lowering from opponents.')
            return
        self._set_boost(key,x)

    def get_evasion(self):
        if self['conditions'].get('PHANTOM_FORCE'):
            return 1
        return 0

    def move_1(self): # Dragon Darts
        hit=True; i=0
        while hit and i<2:
            attack_ret=self.attack()
            if attack_ret['miss'] or attack_ret['immune']: break
            damage_ret=self.get_damage()
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
            attack_ret=self.attack()
            if not (attack_ret['miss'] or attack_ret['immune']):
                damage_ret=self.get_damage()
                damage=damage_ret['damage']
                self.target.take_damage(damage)

# ----------

@Increment(Dragapult,'_move_3')
def value():
    return ('Dragon Dance',0,100000,'Status','Dragon',0,[])

@Increment(Dragapult)
def move_3(self): # Dragon Dance
    self.set_boost('atk',+1,'self')
    self.set_boost('spe',+1,'self')
