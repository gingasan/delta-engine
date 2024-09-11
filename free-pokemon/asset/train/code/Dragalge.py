from engine import *


class Dragalge(PokemonBase):
    _species='Dragalge'
    _types=['Dragon','Poison']
    _gender='Male'
    _ability=['Poison Point']
    _move_1=('Dragon Pulse',85,100,'Special','Dragon',0,[])
    _move_2=('Sludge Bomb',90,100,'Special','Poison',0,[])
    def __init__(self):
        super().__init__()

    def _take_damage_attack(self,x):
        if 'type_efc' in self.target['act'] and self.target['act']['type_efc']<0.1:
            self.logger.log('It is immune by %s.'%self._species)
            return
        self.register_act_taken()
        self.state['hp']=max(0,self['hp']-x)
        self.log('{} loses {} HP.'.format(self._species,x),act_taken=self['act_taken'])
        if self['hp']==0:
            return
        if self['act_taken'] and 'property' in self['act_taken'] and 'contact' in self['act_taken']['property']:
            if rnd()<30/100:
                self.target.set_status('PSN')

    def move_1(self): # Dragon Pulse
        damage_ret=self.get_damage()
        if not damage_ret['miss']:
            damage=damage_ret['damage']
            self.target.take_damage(damage)
    
    def move_2(self): # Sludge Bomb
        damage_ret=self.get_damage()
        if not damage_ret['miss']:
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            if not self.target.isfaint() and rnd()<30/100: self.target.set_status('PSN')

# -------------------------------------------------------------

@Increment(Dragalge,'_move_3')
def value():
    return ('Toxic Dance',0,100000,'Status','Poison',0,[])

@Increment(Dragalge)
def move_3(self): # Toxic Dance
    self.set_boost('spa',+1,'self')
    self.set_boost('spd',+1,'self')
    if self.target.isstatus('PSN') or self.target.isstatus('TOX'):
        self.set_boost('def',+1,'self')