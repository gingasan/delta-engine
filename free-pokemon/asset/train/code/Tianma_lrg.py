from engine import *


class Tianma(PokemonBase):
    _species='Tianma'
    _types=['Flying','Fairy']
    _gender='Neutral'
    _ability=['Heavenly Speed']
    _move_1=('Skybound Rush',100,100000,'Physical','Flying',0,[])
    _move_2=('Jade Strike',90,100,'Physical','Rock',0,[])
    def __init__(self):
        super().__init__()

    def onswitch(self):
        self.set_condition('HEAVENLY_SPEED',counter=0)

    def endturn(self):
        if self['conditions'].get('HEAVENLY_SPEED'):
            self['conditions']['HEAVENLY_SPEED']['counter']+=1
            if self['conditions']['HEAVENLY_SPEED']['counter']==5:
                del self['conditions']['HEAVENLY_SPEED']
        if self.target['conditions'].get('DIZZY'):
            self.target['conditions']['DIZZY']['counter']+=1
            if self.target['conditions']['DIZZY']['counter']==2:
                if rnd()<0.3:
                   self.target.set_status('SLP')
                del self.target['conditions']['DIZZY']

    def get_stat(self,key,boost=None):
        stat=self['stats'][key]
        boost=self['boosts'][key] if boost is None else boost
        stat_ratio={0:1,1:1.5,2:2,3:2.5,4:3,5:3.5,6:4}[min(6,abs(boost))]
        if boost<0:
            stat_ratio=1/stat_ratio
        stat_ratio*=self.get_weather_stat_mult(key)
        if key=='spe' and self.isstatus('PAR'):
            stat_ratio*=0.5
        if key=='spe' and self['conditions'].get('HEAVENLY_SPEED'):
            stat_ratio*=2
        return int(stat*stat_ratio)

    def move_1(self): # Skybound Rush
        damage_ret=self.get_damage()
        if not damage_ret['miss']:
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            if rnd()<0.2:
                self.set_boost('spe',+1,'self')

    def move_2(self): # Jade Strike
        damage_ret=self.get_damage()
        if not damage_ret['miss']:
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            if not self.target.isfaint():
                if rnd()<0.3:
                    self.target.set_condition('DIZZY',counter=0)

# ----------

@Increment(Tianma,'_move_3')
def value():
    return ('Celestial Barrier',0,100000,'Status','Fairy',0,[])

@Increment(Tianma)
def move_3(self): # Celestial Barrier
    self.set_boost('def',+2,'self')
    self.set_boost('spd',+2,'self')

# ----------

@Increment(Tianma,'_ability')
def value():
    return ['Heavenly Speed','Divine Flight']

@Increment(Tianma)
def _take_damage_attack(self,x):
    if 'type_effect' in self.target['act'] and self.target['act']['type_effect']<0.1:
        self.logger.log('It is immune by %s.'%self._species)
        return
    self.register_act_taken()
    if self['act_taken']['type']=='Ground':
        return
    self.state['hp']=max(0,self['hp']-x)
    self.log(script='attack',species=self._species,x=x,**self['act_taken'])

@Increment(Tianma)
def get_evasion(self):
    return 1.2
