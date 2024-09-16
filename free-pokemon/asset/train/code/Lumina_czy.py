from engine import *


class Lumina(PokemonBase):
    _species='Lumina'
    _types=['Psychic','Fairy']
    _gender='Female'
    _ability=['Empathic Link']
    _move_1=('Prismatic Beam',100,90,'Special','Psychic',0,[])
    _move_2=('Fairy Glow',0,100,'Status','Fairy',0,[])
    def __init__(self):
        super().__init__()

    def _take_damage_attack(self,x):
        if 'type_effect' in self.target['act'] and self.target['act']['type_effect']<0.1:
            self.logger.log('It is immune by %s.'%self._species)
            return
        self.register_act_taken()
        if self['hp']==self['max_hp']:
            self.target.take_damage(x,'loss')
        self.state['hp']=max(0,self['hp']-x)
        self.log(script='attack',species=self._species,x=x,**self['act_taken'])

    def move_1(self): # Prismatic Beam
        damage_ret=self.get_damage()
        if not damage_ret['miss']:
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            if not self.target.isfaint() and rnd()<20/100:
                self.target.set_boost('accuracy',-1)

    def move_2(self): # Fairy Glow  
        self.set_boost('spa',1,'self')
        self.set_boost('spd',1,'self')

# ----------

@Increment(Lumina,'_move_3')
def value():
    return ('Dazzling Gleam',80,100,'Special','Fairy',0,[])

@Increment(Lumina)
def move_3(self): # Dazzling Gleam
    damage_ret=self.get_damage() 
    if not damage_ret['miss']:
        damage=damage_ret['damage']
        self.target.take_damage(damage)

# ----------

@Increment(Lumina,'_move_4')
def value():
    return ('Psycho Shift',0,100,'Status','Psychic',0,[])

@Increment(Lumina)
def move_4(self): # Psycho Shift
    if self['status']:
        for k, _ in self['status'].items():
            break
        self.target.set_status(k)
        self.state['status']=None
