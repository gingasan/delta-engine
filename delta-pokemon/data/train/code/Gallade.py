from engine import *


class Gallade(PokemonBase):
    _species='Gallade'
    _types=['Psychic','Fighting']
    _gender='Male'
    _ability=['Sharpness']
    _move_1=('Psycho Cut',70,100,'Physical','Psychic',0,['slicing'])
    _move_2=('Sacred Sword',90,100,'Physical','Fighting',0,['contact','slicing'])
    def __init__(self):
        super().__init__()

    def get_power(self):        
        power=self['act']['power']
        if 'slicing' in self['act']['property']:
            power*=1.5
        return int(power*self.get_weather_power_mult())

    def get_crit(self):
        crit_mult=[0,24,8,2,1]
        crit_ratio=self['boosts']['crit']
        if self['act']['id']=='Psycho Cut':
            crit_ratio=min(3,crit_ratio+1)
        crit=False
        if rnd()*crit_mult[crit_ratio+1]<1:
            crit=True
        return crit

    def move_1(self): # Psycho Cut
        damage_ret=self.get_damage()
        if not damage_ret['miss']:
            damage=damage_ret['damage']
            self.target.take_damage(damage)

    def move_2(self): # Sacred Sword
        damage_ret=self.get_damage()
        if not damage_ret['miss']:
            damage=damage_ret['damage']
            self.target.take_damage(damage)

    def _get_base_damage(self,power,crit):
        atk_boost=self['boosts']['atk'] if self['act']['category']=='Physical' else self['boosts']['spa']
        if self['act']['id']=='Sacred Sword':
            def_boost=0
        else:
            def_boost=self.target['boosts']['def'] if self['act']['category']=='Physical' else self.target['boosts']['spd']

        if crit:
            atk_boost=max(0,atk_boost)
            def_boost=min(0,def_boost)

        attack=self.get_stat('atk' if self['act']['category']=='Physical' else 'spa',atk_boost)
        defense=self.target.get_stat('def' if self['act']['category']=='Physical' else 'spd',def_boost)

        level=100
        base_damage=int(int(int(int(2*level/5+2)*power*attack)/defense)/50)+2

        return base_damage

# -------------------------------------------------------------

@Increment(Gallade,'_move_3')
def value():
    return ('Swords Dance',0,100000,'Status','Normal',0,[])

@Increment(Gallade)
def move_3(self): # Swords Dance
    self.set_boost('atk',+2,'self')

# -------------------------------------------------------------

@Increment(Gallade,'_move_4')
def value():
    return ('Leaf Blade',90,100,'Physical','Grass',0,['contact','slicing'])

@Increment(Gallade)
def get_crit(self):
    crit_mult=[0,24,8,2,1]
    crit_ratio=self['boosts']['crit']
    if self['act']['id']=='Psycho Cut' or self['act']['id']=='Leaf Blade':
        crit_ratio=min(3,crit_ratio+1)
    crit=False
    if rnd()*crit_mult[crit_ratio+1]<1:
        crit=True
    return crit

@Increment(Gallade)
def move_4(self): # Leaf Blade
    damage_ret=self.get_damage()
    if not damage_ret['miss']:
        damage=damage_ret['damage']
        self.target.take_damage(damage)

# -------------------------------------------------------------

@Increment(Gallade,'_ability')
def value():
    return ['Sharpness','Sharpness II']

@Increment(Gallade)
def get_priority(self,move_id):
    if 'slicing' in self._moves[move_id]['property']:
        return self._moves[move_id]['priority'] + 1
    return self._moves[move_id]['priority']

# -------------------------------------------------------------

@Increment(Gallade,'_move_5')
def value():
    return ('Drain Punch',75,100,'Physical','Fighting',0,['contact','punch'])

@Increment(Gallade)
def move_5(self): # Drain Punch
    damage_ret=self.get_damage()
    if not damage_ret['miss']:
        damage=damage_ret['damage']
        self.target.take_damage(damage)
        self.restore(int(1/2*damage),'drain')
