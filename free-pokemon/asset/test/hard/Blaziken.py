from engine import *


class Blaziken(PokemonBase):
    _species='Blaziken'
    _types=['Fire','Fighting']
    _gender='Male'
    _ability=['Speed Boost']
    _move_1=('Blaze Kick II',85,90,'Physical','Fire',2,['contact'])
    _move_2=('Double Kick II',30,100,'Physical','Fighting',0,['contact'])
    _base=(100,160,80,80,80,100)
    def __init__(self):
        super().__init__()

    def move_1(self): # Blaze Kick II
        attack_ret=self.attack()
        if not (attack_ret['miss'] or attack_ret['immune']):
            damage_ret=self.get_damage()
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            if not self.target.isfaint() and rnd()<10/100: self.target.set_status('BRN')
            self.restore(int(1/2*damage),'drain')

    def get_power(self):
        power=self['act']['power']
        if self['act']['id']=='Blaze Kick II' and self['hp']<=self['max_hp']//3:
            power=int(power*1.5)
        return int(power*self.get_weather_power_mult())

    def move_2(self): # Double Kick II
        hit=True; i=0
        while hit and i<4:
            attack_ret=self.attack()
            if attack_ret['miss'] or attack_ret['immune']: break
            damage_ret=self.get_damage()
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            i+=1; hit=False if self.target.isfaint() else True

    def endturn(self):
        self.set_boost('spe',1,'self')

# ----------

@Increment(Blaziken,'_move_3')
def value():
    return ('Thunder Punch',75,100,'Physical','Electric',0,['contact'])

@Increment(Blaziken)
def move_3(self): # Thunder Punch
    attack_ret=self.attack()
    if not (attack_ret['miss'] or attack_ret['immune']):
        damage_ret=self.get_damage()
        damage=damage_ret['damage']
        self.target.take_damage(damage)
        if not self.target.isfaint() and rnd()<10/100:
            self.target.set_status('PAR')

# ----------

@Increment(Blaziken,'_move_4')
def value():
    return ('Swords Dance',0,100000,'Status','Normal',0,[])

@Increment(Blaziken)
def move_4(self): # Swords Dance
    self.set_boost('atk',+2,'self')

# ----------

@Increment(Blaziken,'_ability')
def value():
    return ['Speed Boost','Combat Master']

@Increment(Blaziken)
def get_evasion(self):
    return max(0,self['boosts']['spe'])*0.1

# ----------

@Increment(Blaziken,'_move_5')
def value():
    return ('Burning Bulwark',0,100000,'Status','Fire',4,[])

@Increment(Blaziken)
def move_5(self): # Burning Bulwark
    if self['last_act'] and self['last_act']['id']=='Burning Bulwark':
        return
    self.set_condition('Protected',counter=0)

@Increment(Blaziken)
def get_immune(self):
    if self['conditions'].get('Protected'):
        del self['conditions']['Protected']
        if 'contact' in self.target['act']['property']:
            self.target.set_status('BRN')
        return True
    return False

@Increment(Blaziken)
def endturn(self):
    self.set_boost('spe',1,'self')
    if self['conditions'].get('Protected'):
        del self['conditions']['Protected']

# ----------

@Increment(Blaziken,'_move_6')
def value():
    return ('Earthquake',100,100,'Physical','Ground',0,[])

@Increment(Blaziken)
def move_6(self): # Earthquake
    attack_ret=self.attack()
    if not (attack_ret['miss'] or attack_ret['immune']):
        damage_ret=self.get_damage()
        damage=damage_ret['damage']
        self.target.take_damage(damage)
