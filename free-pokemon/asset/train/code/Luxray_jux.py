from engine import *


class Luxray(PokemonBase):
    _species='Luxray'
    _types=['Electric']
    _gender='Male'
    _ability=['Guts']
    _move_1=('Wild Charge',90,100,'Physical','Electric',0,['contact'])
    _move_2=('Crunch',80,100,'Physical','Dark',0,['contact'])
    def __init__(self):
        super().__init__()

    def get_other_mult(self):
        return 1.
    
    def get_stat(self,key,boost=None):
        stat=self['stats'][key]
        boost=self['boosts'][key] if not boost else boost
        stat_ratio={0:1,1:1.5,2:2,3:2.5,4:3,5:3.5,6:4}[min(6,abs(boost))]
        if boost<0:
            stat_ratio=1/stat_ratio
        stat_ratio*=self.get_weather_stat_mult(key)
        if key=='spe' and self.isstatus('PAR'):
            stat_ratio*=0.5
        if key=='atk' and self['status']:
            stat_ratio*=1.5
        return int(stat*stat_ratio)

    def move_1(self): # Wild Charge  
        attack_ret=self.attack()
        if not (attack_ret['miss'] or attack_ret['immune']):
            damage_ret=self.get_damage()
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            recoil_damage=int(damage*0.25)
            self.take_damage(recoil_damage,'recoil')

    def move_2(self): # Crunch
        attack_ret=self.attack()
        if not (attack_ret['miss'] or attack_ret['immune']):
            damage_ret=self.get_damage()
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            if not self.target.isfaint() and rnd()<20/100:
                self.target.set_boost('def',-1)

# ----------

@Increment(Luxray,'_move_3')
def value():
    return ('Ice Fang',65,95,'Physical','Ice',0,['contact'])

@Increment(Luxray)
def move_3(self): # Ice Fang
    attack_ret=self.attack()
    if not (attack_ret['miss'] or attack_ret['immune']):
        damage_ret=self.get_damage()
        damage=damage_ret['damage']
        self.target.take_damage(damage)
        if not self.target.isfaint():
            if rnd()<10/100:
                self.target.set_condition('Flinch',counter=0)
            if rnd()<10/100: 
                self.target.set_status('FRZ')
