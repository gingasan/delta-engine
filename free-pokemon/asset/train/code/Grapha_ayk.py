from engine import *


class Grapha(PokemonBase):
    _species='Grapha'
    _types=['Dark','Dragon']
    _gender='Male'
    _ability=['Dark Revival']
    _move_1=('Shadow Blast',90,100,'Special','Dark',0,[])
    _move_2=('Dragon Rage',80,100,'Special','Dragon',0,[])
    def __init__(self):
        super().__init__()

    def onswitch(self):
        self.set_condition('REVIVE',counter=1)

    def take_damage(self,x,from_='attack'):
        if from_=='attack':
            self._take_damage_attack(x)
        elif from_=='loss':
            self._take_damage_loss(x)
        elif from_=='recoil':
            self._take_damage_recoil(x)
        if self['hp']==0:
            if self['conditions'].get('REVIVE'):
                self.state['status']=None
                self.state['hp']=self['max_hp']//2
                del self['conditions']['REVIVE']
                self.log('Revive! Lord of Dark, Graphal.',color='purple')
            else:
                self.state['status']='FNT'
                self.log('%s faints.'%self._species)

    def move_1(self): # Shadow Blast
        damage_ret=self.get_damage()
        if not damage_ret['miss']:
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            if not self.target.isfaint() and rnd()<20/100:
                self.target.set_boost('spd',-1)

    def move_2(self): # Dragon Rage
        damage_ret=self.get_damage()
        if not damage_ret['miss']:
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            if not self.target.isfaint() and rnd()<30/100:
                self.target.set_status('BRN')

# -------------------------------------------------------------

@Increment(Grapha,'_move_3')
def value():
    return ('Nightmare Claw',70,100,'Physical','Dark',0,[])

@Increment(Grapha)
def move_3(self): # Nightmare Claw
    damage_ret=self.get_damage()
    if not damage_ret['miss']:
        damage=damage_ret['damage']
        self.target.take_damage(damage)
        if not self.target.isfaint() and rnd()<20/100:
            self.target.set_condition('FLINCH',counter=0)

# -------------------------------------------------------------

@Increment(Grapha,'_move_4')
def value():
    return ('Abyssal Roar',0,100000,'Status','Dragon',0,[])

@Increment(Grapha)
def move_4(self): # Abyssal Roar
    self.target.set_boost('atk',-1)
    self.target.set_boost('spa',-1)

# -------------------------------------------------------------

@Increment(Grapha,'_ability')
def value():
    return ['Dark Revival','Shadow Swap']

@Increment(Grapha)
def move_1(self): # Shadow Blast
    damage_ret=self.get_damage()
    if not damage_ret['miss']:
        damage=damage_ret['damage']
        self.target.take_damage(damage)
        if not self.target.isfaint() and rnd()<20/100:
            self.target.set_boost('spd',-1)
    self.restore(self['max_hp']//10,'heal')

@Increment(Grapha)
def move_3(self): # Nightmare Claw
    damage_ret=self.get_damage()
    if not damage_ret['miss']:
        damage=damage_ret['damage']
        self.target.take_damage(damage)
        if not self.target.isfaint() and rnd()<20/100:
            self.target.set_condition('FLINCH',counter=0)
    self.restore(self['max_hp']//10,'heal')
