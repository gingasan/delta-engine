from engine import *


class Metagross(PokemonBase):
    _species='Metagross'
    _types=['Steel','Psychic']
    _gender='Genderless'
    _ability=['Clear Body']
    _move_1=('Psychic Fangs',85,100,'Physical','Psychic',0,['contact'])
    _move_2=('Bullet Punch',40,100,'Physical','Steel',1,['contact'])
    def __init__(self):
        super().__init__()

    def set_boost(self,key,x,from_='target'):
        if x<0 and from_=='target':
            self.log("Metagross's stats cannot be lowered by opponents.")
            return
        bar=6 if key in ['atk','def','spa','spd','spe'] else 3
        if x>0:
            self['boosts'][key]=min(bar,self['boosts'][key]+x)
        else:
            self['boosts'][key]=max(-bar,self['boosts'][key]+x)
        self.log("{}'s {} is {} by {}.".format(self._species,{
            'atk':'Attack','def':'Defense','spa':'Special Attack','spd':'Special Defense','spe':'Speed'}[key],'raised' if x>0 else 'lowered',x))

    def move_1(self): # Psychic Fangs
        damage_ret=self.get_damage()
        if not damage_ret['miss']:
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            for t in ['REFLECT','LIGHT_SCREEN','AURORA_VEIL']:
                if self.target['side_conditions'].get(t):
                    del self.target['side_conditions'][t]

    def move_2(self): # Bullet Punch
        damage_ret=self.get_damage()
        if not damage_ret['miss']:
            damage=damage_ret['damage']
            self.target.take_damage(damage)

# -------------------------------------------------------------

@Increment(Metagross,'_move_3')
def value():
    return ('Meteor Mash',90,90,'Physical','Steel',0,['contact'])

@Increment(Metagross)
def move_3(self): # Meteor Mash
    damage_ret=self.get_damage()
    if not damage_ret['miss']:
        damage=damage_ret['damage']
        self.target.take_damage(damage)
        if rnd()<20/100:
            self.set_boost('atk',+1,'self')

# -------------------------------------------------------------

@Increment(Metagross,'_move_4')
def value():
    return ('Earthquake',100,100,'Physical','Ground',0,[])

@Increment(Metagross)
def move_4(self): # Earthquake
    damage_ret=self.get_damage()
    if not damage_ret['miss']:
        damage=damage_ret['damage']
        self.target.take_damage(damage)
