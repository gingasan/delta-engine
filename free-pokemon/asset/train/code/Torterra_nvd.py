from engine import *


class Torterra(PokemonBase):
    _species='Torterra'
    _types=['Grass','Ground']
    _gender='Male'
    _ability=['Anger Shell']
    _move_1=('Earth Power',90,100,'Special','Ground',0,[])
    _move_2=('Giga Drain',75,100,'Special','Grass',0,[])
    def __init__(self):
        super().__init__()

    def get_stat(self,key,boost=None):
        stat=self['stats'][key]
        boost=self['boosts'][key] if not boost else boost
        stat_ratio={0:1,1:1.5,2:2,3:2.5,4:3,5:3.5,6:4}[min(6,abs(boost))]
        if boost<0:
            stat_ratio=1/stat_ratio
        stat_ratio*=self.get_weather_stat_mult(key)
        if key=='spe' and self.isstatus('PAR'):
            stat_ratio*=0.5
        if self['hp']<=self['max_hp']//2:
            if key in ['atk','spa','spe']:
                stat_ratio*=1.25
            elif key in ['def','spd']:
                stat_ratio*=0.75
        return int(stat*stat_ratio)

    def take_damage(self,x,from_='attack'):
        prev_hp=self['hp']
        if from_=='attack':
            self._take_damage_attack(x)
        elif from_=='loss':
            self.take_damage_loss(x)
        elif from_=='recoil':
            self.take_damage_recoil(x)
        if self['hp']==0:
            self._faint()
            return
        if prev_hp>self['max_hp']//2 and self['hp']<=self['max_hp']//2:
            self.set_boost('atk',+1,'self')
            self.set_boost('spa',+1,'self')
            self.set_boost('spe',+1,'self')
            self.set_boost('def',-1)
            self.set_boost('spd',-1)

    def move_1(self): # Earth Power
        attack_ret=self.attack()
        if not (attack_ret['miss'] or attack_ret['immune']):
            damage_ret=self.get_damage()
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            if not self.target.isfaint() and rnd()<10/100:
                self.target.set_boost('spd',-1)

    def move_2(self): # Giga Drain
        attack_ret=self.attack()
        if not (attack_ret['miss'] or attack_ret['immune']):
            damage_ret=self.get_damage()
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            self.restore(int(1/2*damage),'drain')
