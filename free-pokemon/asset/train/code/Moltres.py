from engine import *


class Moltres(PokemonBase):
    _species='Moltres'
    _types=['Dark','Flying']
    _gender='Neutral'
    _ability=['Berserk']
    _move_1=('Fiery Wrath',90,100,'Special','Dark',0,[])
    _move_2=('Nasty Plot',0,100000,'Status','Dark',0,[])
    def __init__(self):
        super().__init__()

    def take_damage(self,x,from_='attack'):
        prev_hp=self['hp']
        if from_=='attack':
            self._take_damage_attack(x)
        elif from_=='loss':
            self._take_damage_loss(x)
        elif from_=='recoil':
            self._take_damage_recoil(x)
        if self['hp']==0:
            self.state['status']='FNT'
            self.log('%s faints.'%self._species)
            return
        if prev_hp>self['max_hp']//2 and self['hp']<=self['max_hp']//2:
            self.set_boost('spa',1,'self')

    def move_1(self): # Fiery Wrath
        damage_ret=self.get_damage()
        if not damage_ret['miss']:
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            if not self.target.isfaint() and rnd()<20/100:
                self.target.set_condition('FLINCH',counter=0)

    def move_2(self): # Nasty Plot
        self.set_boost('spa',+2,'self')

# -------------------------------------------------------------

@Increment(Moltres,'_move_3')
def value():
    return ('Air Slash',75,95,'Special','Flying',0,[])

@Increment(Moltres)
def move_3(self): # Air Slash
    damage_ret=self.get_damage()
    if not damage_ret['miss']:
        damage=damage_ret['damage']
        self.target.take_damage(damage)
        if not self.target.isfaint() and rnd()<30/100:
            self.target.set_condition('FLINCH',counter=0)

# -------------------------------------------------------------

@Increment(Moltres,'_move_4')
def value():
    return ('Protect',0,100000,'Status','Normal',4,[])

@Increment(Moltres)
def move_4(self): # Protect
    if self['last_act'] and self['last_act']['id']=='Protect':
        return
    self.set_condition('PROTECT',counter=0)

@Increment(Moltres)
def _take_damage_attack(self,x):
    if 'type_efc' in self.target['act'] and self.target['act']['type_efc']<0.1:
        self.logger.log('It is immune by %s.'%self._species)
        return
    if self['conditions'].get('PROTECT'):
        del self['conditions']['PROTECT']
        return
    self.register_act_taken()
    self.state['hp']=max(0,self['hp']-x)
    self.log('{} loses {} HP.'.format(self._species,x),act_taken=self['act_taken'])

@Increment(Moltres)
def endturn(self):
    if self['conditions'].get('PROTECT'):
        del self['conditions']['PROTECT']

# -------------------------------------------------------------

@Increment(Moltres,'_ability')
def value():
    return ['Berserk','Competitive']

@Increment(Moltres)
def set_boost(self,key,x,from_='target'):
    bar=6 if key in ['atk','def','spa','spd','spe'] else 3
    if x>0:
        self['boosts'][key]=min(bar,self['boosts'][key]+x)
        self.log("{}'s {} is raised by {}.".format(self._species,{
            'atk':'Attack','def':'Defense','spa':'Special Attack','spd':'Special Defense','spe':'Speed'}[key],x))
    else:
        self['boosts'][key]=max(-bar,self['boosts'][key]+x)
        self.log("{}'s {} is lowered by {}.".format(self._species,{
            'atk':'Attack','def':'Defense','spa':'Special Attack','spd':'Special Defense','spe':'Speed'}[key],x))
        if from_=='target':
            for _ in range(x):
                self['boosts']['spa']=min(bar,self['boosts'][key]+2)
            self.log("{}'s Special Attack is raised by {}.".format(self._species,2*x))

# -------------------------------------------------------------

@Increment(Moltres,'_move_5')
def value():
    return ('Roost',0,100000,'Status','Flying',0,[])

@Increment(Moltres)
def move_5(self): # Roost
    self.restore(self['max_hp']//2,'heal')
