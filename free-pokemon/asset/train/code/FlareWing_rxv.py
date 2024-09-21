from engine import *


class FlareWing(PokemonBase):
    _species='Flare-Wing'
    _types=['Fire','Dragon']
    _gender='Male'
    _ability=['Battle Blaze']
    _move_1=('Blazing Assault',100,95,'Physical','Fire',0,[])
    _move_2=('Draco Sweep',90,100,'Physical','Dragon',0,['contact'])
    def __init__(self):
        super().__init__()

    def move_1(self): # Blazing Assault
        attack_ret=self.attack()
        if not (attack_ret['miss'] or attack_ret['immune']):
            damage_ret=self.get_damage()
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            blaze_damage=sum([v for _,v in self.target['boosts'].items() if v>0])*10
            self.target.take_damage(blaze_damage)
            if not self.target.isfaint() and rnd()<20/100:
                self.target.set_status('BRN')

    def move_2(self): # Draco Sweep
        attack_ret=self.attack()
        if not (attack_ret['miss'] or attack_ret['immune']):
            damage_ret=self.get_damage()
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            if not self.target.isfaint():
                self.target.set_boost('spd',-1)

# ----------

@Increment(FlareWing,'_move_3')
def value():
    return ('Ignition Burst',70,100,'Special','Fire',0,[])

@Increment(FlareWing)
def move_3(self): # Ignition Burst
    attack_ret=self.attack()
    if not (attack_ret['miss'] or attack_ret['immune']):
        damage_ret=self.get_damage()
        damage=damage_ret['damage']
        self.target.take_damage(damage)

@Increment(FlareWing)
def get_crit(self):
    if self['act']['id']=='Ignition Burst' and self['hp']<int(self['max_hp']*0.3):
        return True
    crit_mult=[0,24,8,2,1]
    crit_ratio=self['boosts']['crit']
    crit=False
    if rnd()*crit_mult[crit_ratio+1]<1:
        crit=True
    return crit

# ----------

@Increment(FlareWing,'_move_4')
def value():
    return ('Wing Slash',80,95,'Physical','Flying',0,['contact'])

@Increment(FlareWing)
def move_4(self): # Wing Slash
    attack_ret=self.attack()
    if not (attack_ret['miss'] or attack_ret['immune']):
        damage_ret=self.get_damage()
        damage=damage_ret['damage']
        self.target.take_damage(damage)
        if not self.target.isfaint() and rnd()<30/100:
            self.target.set_condition('Flinch',counter=0)

# ----------

@Increment(FlareWing,'_ability')
def value():
    return ['Battle Blaze','Dragon Fury']

@Increment(FlareWing)
def get_other_mult(self):
    mult=1
    if self.isstatus('BRN') and self['act']['category']=='Physical':
        mult*=0.5
    if self['hp']<self['max_hp']//2:
        if self['act']['type']=='Dragon':
            mult*=1.5
    return mult

# ----------

@Increment(FlareWing,'_move_5')
def value():
    return ('Flare Blitz',120,100,'Physical','Fire',0,[])

@Increment(FlareWing)
def move_5(self): # Flare Blitz
    attack_ret=self.attack()
    if not (attack_ret['miss'] or attack_ret['immune']):
        damage_ret=self.get_damage()
        damage=damage_ret['damage']
        self.target.take_damage(damage)
        recoil_damage=damage//3
        self.take_damage(recoil_damage,'recoil')
