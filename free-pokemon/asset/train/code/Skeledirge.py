from engine import *


class Skeledirge(PokemonBase):
    _species='Skeledirge'
    _types=['Fire','Ghost']
    _gender='Male'
    _ability=['Unaware']
    _move_1=('Torch Song',80,100,'Special','Fire',0,[])
    _move_2=('Shadow Ball',80,100,'Special','Ghost',0,[])
    def __init__(self):
        super().__init__()

    def get_base_damage(self,power,crit):
        atk_boost=self['boosts']['atk'] if self['act']['category']=='Physical' else self['boosts']['spa']
        def_boost=0
        
        if crit:
            atk_boost=max(0,atk_boost)
            def_boost=min(0,def_boost)

        attack=self.get_stat('atk' if self['act']['category']=='Physical' else 'spa',atk_boost)
        defense=self.target.get_stat('def' if self['act']['category']=='Physical' else 'spd',def_boost)

        level=100
        base_damage=int(int(int(int(2*level/5+2)*power*attack)/defense)/50)+2

        return base_damage

    def move_1(self): # Torch Song
        damage_ret=self.get_damage()
        if not damage_ret['miss']:
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            self.set_boost('spa',1,'self')

    def move_2(self): # Shadow Ball
        damage_ret=self.get_damage()
        if not damage_ret['miss']:
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            if not self.target.isfaint() and rnd()<20/100:
                self.target.set_boost('spd',-1)

# ----------

@Increment(Skeledirge,'_move_3')
def value():
    return ('Substitute',0,100000,'Status','Normal',0,[])

@Increment(Skeledirge)
def move_3(self): # Substitute
    if self['hp']>self['max_hp']//4 and not self['conditions'].get('SUBSTITUTE'):
        self.take_damage(self['max_hp']//4,'loss')
        self.set_condition('SUBSTITUTE',hp=self['max_hp']//4)

@Increment(Skeledirge)
def _take_damage_attack(self,x):
    if 'type_effect' in self.target['act'] and self.target['act']['type_effect']<0.1:
        self.logger.log('It is immune by %s.'%self._species)
        return
    self.register_act_taken()
    if self['conditions'].get('SUBSTITUTE'):
        self['conditions']['SUBSTITUTE']['hp']-=x
        if self['conditions']['SUBSTITUTE']['hp']<1:
            del self['conditions']['SUBSTITUTE']
    else:
        self.state['hp']=max(0,self['hp']-x)
        self.log(script='attack',species=self._species,x=x,**self['act_taken'])

# ----------

@Increment(Skeledirge,'_move_4')
def value():
    return ('Slack Off',0,100000,'Status','Normal',0,[])

@Increment(Skeledirge)
def move_4(self): # Slack Off
    self.restore(self['max_hp']//2,'heal')

# ----------

@Increment(Skeledirge,'_move_5')
def value():
    return ('Yawn',0,100000,'Status','Normal',0,[])

@Increment(Skeledirge)
def move_5(self): # Yawn
    if not self.target['status']:
        self.target.set_condition('YAWN',counter=0)

@Increment(Skeledirge)
def endturn(self):
    if self.target['conditions'].get('YAWN'):
       self.target['conditions']['YAWN']['counter']+=1
       if self.target['conditions']['YAWN']['counter']==2:
           self.target.set_status('SLP')
           del self.target['conditions']['YAWN']
