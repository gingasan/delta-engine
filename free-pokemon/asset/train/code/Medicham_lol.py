from engine import *


class Medicham(PokemonBase):
    _species='Medicham'
    _types=['Fighting','Psychic']
    _gender='Female'
    _ability=['Pure Power']
    _move_1=('High Jump Kick',130,90,'Physical','Fighting',0,['contact'])
    _move_2=('Zen Headbutt',80,90,'Physical','Psychic',0,['contact'])
    def __init__(self):
        super().__init__()

    def onswitch(self):
        self.set_stat('atk',2)
    
    def move_1(self): # High Jump Kick
        damage_ret=self.get_damage()
        if not damage_ret['miss']:
            damage=damage_ret['damage']
            self.target.take_damage(damage)
        else:
            self.take_damage(self['max_hp']//2,'recoil')
    
    def move_2(self): # Zen Headbutt
        damage_ret=self.get_damage()
        if not damage_ret['miss']:
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            if not self.target.isfaint() and rnd()<20/100:
                self.target.set_condition('Flinch',counter=0)

# ----------

@Increment(Medicham,'_move_3')
def value():
    return ('Ice Punch',75,100,'Physical','Ice',0,['contact','punch'])

@Increment(Medicham)
def move_3(self): # Ice Punch
    damage_ret=self.get_damage()
    if not damage_ret['miss']:
        damage=damage_ret['damage']
        self.target.take_damage(damage)
        if not self.target.isfaint() and rnd()<10/100:
            self.target.set_status('FRZ')

# ----------

@Increment(Medicham,'_move_4')
def value():
    return ('Thunder Punch',75,100,'Physical','Electric',0,['contact','punch'])

@Increment(Medicham)
def move_4(self): # Thunder Punch
    damage_ret=self.get_damage()
    if not damage_ret['miss']:
        damage=damage_ret['damage']
        self.target.take_damage(damage)  
        if not self.target.isfaint() and rnd()<10/100:
            self.target.set_status('PAR')
