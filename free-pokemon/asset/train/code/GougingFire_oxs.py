from engine import *


class GougingFire(PokemonBase):
    _species='Gouging-Fire'
    _types=['Fire','Dragon']
    _gender='Genderless'
    _ability=['Protosynthesis']
    _move_1=('Scale Shot',25,90,'Physical','Dragon',0,[])
    _move_2=('Flare Blitz',120,100,'Physical','Fire',0,['contact'])
    def __init__(self):
        super().__init__()

    def onswitch(self):
        t=max([(k,v) for k,v in self['stats'].items()],key=lambda x:x[1])[0]
        self.set_stat(t,1.5 if t=='spe' else 1.3)

    def move_1(self): # Scale Shot
        hit=True; i=0
        r=rnd()
        if r<0.35:
            n_hits=2
        elif r<0.7:
            n_hits=3
        elif r<0.85:
            n_hits=4
        else:
            n_hits=5
        while hit and i<n_hits:
            attack_ret=self.attack()
            if attack_ret['miss'] or attack_ret['immune']: break
            damage_ret=self.get_damage()
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            i+=1; hit=False if self.target.isfaint() else True
        self.set_boost('def',-1,'self')
        self.set_boost('spe',+1,'self')

    def move_2(self): # Flare Blitz
        attack_ret=self.attack()
        if not (attack_ret['miss'] or attack_ret['immune']):
            damage_ret=self.get_damage()
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            self.take_damage(int(0.33*damage),'recoil')
            if not self.target.isfaint() and rnd()<10/100: self.target.set_status('BRN')

# ----------

@Increment(GougingFire,'_move_3')
def value():
    return ('Morning Sun',0,100000,'Status','Normal',0,[])

@Increment(GougingFire)
def move_3(self): # Morning Sun
    if not any([self.env.get(x) for x in ['Sunlight','Rain','Sandstorm','Snow']]):
        self.restore(self['max_hp']//2,'heal')
    elif self.env.get('Sunlight'):
        self.restore(self['max_hp']//3*2,'heal')
    else:
        self.restore(self['max_hp']//4,'heal')

# ----------

@Increment(GougingFire,'_move_4')
def value():
    return ('Solar Claw',80,100,'Physical','Grass',0,['contact'])

@Increment(GougingFire)
def move_4(self): # Solar Claw
    attack_ret=self.attack()
    if not (attack_ret['miss'] or attack_ret['immune']):
        damage_ret=self.get_damage()
        damage=damage_ret['damage']
        self.target.take_damage(damage)
        if self.env.get('Sunlight'):
            self.set_boost('atk',+1,'self')

# ----------

@Increment(GougingFire,'_move_5')
def value():
    return ('Iron Defense',0,100000,'Status','Steel',0,[])

@Increment(GougingFire)
def move_5(self): # Iron Defense
    self.set_boost('def',+2,'self')
