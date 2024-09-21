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
        attack_ret=self.attack()
        if not (attack_ret['miss'] or attack_ret['immune']):
            damage_ret=self.get_damage()
            damage=damage_ret['damage']
            self.target.take_damage(damage)

    def move_2(self): # Body Press
        attack_ret=self.attack()
        if not (attack_ret['miss'] or attack_ret['immune']):
            damage_ret=self.get_damage()
            damage=damage_ret['damage']
            self.target.take_damage(damage)

# ----------

@Increment(Zamazenta,'_move_3')
def value():
    return ('Iron Defense',0,100000,'Status','Steel',0,[])

@Increment(Zamazenta)
def move_3(self): # Play Rough
    attack_ret=self.attack()
    if not (attack_ret['miss'] or attack_ret['immune']):
        damage_ret=self.get_damage()
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
    self._set_boost(key,x)
    if x>0 and key=='def':
        for _ in range(x):
            self.restore(self['max_hp']//10,'heal')

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
