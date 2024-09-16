from engine import *


class Kangaskhan(PokemonBase):
    _species='Kangaskhan'
    _types=['Normal']
    _gender='Female'
    _ability=['Inner Focus']
    _move_1=('Comet Punch',18,85,'Physical','Normal',0,['contact'])
    _move_2=('Brick Break',75,100,'Physical','Fighting',0,['contact'])
    def __init__(self):
        super().__init__()

    def set_condition(self,x,**kwargs):
        if x=='Flinch': return
        if not self['conditions'].get(x):
            self.state['conditions'].update({x: kwargs})

    def move_1(self): # Comet Punch
        hit=True; i=0
        while hit and i<3:
            damage_ret=self.get_damage()
            if damage_ret['miss']: break
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            i+=1; hit=False if self.target.isfaint() else True

    def move_2(self): # Brick Break
        if self.env.get_side_condition('Reflect',self.target.side_id):
            self.env.remove('Reflect',self.target.side_id)
        if self.env.get_side_condition('Light Screen',self.target.side_id):
            self.env.remove('Light Screen',self.target.side_id)
        damage_ret=self.get_damage()
        if not damage_ret['miss']:
            damage=damage_ret['damage']
            self.target.take_damage(damage)

# ----------

@Increment(Kangaskhan,'_move_3')
def value():
    return ('Crunch',80,100,'Physical','Dark',0,['contact'])

@Increment(Kangaskhan)
def move_3(self): # Crunch
    damage_ret=self.get_damage()
    if not damage_ret['miss']:
        damage=damage_ret['damage']
        self.target.take_damage(damage)
        if not self.target.isfaint() and rnd()<20/100:
            self.target.set_boost('def',-1)

# ----------

@Increment(Kangaskhan,'_move_4')
def value():
    return ('Dizzy Punch',70,100,'Physical','Normal',0,['contact'])

@Increment(Kangaskhan)
def move_4(self): # Dizzy Punch
    damage_ret=self.get_damage()
    if not damage_ret['miss']:
        damage=damage_ret['damage']
        self.target.take_damage(damage) 
        if not self.target.isfaint() and rnd()<20/100:
            self.target.set_boost('spa',-1)
