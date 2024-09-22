from engine import *


class Reshiram(PokemonBase):
    _species='Reshiram'
    _types=['Dragon','Fire']
    _gender='Neutral'
    _ability=['Sun Grace']
    _move_1=('Blue Flare',130,85,'Special','Fire',0,[])
    _move_2=('Truth Beam',120,100,'Special','Dragon',0,[])
    _base=(100,75,100,140,100,85)
    def __init__(self):
        super().__init__()

    def onswitch(self):
        self.env.set_weather('Sunlight',from_=self._species)

    def get_stat(self,key,boost=None):
        stat=self['stats'][key]
        boost=self['boosts'][key] if not boost else boost
        stat_ratio={0:1,1:1.5,2:2,3:2.5,4:3,5:3.5,6:4}[min(6,abs(boost))]
        if boost<0:
            stat_ratio=1/stat_ratio
        stat_ratio*=self.get_weather_stat_mult(key)
        if key=='spe' and self.isstatus('PAR'):
            stat_ratio*=0.5
        if key=='spa' and self.env.get('Sunlight'):
            stat_ratio*=1.35
        return int(stat*stat_ratio)

    def move_1(self): # Blue Flare
        attack_ret=self.attack()
        if not (attack_ret['miss'] or attack_ret['immune']):
            damage_ret=self.get_damage()
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            if not self.target.isfaint() and rnd()<20/100:
                self.target.set_status('BRN')

    def move_2(self): # Truth Beam
        attack_ret=self.attack()
        if not (attack_ret['miss'] or attack_ret['immune']):
            damage_ret=self.get_damage()
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            for key in ['atk','def','spa','spd','spe','accuracy','crit']:
                if self.target['boosts'][key]!=0:
                    self.target.set_boost(key,-self.target['boosts'][key])

# ----------

@Increment(Reshiram,'_move_3')
def value():
    return ('Earth Power',90,100,'Special','Ground',0,[])

@Increment(Reshiram)
def move_3(self): # Earth Power
    attack_ret=self.attack()
    if not (attack_ret['miss'] or attack_ret['immune']):
        damage_ret=self.get_damage()
        damage=damage_ret['damage']
        self.target.take_damage(damage)
        if not self.target.isfaint() and rnd()<10/100:
            self.target.set_boost('spd',-1)

# ----------

@Increment(Reshiram,'_move_4')
def value():
    return ('Solar Beam',120,100,'Special','Grass',0,[])

@Increment(Reshiram)
def move_4(self): # Solar Beam
    if self.env.get('Sunlight') or self['conditions'].get('Charging'):
        if self['conditions'].get('Charging'):
            del self['conditions']['Charging']
        attack_ret=self.attack()
        if not (attack_ret['miss'] or attack_ret['immune']):
            damage_ret=self.get_damage()
            damage=damage_ret['damage']
            self.target.take_damage(damage)
    else:
        self.set_condition('Charging',counter=0)

# ----------

@Increment(Reshiram,'_ability')
def value():
    return ['Sun Grace','White Sun']

@Increment(Reshiram)
def endturn(self):
    self.state['types']=['Normal']

@Increment(Reshiram)
def move_1(self): # Blue Flare
    self.state['types']=['Dragon','Fire']
    attack_ret=self.attack()
    if not (attack_ret['miss'] or attack_ret['immune']):
        damage_ret=self.get_damage()
        damage=damage_ret['damage']
        self.target.take_damage(damage)
        if not self.target.isfaint() and rnd()<20/100:
            self.target.set_status('BRN')

@Increment(Reshiram)
def move_2(self): # Draco Meteor
    self.state['types']=['Dragon','Fire']
    attack_ret=self.attack()
    if not (attack_ret['miss'] or attack_ret['immune']):
        damage_ret=self.get_damage()
        damage=damage_ret['damage']
        self.target.take_damage(damage)
        for key in ['atk','def','spa','spd','spe','accuracy','crit']:
            if self.target['boosts'][key]!=0:
                self.target.set_boost(key,-self.target['boosts'][key])

@Increment(Reshiram)
def move_3(self): # Earth Power
    self.state['types']=['Dragon','Fire']
    attack_ret=self.attack()
    if not (attack_ret['miss'] or attack_ret['immune']):
        damage_ret=self.get_damage()
        damage=damage_ret['damage']
        self.target.take_damage(damage)
        if not self.target.isfaint() and rnd()<10/100:
            self.target.set_boost('spd',-1)

@Increment(Reshiram)
def move_4(self): # Solar Beam
    self.state['types']=['Dragon','Fire']
    if self.env.get('Sunlight') or self['conditions'].get('Charging'):
        if self['conditions'].get('Charging'):
            del self['conditions']['Charging']
        attack_ret=self.attack()
        if not (attack_ret['miss'] or attack_ret['immune']):
            damage_ret=self.get_damage()
            damage=damage_ret['damage']
            self.target.take_damage(damage)
    else:
        self.set_condition('Charging',counter=0)

# ----------

@Increment(Reshiram,'_move_5')
def value():
    return ('Recover',0,100000,'Status','Normal',0,[])

@Increment(Reshiram)
def move_5(self): # Recover
    self.state['types']=['Dragon','Fire']
    self.restore(self['max_hp']//2,'heal')
