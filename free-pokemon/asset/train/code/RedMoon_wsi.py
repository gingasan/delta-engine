from engine import *


class RedMoon(PokemonBase):
    _species='Red-Moon'
    _types=['Dragon','Flying']
    _gender='Male'
    _ability=['Intimidate']
    _move_1=('Dragon Claw',80,100,'Physical','Dragon',0,['contact'])
    _move_2=('Brave Bird',120,100,'Physical','Flying',0,['contact'])
    def __init__(self):
        super().__init__()

    def onswitch(self):
        self.target.set_boost('atk',-1)
        self.env.set_side_condition('Tailwind',self.side_id,from_=self._species,counter=0,max_count=3)
    
    def get_stat(self,key,boost=None):
        stat=self['stats'][key]
        boost=self['boosts'][key] if not boost else boost
        stat_ratio={0:1,1:1.5,2:2,3:2.5,4:3,5:3.5,6:4}[min(6,abs(boost))]
        if boost<0:
            stat_ratio=1/stat_ratio
        stat_ratio*=self.get_weather_stat_mult(key)
        if key=='spe' and self.isstatus('PAR'):
            stat_ratio*=0.5
        if key=='spe' and self.env.get_side_condition('Tailwind',self.side_id):
            stat_ratio*=2
        return int(stat*stat_ratio)

    def move_1(self): # Dragon Claw
        attack_ret=self.attack()
        if not (attack_ret['miss'] or attack_ret['immune']):
            damage_ret=self.get_damage()
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            if not self.target.isfaint() and rnd()<10/100:
                self.target.set_condition('Flinch',counter=0)
    
    def move_2(self): # Brave Bird  
        attack_ret=self.attack()
        if not (attack_ret['miss'] or attack_ret['immune']):
            damage_ret=self.get_damage()
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            self.take_damage(int(0.33*damage),'recoil')
            if not self.isfaint() and rnd()<20/100:
                self.set_boost('def',1,'self')

# ----------

@Increment(RedMoon,'_move_3')
def value():
    return ('Lunar Strike',90,90,'Special','Dragon',0,[])

@Increment(RedMoon)
def move_3(self): # Lunar Strike
    attack_ret=self.attack()
    if not (attack_ret['miss'] or attack_ret['immune']):
        damage_ret=self.get_damage()
        damage=damage_ret['damage']
        self.target.take_damage(damage)
        if not self.target.isfaint() and rnd()<15/100:
            self.target.set_condition('Confusion',counter=0)

# ----------

@Increment(RedMoon,'_move_4')
def value():
    return ('Wind Cutter',60,100,'Physical','Flying',0,['contact'])

@Increment(RedMoon)
def move_4(self): # Wind Cutter
    hit=True; i=0
    while hit and i<2:
        attack_ret=self.attack()
        if attack_ret['miss'] or attack_ret['immune']: break
        damage_ret=self.get_damage()
        damage=damage_ret['damage']
        self.target.take_damage(damage)
        i+=1; hit=False if self.target.isfaint() else True

# ----------

@Increment(RedMoon,'_ability')
def value():
    return ['Intimidate','Eclipse Guard']

@Increment(RedMoon)
def take_damage_attack(self,x):
    self.register_act_taken()
    if self['hp']<self['max_hp']//2 and self['act_taken']['type']=='Fairy':
        x//=2
    self._set_hp(-x)    

# ----------

@Increment(RedMoon,'_move_5')
def value():
    return ('Healing Roar',0,100,'Status','Dragon',1,[])

@Increment(RedMoon)
def move_5(self): # Healing Roar
    self.restore(self['max_hp']//2,'heal')
    self.set_boost('spd',-1)
