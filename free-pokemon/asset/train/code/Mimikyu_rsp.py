from engine import *


class Mimikyu(PokemonBase):
    _species='Mimikyu'
    _types=['Ghost','Fairy']
    _gender='Male'
    _ability=['Disguise']
    _move_1=('Play Rough',90,90,'Physical','Fairy',0,[])
    _move_2=('Shadow Claw',70,100,'Physical','Ghost',0,[])
    def __init__(self):
        super().__init__()

    def onswitch(self):
        self.set_condition('DISGUISE',counter=0)

    def _take_damage_attack(self,x):
        if 'type_effect' in self.target['act'] and self.target['act']['type_effect']<0.1:
            self.logger.log('It is immune by %s.'%self._species)
            return
        if self['conditions'].get('DISGUISE'):
            del self['conditions']['DISGUISE']
        else:
            self.register_act_taken()
            self.state['hp']=max(0,self['hp']-x)
            self.log(script='attack',species=self._species,x=x,**self['act_taken'])

    def get_crit(self):
        crit_mult=[0,24,8,2,1]
        crit_ratio=self['boosts']['crit']
        if self['act']['id']=='Shadow Claw':
            crit_ratio=min(3,crit_ratio+1)
        crit=False
        if rnd()*crit_mult[crit_ratio+1]<1:
            crit=True
        return crit

    def move_1(self): # Energy Ball
        damage_ret=self.get_damage()
        if not damage_ret['miss']:
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            if not self.target.isfaint() and rnd()<10/100:
                self.target.set_boost('atk',-1)

    def move_2(self): # Shadow Claw
        damage_ret=self.get_damage()
        if not damage_ret['miss']:
            damage=damage_ret['damage']
            self.target.take_damage(damage)
