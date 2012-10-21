#!/usr/bin/env python
"""
Create schematic of chest with custom potions.
"""
import os, sys
import Tkinter, tkFileDialog, ttk
import struct

import pynbt

class PotionEffect:
        def __init__(self, i, amp, dur):
                self.id = i
                self.amplifier = amp
                self.duration = dur

        def getNBT(self):
                effecttags = pynbt.TAG_Compound()
                effecttags.add(pynbt.TAG_Byte(name = "Amplifier", value = self.amplifier))
                effecttags.add(pynbt.TAG_Byte(name = "Id", value = self.id))
                effecttags.add(pynbt.TAG_Int(name = "Duration", value = self.duration))
                return effecttags

class Potion:
        def __init__(self, color, stack, eff):
                self.id = 373
                self.damage = color
                self.stacksize = stack
                self.slot = 0
                self.effects = eff

        def getNBT(self, slot):
                potiontags = pynbt.TAG_Compound()
                potiontags.add(pynbt.TAG_Byte(name = "Count", value = self.stacksize))
                potiontags.add(pynbt.TAG_Byte(name = "Slot", value = slot))
                potiontags.add(pynbt.TAG_Short(name = "Damage", value = self.damage))
                potiontags.add(pynbt.TAG_Short(name = "id", value = self.id))
                effectslist = pynbt.TAG_List(name="CustomPotionEffects")
                effectscount = 0
                for effect in self.effects:
                        effectslist.insert(effectscount, effect.getNBT())
                wrappertag = pynbt.TAG_Compound()
                wrappertag.name = "tag"
                wrappertag.add(effectslist)
                potiontags.add(wrappertag)
                return potiontags
                
class Schematic:
        def __init__(self, chest):
                chestList = pynbt.TAG_List(name = "TileEntities", list_type = pynbt.TAG_Compound)
                chestList.insert(0, chest)
                block_data = [0]*1
                block_data[0] = 54
                block_data2 = [0]*1
                block_data2[0] = 0
                self.schematic = pynbt.TAG_Compound()
                self.schematic.name = "Schematic"
                self.schematic.add(pynbt.TAG_Short(name = "Width", value = 1))
                self.schematic.add(pynbt.TAG_Short(name = "Length", value = 1))
                self.schematic.add(pynbt.TAG_Short(name = "Height", value = 1))
                self.schematic.add(pynbt.TAG_String(name = "Materials", value = "Alpha"))
                self.schematic.add(pynbt.TAG_Byte_Array(name = "Blocks", value = bytearray(buffer(struct.pack('b'*len(block_data), *block_data)))))
                self.schematic.add(pynbt.TAG_Byte_Array(name = "Data", value = bytearray(buffer(struct.pack('b'*len(block_data2), *block_data2)))))
                self.schematic.add(pynbt.TAG_List(name = "Entities", list_type = pynbt.TAG_Compound))
                self.schematic.add(chestList)
                
class CustomPotions:
        def __init__(self,frame):
                self.root = frame
                self.root.title('Custom Potions')

                self.currenteffects = []
                self.currentpotions = []

                customcolorFrame = Tkinter.Frame(self.root)
                presetcolorFrame = Tkinter.Frame(customcolorFrame)

                self.presetcolorlist = ["custom value", "regen", "swift", "fire", "heal", "strength", "poison", "weakness", "slowness", "harm", "night vision", "invisibility"]
                self.presetdamagelist = [0, 8193, 8194, 8195, 8197, 8201, 8196, 8200, 8202, 8204, 8198, 8206]
                self.presetsplashdamagelist = [0, 16385, 32658, 16387, 16389, 16393, 16388, 16392, 16394, 16396, 32758, 32702]
                
                colorFrame = Tkinter.Frame(presetcolorFrame)
                colorLabel = Tkinter.Label(colorFrame, text="Potion color:", width=20)
                self.colorSelection = Tkinter.StringVar()
                self.colorBox = ttk.Combobox(colorFrame, textvariable=self.colorSelection, state='readonly')
                self.colorBox['values'] = self.presetcolorlist
                self.colorBox.current(0)
                colorLabel.pack(side='left')
                self.colorBox.pack(side='left')
                colorFrame.pack()

                splashFrame = Tkinter.Frame(presetcolorFrame)
                splashLabel = Tkinter.Label(splashFrame, text="Is splash potion:", width=18)
                self.splashCheck = Tkinter.BooleanVar(value=False)
                self.splashCheckButton = Tkinter.Checkbutton(splashFrame, variable=self.splashCheck, onvalue=True, offvalue=False, height=1)
                splashLabel.pack(side='left')
                self.splashCheckButton.pack(side='left')
                splashFrame.pack()

                presetcolorFrame.pack(side='left')

                damageFrame = Tkinter.Frame(customcolorFrame)
                self.damageVar = Tkinter.IntVar(value=0)
                damageLabel = Tkinter.Label(damageFrame, text="Custom damage value:", width=20)
                self.damageEntry = Tkinter.Entry(damageFrame, textvariable=self.damageVar, width=10)
                damageLabel.pack(side='left')
                self.damageEntry.pack(side='left')
                damageFrame.pack(side='left')

                stacksizeFrame = Tkinter.Frame(self.root)
                self.stacksizeVar = Tkinter.IntVar(value=1)
                stacksizeLabel = Tkinter.Label(stacksizeFrame, text="Stack size:", width=20)
                self.stacksizeEntry = Tkinter.Entry(stacksizeFrame, textvariable=self.stacksizeVar, width=10)
                stacksizeLabel.pack(side='left')
                self.stacksizeEntry.pack(side='left')
                #stacksizeFrame.pack()

                idFrame = Tkinter.Frame(self.root)
                self.idVar = Tkinter.IntVar(value=0)
                idLabel = Tkinter.Label(idFrame, text="Effect ID:", width=20)
                self.idEntry = Tkinter.Entry(idFrame, textvariable=self.idVar, width=10)
                idLabel.pack(side='left')
                self.idEntry.pack(side='left')
                idFrame.pack()

                amplifierFrame = Tkinter.Frame(self.root)
                self.amplifierVar = Tkinter.IntVar(value=0)
                amplifierLabel = Tkinter.Label(amplifierFrame, text="Effect level:", width=20)
                self.amplifierEntry = Tkinter.Entry(amplifierFrame, textvariable=self.amplifierVar, width=10)
                amplifierLabel.pack(side='left')
                self.amplifierEntry.pack(side='left')
                amplifierFrame.pack()

                durationFrame = Tkinter.Frame(self.root)
                self.durationVar = Tkinter.IntVar(value=0)
                durationLabel = Tkinter.Label(durationFrame, text="Effect duration:", width=20)
                self.durationEntry = Tkinter.Entry(durationFrame, textvariable=self.durationVar, width=10)
                durationLabel.pack(side='left')
                self.durationEntry.pack(side='left')
                durationFrame.pack()
                
                effectbuttonandlistFrame = Tkinter.Frame(self.root)
                effectbuttonFrame = Tkinter.Frame(effectbuttonandlistFrame)
                self.addEffectButton = Tkinter.Button(effectbuttonFrame, command=self.addEffect, text="Add effect", width=15, height=2)
                self.removeEffectButton = Tkinter.Button(effectbuttonFrame, command=self.removeEffect, text="Remove effect", width=15, height=2)
                self.removealleffectsButton = Tkinter.Button(effectbuttonFrame, command=self.removeallEffects, text="Remove all", width=15, height=2)
                self.addEffectButton.pack(pady=5)
                self.removeEffectButton.pack(pady=5)
                self.removealleffectsButton.pack(pady=5)
                effectbuttonFrame.pack(side='left')
                self.effectList = Tkinter.Listbox(effectbuttonandlistFrame, selectmode='SINGLE', width=30)
                self.effectList.pack(padx=5, side='left', fill='y', expand=1)
                effectbuttonandlistFrame.pack(pady=5)

                customcolorFrame.pack()
                stacksizeFrame.pack()
                
                chestbuttonandlistFrame = Tkinter.Frame(self.root)
                chestbuttonFrame = Tkinter.Frame(chestbuttonandlistFrame)
                self.addPotionButton = Tkinter.Button(chestbuttonFrame, command=self.addPotion, text="Add potion", width=20, height=2)
                self.removePotionButton = Tkinter.Button(chestbuttonFrame, command=self.removePotion, text="Remove potion", width=20, height=2)
                self.removeallpotionsButton = Tkinter.Button(chestbuttonFrame, command=self.removeallPotions, text="Remove all", width=20, height=2)
                self.createChestButton = Tkinter.Button(chestbuttonFrame, command=self.createChest, text="Create chest schematic", width=20, height=2)
                self.addPotionButton.pack(pady=5)
                self.removePotionButton.pack(pady=5)
                self.removeallpotionsButton.pack(pady=5)
                self.createChestButton.pack(pady=5)
                chestbuttonFrame.pack(side='left')
                self.potionList = Tkinter.Listbox(chestbuttonandlistFrame, selectmode='SINGLE', width=100)
                self.potionList.pack(side='left', fill='y', expand=1)
                chestbuttonandlistFrame.pack(pady=5)

                self.filenameVar = Tkinter.StringVar(value="temp")
                filenameFrame = Tkinter.Frame(self.root)
                filenameLabel1 = Tkinter.Label(filenameFrame, text = "Filename: ", width=15)
                self.filenameEntry = Tkinter.Entry(filenameFrame, textvariable=self.filenameVar, width=30)
                filenameLabel2 = Tkinter.Label(filenameFrame, text = ".schematic", width=15)
                filenameLabel1.pack(side='left')
                self.filenameEntry.pack(side='left')
                filenameLabel2.pack(side='left')
                filenameFrame.pack()
                

        def addEffect(self):
                print("Adding effect to potion")
                effect = PotionEffect(self.idVar.get(), self.amplifierVar.get(), self.durationVar.get())
                self.currenteffects.append(effect)
                effecttxt = ("ID: %s Level: %s Duration: %s" % (self.idVar.get(), self.amplifierVar.get(), self.durationVar.get()))
                self.effectList.insert(self.effectList.size(), effecttxt)

        def removeEffect(self):
                print("Removing effect from potion")
                selection = self.effectList.curselection()
                if len(selection) > 0:
                        self.currenteffects.pop(int(selection[0]))
                        self.effectList.delete(selection)

        def removeallEffects(self):
                print("Clearing effect list")
                self.currenteffects = []
                self.effectList.delete(0,'end')
                
        def addPotion(self):
                print("Adding potion")
                index = int(self.colorBox.current())
                print("index: %s" % (index))
                damage = 0
                if index < 0:
                        print("Color error... defaulting to 0")
                        damage = 0
                elif index == 0:
                        print("using custom damage value")
                        damage = self.damageVar.get()
                else:
                        if self.splashCheck.get():
                                damage = self.presetsplashdamagelist[index]
                        else:
                                damage = self.presetdamagelist[index]
                ce = []
                for e in self.currenteffects:
                        ce.append(e)
                potion = Potion(damage, self.stacksizeVar.get(), ce)
                self.currentpotions.append(potion)
                effecttxt = ""
                effectcount = 1
                for effect in self.currenteffects:
                        effecttxt += " effect%s: ID: %s Level: %s Duration: %s" % (effectcount, effect.id, effect.amplifier, effect.duration)
                        effectcount += 1
                potiontxt = "Damage: %s Count: %s " % (damage, self.stacksizeVar.get())
                potiontxt += effecttxt
                self.potionList.insert(self.potionList.size(), potiontxt)
                
        def removePotion(self):
                print("Removing potion")
                selection = self.potionList.curselection()
                if len(selection) > 0:
                        self.currentpotions.pop(int(selection[0]))
                        self.potionList.delete(selection)

        def removeallPotions(self):
                print("Clearing potion list")
                self.currentpotions = []
                self.potionList.delete(0,'end')

        def createChest(self):
                print("Creating chest schematic")
                if len(self.currentpotions) > 0:
                        chest = pynbt.TAG_Compound()
                        chest.add(pynbt.TAG_Int(name = "x", value = 0))
                        chest.add(pynbt.TAG_Int(name = "y", value = 0))
                        chest.add(pynbt.TAG_Int(name = "z", value = 0))
                        chest.add(pynbt.TAG_String(name = "id", value = "Chest"))
                        items = pynbt.TAG_List(name="Items")
                        itemscount = 0
                        for item in self.currentpotions:
                                items.insert(itemscount, item.getNBT(itemscount))
                                itemscount += 1
                        chest.add(items)
                        schem = Schematic(chest)
                        print(schem.schematic.pretty_string())
                        schem.schematic.save(filename="./schematics/" + self.filenameVar.get() + ".schematic")
                else:
                        print("No potions in list...")
                        
if __name__ == '__main__':
        root = Tkinter.Tk()
        mywindow = CustomPotions(root)
	root.mainloop()


