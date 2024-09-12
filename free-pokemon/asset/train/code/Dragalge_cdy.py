from engine import *


class Dragalge(PokemonBase):
    _species='Dragalge'
    _types=['Poison']
    _gender='Male'
    _ability=['Merciless']
    _move_1=('Dragon Pulse',85,100,'Special','Dragon',0,[])
    _move_2=('Sludge Bomb',90,100,'Special','Poison',0,[])
    def __init__(self):
        super().__init__()

    def get_crit(self):
        if self.target.isstatus('PSN') or self.target.isstatus('TOX'):
            return True
        crit_mult=[0,24,8,2,1]
        crit_ratio=self['boosts']['crit']
        crit=False
        if rnd()*crit_mult[crit_ratio+1]<1:
            crit=True
        return crit

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
            if not self.target.isfaint()and rnd()<30/100:
                self.target.set_status('PSN')

# ----------

@Increment(Dragalge,'_move_3')
def value():
    return ('Toxic',0,90,'Status','Poison',0,[])

@Increment(Dragalge)
def move_3(self): # Toxic
    damage_ret=self.get_damage()
    if not damage_ret['miss']:
        self.target.set_status('TOX')

# ----------

@Increment(Dragalge,'_move_4')
def value():
    return ('Scald',80,100,'Special','Water',0,[])

@Increment(Dragalge)
def move_4(self): # Scald
    damage_ret=self.get_damage()
    if not damage_ret['miss']:
        damage=damage_ret['damage']
        self.target.take_damage(damage)
        if not self.target.isfaint()and rnd()<30/100:
            self.target.set_status('BRN')

# ----------

@Increment(Dragalge,'_ability')
def value():
    return ['Merciless','Intoxicate']

@Increment(Dragalge)
def endturn(self):
    if self['act'] and self['act']['type']=='Poison' and rnd()<10/100:
        self.set_boost('spa',+1,'self')

# ----------

@Increment(Dragalge,'_move_5')
def value():
    return ('Venom Drench',0,100,'Status','Poison',0,[])

@Increment(Dragalge)
def move_5(self): # Venom Drench
    if self.target.isstatus('PSN') or self.target.isstatus('TOX'):
        self.target.set_boost('atk',-1)
        self.target.set_boost('spa',-1)
        self.target.set_boost('spe',-1)
