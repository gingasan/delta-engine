from engine import *


class Mew(PokemonBase):
    _species='Mew'
    _types=['Psychic']
    _gender='Genderless'
    _ability=['Moody']
    _move_1=('Psychic',90,100,'Special','Psychic',0,[])
    _move_2=('Play Rough',90,90,'Physical','Fairy',0,['contact'])
    def __init__(self):
        super().__init__()
    
    def endturn(self):
        t1,t2=rndc(['atk','def','spa','spd','spe'],2)
        self.set_boost(t1,+2)
        self.set_boost(t2,-1)

    def move_1(self): # Psychic
        damage_ret=self.get_damage()
        if not damage_ret['miss']:
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            if not self.target.isfaint() and rnd()<0.1:
                self.target.set_boost('spd',-1)
    
    def move_2(self): # Play Rough
        damage_ret=self.get_damage()
        if not damage_ret['miss']:
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            if not self.target.isfaint() and rnd()<0.1:
                self.target.set_boost('atk',-1)

# -------------------------------------------------------------

@Increment(Mew,'_move_3')
def value():
    return ('Astral Beam',120,85,'Special','Psychic',0,[])

@Increment(Mew)
def move_3(self): # Astral Beam
    damage_ret=self.get_damage()
    if not damage_ret['miss']:
        damage=damage_ret['damage']
        self.target.take_damage(damage)
        if not self.target.isfaint() and rnd()<0.2:
            self.target.set_condition('CONFUSION',counter=0)

# -------------------------------------------------------------

@Increment(Mew,'_move_4')
def value():
    return ('Mind Shield',0,1000000,'Status','Psychic',0,[])

@Increment(Mew)
def move_4(self): # Mind Shield
    self.set_boost('def',+1,'self')
    self.set_boost('spd',+1,'self')

# -------------------------------------------------------------

@Increment(Mew,'_ability')
def value():
    return ['Moody','Mirage Shield']

@Increment(Mew)
def _take_damage_attack(self,x):
    if 'type_efc' in self.target['act'] and self.target['act']['type_efc']<0.1:
        self.logger.log('It is immune by %s.'%self._species)
        return
    self.register_act_taken()
    if x>self['max_hp']//2:
        x//=2
    self.state['hp']=max(0,self['hp']-x)
    self.log('{} loses {} HP.'.format(self._species,x),act_taken=self['act_taken'])
