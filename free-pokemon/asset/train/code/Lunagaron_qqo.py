from engine import *


class Lunagaron(PokemonBase):
    _species='Lunagaron'
    _types=['Ice','Fighting']
    _gender='Male'
    _ability=['Frost Armor']
    _move_1=('Glacial Claws',95,90,'Physical','Ice',0,['contact'])
    _move_2=('Icicle Barrage',70,90,'Physical','Ice',0,['contact'])
    def __init__(self):
        super().__init__()
    
    def take_damage_attack(self,x):
        self.register_act_taken()
        if self['act_taken']['type']!='Fire':
            x=int(x*0.8)
        self._set_hp(-x)        
        if self['hp']==0:
            return
        if 'contact' in self['act_taken']['property']:
            if rnd()<30/100:
                self.target.set_status('FRZ')

    def get_crit(self):
        if self['act']['id']=='Glacial Claws':
            return True
        crit_mult=[0,24,8,2,1]
        crit_ratio=self['boosts']['crit']
        crit=False
        if rnd()*crit_mult[crit_ratio+1]<1:
            crit=True
        return crit

    def move_1(self): # Glacial Claws
        attack_ret=self.attack()
        if not (attack_ret['miss'] or attack_ret['immune']):
            damage_ret=self.get_damage()
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            if not self.target.isfaint() and rnd()<20/100:
                self.target.set_status('FRZ')

    def move_2(self): # Icicle Barrage
        hits=rndc([2,3,4,5])
        for i in range(hits):
            attack_ret=self.attack()
            if attack_ret['miss'] or attack_ret['immune']: break
            damage_ret=self.get_damage()
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            if self.target.isfaint(): break

# ----------

@Increment(Lunagaron,'_move_3')
def value():
    return ('Close Combat',120,100,'Physical','Fighting',0,['contact'])

@Increment(Lunagaron)
def move_3(self): # Close Combat
    attack_ret=self.attack()
    if not (attack_ret['miss'] or attack_ret['immune']):
        damage_ret=self.get_damage()
        damage=damage_ret['damage']
        self.target.take_damage(damage)
        self.set_boost('def',-1,'self')
        self.set_boost('spd',-1,'self')

# ----------

@Increment(Lunagaron,'_move_4')
def value():
    return ('Swords Dance',0,100000,'Status','Normal',0,[])

@Increment(Lunagaron)
def move_4(self): # Swords Dance
    self.set_boost('atk',2,'self')

# ----------

@Increment(Lunagaron,'_ability')
def value():
    return ['Frost Armor','Chilled Circulation']

@Increment(Lunagaron)
def endturn(self):
    if self['act'] and self['act']['type']=='Ice':
        self.set_boost('spe',1,'self')
