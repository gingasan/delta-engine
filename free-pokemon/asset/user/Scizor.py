from engine import *


class Scizor(PokemonBase):
    _species='Scizor'
    _types=['Bug','Steel']
    _gender='Female'
    _ability=['Swarm']
    _move_1=('Bullet Punch',40,100,'Physical','Steel',1,['contact'])
    _move_2=('Bug Tangle',15,90,'Physical','Bug',0,[])
    _base=(70,150,130,75,100,75)
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
        if (key=='atk' or key=='spa') and self['act']['type']=='Bug' and self['hp']<=self['max_hp']//3:
            stat_ratio*=1.5
        return int(stat*stat_ratio)
    
    def move_1(self): # Bullet Punch
        damage_ret=self.get_damage()
        if not damage_ret['miss']:
            damage=damage_ret['damage']
            self.target.take_damage(damage)
    
    def move_2(self): # Bug Tangle
        hit=True; i=0
        while hit and i<4:
            damage_ret=self.get_damage()
            if damage_ret['miss']: break
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            i+=1; hit=False if self.target.isfaint() else True

# -------------------------------------------------------------

@Increment(Scizor,'_move_3')
def value():
    return ('Dual Wingbeat',40,90,'Physical','Flying',0,['contact'])

@Increment(Scizor)
def move_3(self): # Dual Wingbeat
    hit=True; i=0
    while hit and i<2:
        damage_ret=self.get_damage()
        if damage_ret['miss']: break
        damage=damage_ret['damage']
        self.target.take_damage(damage)
        i+=1; hit=False if self.target.isfaint() else True

# -------------------------------------------------------------

@Increment(Scizor,'_move_4')
def value():
    return ('Swords Dance',0,100000,'Status','Normal',0,[])

@Increment(Scizor)
def move_4(self): # Swords Dance
    self.set_boost('atk',+2,'self')

# -------------------------------------------------------------

@Increment(Scizor,'_ability')
def value():
    return ['Swarm','Technician']

@Increment(Scizor)
def get_power(self):
    power=self['act']['power']
    if power<=60:
        power=int(power*1.5)
    return int(power*self.get_weather_power_mult())

# -------------------------------------------------------------

@Increment(Scizor,'_move_5')
def value():
    return ('Close Combat',120,100,'Physical','Fighting',0,['contact'])

@Increment(Scizor)
def move_5(self): # Close Combat
    damage_ret=self.get_damage()
    if not damage_ret['miss']:
        damage=damage_ret['damage']
        self.target.take_damage(damage)
        self.set_boost('def',-1,'self')
        self.set_boost('spd',-1,'self')
