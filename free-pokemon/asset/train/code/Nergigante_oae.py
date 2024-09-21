from engine import *


class Nergigante(PokemonBase):
    _species='Nergigante'
    _types=['Dragon','Steel']
    _gender='Male'
    _ability=['Regenerative Spikes']
    _move_1=('Spike Slam',100,95,'Physical','Steel',0,['contact'])
    _move_2=('Dragon Dive',120,90,'Physical','Dragon',0,['contact'])
    def __init__(self):
        super().__init__()

    def onswitch(self):
        self.set_condition('SPIKES',counter=0)

    def endturn(self):
        if self['conditions'].get('SPIKES'):
            self.restore(self['max_hp']//10,'heal')

    def move_1(self): # Spike Slam
        attack_ret=self.attack()
        if not (attack_ret['miss'] or attack_ret['immune']):
            damage_ret=self.get_damage()
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            if self['conditions'].get('SPIKES'):
                self.target.take_damage(self.target['max_hp']//16,'loss')
                del self['conditions']['SPIKES']

    def move_2(self): # Dragon Dive
        attack_ret=self.attack()
        if not (attack_ret['miss'] or attack_ret['immune']):
            damage_ret=self.get_damage()
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            recoil=int(damage*1/3)
            self.take_damage(recoil,'recoil')

# ----------

@Increment(Nergigante,'_move_3')
def value():
    return ('Regenerate',0,100000,'Status','Normal',0,[])

@Increment(Nergigante)
def move_3(self): # Regenerate
    self.restore(self['max_hp']//2,'heal')
    self.set_condition('SPIKES',counter=0)

# ----------

@Increment(Nergigante,'_move_4')
def value():
    return ('Dragon Dance',0,100000,'Status','Dragon',0,[])

@Increment(Nergigante)
def move_4(self): # Dragon Dance
    self.set_boost('atk',1,'self')
    self.set_boost('spe',1,'self')

# ----------

@Increment(Nergigante,'_ability')
def value():
    return ['Regenerative Spikes','Spike Burst']

@Increment(Nergigante)
def move_1(self): # Spike Slam
    attack_ret=self.attack()
    if not (attack_ret['miss'] or attack_ret['immune']):
        damage_ret=self.get_damage()
        damage=damage_ret['damage']
        self.target.take_damage(damage)
        if self['conditions'].get('SPIKES'):
            self.target.take_damage(self.target['max_hp']//16,'loss')
            del self['conditions']['SPIKES']
            self.target.take_damage(self.target['max_hp']//8,'loss')
            self.set_boost('def',-1)
