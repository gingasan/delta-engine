from engine import *


class Zamazenta(PokemonBase):
    _species='Zamazenta'
    _types=['Steel','Fighting']
    _gender='Male'
    _ability=['Dauntless Shield']
    _move_1=('Behemoth Bash',100,100,'Physical','Steel',0,['contact'])
    _move_2=('Play Rough',90,90,'Physical','Fairy',0,['contact'])
    def __init__(self):
        super().__init__()

    def onswitch(self):
        self.set_boost('def',1,'self')

    def get_base_damage(self,power,crit):
        if self['act']['id']=='Body Press':
            atk_boost=self['boosts']['def']
        else:
            atk_boost=self['boosts']['atk'] if self['act']['category']=='Physical' else self['boosts']['spa']
        def_boost=self.target['boosts']['def'] if self['act']['category']=='Physical' else self.target['boosts']['spd']
        
        if crit:
            atk_boost=max(0,atk_boost)
            def_boost=min(0,def_boost)

        if self['act']['id']=='Body Press':
            attack=self.get_stat('def',atk_boost)
        else:
            attack=self.get_stat('atk' if self['act']['category']=='Physical' else 'spa',atk_boost)
        defense=self.target.get_stat('def' if self['act']['category']=='Physical' else 'spd',def_boost)

        level=100
        base_damage=int(int(int(int(2*level/5+2)*power*attack)/defense)/50)+2

        return base_damage
    
    def move_1(self): # Behemoth Bash
        damage_ret=self.get_damage()
        if not damage_ret['miss']:
            damage=damage_ret['damage']
            self.target.take_damage(damage)

    def move_2(self): # Body Press
        damage_ret=self.get_damage()
        if not damage_ret['miss']:
            damage=damage_ret['damage']
            self.target.take_damage(damage)

# ----------

@Increment(Zamazenta,'_move_3')
def value():
    return ('Iron Defense',0,100000,'Status','Steel',0,[])

@Increment(Zamazenta)
def move_3(self): # Play Rough
    damage_ret=self.get_damage()
    if not damage_ret['miss']:
        damage=damage_ret['damage']
        self.target.take_damage(damage)
        if not self.target.isfaint() and rnd()<10/100: self.target.set_boost('atk',-1)

# ----------

@Increment(Zamazenta,'_move_4')
def value():
    return ('Body Press',80,100,'Physical','Fighting',0,['contact'])

@Increment(Zamazenta)
def move_4(self): # Iron Defense
    self.set_boost('def',2,'self')

# ----------

@Increment(Zamazenta,'_ability')
def value():
    return ['Dauntless Shield','Shield Bash']

@Increment(Zamazenta)
def set_boost(self,key,x,from_='target'):
    bar=6 if key in ['atk','def','spa','spd','spe'] else 3
    if x>0:
        self['boosts'][key]=min(bar,self['boosts'][key]+x)
        if key=='def':
            for _ in range(x):
                self.restore(self['max_hp']//10,'heal')
    else:
        self['boosts'][key]=max(-bar,self['boosts'][key]+x)
    self.log(script='boost',species=self._species,key=key,x=x)

# ----------

@Increment(Zamazenta,'_move_5')
def value():
    return ('Rest',0,100000,'Status','Psychic',0,[])

@Increment(Zamazenta)
def move_5(self): # Rest
    if not self.isstatus('SLP') and self['hp']<self['max_hp']:
        self.state['status']=None
        self.set_status('SLP')
        self.state['hp']=self['max_hp']
