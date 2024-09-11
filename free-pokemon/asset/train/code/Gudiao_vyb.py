from engine import *


class Gudiao(PokemonBase):
    _species='Gudiao'
    _types=['Water','Flying']
    _gender='Genderless'
    _ability=['Abyssal Cry']
    _move_1=('Horn Surge',90,95,'Physical','Water',0,['contact'])
    _move_2=('Eerie Wail',70,100,'Special','Ghost',0,[])
    def __init__(self):
        super().__init__()

    def move_1(self): # Horn Surge
        damage_ret=self.get_damage()
        if not damage_ret['miss']:
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            if not self.target.isfaint() and rnd()<30/100:
                self.target.set_boost('def',-1)
            self.set_boost('spa',1,'self')

    def move_2(self): # Eerie Wail
        damage_ret=self.get_damage()
        if not damage_ret['miss']:
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            if not self.target.isfaint() and rnd()<20/100:
                self.target.set_condition('CONFUSION',counter=0)
            self.set_boost('spa',1,'self')

# -------------------------------------------------------------

@Increment(Gudiao,'_move_3')
def value():
    return ('Wing Slice',80,100,'Physical','Flying',0,['contact'])

@Increment(Gudiao)
def move_3(self): # Wing Slice
    damage_ret=self.get_damage()
    if not damage_ret['miss']:
        damage=damage_ret['damage']
        self.target.take_damage(damage)
        self.set_boost('spa',1,'self')

@Increment(Gudiao)
def _get_base_damage(self,power,crit):
    atk_boost=self['boosts']['atk'] if self['act']['category']=='Physical' else self['boosts']['spa']
    if self['act']['id']=='Wing Slice':
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

@Increment(Gudiao,'_move_4')
def value():
    return ('Aqua Camouflage',0,100000,'Status','Water',0,[])

@Increment(Gudiao)
def move_4(self): # Aqua Camouflage
    self.set_boost('def',1,'self')
    self.state['types']=['Water']

# -------------------------------------------------------------

@Increment(Gudiao,'_ability')
def value():
    return ['Abyssal Cry','Aqua Veil']

@Increment(Gudiao)
def endturn(self):
    if self.get_env('Rain'):
        self.restore(self['max_hp']//8,'heal')
