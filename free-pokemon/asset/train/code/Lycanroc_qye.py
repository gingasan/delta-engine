from engine import *


class Lycanroc(PokemonBase):
    _species='Lycanroc'
    _types=['Rock']
    _gender='Male'
    _ability=['Tough Claws']
    _move_1=('Psychic Fangs',85,100,'Physical','Psychic',0,['contact'])
    _move_2=('Stone Edge',100,80,'Physical','Rock',0,['contact'])
    def __init__(self):
        super().__init__()

    def get_power(self):        
        power=self['act']['power']
        if 'contact' in self['act']['property']:
            power*=1.3
        return int(power*self.get_weather_power_mult())
    
    def get_crit(self):
        crit_mult=[0,24,8,2,1]
        crit_ratio=self['boosts']['crit']
        if self['act']['id']=='Stone Edge':
            crit_ratio=min(3,crit_ratio+1)
        crit=False
        if rnd()*crit_mult[crit_ratio+1]<1:
            crit=True
        return crit

    def move_1(self): # Psychic Fangs
        attack_ret=self.attack()
        if not (attack_ret['miss'] or attack_ret['immune']):
            damage_ret=self.get_damage()
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            for t in ['Reflect','Light Screen','Aurora Veil']:
                if self.env.get_side_condition(t,self.target.side_id):
                    self.env.remove(t,self.target.side_id)

    def move_2(self): # Stone Edge
        attack_ret=self.attack()
        if not (attack_ret['miss'] or attack_ret['immune']):
            damage_ret=self.get_damage()
            damage=damage_ret['damage']
            self.target.take_damage(damage)

# ----------

@Increment(Lycanroc,'_move_3')
def value():
    return ('Zen Headbutt',80,90,'Physical','Psychic',0,['contact'])

@Increment(Lycanroc)
def move_3(self): # Zen Headbutt
    attack_ret=self.attack()
    if not (attack_ret['miss'] or attack_ret['immune']):
        damage_ret=self.get_damage()
        damage=damage_ret['damage']
        self.target.take_damage(damage)
        if not self.target.isfaint() and rnd()<20/100:
            self.target.set_condition('Flinch',counter=0)

# ----------

@Increment(Lycanroc,'_move_4')
def value():
    return ('Earthquake',100,100,'Physical','Ground',0,[])

@Increment(Lycanroc)
def move_4(self): # Earthquake
    attack_ret=self.attack()
    if not (attack_ret['miss'] or attack_ret['immune']):
        damage_ret=self.get_damage()
        damage=damage_ret['damage']
        self.target.take_damage(damage)

# ----------

@Increment(Lycanroc,'_ability')
def value():
    return ['Tough Claws','Keen Eye']

@Increment(Lycanroc)
def set_boost(self,key,x,from_='target'):
    if key=='accuracy' and x<0 and from_=='target':
        return
    self._set_boost(key,x)

# ----------

@Increment(Lycanroc,'_move_5')
def value():
    return ('Swords Dance',0,100000,'Status','Normal',0,[])

@Increment(Lycanroc)
def move_5(self): # Swords Dance
    self.set_boost('atk',+2,'self')
