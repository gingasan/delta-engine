from engine import *


class Tigrex(PokemonBase):
    _species='Tigrex'
    _types=['Dragon','Fire']
    _gender='Male'
    _ability=['Concussive Roar']
    _move_1=('Moltenquake',140,100000,'Special','Dragon',0,['sound'])
    _move_2=('Flare Blitz',120,100,'Physical','Fire',0,['contact'])
    def __init__(self):
        super().__init__()

    def _get_base_damage(self,power,crit):
        if 'sound' in self['act']['property']:
            atk_boost=self['boosts']['atk']
            def_boost=self.target['boosts']['def']
        else:
            atk_boost=self['boosts']['atk'] if self['act']['category']=='Physical' else self['boosts']['spa']
            def_boost=self.target['boosts']['def'] if self['act']['category']=='Physical' else self.target['boosts']['spd']
    
        if crit:
            atk_boost=max(0,atk_boost)
            def_boost=min(0,def_boost)

        if 'sound' in self['act']['property']:
            attack=self.get_stat('atk',atk_boost)
            defense=self.target.get_stat('def',def_boost)
        else:
            attack=self.get_stat('atk' if self['act']['category']=='Physical' else 'spa',atk_boost)
            defense=self.target.get_stat('def' if self['act']['category']=='Physical' else 'spd',def_boost)

        level=100
        base_damage=int(int(int(int(2*level/5+2)*power*attack)/defense)/50)+2

        return base_damage

    def move_1(self): # Moltenquake
        damage_ret=self.get_damage()
        if not damage_ret['miss']:
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            if not self.target.isfaint() and rnd()<30/100:
                self.target.set_condition('FLINCH',counter=0)
    
    def move_2(self): # Flare Blitz
        damage_ret=self.get_damage()
        if not damage_ret['miss']:
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            self.take_damage(int(0.33*damage),'recoil')

# -------------------------------------------------------------

@Increment(Tigrex,'_move_3')
def value():
    return ('Earthquake',100,100,'Physical','Ground',0,[])

@Increment(Tigrex)
def move_3(self): # Earthquake
    damage_ret=self.get_damage()
    if not damage_ret['miss']:
        damage=damage_ret['damage']
        self.target.take_damage(damage)

# -------------------------------------------------------------

@Increment(Tigrex,'_move_4')
def value():
    return ('Bulk Up',0,100000,'Status','Fighting',0,[])

@Increment(Tigrex)
def move_4(self): # Bulk Up
    self.set_boost('atk',+1,'self')
    self.set_boost('def',+1,'self')

# -------------------------------------------------------------

@Increment(Tigrex,'_ability')
def value():
    return ['Concussive Roar','Absolute Power']

@Increment(Tigrex)
def get_power(self):
    power=self['act']['power']
    if self['act']['category']=='Physical':
        power*=1.3
    return int(power*self.get_weather_power_mult())

@Increment(Tigrex)
def get_accuracy(self):
    acc=self['act']['accuracy']
    if self['act']['category']=='Physical':
        acc-=10
    acc_mult=[1.0,1.33,1.67,2.0]
    if self['boosts']['accuracy']>=0:
        acc*=acc_mult[self['boosts']['accuracy']]
    else:
        acc/=acc_mult[self['boosts']['accuracy']]
    acc*=self.target.get_evasion()
    return acc/100

# -------------------------------------------------------------

@Increment(Tigrex,'_move_5')
def value():
    return ('Ice Spinner',80,100,'Physical','Ice',0,['contact'])

@Increment(Tigrex)
def move_5(self): # Ice Spinner
    damage_ret=self.get_damage()
    if not damage_ret['miss']:
        damage=damage_ret['damage']
        self.target.take_damage(damage)
        for t in ['PSYCHIC_TERRAIN','ELECTRIC_TERRAIN','GRASSY_TERRAIN','MISTY_TERRAIN']:
            if self.env.get(t):
                del self.env[t]
