from engine import *


class Xenonova(PokemonBase):
    _species='Xenonova'
    _types=['Dragon','Fire']
    _gender='Male'
    _ability=['Reckless Power']
    _move_1=('Explosive Beam',100,90,'Special','Fire',0,[])
    _move_2=('Trample',120,95,'Physical','Dragon',0,[])
    def __init__(self):
        super().__init__()

    def get_power(self):        
        power=self['act']['power']
        power*=1.3
        return int(power*self.get_weather_power_mult())

    def move_1(self): # Explosive Beam
        damage_ret=self.get_damage()
        if not damage_ret['miss']:
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            if rnd()<30/100:
                self.target.set_status('BRN')
            self.take_damage(int(0.15*damage),'recoil')
    
    def move_2(self): # Trample
        damage_ret=self.get_damage()
        if not damage_ret['miss']:
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            if rnd()<20/100:
                self.target.set_condition('FLINCH',counter=0)
            self.take_damage(int(0.15*damage),'recoil')

# ----------

@Increment(Xenonova,'_move_3')
def value():
    return ('Will-O-Wisp',0,85,'Status','Fire',0,[])

@Increment(Xenonova)
def move_3(self): # Will-O-Wisp
    damage_ret=self.get_damage()
    if not damage_ret['miss']:
        self.target.set_status('BRN')

# ----------

@Increment(Xenonova,'_move_4')
def value():
    return ('Dragon Dance',0,100000,'Status','Dragon',0,[])

@Increment(Xenonova)
def move_4(self): # Dragon Dance
    self.set_boost('atk',+1,'self')
    self.set_boost('spe',+1,'self')

# ----------

@Increment(Xenonova,'_ability')
def value():
    return ['Reckless Power','Unstable Energy']

@Increment(Xenonova)
def endturn(self):
    if rnd()<20/100:
        self.target.set_condition('CONFUSION',counter=0)
