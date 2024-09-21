from engine import *


class Ceruledge(PokemonBase):
    _species='Ceruledge'
    _types=['Fire','Ghost']
    _gender='Male'
    _ability=['Weak Armor']
    _move_1=('Bitter Blade',90,100,'Physical','Fire',0,['contact'])
    _move_2=('Poltergeist',70,100,'Physical','Ghost',0,['contact'])
    def __init__(self):
        super().__init__()

    def take_damage_attack(self,x):
        self.register_act_taken()
        self._set_hp(-x)        
        if self['act_taken'] and self['act_taken']['category']=='Physical':
            self.set_boost('def',-1)
            self.set_boost('spe',2)

    def move_1(self): # Bitter Blade
        attack_ret=self.attack()
        if not (attack_ret['miss'] or attack_ret['immune']):
            damage_ret=self.get_damage()
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            self.restore(int(1/2*damage),'drain')
    
    def move_2(self): # Poltergeist
        attack_ret=self.attack()
        if not (attack_ret['miss'] or attack_ret['immune']):
            damage_ret=self.get_damage()
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            self.restore(int(1/2*damage),'drain')

# ----------

@Increment(Ceruledge,'_move_3')
def value():
    return ('Play Rough',90,90,'Physical','Fairy',0,['contact'])

@Increment(Ceruledge)
def move_3(self): # Play Rough
    attack_ret=self.attack()
    if not (attack_ret['miss'] or attack_ret['immune']):
        damage_ret=self.get_damage()
        damage=damage_ret['damage']
        self.target.take_damage(damage)
        if not self.target.isfaint() and rnd()<10/100: self.target.set_boost('atk',-1)

# ----------

@Increment(Ceruledge,'_move_4')
def value():
    return ('Swords Dance',0,100000,'Status','Normal',0,[])

@Increment(Ceruledge)
def move_4(self): # Swords Dance
    self.set_boost('atk',+2,'self')

# ----------

@Increment(Ceruledge,'_ability')
def value():
    return ['Weak Armor','Sucking']

@Increment(Ceruledge)
def _restore_drain(self,x):
    x=int(x*1.5)
    self.state['hp']=min(self['max_hp'],self['hp']+x)
    self.log('Ceruledge is ravenously hungry. It drains {} HP from {}.'.format(x,self.target._species),color='red')

# ----------

@Increment(Ceruledge,'_move_5')
def value():
    return ('Close Combat',120,100,'Physical','Fighting',0,['contact'])

@Increment(Ceruledge)
def move_5(self): # Close Combat
    attack_ret=self.attack()
    if not (attack_ret['miss'] or attack_ret['immune']):
        damage_ret=self.get_damage()
        damage=damage_ret['damage']
        self.target.take_damage(damage)
        self.set_boost('def',-1,'self')
        self.set_boost('spd',-1,'self')
