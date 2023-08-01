# -*- coding: utf-8 -*-
"""
Created on Tue Aug  1 17:06:53 2023

@author: Soo.Y
"""

class Item:
    def __init__(self, name, price, weight, isdropable):
        self.name = name
        self.price = price
        self.weight = weight
        self.isdropable = isdropable
    
    def sale(self):
        print(f"[{self.name}] 판매가격은 [{self.price}]")
        
    def discard(self):
        if self.isdropable:
            print(f"[{self.name}] 버렸습니다.")
        else:
            print(f"[{self.name}] 버릴 수 없습니다.")
            
class WearableItem(Item):
    def __init__(self, name, price, weight, isdropable, effect):
        super().__init__(name, price, weight, isdropable)
        self.effect = effect
        
    def wear(self):
        print(f"[{self.name}] 착용했습니다. {self.effect}")

class UsableItem(Item):
    def __init__(self, name, price, weight, isdropable, effect):
        super().__init__(name, price, weight, isdropable)
        self.effect = effect
    def use(self):
        print(f"[{self.name}] 사용했습니다. {self.effect}")
        
        
sword = WearableItem("이거닌자의검", 30_000, 3.5, True, "체력 5000 증가, 마력 500 증가")
sword.wear()
sword.sale()
sword.discard()
