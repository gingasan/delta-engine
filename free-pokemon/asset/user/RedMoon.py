from engine import *


class RedMoon(PokemonBase):
    _species='Red-Moon'
    _types=['Dragon','Psychic']
    _gender='Male'
    _ability=['Lunar Aura']
    _move_1=('Lunar Cannon',100,100,'Special','Dragon',0,[])
    _move_2=('Aura Sphere',80,100000,'Special','Fighting',0,[])
    _base=(106,62,95,110,109,118)
    def __init__(self):
        super().__init__()

    def onswitch(self):
        self.set_side_condition('LUNAR_AURA',counter=0)
        self.log('Red-Moon starts Lunar Aura.',color='purple')

    def endturn(self):
        if self['side_conditions'].get('LUNAR_AURA'):
            self['side_conditions']['LUNAR_AURA']['counter']+=1
            if self['side_conditions']['LUNAR_AURA']['counter']==3:
                del self['side_conditions']['LUNAR_AURA']

    def get_type_effect(self):
        move_type=self['act']['type']
        target_types=self.target['types']
        effect=1
        for tt in target_types:
            if tt=='Fairy' and self['act']['id']=='Lunar Cannon':
                effect*=2
            else:
                effect*=TYPEEFFECTIVENESS[move_type][tt]
        return effect

    def move_1(self): # Lunar Cannon
        damage_ret=self.get_damage()
        if not damage_ret['miss']:
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            if not self.target.isfaint():
                if self['side_conditions'].get('LUNAR_AURA'):
                    self.target.set_boost('spd',-1)
                elif rnd()<30/100:
                    self.target.set_boost('spd',-1)

    def move_2(self): # Aura Sphere
        damage_ret=self.get_damage()
        if not damage_ret['miss']:
            damage=damage_ret['damage']
            self.target.take_damage(damage)

# -------------------------------------------------------------

@Increment(RedMoon,'_move_3')
def value():
    return ('Lunar Dance',0,100000,'Status','Psychic',0,[])

@Increment(RedMoon)
def move_3(self): # Lunar Dance
    self.set_boost('spa',+1,'self')
    self.set_boost('spd',+1,'self')
    if self['side_conditions'].get('LUNAR_AURA'):
        self.set_boost('spe',+1,'self')
    elif rnd()<30/100:
        self.set_boost('spe',+1,'self')

# -------------------------------------------------------------

@Increment(RedMoon,'_move_4')
def value():
    return ('Will-O-Wisp',0,85,'Status','Fire',0,[])

@Increment(RedMoon)
def move_4(self): # Will-O-Wisp
    damage_ret=self.get_damage()
    if not damage_ret['miss']:
        self.target.set_status('BRN')

# -------------------------------------------------------------

@Increment(RedMoon,'_ability')
def value():
    return ['Lunar Aura','Bloo Burst']

@Increment(RedMoon)
def endturn(self):
    if self['side_conditions'].get('LUNAR_AURA'):
        self['side_conditions']['LUNAR_AURA']['counter']+=1
        if self['side_conditions']['LUNAR_AURA']['counter']==3:
            del self['side_conditions']['LUNAR_AURA']
            self.log('Lunar Aura ends.')
            if self['hp']<=self['max_hp']//2:
                self.set_condition('BLOO_BURST',counter=0)
                self.log('Bloo Burst! Red-Moon has gone berserk.',color='red')

@Increment(RedMoon)
def get_power(self):
    power=self['act']['power']
    if self['conditions'].get('BLOO_BURST'):
        power*=2
    return int(power*self.get_weather_power_mult())

# -------------------------------------------------------------

@Increment(RedMoon,'_move_5')
def value():
    return ('Recover',0,100000,'Status','Normal',0,[])

@Increment(RedMoon)
def move_5(self): # Recover
    self.restore(self['max_hp']//2,'heal')
