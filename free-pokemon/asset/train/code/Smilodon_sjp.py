from engine import *


class Smilodon(PokemonBase):
    _species='Smilodon'
    _types=['Fighting','Ice']
    _gender='Male'
    _ability=['Precision Strike']
    _move_1=('Ice Fang',65,100,'Physical','Ice',0,['contact'])
    _move_2=('Saber Slash',100,90,'Physical','Fighting',0,['contact'])
    def __init__(self):
        super().__init__()

    def get_accuracy(self):
        return 100000

    def move_1(self): # Ice Fang
        damage_ret=self.get_damage()
        if not damage_ret['miss']:
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            if not self.target.isfaint():
                if rnd()<0.1:
                    self.target.set_status('FRZ')
                if rnd()<0.1:
                    self.target.set_condition('FLINCH',counter=0)

    def move_2(self): # Saber Slash
        damage_ret=self.get_damage()
        if not damage_ret['miss']:
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            if not self.target.isfaint() and rnd()<0.2:
                self.target.set_boost('def',-1)

# ----------

@Increment(Smilodon,'_move_3')
def value():
    return ('Roar of Dominance',0,100000,'Status','Normal',1,[])

@Increment(Smilodon)
def move_3(self): # Roar of Dominance
    self.target.set_boost('atk', -1)
    self.set_boost('atk', 1)

# ----------

@Increment(Smilodon,'_move_4')
def value():
    return ('Frozen Roar',0,60,'Status','Ice',0,[])

@Increment(Smilodon)
def move_4(self): # Frozen Roar
    damage_ret=self.get_damage()
    if not damage_ret['miss']:
        if self.target.isstatus('FRZ'):
            self.set_boost('spe',2)
        else:
            self.target.set_status('FRZ')

# ----------

@Increment(Smilodon,'_ability')
def value():
    return ['Precision Strike','Frost Armor']

@Increment(Smilodon)
def get_stat(self,key,boost=None):
    stat=self['stats'][key]
    boost=self['boosts'][key] if not boost else boost
    stat_ratio={0:1,1:1.5,2:2,3:2.5,4:3,5:3.5,6:4}[min(6,abs(boost))]
    if boost<0:
        stat_ratio=1/stat_ratio
    stat_ratio*=self.get_weather_stat_mult(key)
    if key=='spe' and self.isstatus('PAR'):
        stat_ratio*=0.5
    if key=='def' and self['hp']<self['max_hp']//2:
        stat_ratio*=1.5
    return int(stat*stat_ratio)

# ----------

@Increment(Smilodon,'_move_5')
def value():
    return ('Bone Crush',85,100,'Physical','Fighting',0,['contact'])

@Increment(Smilodon)
def move_5(self): # Bone Crush
    damage_ret=self.get_damage()
    if not damage_ret['miss']:
        damage=damage_ret['damage']
        self.target.take_damage(damage)
