from engine import *


class Tropius(PokemonBase):
    _species='Tropius'
    _types=['Grass','Flying']
    _gender='Male'
    _ability=['Solar Power']
    _move_1=('Calm Mind',0,100000,'Status','Psychic',0,[])
    _move_2=('Air Slash',75,95,'Special','Flying',0,[])
    def __init__(self):
        super().__init__()

    def get_weather_stat_mult(self,key):
        if self.env.get('Sandstorm') and key=='spd' and 'Rock' in self['types']:
            return 1.5
        if self.env.get('Snow') and key=='def' and 'Ice' in self['types']:
            return 1.5
        if self.env.get('Sunlight') and key=='spa':
            return 1.5
        return 1.

    def endturn(self):
        if self.env.get('Sunlight'):
            self.take_damage(self['max_hp']//8,'loss')
    
    def move_1(self): # Calm Mind
        self.set_boost('spa',+1,'self')
        self.set_boost('spd',+1,'self')
    
    def move_2(self): # Air Slash
        attack_ret=self.attack()
        if not (attack_ret['miss'] or attack_ret['immune']):
            damage_ret=self.get_damage()
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            if not self.target.isfaint() and rnd()<30/100:
                self.target.set_condition('Flinch',counter=0)

# ----------

@Increment(Tropius,'_move_3')
def value():
    return ('Giga Drain',75,100,'Special','Grass',0,[])

@Increment(Tropius)
def move_3(self): # Giga Drain
    attack_ret=self.attack()
    if not (attack_ret['miss'] or attack_ret['immune']):
        damage_ret=self.get_damage()
        damage=damage_ret['damage']
        self.target.take_damage(damage)
        self.restore(int(1/2*damage),'drain')

# ----------

@Increment(Tropius,'_move_4')
def value():
    return ('Rest',0,100000,'Status','Psychic',0,[])

@Increment(Tropius)
def move_5(self): # Rest
    if not self.isstatus('SLP') and self['hp']<self['max_hp']:
        self.state['status']=None
        self.set_status('SLP')
        self.state['hp']=self['max_hp']
