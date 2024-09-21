from engine import *


class Tyranotor(PokemonBase):
    _species='Tyranotor'
    _types=['Dragon','Dark']
    _gender='Male'
    _ability=['Apex Predator']
    _move_1=('Savage Bite',90,95,'Physical','Dark',0,['contact','bite'])
    _move_2=('Rend',85,95,'Physical','Dark',0,[])
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
        if (key=='atk' or key=='spe') and self.target['hp']<self.target['max_hp']//2:
            stat_ratio*=1.5
        return int(stat*stat_ratio)

    def get_crit(self):
        crit_mult=[0,24,8,2,1]
        crit_ratio=self['boosts']['crit']
        if self['act']['id']=='Savage Bite':
            crit_ratio=min(3,crit_ratio+1)
        crit=False
        if rnd()*crit_mult[crit_ratio+1]<1:
            crit=True
        return crit

    def move_1(self): # Savage Bite
        attack_ret=self.attack()
        if not (attack_ret['miss'] or attack_ret['immune']):
            damage_ret=self.get_damage()
            damage=damage_ret['damage']
            self.target.take_damage(damage)

    def move_2(self): # Rend
        attack_ret=self.attack()
        if not (attack_ret['miss'] or attack_ret['immune']):
            damage_ret=self.get_damage()
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            self.restore(int(30/100*damage),'drain')

# ----------

@Increment(Tyranotor,'_move_3')
def value():
    return ('Devastating Roar',0,100,'Status','Dragon',0,[])

@Increment(Tyranotor)
def move_3(self): # Devastating Roar
    self.target.set_boost('atk',-1)
    self.target.set_boost('spa',-1)

# ----------

@Increment(Tyranotor,'_move_4')
def value():
    return ('Tail Smash',120,75,'Physical','Dragon',0,['contact'])

@Increment(Tyranotor)
def move_4(self): # Tail Smash
    attack_ret=self.attack()
    if not (attack_ret['miss'] or attack_ret['immune']):
        damage_ret=self.get_damage()
        damage=damage_ret['damage']
        self.target.take_damage(damage)
        if not self.target.isfaint() and rnd()<0.2:
            self.target.set_status('PAR')

# ----------

@Increment(Tyranotor,'_ability')
def value():
    return ['Apex Predator','Titan Bite']

@Increment(Tyranotor)
def move_1(self): # Savage Bite
    attack_ret=self.attack()
    if not (attack_ret['miss'] or attack_ret['immune']):
        damage_ret=self.get_damage()
        damage=damage_ret['damage']
        self.target.take_damage(damage)
        if not self.target.isfaint() and rnd()<0.42:
            self.target.set_condition('Flinch',counter=0)

# ----------

@Increment(Tyranotor,'_move_5')
def value():
    return ('Ice Fang',65,95,'Physical','Ice',0,['contact','bite'])

@Increment(Tyranotor)
def move_5(self): # Ice Fang
    attack_ret=self.attack()
    if not (attack_ret['miss'] or attack_ret['immune']):
        damage_ret=self.get_damage()
        damage=damage_ret['damage']
        self.target.take_damage(damage)
        if not self.target.isfaint():
            if rnd()<0.1:
                self.target.set_status('FRZ')
            if rnd()<0.42:
                self.target.set_condition('Flinch',counter=0)
