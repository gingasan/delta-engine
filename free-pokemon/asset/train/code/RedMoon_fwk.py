from engine import *


class RedMoon(PokemonBase):
    _species='Red-Moon'
    _types=['Dragon','Flying']
    _gender='Male'
    _ability=['Tailwind']
    _move_1=('Dragon Rush',100,95,'Physical','Dragon',0,['contact'])
    _move_2=('Fly',90,100,'Physical','Flying',0,['contact'])
    def __init__(self):
        super().__init__()

    def onswitch(self):
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

    def get_evasion(self):
        if  self['conditions'].get('FLY'):
            return 0
        return 1

    def move_1(self): # Dragon Rush
        attack_ret=self.attack()
        if not (attack_ret['miss'] or attack_ret['immune']):
            damage_ret=self.get_damage()
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            if not self.target.isfaint() and rnd()<20/100: self.target.set_condition('Flinch',counter=0)
        recoil_damage=int(self['max_hp']//3)
        self.take_damage(recoil_damage,'recoil')

    def move_2(self): # Fly
        if not self['conditions'].get('FLY'):
            self.set_condition('FLY',counter=0)
            self.state['canact']='Fly'
        else:
            del self['conditions']['FLY']
            self.state['canact']=True
            attack_ret=self.attack()
            if not (attack_ret['miss'] or attack_ret['immune']):
                damage_ret=self.get_damage()
                damage=damage_ret['damage']
                self.target.take_damage(damage)
