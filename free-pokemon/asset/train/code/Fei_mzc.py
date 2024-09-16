from engine import *


class Fei(PokemonBase):
    _species='Fei'
    _types=['Dark','Poison']
    _gender='Genderless'
    _ability=['Desolate Trail']
    _move_1=('Plague Fang',85,90,'Physical','Poison',0,['contact'])
    _move_2=('Withering Gaze',70,100,'Special','Dark',0,[])
    def __init__(self):
        super().__init__()

    def onswitch(self):
        self.env.set_terrain('Grassy Terrain',from_=self._species,max_count=10)
    
    def move_1(self): # Plague Fang
        damage_ret=self.get_damage()
        if not damage_ret['miss']:
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            if not self.target.isfaint() and rnd()<30/100:
                self.target.set_status('TOX')
    
    def move_2(self): # Withering Gaze
        damage_ret=self.get_damage()
        if not damage_ret['miss']:
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            if not self.target.isfaint() and rnd()<20/100:
                self.target.set_boost('spa',-1)

# ----------

@Increment(Fei,'_move_3')
def value():
    return ('Pestilence',0,100,'Status','Poison',0,[])

@Increment(Fei)
def move_3(self): # Pestilence
    self.target.set_status('PSN')
    self.target.set_boost('spe',-1)

# ----------

@Increment(Fei,'_ability')
def value():
    return ['Desolate Trail','Omen of Plague']

@Increment(Fei)
def endturn(self):
    if rnd()<0.3:
        self.target.set_status('PSN')
