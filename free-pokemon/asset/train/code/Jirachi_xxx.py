from engine import *



class Jirachi(PokemonBase):
    _species='Jirachi'
    _types=['Steel','Psychic']
    _gender='Neutral'
    _ability=['Serene Grace']
    _move_1=('Heart Swap',80,100,'Special','Psychic',0,[])
    _move_2=('Iron Bash',100,95,'Physical','Steel',0,[])
    def __init__(self):
        super().__init__()
    
    def move_1(self): # Heart Swap
        damage_ret=self.get_damage()
        if not damage_ret['miss']:
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            if not self.target.isfaint() and rnd()<40/100:
                self.target.set_boost('spd',-1)
    
    def move_2(self): # Iron Bash
        damage_ret=self.get_damage()
        if not damage_ret['miss']:
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            if not self.target.isfaint() and rnd()<60/100:
                self.target.set_condition('FLINCH',counter=0)

# ----------

@Increment(Jirachi,'_move_3')
def value():
    return ('Lunar Wish',0,100000,'Status','Psychic',0,[])

@Increment(Jirachi)
def move_3(self): # Lunar Wish
    self.restore(self['max_hp']//2,'heal')
    self.state['status']=None

# ----------

@Increment(Jirachi,'_move_4')
def value():
    return ('Meteor Strike',120,85,'Special','Steel',0,[])

@Increment(Jirachi)
def move_4(self): # Meteor Strike
    damage_ret=self.get_damage()
    if not damage_ret['miss']:
        damage=damage_ret['damage']
        self.target.take_damage(damage)
        if not self.target.isfaint() and rnd()<60/100:
            self.target.set_boost('spe',-1)
