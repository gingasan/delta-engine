from engine import *


class Scizor(PokemonBase):
    _species='Scizor'
    _types=['Bug','Steel']
    _gender='Male'
    _ability=['Technician']
    _move_1=('Steel Cutter',20,95,'Physical','Steel',0,['contact'])
    _move_2=('Quik Pinch',45,100,'Physical','Bug',1,['contact'])
    def __init__(self):
        super().__init__()

    def get_power(self):
        power=self['act']['power']
        if power<=60:
            power=power*1.5
        return int(power*self.get_weather_power_mult())

    def move_1(self): # Steel Cutter
        hit=True
        i=0
        while hit and i<5:
            damage_ret=self.get_damage()
            if damage_ret['miss']: break
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            if not self.target.isfaint() and rnd()<30/100:
                self.target.set_boost('def',-1)
            i+=1
            hit=False if self.target.isfaint() else True
            
    def move_2(self): # Quik Pinch
        self.set_boost('spe',1,'self')
        damage_ret=self.get_damage()
        if not damage_ret['miss']:
            damage=damage_ret['damage']
            self.target.take_damage(damage)

# -------------------------------------------------------------

@Increment(Scizor,'_move_3')
def value():
    return ('Iron Buzz',50,95,'Special','Steel',0,[])

@Increment(Scizor)
def move_3(self): # Iron Buzz
    damage_ret=self.get_damage()
    if not damage_ret['miss']:
        damage=damage_ret['damage']
        self.target.take_damage(damage)
        if not self.target.isfaint() and rnd()<0.2:
            self.target.set_condition('CONFUSION',counter=0)

# -------------------------------------------------------------

@Increment(Scizor,'_move_4')
def value():
    return ('Bug Echo',40,100,'Special','Bug',1,[])

@Increment(Scizor)
def move_4(self): # Bug Echo
    damage_ret=self.get_damage()
    if not damage_ret['miss']:
        damage=damage_ret['damage']
        self.target.take_damage(damage)

# -------------------------------------------------------------

@Increment(Scizor,'_ability')
def value():
    return ['Technician','Metalic Surge']

@Increment(Scizor)
def onswitch(self):
    self.set_boost('spe',1,'self')

# -------------------------------------------------------------

@Increment(Scizor,'_move_5')
def value():
    return ('Sharp Agility',0,100000,'Status','Normal',0,[])

@Increment(Scizor)
def move_5(self): # Sharp Agility
    self.set_boost('spe',1,'self')
    self.set_boost('accuracy',1,'self')
