from engine import *


class Dragomir(PokemonBase):
    _species='Dragomir'
    _types=['Dragon','Psychic']
    _gender='Male'
    _ability=['Mystic Eyes']
    _move_1=('Legend Strike',90,100,'Physical','Dragon',0,[])
    _move_2=('Mind Shatter',70,100,'Special','Psychic',0,[])
    def __init__(self):
        super().__init__()

    def set_boost(self,key,x,from_='target'):
        bar=6 if key in ['atk','def','spa','spd','spe'] else 3
        if x>0:
            self['boosts'][key]=min(bar,self['boosts'][key]+x)
            self.log("{}'s {} is raised by {}.".format(self._species,{
                'atk':'Attack','def':'Defense','spa':'Special Attack','spd':'Special Defense','spe':'Speed'}[key],x))
    
    def move_1(self): # Legend Strike
        damage_ret=self.get_damage()
        if not damage_ret['miss']:
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            if not self.target.isfaint() and rnd()<20/100: self.target.set_condition('CONFUSION',counter=0)
    
    def move_2(self): # Mind Shatter
        damage_ret=self.get_damage()
        if not damage_ret['miss']:
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            if not self.target.isfaint() and rnd()<30/100: self.target.set_boost('spd',-1)

# -------------------------------------------------------------

@Increment(Dragomir,'_move_3')
def value():
    return ('Recover',0,100000,'Status','Normal',0,[])

@Increment(Dragomir)
def move_3(self): # Recover
    self.restore(self['max_hp']//2,'heal')

# -------------------------------------------------------------

@Increment(Dragomir,'_move_4')
def value():
    return ('Psychic Blast',100,95,'Special','Psychic',0,[])

@Increment(Dragomir)
def move_4(self): # Psychic Blast
    damage_ret=self.get_damage()
    if not damage_ret['miss']:
        damage=damage_ret['damage']
        self.target.take_damage(damage)
        if not self.target.isfaint() and rnd()<10/100: self.target.set_status('PAR')

# -------------------------------------------------------------

@Increment(Dragomir,'_ability')
def value():
    return ['Mystic Eyes','Focused Destruction']

@Increment(Dragomir)
def endturn(self):
    self.target.set_boost(rndc(['atk','def','spa','spd','spe']),-1)
