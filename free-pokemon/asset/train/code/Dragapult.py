from engine import *


class Dragapult(PokemonBase):
    _species='Dragapult'
    _types=['Dragon','Ghost']
    _gender='Female'
    _ability=['Clear Body']
    _move_1=('Dragon Darts',50,100,'Physical','Dragon',0,[])
    _move_2=('Phantom Force',90,100,'Physical','Ghost',0,['contact'])
    def __init__(self):
        super().__init__()

    def set_boost(self,key,x,from_='target'):
        if x<0 and from_=='target':
            self.log("Dragapult's stats cannot be lowered by opponents.")
            return
        bar=6 if key in ['atk','def','spa','spd','spe'] else 3
        if x>0:
            self['boosts'][key]=min(bar,self['boosts'][key]+x)
        else:
            self['boosts'][key]=max(-bar,self['boosts'][key]+x)
        self.log("{}'s {} is {} by {}.".format(self._species,{
            'atk':'Attack','def':'Defense','spa':'Special Attack','spd':'Special Defense','spe':'Speed'}[key],'raised' if x>0 else 'lowered',x))

    def get_evasion(self):
        if self['conditions'].get('PHANTOM_FORCE'):
            return 0
        return 1

    def move_1(self): # Dragon Darts
        hit=True; i=0
        while hit and i<2:
            damage_ret=self.get_damage()
            if damage_ret['miss']: break
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            i+=1; hit=False if self.target.isfaint() else True
    
    def move_2(self): # Phantom Force
        if not self['conditions'].get('PHANTOM_FORCE'):
            self.set_condition('PHANTOM_FORCE',counter=0)
            self.state['canact']='Phantom Force'
        else:
            del self['conditions']['PHANTOM_FORCE']
            self.state['canact']=True
            damage_ret=self.get_damage()
            if not damage_ret['miss']:
                damage=damage_ret['damage']
                self.target.take_damage(damage)

# -------------------------------------------------------------

@Increment(Dragapult,'_move_3')
def value():
    return ('Dragon Dance',0,100000,'Status','Dragon',0,[])

@Increment(Dragapult)
def move_3(self): # Dragon Dance
    self.set_boost('atk',+1,'self')
    self.set_boost('spe',+1,'self')
