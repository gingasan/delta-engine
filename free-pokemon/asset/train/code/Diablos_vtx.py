from engine import *


class Diablos(PokemonBase):
    _species='Diablos'
    _types=['Ground','Dragon']
    _gender='Male'
    _ability=['Unyielding Fury','Berserker Mode']
    _move_1=('Corkscrew Burrow',120,60,'Physical','Ground',0,['contact'])
    _move_2=('Multi-Charge',100,95,'Physical','Dragon',0,['contact'])
    def __init__(self):
        super().__init__()

    def get_stat(self,key,boost=None):
        stat=self['stats'][key]
        boost=self['boosts'][key] if not boost else boost
        stat_ratio={0:1,1:1.5,2:2,3:2.5,4:3,5:3.5,6:4}[min(6,abs(boost))]
        if boost<0:
            stat_ratio=1/stat_ratio
        stat_ratio*=self.get_weather_stat_mult(key)
        if key=='spe' and self.isstatus('PAR'):
            stat_ratio*=0.5
        if key in ['atk','spe'] and self['hp']<self['max_hp']//2:
            stat_ratio*=1.5
        return int(stat*stat_ratio)

    def endturn(self):
        if self['hp']<self['max_hp']//2:
            self.set_condition('BERSERKER_MODE',counter=0)

    def move_1(self): # Corkscrew Burrow
        damage_ret=self.get_damage()
        if not damage_ret['miss']:
            damage=damage_ret['damage']
            self.target.take_damage(damage)
        if self['conditions'].get('BERSERKER_MODE'):
            damage_ret=self.get_damage()
            if not damage_ret['miss']:
                damage=damage_ret['damage']
                self.target.take_damage(damage)

    def move_2(self): # Multi-Charge
        for _ in range(rndc([2,3,4,5])):
            damage_ret=self.get_damage()
            if damage_ret['miss']: break
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            if self.target.isfaint(): break
            if rnd()<10/100: self.target.set_condition('FLINCH')

# -------------------------------------------------------------

@Increment(Diablos,'_move_3')
def value():
    return ('Raging Earth',120,85,'Special','Ground',0,[])

@Increment(Diablos)
def move_3(self): # Raging Earth
    damage_ret=self.get_damage()
    if not damage_ret['miss']:
        damage=damage_ret['damage']
        self.target.take_damage(damage)
        if self.target.isfaint() and rnd()<30/100:
            self.target.set_boost('spe',-1)

# -------------------------------------------------------------

@Increment(Diablos,'_move_4')
def value():
    return ('Infernal Roar',80,100,'Special','Dragon',0,['sound'])

@Increment(Diablos)
def move_4(self): # Infernal Roar
    damage_ret=self.get_damage()
    if not damage_ret['miss']:
        damage=damage_ret['damage']
        self.target.take_damage(damage)
        if self.target.isfaint() and rnd()<20/100:
            self.target.set_status('BRN')

# -------------------------------------------------------------

@Increment(Diablos,'_ability')
def value():
    return ['Berserker Mode','Unyielding Fury']

@Increment(Diablos)
def take_damage(self,x,from_='attack'):
    if from_=='attack':
        self._take_damage_attack(x)
    elif from_=='loss':
        self._take_damage_loss(x)
    elif from_=='recoil':
        self._take_damage_recoil(x)
    if rnd()<0.3:
        self.set_boost('atk',1,'self')
