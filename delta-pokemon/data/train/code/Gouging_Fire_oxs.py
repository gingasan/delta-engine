from engine import *


class Gouging_Fire(PokemonBase):
    _species='Gouging Fire'
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
            damage_ret=self.get_damage()
            if damage_ret['miss']: break
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            i+=1; hit=False if self.target.isfaint() else True
        self.set_boost('def',-1,'self')
        self.set_boost('spe',+1,'self')

    def move_2(self): # Flare Blitz
        damage_ret=self.get_damage()
        if not damage_ret['miss']:
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            self.take_damage(int(0.33*damage),'recoil')
            if not self.target.isfaint() and rnd()<10/100: self.target.set_status('BRN')

# -------------------------------------------------------------

@Increment(Gouging_Fire,'_move_3')
def value():
    return ('Morning Sun',0,100000,'Status','Normal',0,[])

@Increment(Gouging_Fire)
def move_3(self): # Morning Sun
    if not any([x in self.env for x in ['SUNNYDAY','RAINDANCE','SANDSTORM','SNOW','HAIL']]):
        self.restore(self['max_hp']//2,'heal')
    elif self.env.get('SUNNYDAY'):
        self.restore(self['max_hp']//3*2,'heal')
    else:
        self.restore(self['max_hp']//4,'heal')

# -------------------------------------------------------------

@Increment(Gouging_Fire,'_move_4')
def value():
    return ('Solar Claw',80,100,'Physical','Grass',0,['contact'])

@Increment(Gouging_Fire)
def move_4(self): # Solar Claw
    damage_ret=self.get_damage()
    if not damage_ret['miss']:
        damage=damage_ret['damage']
        self.target.take_damage(damage)
        if self.env.get('SUNNYDAY'):
            self.set_boost('atk',+1,'self')

# -------------------------------------------------------------

@Increment(Gouging_Fire,'_move_5')
def value():
    return ('Iron Defense',0,100000,'Status','Steel',0,[])

@Increment(Gouging_Fire)
def move_5(self): # Iron Defense
    self.set_boost('def',+2,'self')
