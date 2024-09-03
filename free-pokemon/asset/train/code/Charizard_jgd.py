from engine import *


class Charizard(PokemonBase):
    _species='Charizard'
    _types=['Fire','Flying']
    _gender='Male'
    _ability=['Solar Power','Flame Aura']
    _move_1=('Flare Blitz',120,100,'Physical','Fire',0,['contact'])
    _move_2=('Air Slash',75,95,'Special','Flying',0,[])
    def __init__(self):
        super().__init__()

    def get_weather_stat_mult(self,key):
        if self.env.get('SANDSTORM') and key=='spd' and 'Rock' in self['types']:
            return 1.5
        if self.env.get('SNOW') and key=='def' and 'Ice' in self['types']:
            return 1.5
        if self.env.get('SUNNYDAY') and key=='spa':
            return 1.5
        return 1.

    def endturn(self):
        if self.env.get('SUNNYDAY'):
            self.take_damage(self['max_hp']//8,'loss')

    def get_accuracy(self):
        acc=self['act']['accuracy']
        if self['act']['id']=='Flare Blitz':
            if self.env.get('SUNNYDAY'):
                acc=1e5
        elif self['act']['id']=='Air Slash':
            if self.env.get('RAINDANCE'):
                acc=50
        acc_mult=[1.0,1.33,1.67,2.0]
        if self['boosts']['accuracy']>=0:
            acc*=acc_mult[self['boosts']['accuracy']]
        else:
            acc/=acc_mult[self['boosts']['accuracy']]
        acc*=self.target.get_evasion()
        return acc/100

    def move_1(self): # Flare Blitz
        damage_ret=self.get_damage()
        if not damage_ret['miss']:
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            recoil_damage=int(damage//3)
            self.take_damage(recoil_damage,'recoil')
            if not self.target.isfaint() and rnd()<20/100: self.target.set_status('BRN')

    def move_2(self): # Air Slash 
        damage_ret=self.get_damage()
        if not damage_ret['miss']:
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            if not self.target.isfaint() and rnd()<30/100:
                self.target.set_condition('FLINCH',counter=0)

# -------------------------------------------------------------

@Increment(Charizard,'_move_3')
def value():
    return ('Inferno Cyclone',90,85,'Special','Fire',0,['ranged'])

@Increment(Charizard)
def move_3(self): # Inferno Cyclone
    damage_ret=self.get_damage()
    if not damage_ret['miss']:
        damage=damage_ret['damage']
        self.target.take_damage(damage)
        if not self.target.isfaint():
            if self.env.get('SUNNYDAY'):
                self.target.set_status('BRN')
            elif rnd()<50/100:
                self.target.set_status('BRN')

# -------------------------------------------------------------

@Increment(Charizard,'_move_4')
def value():
    return ('Sky Blaze',100,90,'Physical','Flying',0,['contact'])

@Increment(Charizard)
def move_4(self): # Sky Blaze
    damage_ret=self.get_damage()
    if not damage_ret['miss']:
        damage=damage_ret['damage']
        self.target.take_damage(damage)
        if self.target.isfaint():
            self.set_boost('spe',+1,'self')

# -------------------------------------------------------------

@Increment(Charizard,'_move_5')
def value():
    return ('Heat Wave',95,90,'Special','Fire',0,['ranged'])

@Increment(Charizard)
def move_5(self): # Heat Wave
    damage_ret=self.get_damage()
    if not damage_ret['miss']:
        damage=damage_ret['damage']
        self.target.take_damage(damage)
        if rnd()<10/100: self.target.set_status('BRN')
