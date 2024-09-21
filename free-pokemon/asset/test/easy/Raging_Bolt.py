from engine import *


class Raging_Bolt(PokemonBase):
    _species='Raging Bolt'
    _types=['Electric','Dragon']
    _gender='Genderless'
    _ability=['Protosynthesis']
    _move_1=('Calm Mind',0,100000,'Status','Psychic',0,[])
    _move_2=('Dragon Pulse',85,100,'Special','Dragon',0,[])
    def __init__(self):
        super().__init__()

    def onswitch(self):
        if self.env.get('Sunlight'):
            t=max([(k,v) for k,v in self['stats'].items()],key=lambda x:x[1])[0]
            self.set_stat(t,1.5 if t=='spe' else 1.3)
    
    def move_1(self): # Calm Mind
        self.set_boost('spa',+1,'self')
        self.set_boost('spd',+1,'self')
    
    def move_2(self): # Dragon Pulse
        attack_ret=self.attack()
        if not (attack_ret['miss'] or attack_ret['immune']):
            damage_ret=self.get_damage()
            damage=damage_ret['damage']
            self.target.take_damage(damage)

# ----------

@Increment(Raging_Bolt,'_move_3')
def value():
    return ('Thunderbolt',90,100,'Special','Electric',0,[])

@Increment(Raging_Bolt)
def move_3(self): # Thunderbolt
    attack_ret=self.attack()
    if not (attack_ret['miss'] or attack_ret['immune']):
        damage_ret=self.get_damage()
        damage=damage_ret['damage']
        self.target.take_damage(damage)
        if not self.target.isfaint() and rnd()<10/100:
            self.target.set_status('PAR')
