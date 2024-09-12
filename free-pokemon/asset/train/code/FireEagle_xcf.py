from engine import *


class FireEagle(PokemonBase):
    _species='Fire-Eagle'
    _types=['Fire','Flying']
    _gender='Male'
    _ability=['Flame Shield']
    _move_1=('Inferno Wing',90,85,'Special','Fire',0,[])
    _move_2=('Blazing Claw',75,100,'Physical','Fire',0,['contact'])
    def __init__(self):
        super().__init__()

    def _take_damage_attack(self,x):
        if 'type_efc' in self.target['act'] and self.target['act']['type_efc']<0.1:
            self.logger.log('It is immune by %s.'%self._species)
            return
        self.register_act_taken()
        x=int(x*0.5)
        self.state['hp']=max(0,self['hp']-x)
        self.log(script='attack',species=self._species,x=x,**self['act_taken'])

    def endturn(self):
        self.take_damage(self['max_hp']//8,'loss')
    
    def get_crit(self):
        crit_mult=[0,24,8,2,1]
        crit_ratio=self['boosts']['crit']
        if self['act']['id']=='Blazing Claw':
            crit_ratio=min(3,crit_ratio+1)
        crit=False
        if rnd()*crit_mult[crit_ratio+1]<1:
            crit=True
        return crit
    
    def move_1(self): # Inferno Wing
        damage_ret=self.get_damage()
        if not damage_ret['miss']:
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            if not self.target.isfaint() and rnd()<30/100:
                self.target.set_status('BRN')

    def move_2(self): # Blazing Claw
        damage_ret=self.get_damage()
        if not damage_ret['miss']:
            damage=damage_ret['damage']
            self.target.take_damage(damage)

# ----------

@Increment(FireEagle,'_move_3')
def value():
    return ('Eagle Dive',80,95,'Physical','Flying',0,['contact'])

@Increment(FireEagle)
def move_3(self): # Eagle Dive
    damage_ret=self.get_damage()
    if not damage_ret['miss']:
        damage=damage_ret['damage']
        self.target.take_damage(damage)
        self.restore(int(0.5*damage),'drain')

# ----------

@Increment(FireEagle,'_move_4')
def value():
    return ('Flame Storm',0,100000,'Status','Fire',0,[])

@Increment(FireEagle)
def move_4(self): # Flame Storm
    self.target.set_boost('def',-2)

# ----------

@Increment(FireEagle,'_move_5')
def value():
    return ('Sky Inferno',110,85,'Special','Fire',0,[])

@Increment(FireEagle)
def move_5(self): # Sky Inferno
    damage_ret=self.get_damage()
    if not damage_ret['miss']:
        damage=damage_ret['damage']
        self.target.take_damage(damage)
        self.take_damage(int(1/3*damage),'recoil')
