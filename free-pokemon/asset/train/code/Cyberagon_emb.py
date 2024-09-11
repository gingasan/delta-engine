from engine import *


class Cyberagon(PokemonBase):
    _species='Cyberagon'
    _types=['Steel','Dragon']
    _gender='Neutral'
    _ability=['Material Gain']
    _move_1=('Infinity Cannon',100,100,'Special','Steel',0,['contact'])
    _move_2=('Dragon Pulse',85,100,'Special','Dragon',0,[])
    def __init__(self):
        super().__init__()

    def onswitch(self):
        self.set_condition('MATERIAL',counter=0)

    def endturn(self):
        self['conditions']['MATERIAL']['counter']+=1

    def get_power(self):
        power=self['act']['power']
        power*=1+(self['conditions']['MATERIAL']['counter']*0.1)
        return int(power*self.get_weather_power_mult())

    def move_1(self): # Infinity Cannon
        damage_ret=self.get_damage()
        if not damage_ret['miss']:
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            self['conditions']['MATERIAL']['counter']+=1

    def move_2(self): # Dragon Pulse
        damage_ret=self.get_damage()
        if not damage_ret['miss']:
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            if not self.target.isfaint() and rnd()<20/100:
                self.target.set_boost('spd',-1)

# -------------------------------------------------------------

@Increment(Cyberagon,'_move_3')
def value():
    return ('Thunder Charge',90,100,'Special','Electric',0,['contact'])

@Increment(Cyberagon)
def move_3(self): # Thunder Charge
    damage_ret=self.get_damage()
    if not damage_ret['miss']:
        damage=damage_ret['damage']
        self.target.take_damage(damage)
        if not self.target.isfaint() and rnd()<20/100:
            self.target.set_status('PAR')

# -------------------------------------------------------------

@Increment(Cyberagon,'_move_4')
def value():
    return ('Barrier Break',75,95,'Physical','Steel',0,['contact'])

@Increment(Cyberagon)
def move_4(self): # Barrier Break
    damage_ret=self.get_damage()
    if not damage_ret['miss']:
        damage=damage_ret['damage']
        self.target.take_damage(damage)

@Increment(Cyberagon)
def _get_base_damage(self,power,crit):
    atk_boost=self['boosts']['atk'] if self['act']['category']=='Physical' else self['boosts']['spa']
    def_boost=self.target['boosts']['def'] if self['act']['category']=='Physical' else self.target['boosts']['spd']
    
    if crit:
        atk_boost=max(0,atk_boost)
        def_boost=min(0,def_boost)

    attack=self.get_stat('atk' if self['act']['category']=='Physical' else 'spa',atk_boost)
    if self['act']['id']=='Barrier Break':
        defense=self.target.get_stat('spd',0)
    else:
        defense=self.target.get_stat('def' if self['act']['category']=='Physical' else 'spd',def_boost)

    level=100
    base_damage=int(int(int(int(2*level/5+2)*power*attack)/defense)/50)+2

    return base_damage

# -------------------------------------------------------------

@Increment(Cyberagon,'_ability')
def value():
    return ['Material Gain','Clear Body']

@Increment(Cyberagon)
def set_boost(self,key,x,from_='target'):
    if x<0 and from_=='target':
        self.log("Cyberagon's stats cannot be lowered by opponents.")
        return
    bar=6 if key in ['atk','def','spa','spd','spe'] else 3
    if x>0:
        self['boosts'][key]=min(bar,self['boosts'][key]+x)
    else:
        self['boosts'][key]=max(-bar,self['boosts'][key]+x)
    self.log("{}'s {} is {} by {}.".format(self._species,{
        'atk':'Attack','def':'Defense','spa':'Special Attack','spd':'Special Defense','spe':'Speed'}[key],'raised' if x>0 else 'lowered',x))
