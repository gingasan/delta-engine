from engine import *


class Feraligatr(PokemonBase):
    _species='Feraligatr'
    _types=['Water']
    _gender='Male'
    _ability=['Sheer Force']
    _move_1=('Waterfall',80,100,'Physical','Water',0,['contact'])
    _move_2=('Ice Fang',65,95,'Physical','Ice',0,['contact'])
    def __init__(self):
        super().__init__()

    def get_power(self):
        power=self['act']['power']
        if self['act']['id'] in ['Waterfall','Ice Fang']:
            power*=1.3
        return int(power*self.get_weather_power_mult())

    def move_1(self): # Waterfall
        damage_ret=self.get_damage()
        if not damage_ret['miss']:
            damage=damage_ret['damage']
            self.target.take_damage(damage)

    def move_2(self): # Ice Fang
        damage_ret=self.get_damage()
        if not damage_ret['miss']:
            damage=damage_ret['damage']
            self.target.take_damage(damage)

# -------------------------------------------------------------

@Increment(Feraligatr,'_move_3')
def value():
    return ('Rock Slide',75,90,'Physical','Rock',0,[])

@Increment(Feraligatr)
def move_3(self): # Rock Slide
    damage_ret=self.get_damage()
    if not damage_ret['miss']:
        damage=damage_ret['damage']
        self.target.take_damage(damage)

@Increment(Feraligatr)
def get_power(self):
    power=self['act']['power']
    if self['act']['id'] in ['Waterfall','Ice Fang','Rock Slide']:
        power*=1.3
    return int(power*self.get_weather_power_mult())

# -------------------------------------------------------------

@Increment(Feraligatr,'_move_4')
def value():
    return ('Scale Shot',25,90,'Physical','Dragon',0,[])

@Increment(Feraligatr)
def move_1(self): # Scale Shot
    hit=True; i=0
    r=rnd()
    if r<0.35:
        n_hits=2
    elif r<0.7:
        n_hits=3
    elif r<0.85:
        n_hits=4
    else:
        n_hits=5
    while hit and i<n_hits:
        damage_ret=self.get_damage()
        if damage_ret['miss']: break
        damage=damage_ret['damage']
        self.target.take_damage(damage)
        i+=1; hit=False if self.target.isfaint() else True
    self.set_boost('def',-1,'self')
    self.set_boost('spe',+1,'self')

# -------------------------------------------------------------

@Increment(Feraligatr,'_ability')
def value():
    return ['Sheer Force','Sheer Predator']

@Increment(Feraligatr)
def get_priority(self,move_id):
    if self._moves[move_id]['power']<=75:
        return self._moves[move_id]['priority'] + 1
    return self._moves[move_id]['priority']

# -------------------------------------------------------------

@Increment(Feraligatr,'_move_5')
def value():
    return ('Bulldoze',60,100,'Physical','Ground',0,[])

@Increment(Feraligatr)
def move_5(self): # Bulldoze
    damage_ret=self.get_damage()
    if not damage_ret['miss']:
        damage=damage_ret['damage']
        self.target.take_damage(damage)

@Increment(Feraligatr)
def get_power(self):
    power=self['act']['power']
    if self['act']['id'] in ['Waterfall','Ice Fang','Rock Slide','Bulldoze']:
        power*=1.3
    return int(power*self.get_weather_power_mult())
