#!/usr/bin/env python
"""
Create schematic of customized spawner.
"""
import os, sys
import Tkinter, tkFileDialog, ttk
import struct

import pynbt


class Spawner:
        def __init__(self, mobID):
                self.spawner = pynbt.TAG_Compound()
                self.spawner.add(pynbt.TAG_Short(name = "Delay", value = 20))
                self.spawner.add(pynbt.TAG_Short(name = "MaxSpawnDelay", value = 800))
                self.spawner.add(pynbt.TAG_Short(name = "MinSpawnDelay", value = 200))
                self.spawner.add(pynbt.TAG_Short(name = "SpawnCount", value = 4))
                self.spawner.add(pynbt.TAG_Int(name = "x", value = 0))
                self.spawner.add(pynbt.TAG_Int(name = "y", value = 0))
                self.spawner.add(pynbt.TAG_Int(name = "z", value = 0))
                self.spawner.add(pynbt.TAG_String(name = "EntityId", value = mobID))
                self.spawner.add(pynbt.TAG_String(name = "id", value = "MobSpawner"))

class Schematic:
        def __init__(self, spawner):
                spawnerList = pynbt.TAG_List(name = "TileEntities", list_type = pynbt.TAG_Compound)
                spawnerList.insert(0, spawner)
                block_data = [0]*1
                block_data[0] = 52
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
                self.schematic.add(spawnerList)

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
        def __init__(self, color, eff):
                self.damage = color
                self.effects = eff

        def getNBT(self):
                effectslist = pynbt.TAG_List(name="CustomPotionEffects")
                effectscount = 0
                for effect in self.effects:
                        effectslist.insert(effectscount, effect.getNBT())
                wrappertag = pynbt.TAG_Compound()
                wrappertag.name = "tag"
                wrappertag.add(effectslist)
                return wrappertag
                
class MakeSpawner:
        def __init__(self,frame):
                mobFile = open("MobList.txt", 'r')
                self.mobList = []
                for line in mobFile:
                        if line.count('#') == 0:
                                mob = line.strip()
                                self.mobList.append(mob)
##                spawndataFile = open("SpawnDataList.txt", 'r')
##                self.spawndataList = []
##                for line in spawndataFile:
##                        if line.count('#') == 0:
##                                spawndata = line.strip()
##                                self.spawndataList.append(spawndata)
                self.root = frame
                #self.root.title('Custom Spawner')

                #self.mobBox = Tix.ComboBox(self.root, label="Mob to spawn: ", dropdown=1, editable=0, command=self.mob_selected)
                self.mobBoxSelection = Tkinter.StringVar()
                self.mobBox = ttk.Combobox(self.root, textvariable=self.mobBoxSelection, state='readonly')
                self.mobBox['values'] = self.mobList
                self.mobBox.current(0)
                #x = 0
                #for mob in self.mobList:
                #        self.mobBox.insert(x, mob)
                #        x += 1
                self.mobBox.pack(pady=5)

                self.tabbedWindows = ttk.Notebook(self.root)
                self.windowCount = 0

                self.filenameVar = Tkinter.StringVar(value="temp")
                self.filenameFrame = Tkinter.Frame(self.root)
                filenameLabel1 = Tkinter.Label(self.filenameFrame, text = "Filename: ", width=15)
                self.filenameEntry = Tkinter.Entry(self.filenameFrame, textvariable=self.filenameVar, width=30)
                filenameLabel2 = Tkinter.Label(self.filenameFrame, text = ".schematic", width=15)
                filenameLabel1.pack(side='left')
                self.filenameEntry.pack(side='left')
                filenameLabel2.pack(side='left')

## custom potion effect stuff
                self.currenteffects = []

                self.custompotioneffectFrame = Tkinter.Frame(self.tabbedWindows)
                custompotioneffectLabel = Tkinter.Label(self.custompotioneffectFrame, text="Multi-effect potion data",width=20)
                custompotioneffectLabel.pack(pady=5)
                self.custompotioneffectCheck = Tkinter.BooleanVar(value=False)
                self.custompotioneffectCheckButton = Tkinter.Checkbutton(self.custompotioneffectFrame, variable=self.custompotioneffectCheck, onvalue=True, offvalue=False, height=1)
                self.custompotioneffectCheckButton.pack()
                customcolorFrame = Tkinter.Frame(self.custompotioneffectFrame)
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

                effectdamageFrame = Tkinter.Frame(customcolorFrame)
                self.effectdamageVar = Tkinter.IntVar(value=0)
                effectdamageLabel = Tkinter.Label(effectdamageFrame, text="Custom damage value:", width=20)
                self.effectdamageEntry = Tkinter.Entry(effectdamageFrame, textvariable=self.effectdamageVar, width=10)
                effectdamageLabel.pack(side='left')
                self.effectdamageEntry.pack(side='left')
                effectdamageFrame.pack(side='left')

                effectidFrame = Tkinter.Frame(self.custompotioneffectFrame)
                self.effectidVar = Tkinter.IntVar(value=0)
                effectidLabel = Tkinter.Label(effectidFrame, text="Effect ID:", width=20)
                self.effectidEntry = Tkinter.Entry(effectidFrame, textvariable=self.effectidVar, width=10)
                effectidLabel.pack(side='left')
                self.effectidEntry.pack(side='left')
                effectidFrame.pack()

                effectamplifierFrame = Tkinter.Frame(self.custompotioneffectFrame)
                self.effectamplifierVar = Tkinter.IntVar(value=0)
                effectamplifierLabel = Tkinter.Label(effectamplifierFrame, text="Effect level:", width=20)
                self.effectamplifierEntry = Tkinter.Entry(effectamplifierFrame, textvariable=self.effectamplifierVar, width=10)
                effectamplifierLabel.pack(side='left')
                self.effectamplifierEntry.pack(side='left')
                effectamplifierFrame.pack()

                effectdurationFrame = Tkinter.Frame(self.custompotioneffectFrame)
                self.effectdurationVar = Tkinter.IntVar(value=0)
                effectdurationLabel = Tkinter.Label(effectdurationFrame, text="Effect duration:", width=20)
                self.effectdurationEntry = Tkinter.Entry(effectdurationFrame, textvariable=self.effectdurationVar, width=10)
                effectdurationLabel.pack(side='left')
                self.effectdurationEntry.pack(side='left')
                effectdurationFrame.pack()

                effectbuttonandlistFrame = Tkinter.Frame(self.custompotioneffectFrame)
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
##
                self.MaxNearbyEntitiesVar = Tkinter.IntVar(value=6)
                self.MaxNearbyEntitiesCheck = Tkinter.BooleanVar(value=False)

                self.RequiredPlayerRangeVar = Tkinter.IntVar(value=16)
                self.RequiredPlayerRangeCheck = Tkinter.BooleanVar(value=False)

                self.SpawnRangeVar = Tkinter.IntVar(value=4)
                self.SpawnRangeCheck = Tkinter.BooleanVar(value=False)
                
                self.positionXVar = Tkinter.DoubleVar(value=0)
                self.positionCheck = Tkinter.BooleanVar(value=False)
                self.positionYVar = Tkinter.DoubleVar(value=0)
                self.positionZVar = Tkinter.DoubleVar(value=0)

                self.motionXVar = Tkinter.DoubleVar(value=0)
                self.motionCheck = Tkinter.BooleanVar(value=False)
                self.motionYVar = Tkinter.DoubleVar(value=0)
                self.motionZVar = Tkinter.DoubleVar(value=0)

                self.directionCheck = Tkinter.BooleanVar(value=False)
                self.directionXVar = Tkinter.DoubleVar(value=0)
                self.directionYVar = Tkinter.DoubleVar(value=0)
                self.directionZVar = Tkinter.DoubleVar(value=0)

                self.delayVar = Tkinter.IntVar(value=20)
                self.delayCheck = Tkinter.BooleanVar(value=False)
                self.minspawndelayVar = Tkinter.IntVar(value=200)
                self.minspawndelayCheck = Tkinter.BooleanVar(value=False)
                self.maxspawndelayVar = Tkinter.IntVar(value=800)
                self.maxspawndelayCheck = Tkinter.BooleanVar(value=False)
                self.spawncountVar = Tkinter.IntVar(value=4)
                self.spawncountCheck = Tkinter.BooleanVar(value=False)
                
                self.healthVar = Tkinter.IntVar(value=20)
                self.healthCheck = Tkinter.BooleanVar(value=False)
                self.fireVar = Tkinter.IntVar(value=0)
                self.fireCheck = Tkinter.BooleanVar(value=False)
                self.airVar = Tkinter.IntVar(value=300)
                self.airCheck = Tkinter.BooleanVar(value=False)
                self.attacktimeVar = Tkinter.IntVar(value=15)
                self.attacktimeCheck = Tkinter.BooleanVar(value=False)
                self.hurttimeVar = Tkinter.IntVar(value=10)
                self.hurttimeCheck = Tkinter.BooleanVar(value=False)
                self.deathtimeVar = Tkinter.IntVar(value=10)
                self.deathtimeCheck = Tkinter.BooleanVar(value=False)
                self.canlootVar = Tkinter.IntVar(value=1)
                self.canlootCheck = Tkinter.BooleanVar(value=False)
                self.dimensionVar = Tkinter.IntVar(value=0)
                self.dimensionCheck = Tkinter.BooleanVar(value=False)
                self.persistencereqVar = Tkinter.IntVar(value=1)
                self.persistencereqCheck = Tkinter.BooleanVar(value=False)
                self.invulnerableVar = Tkinter.IntVar(value=1)
                self.invulnerableCheck = Tkinter.BooleanVar(value=False)

                self.inloveVar = Tkinter.IntVar(value=1)
                self.inloveCheck = Tkinter.BooleanVar(value=False)
                self.mobageVar = Tkinter.IntVar(value=0)
                self.mobageCheck = Tkinter.BooleanVar(value=False)

                self.saddleVar = Tkinter.IntVar(value=1)
                self.saddleCheck = Tkinter.BooleanVar(value=False)

                self.shearedVar = Tkinter.IntVar(value=0)
                self.shearedCheck = Tkinter.BooleanVar(value=False)
                self.colorVar = Tkinter.IntVar(value=0)
                self.colorCheck = Tkinter.BooleanVar(value=False)

                self.poweredVar = Tkinter.IntVar(value=1)
                self.poweredCheck = Tkinter.BooleanVar(value=False)

                self.creeperfuseVar = Tkinter.IntVar(value=30)
                self.creeperfuseCheck = Tkinter.BooleanVar(value=False)

                self.explosionradiusVar = Tkinter.IntVar(value=3)
                self.explosionradiusCheck = Tkinter.BooleanVar(value=False)

                self.batflagsVar = Tkinter.IntVar(value=0)
                self.batflagsCheck = Tkinter.BooleanVar(value=False)

                self.skeletontypeVar = Tkinter.IntVar(value=0)
                self.skeletontypeCheck = Tkinter.BooleanVar(value=False)

                self.witherinvulVar = Tkinter.IntVar(value=0)
                self.witherinvulCheck = Tkinter.BooleanVar(value=False)

                self.sizeVar = Tkinter.IntVar(value=0)
                self.sizeCheck = Tkinter.BooleanVar(value=False)

                self.ownerVar = Tkinter.StringVar(value="")
                self.ownerCheck = Tkinter.BooleanVar(value=False)
                self.sittingVar = Tkinter.IntVar(value=1)
                self.sittingCheck = Tkinter.BooleanVar(value=False)
                self.angryVar = Tkinter.IntVar(value=1)
                self.angryCheck = Tkinter.BooleanVar(value=False)
                self.cattypeVar = Tkinter.IntVar(value=0)
                self.cattypeCheck = Tkinter.BooleanVar(value=False)
                self.collarcolorVar = Tkinter.IntVar(value=1)
                self.collarcolorCheck = Tkinter.BooleanVar(value=False)

                self.angerVar = Tkinter.IntVar(value=1)
                self.angerCheck = Tkinter.BooleanVar(value=False)

                self.carriedVar = Tkinter.IntVar(value=0)
                self.carriedCheck = Tkinter.BooleanVar(value=False)
                self.carrieddataVar = Tkinter.IntVar(value=0)
                self.carrieddataCheck = Tkinter.BooleanVar(value=False)

                self.professionVar = Tkinter.IntVar(value=0)
                self.professionCheck = Tkinter.BooleanVar(value=False)
                self.richesVar = Tkinter.IntVar(value=0)
                self.richesCheck = Tkinter.BooleanVar(value=False)

                self.PlayerCreatedVar = Tkinter.IntVar(value=1)
                self.PlayerCreatedCheck = Tkinter.BooleanVar(value=False)

                self.thrownpotionvalueVar = Tkinter.IntVar(value=0)
                self.thrownpotionvalueCheck = Tkinter.BooleanVar(value=False)

                self.fuseVar = Tkinter.IntVar(value=0)
                self.fuseCheck = Tkinter.BooleanVar(value=False)

                self.dataVar = Tkinter.IntVar(value=0)
                self.dataCheck = Tkinter.BooleanVar(value=False)
                self.ongroundVar = Tkinter.IntVar(value=0)
                self.ongroundCheck = Tkinter.BooleanVar(value=False)
                self.tileVar = Tkinter.IntVar(value=0)
                self.tileCheck = Tkinter.BooleanVar(value=False)
                self.timeVar = Tkinter.IntVar(value=1)
                self.timeCheck = Tkinter.BooleanVar(value=False)
                self.falldistanceVar = Tkinter.DoubleVar(value=1)
                self.falldistanceCheck = Tkinter.BooleanVar(value=False)
                self.dropitemVar = Tkinter.IntVar(value=0)
                self.dropitemCheck = Tkinter.BooleanVar(value=False)
                self.HurtEntitiesVar = Tkinter.IntVar(value=1)
                self.HurtEntitiesCheck = Tkinter.BooleanVar(value=False)
                self.FallHurtMaxVar = Tkinter.IntVar(value=20)
                self.FallHurtMaxCheck = Tkinter.BooleanVar(value=False)
                self.FallHurtAmountVar = Tkinter.DoubleVar(value=2)
                self.FallHurtAmountCheck = Tkinter.BooleanVar(value=False)

                self.valueVar = Tkinter.IntVar(value=0)
                self.valueCheck = Tkinter.BooleanVar(value=False)

                self.itemageVar = Tkinter.IntVar(value=0)
                self.itemageCheck = Tkinter.BooleanVar(value=False)
                self.idVar = Tkinter.IntVar(value=0)
                self.idCheck = Tkinter.BooleanVar(value=False)
                self.damageitemVar = Tkinter.IntVar(value=0)
                self.damageitemCheck = Tkinter.BooleanVar(value=False)
                self.countVar = Tkinter.IntVar(value=0)
                self.countCheck = Tkinter.BooleanVar(value=False)
                self.enchantsVar = Tkinter.StringVar(value="")
                self.enchantsCheck = Tkinter.BooleanVar(value=False)
                self.itemskullownerVar = Tkinter.StringVar(value="")
                self.itemskullownerCheck = Tkinter.BooleanVar(value=False)
                self.itemnameVar = Tkinter.StringVar(value="")
                self.itemnameCheck = Tkinter.BooleanVar(value=False)
                self.itemloreVar = Tkinter.StringVar(value="")
                self.itemloreCheck = Tkinter.BooleanVar(value=False)
                self.itemcolorVar = Tkinter.IntVar(value=-1)
                self.itemcolorCheck = Tkinter.BooleanVar(value=False)

                self.xtileVar = Tkinter.IntVar(value=-1)
                self.xtileCheck = Tkinter.BooleanVar(value=False)
                self.ytileVar = Tkinter.IntVar(value=-1)
                self.ytileCheck = Tkinter.BooleanVar(value=False)
                self.ztileVar = Tkinter.IntVar(value=-1)
                self.ztileCheck = Tkinter.BooleanVar(value=False)
                self.intileVar = Tkinter.IntVar(value=0)
                self.intileCheck = Tkinter.BooleanVar(value=False)
                self.shakeVar = Tkinter.IntVar(value=0)
                self.shakeCheck = Tkinter.BooleanVar(value=False)
                self.ingroundVar = Tkinter.IntVar(value=0)
                self.ingroundCheck = Tkinter.BooleanVar(value=False)

                self.indataVar = Tkinter.IntVar(value=0)
                self.indataCheck = Tkinter.BooleanVar(value=False)
                self.pickupVar = Tkinter.IntVar(value=0)
                self.pickupCheck = Tkinter.BooleanVar(value=False)
                self.damageVar = Tkinter.DoubleVar(value=0)
                self.damageCheck = Tkinter.BooleanVar(value=False)

                self.pspeedlevelVar = Tkinter.IntVar(value=0)
                self.pspeeddurationVar = Tkinter.IntVar(value=0)
                self.pspeedambientVar = Tkinter.IntVar(value=0)
                self.pspeedCheck = Tkinter.BooleanVar(value=False)
                self.pslowlevelVar = Tkinter.IntVar(value=0)
                self.pslowdurationVar = Tkinter.IntVar(value=0)
                self.pslowambientVar = Tkinter.IntVar(value=0)
                self.pslowCheck = Tkinter.BooleanVar(value=False)
                self.phastelevelVar = Tkinter.IntVar(value=0)
                self.phastedurationVar = Tkinter.IntVar(value=0)
                self.phasteambientVar = Tkinter.IntVar(value=0)
                self.phasteCheck = Tkinter.BooleanVar(value=False)
                self.pfatiguelevelVar = Tkinter.IntVar(value=0)
                self.pfatiguedurationVar = Tkinter.IntVar(value=0)
                self.pfatigueambientVar = Tkinter.IntVar(value=0)
                self.pfatigueCheck = Tkinter.BooleanVar(value=False)
                self.pstrengthlevelVar = Tkinter.IntVar(value=0)
                self.pstrengthdurationVar = Tkinter.IntVar(value=0)
                self.pstrengthambientVar = Tkinter.IntVar(value=0)
                self.pstrengthCheck = Tkinter.BooleanVar(value=False)
                self.pjumplevelVar = Tkinter.IntVar(value=0)
                self.pjumpdurationVar = Tkinter.IntVar(value=0)
                self.pjumpambientVar = Tkinter.IntVar(value=0)
                self.pjumpCheck = Tkinter.BooleanVar(value=False)
                self.pnausealevelVar = Tkinter.IntVar(value=0)
                self.pnauseadurationVar = Tkinter.IntVar(value=0)
                self.pnauseaambientVar = Tkinter.IntVar(value=0)
                self.pnauseaCheck = Tkinter.BooleanVar(value=False)
                self.pregenlevelVar = Tkinter.IntVar(value=0)
                self.pregendurationVar = Tkinter.IntVar(value=0)
                self.pregenambientVar = Tkinter.IntVar(value=0)
                self.pregenCheck = Tkinter.BooleanVar(value=False)
                self.presistlevelVar = Tkinter.IntVar(value=0)
                self.presistdurationVar = Tkinter.IntVar(value=0)
                self.presistambientVar = Tkinter.IntVar(value=0)
                self.presistCheck = Tkinter.BooleanVar(value=False)
                self.pfirereslevelVar = Tkinter.IntVar(value=0)
                self.pfireresdurationVar = Tkinter.IntVar(value=0)
                self.pfireresambientVar = Tkinter.IntVar(value=0)
                self.pfireresCheck = Tkinter.BooleanVar(value=False)
                self.pwaterbrlevelVar = Tkinter.IntVar(value=0)
                self.pwaterbrdurationVar = Tkinter.IntVar(value=0)
                self.pwaterbrambientVar = Tkinter.IntVar(value=0)
                self.pwaterbrCheck = Tkinter.BooleanVar(value=False)
                self.pinvislevelVar = Tkinter.IntVar(value=0)
                self.pinvisdurationVar = Tkinter.IntVar(value=0)
                self.pinvisambientVar = Tkinter.IntVar(value=0)
                self.pinvisCheck = Tkinter.BooleanVar(value=False)
                self.pblindlevelVar = Tkinter.IntVar(value=0)
                self.pblinddurationVar = Tkinter.IntVar(value=0)
                self.pblindambientVar = Tkinter.IntVar(value=0)
                self.pblindCheck = Tkinter.BooleanVar(value=False)
                self.pnightvlevelVar = Tkinter.IntVar(value=0)
                self.pnightvdurationVar = Tkinter.IntVar(value=0)
                self.pnightvambientVar = Tkinter.IntVar(value=0)
                self.pnightvCheck = Tkinter.BooleanVar(value=False)
                self.phungerlevelVar = Tkinter.IntVar(value=0)
                self.phungerdurationVar = Tkinter.IntVar(value=0)
                self.phungerambientVar = Tkinter.IntVar(value=0)
                self.phungerCheck = Tkinter.BooleanVar(value=False)
                self.pweaklevelVar = Tkinter.IntVar(value=0)
                self.pweakdurationVar = Tkinter.IntVar(value=0)
                self.pweakambientVar = Tkinter.IntVar(value=0)
                self.pweakCheck = Tkinter.BooleanVar(value=False)
                self.ppoisonlevelVar = Tkinter.IntVar(value=0)
                self.ppoisondurationVar = Tkinter.IntVar(value=0)
                self.ppoisonambientVar = Tkinter.IntVar(value=0)
                self.ppoisonCheck = Tkinter.BooleanVar(value=False)
                self.phealthlevelVar = Tkinter.IntVar(value=0)
                self.phealthdurationVar = Tkinter.IntVar(value=0)
                self.phealthambientVar = Tkinter.IntVar(value=0)
                self.phealthCheck = Tkinter.BooleanVar(value=False)
                self.pdamagelevelVar = Tkinter.IntVar(value=0)
                self.pdamagedurationVar = Tkinter.IntVar(value=0)
                self.pdamageambientVar = Tkinter.IntVar(value=0)
                self.pdamageCheck = Tkinter.BooleanVar(value=False)
                self.pwitherlevelVar = Tkinter.IntVar(value=0)
                self.pwitherdurationVar = Tkinter.IntVar(value=0)
                self.pwitherambientVar = Tkinter.IntVar(value=0)
                self.pwitherCheck = Tkinter.BooleanVar(value=False)

                self.mobweaponCheck = Tkinter.BooleanVar(value=False)
                self.mobweaponidVar = Tkinter.IntVar(value=0)
                self.mobweapondamageVar = Tkinter.IntVar(value=0)
                self.mobweaponcountVar = Tkinter.IntVar(value=1)
                self.mobweaponenchantsVar = Tkinter.StringVar(value="")
                self.mobweaponchanceVar = Tkinter.DoubleVar(value=0.05)
                self.mobhelmetCheck = Tkinter.BooleanVar(value=False)
                self.mobhelmetidVar = Tkinter.IntVar(value=0)
                self.mobhelmetdamageVar = Tkinter.IntVar(value=0)
                self.mobhelmetcountVar = Tkinter.IntVar(value=1)
                self.mobhelmetenchantsVar = Tkinter.StringVar(value="")
                self.mobhelmetchanceVar = Tkinter.DoubleVar(value=0.05)
                self.mobchestCheck = Tkinter.BooleanVar(value=False)
                self.mobchestidVar = Tkinter.IntVar(value=0)
                self.mobchestdamageVar = Tkinter.IntVar(value=0)
                self.mobchestcountVar = Tkinter.IntVar(value=1)
                self.mobchestenchantsVar = Tkinter.StringVar(value="")
                self.mobchestchanceVar = Tkinter.DoubleVar(value=0.05)
                self.moblegsCheck = Tkinter.BooleanVar(value=False)
                self.moblegsidVar = Tkinter.IntVar(value=0)
                self.moblegsdamageVar = Tkinter.IntVar(value=0)
                self.moblegscountVar = Tkinter.IntVar(value=1)
                self.moblegsenchantsVar = Tkinter.StringVar(value="")
                self.moblegschanceVar = Tkinter.DoubleVar(value=0.05)
                self.mobbootsCheck = Tkinter.BooleanVar(value=False)
                self.mobbootsidVar = Tkinter.IntVar(value=0)
                self.mobbootsdamageVar = Tkinter.IntVar(value=0)
                self.mobbootscountVar = Tkinter.IntVar(value=1)
                self.mobbootsenchantsVar = Tkinter.StringVar(value="")
                self.mobbootschanceVar = Tkinter.DoubleVar(value=0.05)
                self.mobweaponnameVar = Tkinter.StringVar(value="")
                self.mobhelmetnameVar = Tkinter.StringVar(value="")
                self.mobchestnameVar = Tkinter.StringVar(value="")
                self.moblegsnameVar = Tkinter.StringVar(value="")
                self.mobbootsnameVar = Tkinter.StringVar(value="")
                self.mobweaponloreVar = Tkinter.StringVar(value="")
                self.mobhelmetloreVar = Tkinter.StringVar(value="")
                self.mobchestloreVar = Tkinter.StringVar(value="")
                self.moblegsloreVar = Tkinter.StringVar(value="")
                self.mobbootsloreVar = Tkinter.StringVar(value="")
                self.mobweaponcolorVar = Tkinter.IntVar(value=-1)
                self.mobhelmetcolorVar = Tkinter.IntVar(value=-1)
                self.mobchestcolorVar = Tkinter.IntVar(value=-1)
                self.moblegscolorVar = Tkinter.IntVar(value=-1)
                self.mobbootscolorVar = Tkinter.IntVar(value=-1)
                self.mobhelmetskullownerVar = Tkinter.StringVar(value="")

                self.isvillagerVar = Tkinter.IntVar(value=1)
                self.isvillagerCheck = Tkinter.BooleanVar(value=False)
                self.isbabyVar = Tkinter.IntVar(value=1)
                self.isbabyCheck = Tkinter.BooleanVar(value=False)
                self.conversiontimeVar = Tkinter.IntVar(value= -1)
                self.conversiontimeCheck = Tkinter.BooleanVar(value=False)

#### potion tags
                self.potionsFrame = Tkinter.Frame(self.tabbedWindows)
                
                (Tkinter.Label(self.potionsFrame, text = "Potion data")).pack(pady=3)

                self.pspeedFrame = Tkinter.Frame(self.potionsFrame)
                self.pspeedCheckButton = Tkinter.Checkbutton(self.pspeedFrame, variable=self.pspeedCheck, onvalue=True, offvalue=False, height=1)
                pspeedLabel1 = Tkinter.Label(self.pspeedFrame, text = "Speed:  level: ", width=20)
                pspeedLabel2 = Tkinter.Label(self.pspeedFrame, text = "duration: ", width=15)
                pspeedLabel3 = Tkinter.Label(self.pspeedFrame, text = "ambient: ", width=15)
                self.pspeedlevelEntry = Tkinter.Entry(self.pspeedFrame, textvariable=self.pspeedlevelVar, width=10)
                self.pspeeddurationEntry = Tkinter.Entry(self.pspeedFrame, textvariable=self.pspeeddurationVar, width=10)
                self.pspeedambientEntry = Tkinter.Entry(self.pspeedFrame, textvariable=self.pspeedambientVar, width=10)
                self.pspeedCheckButton.pack(side='left')
                pspeedLabel1.pack(side='left')
                self.pspeedlevelEntry.pack(side='left')
                pspeedLabel2.pack(side='left')
                self.pspeeddurationEntry.pack(side='left')
                pspeedLabel3.pack(side='left')
                self.pspeedambientEntry.pack(side='left')
                self.pspeedFrame.pack()

                self.pslowFrame = Tkinter.Frame(self.potionsFrame)
                self.pslowCheckButton = Tkinter.Checkbutton(self.pslowFrame, variable=self.pslowCheck, onvalue=True, offvalue=False, height=1)
                pslowLabel1 = Tkinter.Label(self.pslowFrame, text = "Slow:  level: ", width=20)
                pslowLabel2 = Tkinter.Label(self.pslowFrame, text = "duration: ", width=15)
                pslowLabel3 = Tkinter.Label(self.pslowFrame, text = "ambient: ", width=15)
                self.pslowlevelEntry = Tkinter.Entry(self.pslowFrame, textvariable=self.pslowlevelVar, width=10)
                self.pslowdurationEntry = Tkinter.Entry(self.pslowFrame, textvariable=self.pslowdurationVar, width=10)
                self.pslowambientEntry = Tkinter.Entry(self.pslowFrame, textvariable=self.pslowambientVar, width=10)
                self.pslowCheckButton.pack(side='left')
                pslowLabel1.pack(side='left')
                self.pslowlevelEntry.pack(side='left')
                pslowLabel2.pack(side='left')
                self.pslowdurationEntry.pack(side='left')
                pslowLabel3.pack(side='left')
                self.pslowambientEntry.pack(side='left')
                self.pslowFrame.pack()

                self.phasteFrame = Tkinter.Frame(self.potionsFrame)
                self.phasteCheckButton = Tkinter.Checkbutton(self.phasteFrame, variable=self.phasteCheck, onvalue=True, offvalue=False, height=1)
                phasteLabel1 = Tkinter.Label(self.phasteFrame, text = "Haste:  level: ", width=20)
                phasteLabel2 = Tkinter.Label(self.phasteFrame, text = "duration: ", width=15)
                phasteLabel3 = Tkinter.Label(self.phasteFrame, text = "ambient: ", width=15)
                self.phastelevelEntry = Tkinter.Entry(self.phasteFrame, textvariable=self.phastelevelVar, width=10)
                self.phastedurationEntry = Tkinter.Entry(self.phasteFrame, textvariable=self.phastedurationVar, width=10)
                self.phasteambientEntry = Tkinter.Entry(self.phasteFrame, textvariable=self.phasteambientVar, width=10)
                self.phasteCheckButton.pack(side='left')
                phasteLabel1.pack(side='left')
                self.phastelevelEntry.pack(side='left')
                phasteLabel2.pack(side='left')
                self.phastedurationEntry.pack(side='left')
                phasteLabel3.pack(side='left')
                self.phasteambientEntry.pack(side='left')
                self.phasteFrame.pack()

                self.pfatigueFrame = Tkinter.Frame(self.potionsFrame)
                self.pfatigueCheckButton = Tkinter.Checkbutton(self.pfatigueFrame, variable=self.pfatigueCheck, onvalue=True, offvalue=False, height=1)
                pfatigueLabel1 = Tkinter.Label(self.pfatigueFrame, text = "Mining Fatigue:  level: ", width=20)
                pfatigueLabel2 = Tkinter.Label(self.pfatigueFrame, text = "duration: ", width=15)
                pfatigueLabel3 = Tkinter.Label(self.pfatigueFrame, text = "ambient: ", width=15)
                self.pfatiguelevelEntry = Tkinter.Entry(self.pfatigueFrame, textvariable=self.pfatiguelevelVar, width=10)
                self.pfatiguedurationEntry = Tkinter.Entry(self.pfatigueFrame, textvariable=self.pfatiguedurationVar, width=10)
                self.pfatigueambientEntry = Tkinter.Entry(self.pfatigueFrame, textvariable=self.pfatigueambientVar, width=10)
                self.pfatigueCheckButton.pack(side='left')
                pfatigueLabel1.pack(side='left')
                self.pfatiguelevelEntry.pack(side='left')
                pfatigueLabel2.pack(side='left')
                self.pfatiguedurationEntry.pack(side='left')
                pfatigueLabel3.pack(side='left')
                self.pfatigueambientEntry.pack(side='left')
                self.pfatigueFrame.pack()

                self.pstrengthFrame = Tkinter.Frame(self.potionsFrame)
                self.pstrengthCheckButton = Tkinter.Checkbutton(self.pstrengthFrame, variable=self.pstrengthCheck, onvalue=True, offvalue=False, height=1)
                pstrengthLabel1 = Tkinter.Label(self.pstrengthFrame, text = "Strength:  level: ", width=20)
                pstrengthLabel2 = Tkinter.Label(self.pstrengthFrame, text = "duration: ", width=15)
                pstrengthLabel3 = Tkinter.Label(self.pstrengthFrame, text = "ambient: ", width=15)
                self.pstrengthlevelEntry = Tkinter.Entry(self.pstrengthFrame, textvariable=self.pstrengthlevelVar, width=10)
                self.pstrengthdurationEntry = Tkinter.Entry(self.pstrengthFrame, textvariable=self.pstrengthdurationVar, width=10)
                self.pstrengthambientEntry = Tkinter.Entry(self.pstrengthFrame, textvariable=self.pstrengthambientVar, width=10)
                self.pstrengthCheckButton.pack(side='left')
                pstrengthLabel1.pack(side='left')
                self.pstrengthlevelEntry.pack(side='left')
                pstrengthLabel2.pack(side='left')
                self.pstrengthdurationEntry.pack(side='left')
                pstrengthLabel3.pack(side='left')
                self.pstrengthambientEntry.pack(side='left')
                self.pstrengthFrame.pack()

                self.pjumpFrame = Tkinter.Frame(self.potionsFrame)
                self.pjumpCheckButton = Tkinter.Checkbutton(self.pjumpFrame, variable=self.pjumpCheck, onvalue=True, offvalue=False, height=1)
                pjumpLabel1 = Tkinter.Label(self.pjumpFrame, text = "Jump:  level: ", width=20)
                pjumpLabel2 = Tkinter.Label(self.pjumpFrame, text = "duration: ", width=15)
                pjumpLabel3 = Tkinter.Label(self.pjumpFrame, text = "ambient: ", width=15)
                self.pjumplevelEntry = Tkinter.Entry(self.pjumpFrame, textvariable=self.pjumplevelVar, width=10)
                self.pjumpdurationEntry = Tkinter.Entry(self.pjumpFrame, textvariable=self.pjumpdurationVar, width=10)
                self.pjumpambientEntry = Tkinter.Entry(self.pjumpFrame, textvariable=self.pjumpambientVar, width=10)
                self.pjumpCheckButton.pack(side='left')
                pjumpLabel1.pack(side='left')
                self.pjumplevelEntry.pack(side='left')
                pjumpLabel2.pack(side='left')
                self.pjumpdurationEntry.pack(side='left')
                pjumpLabel3.pack(side='left')
                self.pjumpambientEntry.pack(side='left')
                self.pjumpFrame.pack()

                self.pnauseaFrame = Tkinter.Frame(self.potionsFrame)
                self.pnauseaCheckButton = Tkinter.Checkbutton(self.pnauseaFrame, variable=self.pnauseaCheck, onvalue=True, offvalue=False, height=1)
                pnauseaLabel1 = Tkinter.Label(self.pnauseaFrame, text = "Nausea:  level: ", width=20)
                pnauseaLabel2 = Tkinter.Label(self.pnauseaFrame, text = "duration: ", width=15)
                pnauseaLabel3 = Tkinter.Label(self.pnauseaFrame, text = "ambient: ", width=15)
                self.pnausealevelEntry = Tkinter.Entry(self.pnauseaFrame, textvariable=self.pnausealevelVar, width=10)
                self.pnauseadurationEntry = Tkinter.Entry(self.pnauseaFrame, textvariable=self.pnauseadurationVar, width=10)
                self.pnauseaambientEntry = Tkinter.Entry(self.pnauseaFrame, textvariable=self.pnauseaambientVar, width=10)
                self.pnauseaCheckButton.pack(side='left')
                pnauseaLabel1.pack(side='left')
                self.pnausealevelEntry.pack(side='left')
                pnauseaLabel2.pack(side='left')
                self.pnauseadurationEntry.pack(side='left')
                pnauseaLabel3.pack(side='left')
                self.pnauseaambientEntry.pack(side='left')
                self.pnauseaFrame.pack()

                self.pregenFrame = Tkinter.Frame(self.potionsFrame)
                self.pregenCheckButton = Tkinter.Checkbutton(self.pregenFrame, variable=self.pregenCheck, onvalue=True, offvalue=False, height=1)
                pregenLabel1 = Tkinter.Label(self.pregenFrame, text = "Regeneration:  level: ", width=20)
                pregenLabel2 = Tkinter.Label(self.pregenFrame, text = "duration: ", width=15)
                pregenLabel3 = Tkinter.Label(self.pregenFrame, text = "ambient: ", width=15)
                self.pregenlevelEntry = Tkinter.Entry(self.pregenFrame, textvariable=self.pregenlevelVar, width=10)
                self.pregendurationEntry = Tkinter.Entry(self.pregenFrame, textvariable=self.pregendurationVar, width=10)
                self.pregenambientEntry = Tkinter.Entry(self.pregenFrame, textvariable=self.pregenambientVar, width=10)
                self.pregenCheckButton.pack(side='left')
                pregenLabel1.pack(side='left')
                self.pregenlevelEntry.pack(side='left')
                pregenLabel2.pack(side='left')
                self.pregendurationEntry.pack(side='left')
                pregenLabel3.pack(side='left')
                self.pregenambientEntry.pack(side='left')
                self.pregenFrame.pack()

                self.presistFrame = Tkinter.Frame(self.potionsFrame)
                self.presistCheckButton = Tkinter.Checkbutton(self.presistFrame, variable=self.presistCheck, onvalue=True, offvalue=False, height=1)
                presistLabel1 = Tkinter.Label(self.presistFrame, text = "Resistance:  level: ", width=20)
                presistLabel2 = Tkinter.Label(self.presistFrame, text = "duration: ", width=15)
                presistLabel3 = Tkinter.Label(self.presistFrame, text = "ambient: ", width=15)
                self.presistlevelEntry = Tkinter.Entry(self.presistFrame, textvariable=self.presistlevelVar, width=10)
                self.presistdurationEntry = Tkinter.Entry(self.presistFrame, textvariable=self.presistdurationVar, width=10)
                self.presistambientEntry = Tkinter.Entry(self.presistFrame, textvariable=self.presistambientVar, width=10)
                self.presistCheckButton.pack(side='left')
                presistLabel1.pack(side='left')
                self.presistlevelEntry.pack(side='left')
                presistLabel2.pack(side='left')
                self.presistdurationEntry.pack(side='left')
                presistLabel3.pack(side='left')
                self.presistambientEntry.pack(side='left')
                self.presistFrame.pack()

                self.pfireresFrame = Tkinter.Frame(self.potionsFrame)
                self.pfireresCheckButton = Tkinter.Checkbutton(self.pfireresFrame, variable=self.pfireresCheck, onvalue=True, offvalue=False, height=1)
                pfireresLabel1 = Tkinter.Label(self.pfireresFrame, text = "Fire resist:  level: ", width=20)
                pfireresLabel2 = Tkinter.Label(self.pfireresFrame, text = "duration: ", width=15)
                pfireresLabel3 = Tkinter.Label(self.pfireresFrame, text = "ambient: ", width=15)
                self.pfirereslevelEntry = Tkinter.Entry(self.pfireresFrame, textvariable=self.pfirereslevelVar, width=10)
                self.pfireresdurationEntry = Tkinter.Entry(self.pfireresFrame, textvariable=self.pfireresdurationVar, width=10)
                self.pfireresambientEntry = Tkinter.Entry(self.pfireresFrame, textvariable=self.pfireresambientVar, width=10)
                self.pfireresCheckButton.pack(side='left')
                pfireresLabel1.pack(side='left')
                self.pfirereslevelEntry.pack(side='left')
                pfireresLabel2.pack(side='left')
                self.pfireresdurationEntry.pack(side='left')
                pfireresLabel3.pack(side='left')
                self.pfireresambientEntry.pack(side='left')
                self.pfireresFrame.pack()

                self.pwaterbrFrame = Tkinter.Frame(self.potionsFrame)
                self.pwaterbrCheckButton = Tkinter.Checkbutton(self.pwaterbrFrame, variable=self.pwaterbrCheck, onvalue=True, offvalue=False, height=1)
                pwaterbrLabel1 = Tkinter.Label(self.pwaterbrFrame, text = "Water breathing:  level: ", width=20)
                pwaterbrLabel2 = Tkinter.Label(self.pwaterbrFrame, text = "duration: ", width=15)
                pwaterbrLabel3 = Tkinter.Label(self.pwaterbrFrame, text = "ambient: ", width=15)
                self.pwaterbrlevelEntry = Tkinter.Entry(self.pwaterbrFrame, textvariable=self.pwaterbrlevelVar, width=10)
                self.pwaterbrdurationEntry = Tkinter.Entry(self.pwaterbrFrame, textvariable=self.pwaterbrdurationVar, width=10)
                self.pwaterbrambientEntry = Tkinter.Entry(self.pwaterbrFrame, textvariable=self.pwaterbrambientVar, width=10)
                self.pwaterbrCheckButton.pack(side='left')
                pwaterbrLabel1.pack(side='left')
                self.pwaterbrlevelEntry.pack(side='left')
                pwaterbrLabel2.pack(side='left')
                self.pwaterbrdurationEntry.pack(side='left')
                pwaterbrLabel3.pack(side='left')
                self.pwaterbrambientEntry.pack(side='left')
                self.pwaterbrFrame.pack()

                self.pinvisFrame = Tkinter.Frame(self.potionsFrame)
                self.pinvisCheckButton = Tkinter.Checkbutton(self.pinvisFrame, variable=self.pinvisCheck, onvalue=True, offvalue=False, height=1)
                pinvisLabel1 = Tkinter.Label(self.pinvisFrame, text = "Invisibility:  level: ", width=20)
                pinvisLabel2 = Tkinter.Label(self.pinvisFrame, text = "duration: ", width=15)
                pinvisLabel3 = Tkinter.Label(self.pinvisFrame, text = "ambient: ", width=15)
                self.pinvislevelEntry = Tkinter.Entry(self.pinvisFrame, textvariable=self.pinvislevelVar, width=10)
                self.pinvisdurationEntry = Tkinter.Entry(self.pinvisFrame, textvariable=self.pinvisdurationVar, width=10)
                self.pinvisambientEntry = Tkinter.Entry(self.pinvisFrame, textvariable=self.pinvisambientVar, width=10)
                self.pinvisCheckButton.pack(side='left')
                pinvisLabel1.pack(side='left')
                self.pinvislevelEntry.pack(side='left')
                pinvisLabel2.pack(side='left')
                self.pinvisdurationEntry.pack(side='left')
                pinvisLabel3.pack(side='left')
                self.pinvisambientEntry.pack(side='left')
                self.pinvisFrame.pack()

                self.pblindFrame = Tkinter.Frame(self.potionsFrame)
                self.pblindCheckButton = Tkinter.Checkbutton(self.pblindFrame, variable=self.pblindCheck, onvalue=True, offvalue=False, height=1)
                pblindLabel1 = Tkinter.Label(self.pblindFrame, text = "Blindness:  level: ", width=20)
                pblindLabel2 = Tkinter.Label(self.pblindFrame, text = "duration: ", width=15)
                pblindLabel3 = Tkinter.Label(self.pblindFrame, text = "ambient: ", width=15)
                self.pblindlevelEntry = Tkinter.Entry(self.pblindFrame, textvariable=self.pblindlevelVar, width=10)
                self.pblinddurationEntry = Tkinter.Entry(self.pblindFrame, textvariable=self.pblinddurationVar, width=10)
                self.pblindambientEntry = Tkinter.Entry(self.pblindFrame, textvariable=self.pblindambientVar, width=10)
                self.pblindCheckButton.pack(side='left')
                pblindLabel1.pack(side='left')
                self.pblindlevelEntry.pack(side='left')
                pblindLabel2.pack(side='left')
                self.pblinddurationEntry.pack(side='left')
                pblindLabel3.pack(side='left')
                self.pblindambientEntry.pack(side='left')
                self.pblindFrame.pack()

                self.pnightvFrame = Tkinter.Frame(self.potionsFrame)
                self.pnightvCheckButton = Tkinter.Checkbutton(self.pnightvFrame, variable=self.pnightvCheck, onvalue=True, offvalue=False, height=1)
                pnightvLabel1 = Tkinter.Label(self.pnightvFrame, text = "Night vision:  level: ", width=20)
                pnightvLabel2 = Tkinter.Label(self.pnightvFrame, text = "duration: ", width=15)
                pnightvLabel3 = Tkinter.Label(self.pnightvFrame, text = "ambient: ", width=15)
                self.pnightvlevelEntry = Tkinter.Entry(self.pnightvFrame, textvariable=self.pnightvlevelVar, width=10)
                self.pnightvdurationEntry = Tkinter.Entry(self.pnightvFrame, textvariable=self.pnightvdurationVar, width=10)
                self.pnightvambientEntry = Tkinter.Entry(self.pnightvFrame, textvariable=self.pnightvambientVar, width=10)
                self.pnightvCheckButton.pack(side='left')
                pnightvLabel1.pack(side='left')
                self.pnightvlevelEntry.pack(side='left')
                pnightvLabel2.pack(side='left')
                self.pnightvdurationEntry.pack(side='left')
                pnightvLabel3.pack(side='left')
                self.pnightvambientEntry.pack(side='left')
                self.pnightvFrame.pack()

                self.phungerFrame = Tkinter.Frame(self.potionsFrame)
                self.phungerCheckButton = Tkinter.Checkbutton(self.phungerFrame, variable=self.phungerCheck, onvalue=True, offvalue=False, height=1)
                phungerLabel1 = Tkinter.Label(self.phungerFrame, text = "Hunger:  level: ", width=20)
                phungerLabel2 = Tkinter.Label(self.phungerFrame, text = "duration: ", width=15)
                phungerLabel3 = Tkinter.Label(self.phungerFrame, text = "ambient: ", width=15)
                self.phungerlevelEntry = Tkinter.Entry(self.phungerFrame, textvariable=self.phungerlevelVar, width=10)
                self.phungerdurationEntry = Tkinter.Entry(self.phungerFrame, textvariable=self.phungerdurationVar, width=10)
                self.phungerambientEntry = Tkinter.Entry(self.phungerFrame, textvariable=self.phungerambientVar, width=10)
                self.phungerCheckButton.pack(side='left')
                phungerLabel1.pack(side='left')
                self.phungerlevelEntry.pack(side='left')
                phungerLabel2.pack(side='left')
                self.phungerdurationEntry.pack(side='left')
                phungerLabel3.pack(side='left')
                self.phungerambientEntry.pack(side='left')
                self.phungerFrame.pack()

                self.pweakFrame = Tkinter.Frame(self.potionsFrame)
                self.pweakCheckButton = Tkinter.Checkbutton(self.pweakFrame, variable=self.pweakCheck, onvalue=True, offvalue=False, height=1)
                pweakLabel1 = Tkinter.Label(self.pweakFrame, text = "Weakness:  level: ", width=20)
                pweakLabel2 = Tkinter.Label(self.pweakFrame, text = "duration: ", width=15)
                pweakLabel3 = Tkinter.Label(self.pweakFrame, text = "ambient: ", width=15)
                self.pweaklevelEntry = Tkinter.Entry(self.pweakFrame, textvariable=self.pweaklevelVar, width=10)
                self.pweakdurationEntry = Tkinter.Entry(self.pweakFrame, textvariable=self.pweakdurationVar, width=10)
                self.pweakambientEntry = Tkinter.Entry(self.pweakFrame, textvariable=self.pweakambientVar, width=10)
                self.pweakCheckButton.pack(side='left')
                pweakLabel1.pack(side='left')
                self.pweaklevelEntry.pack(side='left')
                pweakLabel2.pack(side='left')
                self.pweakdurationEntry.pack(side='left')
                pweakLabel3.pack(side='left')
                self.pweakambientEntry.pack(side='left')
                self.pweakFrame.pack()

                self.ppoisonFrame = Tkinter.Frame(self.potionsFrame)
                self.ppoisonCheckButton = Tkinter.Checkbutton(self.ppoisonFrame, variable=self.ppoisonCheck, onvalue=True, offvalue=False, height=1)
                ppoisonLabel1 = Tkinter.Label(self.ppoisonFrame, text = "Poison:  level: ", width=20)
                ppoisonLabel2 = Tkinter.Label(self.ppoisonFrame, text = "duration: ", width=15)
                ppoisonLabel3 = Tkinter.Label(self.ppoisonFrame, text = "ambient: ", width=15)
                self.ppoisonlevelEntry = Tkinter.Entry(self.ppoisonFrame, textvariable=self.ppoisonlevelVar, width=10)
                self.ppoisondurationEntry = Tkinter.Entry(self.ppoisonFrame, textvariable=self.ppoisondurationVar, width=10)
                self.ppoisonambientEntry = Tkinter.Entry(self.ppoisonFrame, textvariable=self.ppoisonambientVar, width=10)
                self.ppoisonCheckButton.pack(side='left')
                ppoisonLabel1.pack(side='left')
                self.ppoisonlevelEntry.pack(side='left')
                ppoisonLabel2.pack(side='left')
                self.ppoisondurationEntry.pack(side='left')
                ppoisonLabel3.pack(side='left')
                self.ppoisonambientEntry.pack(side='left')
                self.ppoisonFrame.pack()

                self.phealthFrame = Tkinter.Frame(self.potionsFrame)
                self.phealthCheckButton = Tkinter.Checkbutton(self.phealthFrame, variable=self.phealthCheck, onvalue=True, offvalue=False, height=1)
                phealthLabel1 = Tkinter.Label(self.phealthFrame, text = "Instant Health:  level: ", width=20)
                phealthLabel2 = Tkinter.Label(self.phealthFrame, text = "duration: ", width=15)
                phealthLabel3 = Tkinter.Label(self.phealthFrame, text = "ambient: ", width=15)
                self.phealthlevelEntry = Tkinter.Entry(self.phealthFrame, textvariable=self.phealthlevelVar, width=10)
                self.phealthdurationEntry = Tkinter.Entry(self.phealthFrame, textvariable=self.phealthdurationVar, width=10)
                self.phealthambientEntry = Tkinter.Entry(self.phealthFrame, textvariable=self.phealthambientVar, width=10)
                self.phealthCheckButton.pack(side='left')
                phealthLabel1.pack(side='left')
                self.phealthlevelEntry.pack(side='left')
                phealthLabel2.pack(side='left')
                self.phealthdurationEntry.pack(side='left')
                phealthLabel3.pack(side='left')
                self.phealthambientEntry.pack(side='left')
                self.phealthFrame.pack()

                self.pdamageFrame = Tkinter.Frame(self.potionsFrame)
                self.pdamageCheckButton = Tkinter.Checkbutton(self.pdamageFrame, variable=self.pdamageCheck, onvalue=True, offvalue=False, height=1)
                pdamageLabel1 = Tkinter.Label(self.pdamageFrame, text = "Instant Damage:  level: ", width=20)
                pdamageLabel2 = Tkinter.Label(self.pdamageFrame, text = "duration: ", width=15)
                pdamageLabel3 = Tkinter.Label(self.pdamageFrame, text = "ambient: ", width=15)
                self.pdamagelevelEntry = Tkinter.Entry(self.pdamageFrame, textvariable=self.pdamagelevelVar, width=10)
                self.pdamagedurationEntry = Tkinter.Entry(self.pdamageFrame, textvariable=self.pdamagedurationVar, width=10)
                self.pdamageambientEntry = Tkinter.Entry(self.pdamageFrame, textvariable=self.pdamageambientVar, width=10)
                self.pdamageCheckButton.pack(side='left')
                pdamageLabel1.pack(side='left')
                self.pdamagelevelEntry.pack(side='left')
                pdamageLabel2.pack(side='left')
                self.pdamagedurationEntry.pack(side='left')
                pdamageLabel3.pack(side='left')
                self.pdamageambientEntry.pack(side='left')
                self.pdamageFrame.pack()

                self.pwitherFrame = Tkinter.Frame(self.potionsFrame)
                self.pwitherCheckButton = Tkinter.Checkbutton(self.pwitherFrame, variable=self.pwitherCheck, onvalue=True, offvalue=False, height=1)
                pwitherLabel1 = Tkinter.Label(self.pwitherFrame, text = "Wither:  level: ", width=20)
                pwitherLabel2 = Tkinter.Label(self.pwitherFrame, text = "duration: ", width=15)
                pwitherLabel3 = Tkinter.Label(self.pwitherFrame, text = "ambient: ", width=15)
                self.pwitherlevelEntry = Tkinter.Entry(self.pwitherFrame, textvariable=self.pwitherlevelVar, width=10)
                self.pwitherdurationEntry = Tkinter.Entry(self.pwitherFrame, textvariable=self.pwitherdurationVar, width=10)
                self.pwitherambientEntry = Tkinter.Entry(self.pwitherFrame, textvariable=self.pwitherambientVar, width=10)
                self.pwitherCheckButton.pack(side='left')
                pwitherLabel1.pack(side='left')
                self.pwitherlevelEntry.pack(side='left')
                pwitherLabel2.pack(side='left')
                self.pwitherdurationEntry.pack(side='left')
                pwitherLabel3.pack(side='left')
                self.pwitherambientEntry.pack(side='left')
                self.pwitherFrame.pack()

#### spawner tags
                self.spawnerandbaseFrame = Tkinter.Frame(self.tabbedWindows)
                
                self.spawnerFrame = Tkinter.Frame(self.spawnerandbaseFrame)
                (Tkinter.Label(self.spawnerFrame, text = "Spawner data")).pack(pady=3)

                self.delayFrame = Tkinter.Frame(self.spawnerFrame)
                self.delayCheckButton = Tkinter.Checkbutton(self.delayFrame, variable=self.delayCheck, onvalue=True, offvalue=False, height=1)
                delayLabel = Tkinter.Label(self.delayFrame, text = "Delay: ", width=15)
                self.delayEntry = Tkinter.Entry(self.delayFrame, textvariable=self.delayVar, width=10)
                self.delayCheckButton.pack(side='left')
                delayLabel.pack(side='left')
                self.delayEntry.pack(side='left')
                self.delayFrame.pack()

                self.minspawndelayFrame = Tkinter.Frame(self.spawnerFrame)
                self.minspawndelayCheckButton = Tkinter.Checkbutton(self.minspawndelayFrame, variable=self.minspawndelayCheck, onvalue=True, offvalue=False, height=1)
                minspawndelayLabel = Tkinter.Label(self.minspawndelayFrame, text = "Min Spawn Delay: ", width=15)
                self.minspawndelayEntry = Tkinter.Entry(self.minspawndelayFrame, textvariable=self.minspawndelayVar, width=10)
                self.minspawndelayCheckButton.pack(side='left')
                minspawndelayLabel.pack(side='left')
                self.minspawndelayEntry.pack(side='left')
                self.minspawndelayFrame.pack()

                self.maxspawndelayFrame = Tkinter.Frame(self.spawnerFrame)
                self.maxspawndelayCheckButton = Tkinter.Checkbutton(self.maxspawndelayFrame, variable=self.maxspawndelayCheck, onvalue=True, offvalue=False, height=1)
                maxspawndelayLabel = Tkinter.Label(self.maxspawndelayFrame, text = "Max Spawn Delay: ", width=15)
                self.maxspawndelayEntry = Tkinter.Entry(self.maxspawndelayFrame, textvariable=self.maxspawndelayVar, width=10)
                self.maxspawndelayCheckButton.pack(side='left')
                maxspawndelayLabel.pack(side='left')
                self.maxspawndelayEntry.pack(side='left')
                self.maxspawndelayFrame.pack()

                self.spawncountFrame = Tkinter.Frame(self.spawnerFrame)
                self.spawncountCheckButton = Tkinter.Checkbutton(self.spawncountFrame, variable=self.spawncountCheck, onvalue=True, offvalue=False, height=1)
                spawncountLabel = Tkinter.Label(self.spawncountFrame, text = "Spawn Count: ", width=15)
                self.spawncountEntry = Tkinter.Entry(self.spawncountFrame, textvariable=self.spawncountVar, width=10)
                self.spawncountCheckButton.pack(side='left')
                spawncountLabel.pack(side='left')
                self.spawncountEntry.pack(side='left')
                self.spawncountFrame.pack()

                self.MaxNearbyEntitiesFrame = Tkinter.Frame(self.spawnerFrame)
                self.MaxNearbyEntitiesCheckButton = Tkinter.Checkbutton(self.MaxNearbyEntitiesFrame, variable=self.MaxNearbyEntitiesCheck, onvalue=True, offvalue=False, height=1)
                MaxNearbyEntitiesLabel = Tkinter.Label(self.MaxNearbyEntitiesFrame, text = "Max Nearby Entities: ", width=20)
                self.MaxNearbyEntitiesEntry = Tkinter.Entry(self.MaxNearbyEntitiesFrame, textvariable=self.MaxNearbyEntitiesVar, width=10)
                self.MaxNearbyEntitiesCheckButton.pack(side='left')
                MaxNearbyEntitiesLabel.pack(side='left')
                self.MaxNearbyEntitiesEntry.pack(side='left')
                self.MaxNearbyEntitiesFrame.pack()

                self.RequiredPlayerRangeFrame = Tkinter.Frame(self.spawnerFrame)
                self.RequiredPlayerRangeCheckButton = Tkinter.Checkbutton(self.RequiredPlayerRangeFrame, variable=self.RequiredPlayerRangeCheck, onvalue=True, offvalue=False, height=1)
                RequiredPlayerRangeLabel = Tkinter.Label(self.RequiredPlayerRangeFrame, text = "Required Player Range: ", width=20)
                self.RequiredPlayerRangeEntry = Tkinter.Entry(self.RequiredPlayerRangeFrame, textvariable=self.RequiredPlayerRangeVar, width=10)
                self.RequiredPlayerRangeCheckButton.pack(side='left')
                RequiredPlayerRangeLabel.pack(side='left')
                self.RequiredPlayerRangeEntry.pack(side='left')
                self.RequiredPlayerRangeFrame.pack()

                self.SpawnRangeFrame = Tkinter.Frame(self.spawnerFrame)
                self.SpawnRangeCheckButton = Tkinter.Checkbutton(self.SpawnRangeFrame, variable=self.SpawnRangeCheck, onvalue=True, offvalue=False, height=1)
                SpawnRangeLabel = Tkinter.Label(self.SpawnRangeFrame, text = "Spawn Range: ", width=20)
                self.SpawnRangeEntry = Tkinter.Entry(self.SpawnRangeFrame, textvariable=self.SpawnRangeVar, width=10)
                self.SpawnRangeCheckButton.pack(side='left')
                SpawnRangeLabel.pack(side='left')
                self.SpawnRangeEntry.pack(side='left')
                self.SpawnRangeFrame.pack()
                
#### base tags
                self.baseFrame = Tkinter.Frame(self.spawnerandbaseFrame)
                (Tkinter.Label(self.baseFrame, text = "Base mob data")).pack(pady=3)
                                
                self.healthFrame = Tkinter.Frame(self.baseFrame)
                self.healthCheckButton = Tkinter.Checkbutton(self.healthFrame, variable=self.healthCheck, onvalue=True, offvalue=False, height=1)
                healthLabel = Tkinter.Label(self.healthFrame, text = "Health: ", width=15)
                self.healthEntry = Tkinter.Entry(self.healthFrame, textvariable=self.healthVar, width=10)
                self.healthCheckButton.pack(side='left')
                healthLabel.pack(side='left')
                self.healthEntry.pack(side='left')
                self.healthFrame.pack()

                self.fireFrame = Tkinter.Frame(self.baseFrame)
                self.fireCheckButton = Tkinter.Checkbutton(self.fireFrame, variable=self.fireCheck, onvalue=True, offvalue=False, height=1)
                fireLabel = Tkinter.Label(self.fireFrame, text = "Fire: ", width=15)
                self.fireEntry = Tkinter.Entry(self.fireFrame, textvariable=self.fireVar, width=10)
                self.fireCheckButton.pack(side='left')
                fireLabel.pack(side='left')
                self.fireEntry.pack(side='left')
                self.fireFrame.pack()

                self.airFrame = Tkinter.Frame(self.baseFrame)
                self.airCheckButton = Tkinter.Checkbutton(self.airFrame, variable=self.airCheck, onvalue=True, offvalue=False, height=1)
                airLabel = Tkinter.Label(self.airFrame, text = "Air: ", width=15)
                self.airEntry = Tkinter.Entry(self.airFrame, textvariable=self.airVar, width=10)
                self.airCheckButton.pack(side='left')
                airLabel.pack(side='left')
                self.airEntry.pack(side='left')
                self.airFrame.pack()

                self.attacktimeFrame = Tkinter.Frame(self.baseFrame)
                self.attacktimeCheckButton = Tkinter.Checkbutton(self.attacktimeFrame, variable=self.attacktimeCheck, onvalue=True, offvalue=False, height=1)
                attacktimeLabel = Tkinter.Label(self.attacktimeFrame, text = "Attack Time: ", width=15)
                self.attacktimeEntry = Tkinter.Entry(self.attacktimeFrame, textvariable=self.attacktimeVar, width=10)
                self.attacktimeCheckButton.pack(side='left')
                attacktimeLabel.pack(side='left')
                self.attacktimeEntry.pack(side='left')
                self.attacktimeFrame.pack()

                self.hurttimeFrame = Tkinter.Frame(self.baseFrame)
                self.hurttimeCheckButton = Tkinter.Checkbutton(self.hurttimeFrame, variable=self.hurttimeCheck, onvalue=True, offvalue=False, height=1)
                hurttimeLabel = Tkinter.Label(self.hurttimeFrame, text = "Hurt Time: ", width=15)
                self.hurttimeEntry = Tkinter.Entry(self.hurttimeFrame, textvariable=self.hurttimeVar, width=10)
                self.hurttimeCheckButton.pack(side='left')
                hurttimeLabel.pack(side='left')
                self.hurttimeEntry.pack(side='left')
                self.hurttimeFrame.pack()

                self.deathtimeFrame = Tkinter.Frame(self.baseFrame)
                self.deathtimeCheckButton = Tkinter.Checkbutton(self.deathtimeFrame, variable=self.deathtimeCheck, onvalue=True, offvalue=False, height=1)
                deathtimeLabel = Tkinter.Label(self.deathtimeFrame, text = "Death Time: ", width=15)
                self.deathtimeEntry = Tkinter.Entry(self.deathtimeFrame, textvariable=self.deathtimeVar, width=10)
                self.deathtimeCheckButton.pack(side='left')
                deathtimeLabel.pack(side='left')
                self.deathtimeEntry.pack(side='left')
                self.deathtimeFrame.pack()

                self.canlootFrame = Tkinter.Frame(self.baseFrame)
                self.canlootCheckButton = Tkinter.Checkbutton(self.canlootFrame, variable=self.canlootCheck, onvalue=True, offvalue=False, height=1)
                canlootLabel = Tkinter.Label(self.canlootFrame, text = "Can Pick Up Loot: ", width=15)
                self.canlootEntry = Tkinter.Entry(self.canlootFrame, textvariable=self.canlootVar, width=10)
                self.canlootCheckButton.pack(side='left')
                canlootLabel.pack(side='left')
                self.canlootEntry.pack(side='left')
                self.canlootFrame.pack()

                self.dimensionFrame = Tkinter.Frame(self.baseFrame)
                self.dimensionCheckButton = Tkinter.Checkbutton(self.dimensionFrame, variable=self.dimensionCheck, onvalue=True, offvalue=False, height=1)
                dimensionLabel = Tkinter.Label(self.dimensionFrame, text = "Dimension: ", width=15)
                self.dimensionEntry = Tkinter.Entry(self.dimensionFrame, textvariable=self.dimensionVar, width=10)
                self.dimensionCheckButton.pack(side='left')
                dimensionLabel.pack(side='left')
                self.dimensionEntry.pack(side='left')
                self.dimensionFrame.pack()

                self.persistencereqFrame = Tkinter.Frame(self.baseFrame)
                self.persistencereqCheckButton = Tkinter.Checkbutton(self.persistencereqFrame, variable=self.persistencereqCheck, onvalue=True, offvalue=False, height=1)
                persistencereqLabel = Tkinter.Label(self.persistencereqFrame, text = "Persistence Req: ", width=15)
                self.persistencereqEntry = Tkinter.Entry(self.persistencereqFrame, textvariable=self.persistencereqVar, width=10)
                self.persistencereqCheckButton.pack(side='left')
                persistencereqLabel.pack(side='left')
                self.persistencereqEntry.pack(side='left')
                self.persistencereqFrame.pack()

                self.invulnerableFrame = Tkinter.Frame(self.baseFrame)
                self.invulnerableCheckButton = Tkinter.Checkbutton(self.invulnerableFrame, variable=self.invulnerableCheck, onvalue=True, offvalue=False, height=1)
                invulnerableLabel = Tkinter.Label(self.invulnerableFrame, text = "Invulnerable: ", width=15)
                self.invulnerableEntry = Tkinter.Entry(self.invulnerableFrame, textvariable=self.invulnerableVar, width=10)
                self.invulnerableCheckButton.pack(side='left')
                invulnerableLabel.pack(side='left')
                self.invulnerableEntry.pack(side='left')
                self.invulnerableFrame.pack()

#### position and motion tags
                self.positionmotionFrame = Tkinter.Frame(self.tabbedWindows)
                self.positionFrame = Tkinter.Frame(self.positionmotionFrame)
                (Tkinter.Label(self.positionFrame, text = "Mob position data")).pack(pady=3)
                                
                self.positionCheckButton = Tkinter.Checkbutton(self.positionFrame, variable=self.positionCheck, onvalue=True, offvalue=False, height=1)
                self.positionCheckButton.pack()
                self.positionXFrame = Tkinter.Frame(self.positionFrame)
                positionXLabel = Tkinter.Label(self.positionXFrame, text = "X coordinate: ", width=15)
                self.positionXEntry = Tkinter.Entry(self.positionXFrame, textvariable=self.positionXVar, width=10)
                positionXLabel.pack(side='left')
                self.positionXEntry.pack(side='left')
                self.positionXFrame.pack()

                self.positionYFrame = Tkinter.Frame(self.positionFrame)
                positionYLabel = Tkinter.Label(self.positionYFrame, text = "Y coordinate: ", width=15)
                self.positionYEntry = Tkinter.Entry(self.positionYFrame, textvariable=self.positionYVar, width=10)
                positionYLabel.pack(side='left')
                self.positionYEntry.pack(side='left')
                self.positionYFrame.pack()

                self.positionZFrame = Tkinter.Frame(self.positionFrame)
                positionZLabel = Tkinter.Label(self.positionZFrame, text = "Z coordinate: ", width=15)
                self.positionZEntry = Tkinter.Entry(self.positionZFrame, textvariable=self.positionZVar, width=10)
                positionZLabel.pack(side='left')
                self.positionZEntry.pack(side='left')
                self.positionZFrame.pack()

                self.motionFrame = Tkinter.Frame(self.positionmotionFrame)
                (Tkinter.Label(self.motionFrame, text = "Mob motion data")).pack(pady=3)
                
                self.motionCheckButton = Tkinter.Checkbutton(self.motionFrame, variable=self.motionCheck, onvalue=True, offvalue=False, height=1)
                self.motionCheckButton.pack()
                self.motionXFrame = Tkinter.Frame(self.motionFrame)
                motionXLabel = Tkinter.Label(self.motionXFrame, text = "X motion: ", width=15)
                self.motionXEntry = Tkinter.Entry(self.motionXFrame, textvariable=self.motionXVar, width=10)
                motionXLabel.pack(side='left')
                self.motionXEntry.pack(side='left')
                self.motionXFrame.pack()

                self.motionYFrame = Tkinter.Frame(self.motionFrame)
                motionYLabel = Tkinter.Label(self.motionYFrame, text = "Y motion: ", width=15)
                self.motionYEntry = Tkinter.Entry(self.motionYFrame, textvariable=self.motionYVar, width=10)
                motionYLabel.pack(side='left')
                self.motionYEntry.pack(side='left')
                self.motionYFrame.pack()

                self.motionZFrame = Tkinter.Frame(self.motionFrame)
                motionZLabel = Tkinter.Label(self.motionZFrame, text = "Z motion: ", width=15)
                self.motionZEntry = Tkinter.Entry(self.motionZFrame, textvariable=self.motionZVar, width=10)
                motionZLabel.pack(side='left')
                self.motionZEntry.pack(side='left')
                self.motionZFrame.pack()

                self.directionFrame = Tkinter.Frame(self.positionmotionFrame)
                (Tkinter.Label(self.directionFrame, text = "Entity direction data")).pack(pady=3)

                self.directionCheckButton = Tkinter.Checkbutton(self.directionFrame, variable=self.directionCheck, onvalue=True, offvalue=False, height=1)
                self.directionCheckButton.pack()
                self.directionXFrame = Tkinter.Frame(self.directionFrame)
                directionXLabel = Tkinter.Label(self.directionXFrame, text = "X direction: ", width=15)
                self.directionXEntry = Tkinter.Entry(self.directionXFrame, textvariable=self.directionXVar, width=10)
                directionXLabel.pack(side='left')
                self.directionXEntry.pack(side='left')
                self.directionXFrame.pack()

                self.directionYFrame = Tkinter.Frame(self.directionFrame)
                directionYLabel = Tkinter.Label(self.directionYFrame, text = "Y direction: ", width=15)
                self.directionYEntry = Tkinter.Entry(self.directionYFrame, textvariable=self.directionYVar, width=10)
                directionYLabel.pack(side='left')
                self.directionYEntry.pack(side='left')
                self.directionYFrame.pack()

                self.directionZFrame = Tkinter.Frame(self.directionFrame)
                directionZLabel = Tkinter.Label(self.directionZFrame, text = "Z direction: ", width=15)
                self.directionZEntry = Tkinter.Entry(self.directionZFrame, textvariable=self.directionZVar, width=10)
                directionZLabel.pack(side='left')
                self.directionZEntry.pack(side='left')
                self.directionZFrame.pack()

#### mob specific frame stuff
                
                self.mobspecificFrame = Tkinter.Frame(self.tabbedWindows)
                self.breedableFrame = Tkinter.Frame(self.mobspecificFrame)
                self.hostileotherFrame = Tkinter.Frame(self.mobspecificFrame)

#### golem tags
                self.golemFrame = Tkinter.Frame(self.breedableFrame)
                (Tkinter.Label(self.golemFrame, text = "Golem data")).pack(pady=3)

                self.PlayerCreatedFrame = Tkinter.Frame(self.golemFrame)
                self.PlayerCreatedCheckButton = Tkinter.Checkbutton(self.PlayerCreatedFrame, variable=self.PlayerCreatedCheck, onvalue=True, offvalue=False, height=1)
                PlayerCreatedLabel = Tkinter.Label(self.PlayerCreatedFrame, text = "Player Created: ", width=15)
                self.PlayerCreatedEntry = Tkinter.Entry(self.PlayerCreatedFrame, textvariable=self.PlayerCreatedVar, width=10)
                self.PlayerCreatedCheckButton.pack(side='left')
                PlayerCreatedLabel.pack(side='left')
                self.PlayerCreatedEntry.pack(side='left')
                self.PlayerCreatedFrame.pack()

#### breedable tags
                
                self.breedFrame = Tkinter.Frame(self.breedableFrame)
                (Tkinter.Label(self.breedFrame, text = "Breedable mob data")).pack(pady=3)

                self.inloveFrame = Tkinter.Frame(self.breedFrame)
                self.inloveCheckButton = Tkinter.Checkbutton(self.inloveFrame, variable=self.inloveCheck, onvalue=True, offvalue=False, height=1)
                inloveLabel = Tkinter.Label(self.inloveFrame, text = "In Love: ", width=15)
                self.inloveEntry = Tkinter.Entry(self.inloveFrame, textvariable=self.inloveVar, width=10)
                self.inloveCheckButton.pack(side='left')
                inloveLabel.pack(side='left')
                self.inloveEntry.pack(side='left')
                self.inloveFrame.pack()

                self.mobageFrame = Tkinter.Frame(self.breedFrame)
                self.mobageCheckButton = Tkinter.Checkbutton(self.mobageFrame, variable=self.mobageCheck, onvalue=True, offvalue=False, height=1)
                mobageLabel = Tkinter.Label(self.mobageFrame, text = "Age: ", width=15)
                self.mobageEntry = Tkinter.Entry(self.mobageFrame, textvariable=self.mobageVar, width=10)
                self.mobageCheckButton.pack(side='left')
                mobageLabel.pack(side='left')
                self.mobageEntry.pack(side='left')
                self.mobageFrame.pack()

#### pig tags
                self.pigFrame = Tkinter.Frame(self.breedableFrame)
                (Tkinter.Label(self.pigFrame, text = "Pig data")).pack(pady=3)

                self.saddleFrame = Tkinter.Frame(self.pigFrame)
                self.saddleCheckButton = Tkinter.Checkbutton(self.saddleFrame, variable=self.saddleCheck, onvalue=True, offvalue=False, height=1)
                saddleLabel = Tkinter.Label(self.saddleFrame, text = "Saddle: ", width=15)
                self.saddleEntry = Tkinter.Entry(self.saddleFrame, textvariable=self.saddleVar, width=10)
                self.saddleCheckButton.pack(side='left')
                saddleLabel.pack(side='left')
                self.saddleEntry.pack(side='left')
                self.saddleFrame.pack()

#### sheep tags
                self.sheepFrame = Tkinter.Frame(self.breedableFrame)
                (Tkinter.Label(self.sheepFrame, text = "Sheep data")).pack(pady=3)

                self.shearedFrame = Tkinter.Frame(self.sheepFrame)
                self.shearedCheckButton = Tkinter.Checkbutton(self.shearedFrame, variable=self.shearedCheck, onvalue=True, offvalue=False, height=1)
                shearedLabel = Tkinter.Label(self.shearedFrame, text = "Sheared: ", width=15)
                self.shearedEntry = Tkinter.Entry(self.shearedFrame, textvariable=self.shearedVar, width=10)
                self.shearedCheckButton.pack(side='left')
                shearedLabel.pack(side='left')
                self.shearedEntry.pack(side='left')
                self.shearedFrame.pack()

                self.sheepcolorFrame = Tkinter.Frame(self.sheepFrame)
                self.colorCheckButton = Tkinter.Checkbutton(self.sheepcolorFrame, variable=self.colorCheck, onvalue=True, offvalue=False, height=1)
                sheepcolorLabel = Tkinter.Label(self.sheepcolorFrame, text = "Color: ", width=15)
                self.colorEntry = Tkinter.Entry(self.sheepcolorFrame, textvariable=self.colorVar, width=10)
                self.colorCheckButton.pack(side='left')
                sheepcolorLabel.pack(side='left')
                self.colorEntry.pack(side='left')
                self.sheepcolorFrame.pack()

#### zombie tags
                self.zombieFrame = Tkinter.Frame(self.hostileotherFrame)
                (Tkinter.Label(self.zombieFrame, text = "Zombie data")).pack(pady=3)

                self.isvillagerFrame = Tkinter.Frame(self.zombieFrame)
                self.isvillagerCheckButton = Tkinter.Checkbutton(self.isvillagerFrame, variable=self.isvillagerCheck, onvalue=True, offvalue=False, height=1)
                isvillagerLabel = Tkinter.Label(self.isvillagerFrame, text = "Is villager: ", width=15)
                self.isvillagerEntry = Tkinter.Entry(self.isvillagerFrame, textvariable=self.isvillagerVar, width=10)
                self.isvillagerCheckButton.pack(side='left')
                isvillagerLabel.pack(side='left')
                self.isvillagerEntry.pack(side='left')
                self.isvillagerFrame.pack()

                self.isbabyFrame = Tkinter.Frame(self.zombieFrame)
                self.isbabyCheckButton = Tkinter.Checkbutton(self.isbabyFrame, variable=self.isbabyCheck, onvalue=True, offvalue=False, height=1)
                isbabyLabel = Tkinter.Label(self.isbabyFrame, text = "Is baby: ", width=15)
                self.isbabyEntry = Tkinter.Entry(self.isbabyFrame, textvariable=self.isbabyVar, width=10)
                self.isbabyCheckButton.pack(side='left')
                isbabyLabel.pack(side='left')
                self.isbabyEntry.pack(side='left')
                self.isbabyFrame.pack()

                self.conversiontimeFrame = Tkinter.Frame(self.zombieFrame)
                self.conversiontimeCheckButton = Tkinter.Checkbutton(self.conversiontimeFrame, variable=self.conversiontimeCheck, onvalue=True, offvalue=False, height=1)
                conversiontimeLabel = Tkinter.Label(self.conversiontimeFrame, text = "Conversion time: ", width=15)
                self.conversiontimeEntry = Tkinter.Entry(self.conversiontimeFrame, textvariable=self.conversiontimeVar, width=10)
                self.conversiontimeCheckButton.pack(side='left')
                conversiontimeLabel.pack(side='left')
                self.conversiontimeEntry.pack(side='left')
                self.conversiontimeFrame.pack()                 

#### creeper tags
                self.creeperFrame = Tkinter.Frame(self.hostileotherFrame)
                (Tkinter.Label(self.creeperFrame, text = "Creeper data")).pack(pady=3)

                self.poweredFrame = Tkinter.Frame(self.creeperFrame)
                self.poweredCheckButton = Tkinter.Checkbutton(self.poweredFrame, variable=self.poweredCheck, onvalue=True, offvalue=False, height=1)
                poweredLabel = Tkinter.Label(self.poweredFrame, text = "Charged: ", width=15)
                self.poweredEntry = Tkinter.Entry(self.poweredFrame, textvariable=self.poweredVar, width=10)
                self.poweredCheckButton.pack(side='left')
                poweredLabel.pack(side='left')
                self.poweredEntry.pack(side='left')
                self.poweredFrame.pack()

                self.creeperfuseFrame = Tkinter.Frame(self.creeperFrame)
                self.creeperfuseCheckButton = Tkinter.Checkbutton(self.creeperfuseFrame, variable=self.creeperfuseCheck, onvalue=True, offvalue=False, height=1)
                creeperfuseLabel = Tkinter.Label(self.creeperfuseFrame, text = "Fuse: ", width=15)
                self.creeperfuseEntry = Tkinter.Entry(self.creeperfuseFrame, textvariable=self.creeperfuseVar, width=10)
                self.creeperfuseCheckButton.pack(side='left')
                creeperfuseLabel.pack(side='left')
                self.creeperfuseEntry.pack(side='left')
                self.creeperfuseFrame.pack()

                self.explosionradiusFrame = Tkinter.Frame(self.creeperFrame)
                self.explosionradiusCheckButton = Tkinter.Checkbutton(self.explosionradiusFrame, variable=self.explosionradiusCheck, onvalue=True, offvalue=False, height=1)
                explosionradiusLabel = Tkinter.Label(self.explosionradiusFrame, text = "Exp Radius: ", width=15)
                self.explosionradiusEntry = Tkinter.Entry(self.explosionradiusFrame, textvariable=self.explosionradiusVar, width=10)
                self.explosionradiusCheckButton.pack(side='left')
                explosionradiusLabel.pack(side='left')
                self.explosionradiusEntry.pack(side='left')
                self.explosionradiusFrame.pack()
                
#### bat tags
                self.batFrame = Tkinter.Frame(self.hostileotherFrame)
                (Tkinter.Label(self.batFrame, text = "Bat data")).pack(pady=3)

                self.batflagsFrame = Tkinter.Frame(self.batFrame)
                self.batflagsCheckButton = Tkinter.Checkbutton(self.batflagsFrame, variable=self.batflagsCheck, onvalue=True, offvalue=False, height=1)
                batflagsLabel = Tkinter.Label(self.batflagsFrame, text = "Bat Flags: ", width=15)
                self.batflagsEntry = Tkinter.Entry(self.batflagsFrame, textvariable=self.batflagsVar, width=10)
                self.batflagsCheckButton.pack(side='left')
                batflagsLabel.pack(side='left')
                self.batflagsEntry.pack(side='left')
                self.batflagsFrame.pack()

#### skeleton tags
                self.skeletonFrame = Tkinter.Frame(self.hostileotherFrame)
                (Tkinter.Label(self.skeletonFrame, text = "Skeleton data")).pack(pady=3)

                self.skeletontypeFrame = Tkinter.Frame(self.skeletonFrame)
                self.skeletontypeCheckButton = Tkinter.Checkbutton(self.skeletontypeFrame, variable=self.skeletontypeCheck, onvalue=True, offvalue=False, height=1)
                skeletontypeLabel = Tkinter.Label(self.skeletontypeFrame, text = "Skeleton Type: ", width=15)
                self.skeletontypeEntry = Tkinter.Entry(self.skeletontypeFrame, textvariable=self.skeletontypeVar, width=10)
                self.skeletontypeCheckButton.pack(side='left')
                skeletontypeLabel.pack(side='left')
                self.skeletontypeEntry.pack(side='left')
                self.skeletontypeFrame.pack()

#### skeleton tags
                self.witherbossFrame = Tkinter.Frame(self.hostileotherFrame)
                (Tkinter.Label(self.witherbossFrame, text = "Wither boss data")).pack(pady=3)

                self.witherinvulFrame = Tkinter.Frame(self.witherbossFrame)
                self.witherinvulCheckButton = Tkinter.Checkbutton(self.witherinvulFrame, variable=self.witherinvulCheck, onvalue=True, offvalue=False, height=1)
                witherinvulLabel = Tkinter.Label(self.witherinvulFrame, text = "Invul: ", width=15)
                self.witherinvulEntry = Tkinter.Entry(self.witherinvulFrame, textvariable=self.witherinvulVar, width=10)
                self.witherinvulCheckButton.pack(side='left')
                witherinvulLabel.pack(side='left')
                self.witherinvulEntry.pack(side='left')
                self.witherinvulFrame.pack()
#### slime tags
                self.slimeFrame = Tkinter.Frame(self.hostileotherFrame)
                (Tkinter.Label(self.slimeFrame, text = "Slime data")).pack(pady=3)

                self.sizeFrame = Tkinter.Frame(self.slimeFrame)
                self.sizeCheckButton = Tkinter.Checkbutton(self.sizeFrame, variable=self.sizeCheck, onvalue=True, offvalue=False, height=1)
                sizeLabel = Tkinter.Label(self.sizeFrame, text = "Size: ", width=15)
                self.sizeEntry = Tkinter.Entry(self.sizeFrame, textvariable=self.sizeVar, width=10)
                self.sizeCheckButton.pack(side='left')
                sizeLabel.pack(side='left')
                self.sizeEntry.pack(side='left')
                self.sizeFrame.pack()

#### wolf and cat tags
                self.wolfcatFrame = Tkinter.Frame(self.breedableFrame)
                (Tkinter.Label(self.wolfcatFrame, text = "Wolf and cat data")).pack(pady=3)

                self.ownerFrame = Tkinter.Frame(self.wolfcatFrame)
                self.ownerCheckButton = Tkinter.Checkbutton(self.ownerFrame, variable=self.ownerCheck, onvalue=True, offvalue=False, height=1)
                ownerLabel = Tkinter.Label(self.ownerFrame, text = "Owner: ", width=15)
                self.ownerEntry = Tkinter.Entry(self.ownerFrame, textvariable=self.ownerVar, width=10)
                self.ownerCheckButton.pack(side='left')
                ownerLabel.pack(side='left')
                self.ownerEntry.pack(side='left')
                self.ownerFrame.pack()

                self.sittingFrame = Tkinter.Frame(self.wolfcatFrame)
                self.sittingCheckButton = Tkinter.Checkbutton(self.sittingFrame, variable=self.sittingCheck, onvalue=True, offvalue=False, height=1)
                sittingLabel = Tkinter.Label(self.sittingFrame, text = "Sitting: ", width=15)
                self.sittingEntry = Tkinter.Entry(self.sittingFrame, textvariable=self.sittingVar, width=10)
                self.sittingCheckButton.pack(side='left')
                sittingLabel.pack(side='left')
                self.sittingEntry.pack(side='left')
                self.sittingFrame.pack()

#### wolf tags
                self.wolfFrame = Tkinter.Frame(self.breedableFrame)
                (Tkinter.Label(self.wolfFrame, text = "Wolf data")).pack(pady=3)

                self.angryFrame = Tkinter.Frame(self.wolfFrame)
                self.angryCheckButton = Tkinter.Checkbutton(self.angryFrame, variable=self.angryCheck, onvalue=True, offvalue=False, height=1)
                angryLabel = Tkinter.Label(self.angryFrame, text = "Angry: ", width=15)
                self.angryEntry = Tkinter.Entry(self.angryFrame, textvariable=self.angryVar, width=10)
                self.angryCheckButton.pack(side='left')
                angryLabel.pack(side='left')
                self.angryEntry.pack(side='left')
                self.angryFrame.pack()

                self.collarcolorFrame = Tkinter.Frame(self.wolfFrame)
                self.collarcolorCheckButton = Tkinter.Checkbutton(self.collarcolorFrame, variable=self.collarcolorCheck, onvalue=True, offvalue=False, height=1)
                collarcolorLabel = Tkinter.Label(self.collarcolorFrame, text = "Collar color: ", width=15)
                self.collarcolorEntry = Tkinter.Entry(self.collarcolorFrame, textvariable=self.collarcolorVar, width=10)
                self.collarcolorCheckButton.pack(side='left')
                collarcolorLabel.pack(side='left')
                self.collarcolorEntry.pack(side='left')
                self.collarcolorFrame.pack()

#### cat tags
                self.catFrame = Tkinter.Frame(self.breedableFrame)
                (Tkinter.Label(self.catFrame, text = "Cat data")).pack(pady=3)

                self.cattypeFrame = Tkinter.Frame(self.catFrame)
                self.cattypeCheckButton = Tkinter.Checkbutton(self.cattypeFrame, variable=self.cattypeCheck, onvalue=True, offvalue=False, height=1)
                cattypeLabel = Tkinter.Label(self.cattypeFrame, text = "CatType: ", width=15)
                self.cattypeEntry = Tkinter.Entry(self.cattypeFrame, textvariable=self.cattypeVar, width=10)
                self.cattypeCheckButton.pack(side='left')
                cattypeLabel.pack(side='left')
                self.cattypeEntry.pack(side='left')
                self.cattypeFrame.pack()

#### pigman tags
                self.pigmanFrame = Tkinter.Frame(self.hostileotherFrame)
                (Tkinter.Label(self.pigmanFrame, text = "Pigman data")).pack(pady=3)

                self.angerFrame = Tkinter.Frame(self.pigmanFrame)
                self.angerCheckButton = Tkinter.Checkbutton(self.angerFrame, variable=self.angerCheck, onvalue=True, offvalue=False, height=1)
                angerLabel = Tkinter.Label(self.angerFrame, text = "Anger: ", width=15)
                self.angerEntry = Tkinter.Entry(self.angerFrame, textvariable=self.angerVar, width=10)
                self.angerCheckButton.pack(side='left')
                angerLabel.pack(side='left')
                self.angerEntry.pack(side='left')
                self.angerFrame.pack()

#### enderman tags
                self.endermanFrame = Tkinter.Frame(self.hostileotherFrame)
                (Tkinter.Label(self.endermanFrame, text = "Enderman data")).pack(pady=3)

                self.carriedFrame = Tkinter.Frame(self.endermanFrame)
                self.carriedCheckButton = Tkinter.Checkbutton(self.carriedFrame, variable=self.carriedCheck, onvalue=True, offvalue=False, height=1)
                carriedLabel = Tkinter.Label(self.carriedFrame, text = "Carried: ", width=15)
                self.carriedEntry = Tkinter.Entry(self.carriedFrame, textvariable=self.carriedVar, width=10)
                self.carriedCheckButton.pack(side='left')
                carriedLabel.pack(side='left')
                self.carriedEntry.pack(side='left')
                self.carriedFrame.pack()

                self.carrieddataFrame = Tkinter.Frame(self.endermanFrame)
                self.carrieddataCheckButton = Tkinter.Checkbutton(self.carrieddataFrame, variable=self.carrieddataCheck, onvalue=True, offvalue=False, height=1)
                carrieddataLabel = Tkinter.Label(self.carrieddataFrame, text = "Carried Data: ", width=15)
                self.carrieddataEntry = Tkinter.Entry(self.carrieddataFrame, textvariable=self.carrieddataVar, width=10)
                self.carrieddataCheckButton.pack(side='left')
                carrieddataLabel.pack(side='left')
                self.carrieddataEntry.pack(side='left')
                self.carrieddataFrame.pack()

#### villager tags
                self.villagerFrame = Tkinter.Frame(self.hostileotherFrame)
                (Tkinter.Label(self.villagerFrame, text = "Villager data")).pack(pady=3)

                self.professionFrame = Tkinter.Frame(self.villagerFrame)
                self.professionCheckButton = Tkinter.Checkbutton(self.professionFrame, variable=self.professionCheck, onvalue=True, offvalue=False, height=1)
                professionLabel = Tkinter.Label(self.professionFrame, text = "Profession: ", width=15)
                self.professionEntry = Tkinter.Entry(self.professionFrame, textvariable=self.professionVar, width=10)
                self.professionCheckButton.pack(side='left')
                professionLabel.pack(side='left')
                self.professionEntry.pack(side='left')
                self.professionFrame.pack()

                self.richesFrame = Tkinter.Frame(self.villagerFrame)
                self.richesCheckButton = Tkinter.Checkbutton(self.richesFrame, variable=self.richesCheck, onvalue=True, offvalue=False, height=1)
                richesLabel = Tkinter.Label(self.richesFrame, text = "Riches: ", width=15)
                self.richesEntry = Tkinter.Entry(self.richesFrame, textvariable=self.richesVar, width=10)
                self.richesCheckButton.pack(side='left')
                richesLabel.pack(side='left')
                self.richesEntry.pack(side='left')
                self.richesFrame.pack()

#### thrown potion tags
                self.itemsblocksFrame = Tkinter.Frame(self.tabbedWindows)
                
                self.thrownpotionFrame = Tkinter.Frame(self.itemsblocksFrame)
                (Tkinter.Label(self.thrownpotionFrame, text = "Thrown potion data")).pack(pady=3)

                self.thrownpotionvalueFrame = Tkinter.Frame(self.thrownpotionFrame)
                self.thrownpotionvalueCheckButton = Tkinter.Checkbutton(self.thrownpotionvalueFrame, variable=self.thrownpotionvalueCheck, onvalue=True, offvalue=False, height=1)
                thrownpotionvalueLabel = Tkinter.Label(self.thrownpotionvalueFrame, text = "Potion value: ", width=15)
                self.thrownpotionvalueEntry = Tkinter.Entry(self.thrownpotionvalueFrame, textvariable=self.thrownpotionvalueVar, width=10)
                self.thrownpotionvalueCheckButton.pack(side='left')
                thrownpotionvalueLabel.pack(side='left')
                self.thrownpotionvalueEntry.pack(side='left')
                self.thrownpotionvalueFrame.pack()

#### primed tnt tags
                self.primedtntFrame = Tkinter.Frame(self.itemsblocksFrame)
                (Tkinter.Label(self.primedtntFrame, text = "Primed TNT data")).pack(pady=3)

                self.fuseFrame = Tkinter.Frame(self.primedtntFrame)
                self.fuseCheckButton = Tkinter.Checkbutton(self.fuseFrame, variable=self.fuseCheck, onvalue=True, offvalue=False, height=1)
                fuseLabel = Tkinter.Label(self.fuseFrame, text = "Fuse: ", width=15)
                self.fuseEntry = Tkinter.Entry(self.fuseFrame, textvariable=self.fuseVar, width=10)
                self.fuseCheckButton.pack(side='left')
                fuseLabel.pack(side='left')
                self.fuseEntry.pack(side='left')
                self.fuseFrame.pack()

#### falling sand tags
                self.fallingsandFrame = Tkinter.Frame(self.itemsblocksFrame)
                (Tkinter.Label(self.fallingsandFrame, text = "Falling sand data")).pack(pady=3)

                self.dataFrame = Tkinter.Frame(self.fallingsandFrame)
                self.dataCheckButton = Tkinter.Checkbutton(self.dataFrame, variable=self.dataCheck, onvalue=True, offvalue=False, height=1)
                dataLabel = Tkinter.Label(self.dataFrame, text = "Data: ", width=15)
                self.dataEntry = Tkinter.Entry(self.dataFrame, textvariable=self.dataVar, width=10)
                self.dataCheckButton.pack(side='left')
                dataLabel.pack(side='left')
                self.dataEntry.pack(side='left')
                self.dataFrame.pack()

                self.ongroundFrame = Tkinter.Frame(self.fallingsandFrame)
                self.ongroundCheckButton = Tkinter.Checkbutton(self.ongroundFrame, variable=self.ongroundCheck, onvalue=True, offvalue=False, height=1)
                ongroundLabel = Tkinter.Label(self.ongroundFrame, text = "On ground: ", width=15)
                self.ongroundEntry = Tkinter.Entry(self.ongroundFrame, textvariable=self.ongroundVar, width=10)
                self.ongroundCheckButton.pack(side='left')
                ongroundLabel.pack(side='left')
                self.ongroundEntry.pack(side='left')
                self.ongroundFrame.pack()

                self.tileFrame = Tkinter.Frame(self.fallingsandFrame)
                self.tileCheckButton = Tkinter.Checkbutton(self.tileFrame, variable=self.tileCheck, onvalue=True, offvalue=False, height=1)
                tileLabel = Tkinter.Label(self.tileFrame, text = "Tile: ", width=15)
                self.tileEntry = Tkinter.Entry(self.tileFrame, textvariable=self.tileVar, width=10)
                self.tileCheckButton.pack(side='left')
                tileLabel.pack(side='left')
                self.tileEntry.pack(side='left')
                self.tileFrame.pack()

                self.timeFrame = Tkinter.Frame(self.fallingsandFrame)
                self.timeCheckButton = Tkinter.Checkbutton(self.timeFrame, variable=self.timeCheck, onvalue=True, offvalue=False, height=1)
                timeLabel = Tkinter.Label(self.timeFrame, text = "Time: ", width=15)
                self.timeEntry = Tkinter.Entry(self.timeFrame, textvariable=self.timeVar, width=10)
                self.timeCheckButton.pack(side='left')
                timeLabel.pack(side='left')
                self.timeEntry.pack(side='left')
                self.timeFrame.pack()

                self.falldistanceFrame = Tkinter.Frame(self.fallingsandFrame)
                self.falldistanceCheckButton = Tkinter.Checkbutton(self.falldistanceFrame, variable=self.falldistanceCheck, onvalue=True, offvalue=False, height=1)
                falldistanceLabel = Tkinter.Label(self.falldistanceFrame, text = "Fall distance: ", width=15)
                self.falldistanceEntry = Tkinter.Entry(self.falldistanceFrame, textvariable=self.falldistanceVar, width=10)
                self.falldistanceCheckButton.pack(side='left')
                falldistanceLabel.pack(side='left')
                self.falldistanceEntry.pack(side='left')
                self.falldistanceFrame.pack()

                self.dropitemFrame = Tkinter.Frame(self.fallingsandFrame)
                self.dropitemCheckButton = Tkinter.Checkbutton(self.dropitemFrame, variable=self.dropitemCheck, onvalue=True, offvalue=False, height=1)
                dropitemLabel = Tkinter.Label(self.dropitemFrame, text = "Drop Item: ", width=15)
                self.dropitemEntry = Tkinter.Entry(self.dropitemFrame, textvariable=self.dropitemVar, width=10)
                self.dropitemCheckButton.pack(side='left')
                dropitemLabel.pack(side='left')
                self.dropitemEntry.pack(side='left')
                self.dropitemFrame.pack()

                self.HurtEntitiesFrame = Tkinter.Frame(self.fallingsandFrame)
                self.HurtEntitiesCheckButton = Tkinter.Checkbutton(self.HurtEntitiesFrame, variable=self.HurtEntitiesCheck, onvalue=True, offvalue=False, height=1)
                HurtEntitiesLabel = Tkinter.Label(self.HurtEntitiesFrame, text = "Hurt Entities: ", width=15)
                self.HurtEntitiesEntry = Tkinter.Entry(self.HurtEntitiesFrame, textvariable=self.HurtEntitiesVar, width=10)
                self.HurtEntitiesCheckButton.pack(side='left')
                HurtEntitiesLabel.pack(side='left')
                self.HurtEntitiesEntry.pack(side='left')
                self.HurtEntitiesFrame.pack()

                self.FallHurtMaxFrame = Tkinter.Frame(self.fallingsandFrame)
                self.FallHurtMaxCheckButton = Tkinter.Checkbutton(self.FallHurtMaxFrame, variable=self.FallHurtMaxCheck, onvalue=True, offvalue=False, height=1)
                FallHurtMaxLabel = Tkinter.Label(self.FallHurtMaxFrame, text = "Fall Hurt Max: ", width=15)
                self.FallHurtMaxEntry = Tkinter.Entry(self.FallHurtMaxFrame, textvariable=self.FallHurtMaxVar, width=10)
                self.FallHurtMaxCheckButton.pack(side='left')
                FallHurtMaxLabel.pack(side='left')
                self.FallHurtMaxEntry.pack(side='left')
                self.FallHurtMaxFrame.pack()

                self.FallHurtAmountFrame = Tkinter.Frame(self.fallingsandFrame)
                self.FallHurtAmountCheckButton = Tkinter.Checkbutton(self.FallHurtAmountFrame, variable=self.FallHurtAmountCheck, onvalue=True, offvalue=False, height=1)
                FallHurtAmountLabel = Tkinter.Label(self.FallHurtAmountFrame, text = "Fall Hurt Amt: ", width=15)
                self.FallHurtAmountEntry = Tkinter.Entry(self.FallHurtAmountFrame, textvariable=self.FallHurtAmountVar, width=10)
                self.FallHurtAmountCheckButton.pack(side='left')
                FallHurtAmountLabel.pack(side='left')
                self.FallHurtAmountEntry.pack(side='left')
                self.FallHurtAmountFrame.pack()

#### xp orb tags
                self.xporbFrame = Tkinter.Frame(self.itemsblocksFrame)
                (Tkinter.Label(self.xporbFrame, text = "XP orb data")).pack(pady=3)

                self.valueFrame = Tkinter.Frame(self.xporbFrame)
                self.valueCheckButton = Tkinter.Checkbutton(self.valueFrame, variable=self.valueCheck, onvalue=True, offvalue=False, height=1)
                valueLabel = Tkinter.Label(self.valueFrame, text = "Value: ", width=15)
                self.valueEntry = Tkinter.Entry(self.valueFrame, textvariable=self.valueVar, width=10)
                self.valueCheckButton.pack(side='left')
                valueLabel.pack(side='left')
                self.valueEntry.pack(side='left')
                self.valueFrame.pack()

#### item tags
                self.itemFrame = Tkinter.Frame(self.itemsblocksFrame)
                (Tkinter.Label(self.itemFrame, text = "Item data")).pack(pady=3)

                self.itemageFrame = Tkinter.Frame(self.itemFrame)
                self.itemageCheckButton = Tkinter.Checkbutton(self.itemageFrame, variable=self.itemageCheck, onvalue=True, offvalue=False, height=1)
                itemageLabel = Tkinter.Label(self.itemageFrame, text = "Age: ", width=15)
                self.itemageEntry = Tkinter.Entry(self.itemageFrame, textvariable=self.itemageVar, width=10)
                self.itemageCheckButton.pack(side='left')
                itemageLabel.pack(side='left')
                self.itemageEntry.pack(side='left')
                self.itemageFrame.pack()                  

                self.idFrame = Tkinter.Frame(self.itemFrame)
                self.idCheckButton = Tkinter.Checkbutton(self.idFrame, variable=self.idCheck, onvalue=True, offvalue=False, height=1)
                idLabel = Tkinter.Label(self.idFrame, text = "id: ", width=15)
                self.idEntry = Tkinter.Entry(self.idFrame, textvariable=self.idVar, width=10)
                self.idCheckButton.pack(side='left')
                idLabel.pack(side='left')
                self.idEntry.pack(side='left')
                self.idFrame.pack()

                self.damageitemFrame = Tkinter.Frame(self.itemFrame)
                self.damageitemCheckButton = Tkinter.Checkbutton(self.damageitemFrame, variable=self.damageitemCheck, onvalue=True, offvalue=False, height=1)
                damageitemLabel = Tkinter.Label(self.damageitemFrame, text = "Damage value: ", width=15)
                self.damageitemEntry = Tkinter.Entry(self.damageitemFrame, textvariable=self.damageitemVar, width=10)
                self.damageitemCheckButton.pack(side='left')
                damageitemLabel.pack(side='left')
                self.damageitemEntry.pack(side='left')
                self.damageitemFrame.pack()

                self.countFrame = Tkinter.Frame(self.itemFrame)
                self.countCheckButton = Tkinter.Checkbutton(self.countFrame, variable=self.countCheck, onvalue=True, offvalue=False, height=1)
                countLabel = Tkinter.Label(self.countFrame, text = "Count: ", width=15)
                self.countEntry = Tkinter.Entry(self.countFrame, textvariable=self.countVar, width=10)
                self.countCheckButton.pack(side='left')
                countLabel.pack(side='left')
                self.countEntry.pack(side='left')
                self.countFrame.pack()

                self.enchantsFrame = Tkinter.Frame(self.itemFrame)
                self.enchantsCheckButton = Tkinter.Checkbutton(self.enchantsFrame, variable=self.enchantsCheck, onvalue=True, offvalue=False, height=1)
                enchantsLabel = Tkinter.Label(self.enchantsFrame, text = "Enchants: ", width=15)
                self.enchantsEntry = Tkinter.Entry(self.enchantsFrame, textvariable=self.enchantsVar, width=10)
                self.enchantsCheckButton.pack(side='left')
                enchantsLabel.pack(side='left')
                self.enchantsEntry.pack(side='left')
                self.enchantsFrame.pack()

                self.itemskullownerFrame = Tkinter.Frame(self.itemFrame)
                self.itemskullownerCheckButton = Tkinter.Checkbutton(self.itemskullownerFrame, variable=self.itemskullownerCheck, onvalue=True, offvalue=False, height=1)
                itemskullownerLabel = Tkinter.Label(self.itemskullownerFrame, text = "Skull Owner: ", width=15)
                self.itemskullownerEntry = Tkinter.Entry(self.itemskullownerFrame, textvariable=self.itemskullownerVar, width=10)
                self.itemskullownerCheckButton.pack(side='left')
                itemskullownerLabel.pack(side='left')
                self.itemskullownerEntry.pack(side='left')
                self.itemskullownerFrame.pack()

                self.itemcolorFrame = Tkinter.Frame(self.itemFrame)
                self.itemcolorCheckButton = Tkinter.Checkbutton(self.itemcolorFrame, variable=self.itemcolorCheck, onvalue=True, offvalue=False, height=1)
                itemcolorLabel = Tkinter.Label(self.itemcolorFrame, text = "Color: ", width=15)
                self.itemcolorEntry = Tkinter.Entry(self.itemcolorFrame, textvariable=self.itemcolorVar, width=10)
                self.itemcolorCheckButton.pack(side='left')
                itemcolorLabel.pack(side='left')
                self.itemcolorEntry.pack(side='left')
                self.itemcolorFrame.pack()

                self.itemnameFrame = Tkinter.Frame(self.itemFrame)
                self.itemnameCheckButton = Tkinter.Checkbutton(self.itemnameFrame, variable=self.itemnameCheck, onvalue=True, offvalue=False, height=1)
                itemnameLabel = Tkinter.Label(self.itemnameFrame, text = "Name: ", width=15)
                self.itemnameEntry = Tkinter.Entry(self.itemnameFrame, textvariable=self.itemnameVar, width=10)
                self.itemnameCheckButton.pack(side='left')
                itemnameLabel.pack(side='left')
                self.itemnameEntry.pack(side='left')
                self.itemnameFrame.pack()

                self.itemloreFrame = Tkinter.Frame(self.itemFrame)
                self.itemloreCheckButton = Tkinter.Checkbutton(self.itemloreFrame, variable=self.itemloreCheck, onvalue=True, offvalue=False, height=1)
                itemloreLabel = Tkinter.Label(self.itemloreFrame, text = "Lore: ", width=15)
                self.itemloreEntry = Tkinter.Entry(self.itemloreFrame, textvariable=self.itemloreVar, width=50)
                self.itemloreCheckButton.pack(side='left')
                itemloreLabel.pack(side='left')
                self.itemloreEntry.pack(side='left')
                self.itemloreFrame.pack()

#### generic projectile tags
                self.projectileFrame = Tkinter.Frame(self.tabbedWindows)
                self.allprojectilesFrame = Tkinter.Frame(self.projectileFrame)
                (Tkinter.Label(self.allprojectilesFrame, text = "Projectile data")).pack(pady=3)

                self.xtileFrame = Tkinter.Frame(self.allprojectilesFrame)
                self.xtileCheckButton = Tkinter.Checkbutton(self.xtileFrame, variable=self.xtileCheck, onvalue=True, offvalue=False, height=1)
                xtileLabel = Tkinter.Label(self.xtileFrame, text = "X tile: ", width=15)
                self.xtileEntry = Tkinter.Entry(self.xtileFrame, textvariable=self.xtileVar, width=10)
                self.xtileCheckButton.pack(side='left')
                xtileLabel.pack(side='left')
                self.xtileEntry.pack(side='left')
                self.xtileFrame.pack()

                self.ytileFrame = Tkinter.Frame(self.allprojectilesFrame)
                self.ytileCheckButton = Tkinter.Checkbutton(self.ytileFrame, variable=self.ytileCheck, onvalue=True, offvalue=False, height=1)
                ytileLabel = Tkinter.Label(self.ytileFrame, text = "Y tile: ", width=15)
                self.ytileEntry = Tkinter.Entry(self.ytileFrame, textvariable=self.ytileVar, width=10)
                self.ytileCheckButton.pack(side='left')
                ytileLabel.pack(side='left')
                self.ytileEntry.pack(side='left')
                self.ytileFrame.pack()

                self.ztileFrame = Tkinter.Frame(self.allprojectilesFrame)
                self.ztileCheckButton = Tkinter.Checkbutton(self.ztileFrame, variable=self.ztileCheck, onvalue=True, offvalue=False, height=1)
                ztileLabel = Tkinter.Label(self.ztileFrame, text = "Z tile: ", width=15)
                self.ztileEntry = Tkinter.Entry(self.ztileFrame, textvariable=self.ztileVar, width=10)
                self.ztileCheckButton.pack(side='left')
                ztileLabel.pack(side='left')
                self.ztileEntry.pack(side='left')
                self.ztileFrame.pack()

                self.intileFrame = Tkinter.Frame(self.allprojectilesFrame)
                self.intileCheckButton = Tkinter.Checkbutton(self.intileFrame, variable=self.intileCheck, onvalue=True, offvalue=False, height=1)
                intileLabel = Tkinter.Label(self.intileFrame, text = "In tile: ", width=15)
                self.intileEntry = Tkinter.Entry(self.intileFrame, textvariable=self.intileVar, width=10)
                self.intileCheckButton.pack(side='left')
                intileLabel.pack(side='left')
                self.intileEntry.pack(side='left')
                self.intileFrame.pack()

                self.shakeFrame = Tkinter.Frame(self.allprojectilesFrame)
                self.shakeCheckButton = Tkinter.Checkbutton(self.shakeFrame, variable=self.shakeCheck, onvalue=True, offvalue=False, height=1)
                shakeLabel = Tkinter.Label(self.shakeFrame, text = "Shake: ", width=15)
                self.shakeEntry = Tkinter.Entry(self.shakeFrame, textvariable=self.shakeVar, width=10)
                self.shakeCheckButton.pack(side='left')
                shakeLabel.pack(side='left')
                self.shakeEntry.pack(side='left')
                self.shakeFrame.pack()

                self.ingroundFrame = Tkinter.Frame(self.allprojectilesFrame)
                self.ingroundCheckButton = Tkinter.Checkbutton(self.ingroundFrame, variable=self.ingroundCheck, onvalue=True, offvalue=False, height=1)
                ingroundLabel = Tkinter.Label(self.ingroundFrame, text = "In ground: ", width=15)
                self.ingroundEntry = Tkinter.Entry(self.ingroundFrame, textvariable=self.ingroundVar, width=10)
                self.ingroundCheckButton.pack(side='left')
                ingroundLabel.pack(side='left')
                self.ingroundEntry.pack(side='left')
                self.ingroundFrame.pack()

#### arrow tags
                self.arrowFrame = Tkinter.Frame(self.projectileFrame)
                (Tkinter.Label(self.allprojectilesFrame, text = "Arrow data")).pack(pady=3)

                self.indataFrame = Tkinter.Frame(self.arrowFrame)
                self.indataCheckButton = Tkinter.Checkbutton(self.indataFrame, variable=self.indataCheck, onvalue=True, offvalue=False, height=1)
                indataLabel = Tkinter.Label(self.indataFrame, text = "In data: ", width=15)
                self.indataEntry = Tkinter.Entry(self.indataFrame, textvariable=self.indataVar, width=10)
                self.indataCheckButton.pack(side='left')
                indataLabel.pack(side='left')
                self.indataEntry.pack(side='left')
                self.indataFrame.pack()

                self.pickupFrame = Tkinter.Frame(self.arrowFrame)
                self.pickupCheckButton = Tkinter.Checkbutton(self.pickupFrame, variable=self.pickupCheck, onvalue=True, offvalue=False, height=1)
                pickupLabel = Tkinter.Label(self.pickupFrame, text = "Pickup: ", width=15)
                self.pickupEntry = Tkinter.Entry(self.pickupFrame, textvariable=self.pickupVar, width=10)
                self.pickupCheckButton.pack(side='left')
                pickupLabel.pack(side='left')
                self.pickupEntry.pack(side='left')
                self.pickupFrame.pack()

                self.damageFrame = Tkinter.Frame(self.arrowFrame)
                self.damageCheckButton = Tkinter.Checkbutton(self.damageFrame, variable=self.damageCheck, onvalue=True, offvalue=False, height=1)
                damageLabel = Tkinter.Label(self.damageFrame, text = "Damage: ", width=15)
                self.damageEntry = Tkinter.Entry(self.damageFrame, textvariable=self.damageVar, width=10)
                self.damageCheckButton.pack(side='left')
                damageLabel.pack(side='left')
                self.damageEntry.pack(side='left')
                self.damageFrame.pack()

#### mob equipment tags
                self.mobequipFrame = Tkinter.Frame(self.tabbedWindows)

                (Tkinter.Label(self.mobequipFrame, text = "Mob equipment data")).pack(pady=3)

                self.mobweapon1Frame = Tkinter.Frame(self.mobequipFrame)
                self.mobweapondisplayFrame = Tkinter.Frame(self.mobweapon1Frame)

                self.mobweaponFrame = Tkinter.Frame(self.mobweapon1Frame)
                self.mobweaponCheckButton = Tkinter.Checkbutton(self.mobweaponFrame, variable=self.mobweaponCheck, onvalue=True, offvalue=False, height=1)
                self.mobweaponCheckButton.pack(side='left')

                self.mobweaponidFrame = Tkinter.Frame(self.mobweaponFrame)
                mobweaponidLabel = Tkinter.Label(self.mobweaponidFrame, text = "Weapon ID: ", width=20)
                self.mobweaponidEntry = Tkinter.Entry(self.mobweaponidFrame, textvariable=self.mobweaponidVar, width=10)
                mobweaponidLabel.pack(side='left')
                self.mobweaponidEntry.pack(side='left')
                self.mobweaponidFrame.pack()

                self.mobweapondamageFrame = Tkinter.Frame(self.mobweaponFrame)
                mobweapondamageLabel = Tkinter.Label(self.mobweapondamageFrame, text = "Weapon damage value: ", width=20)
                self.mobweapondamageEntry = Tkinter.Entry(self.mobweapondamageFrame, textvariable=self.mobweapondamageVar, width=10)
                mobweapondamageLabel.pack(side='left')
                self.mobweapondamageEntry.pack(side='left')
                self.mobweapondamageFrame.pack()

                self.mobweaponcountFrame = Tkinter.Frame(self.mobweaponFrame)
                mobweaponcountLabel = Tkinter.Label(self.mobweaponcountFrame, text = "Weapon count: ", width=20)
                self.mobweaponcountEntry = Tkinter.Entry(self.mobweaponcountFrame, textvariable=self.mobweaponcountVar, width=10)
                mobweaponcountLabel.pack(side='left')
                self.mobweaponcountEntry.pack(side='left')
                self.mobweaponcountFrame.pack()

                self.mobweaponenchantsFrame = Tkinter.Frame(self.mobweaponFrame)
                mobweaponenchantsLabel = Tkinter.Label(self.mobweaponenchantsFrame, text = "Weapon enchants: ", width=20)
                self.mobweaponenchantsEntry = Tkinter.Entry(self.mobweaponenchantsFrame, textvariable=self.mobweaponenchantsVar, width=10)
                mobweaponenchantsLabel.pack(side='left')
                self.mobweaponenchantsEntry.pack(side='left')
                self.mobweaponenchantsFrame.pack()

                self.mobweaponchanceFrame = Tkinter.Frame(self.mobweaponFrame)
                mobweaponchanceLabel = Tkinter.Label(self.mobweaponchanceFrame, text = "Weapon drop chance: ", width=20)
                self.mobweaponchanceEntry = Tkinter.Entry(self.mobweaponchanceFrame, textvariable=self.mobweaponchanceVar, width=10)
                mobweaponchanceLabel.pack(side='left')
                self.mobweaponchanceEntry.pack(side='left')
                self.mobweaponchanceFrame.pack()

                self.mobweaponnameFrame = Tkinter.Frame(self.mobweapondisplayFrame)
                mobweaponnameLabel = Tkinter.Label(self.mobweaponnameFrame, text = "Weapon name: ", width=20)
                self.mobweaponnameEntry = Tkinter.Entry(self.mobweaponnameFrame, textvariable=self.mobweaponnameVar, width=10)
                mobweaponnameLabel.pack(side='left')
                self.mobweaponnameEntry.pack(side='left')
                self.mobweaponnameFrame.pack()

                self.mobweaponloreFrame = Tkinter.Frame(self.mobweapondisplayFrame)
                mobweaponloreLabel = Tkinter.Label(self.mobweaponloreFrame, text = "Weapon lore: ", width=20)
                self.mobweaponloreEntry = Tkinter.Entry(self.mobweaponloreFrame, textvariable=self.mobweaponloreVar, width=50)
                mobweaponloreLabel.pack(side='left')
                self.mobweaponloreEntry.pack(side='left')
                self.mobweaponloreFrame.pack()

                self.mobweaponcolorFrame = Tkinter.Frame(self.mobweapondisplayFrame)
                mobweaponcolorLabel = Tkinter.Label(self.mobweaponcolorFrame, text = "Weapon color: ", width=20)
                self.mobweaponcolorEntry = Tkinter.Entry(self.mobweaponcolorFrame, textvariable=self.mobweaponcolorVar, width=10)
                mobweaponcolorLabel.pack(side='left')
                self.mobweaponcolorEntry.pack(side='left')
                self.mobweaponcolorFrame.pack()

                self.mobhelmet1Frame = Tkinter.Frame(self.mobequipFrame)
                self.mobhelmetdisplayFrame = Tkinter.Frame(self.mobhelmet1Frame)

                self.mobhelmetFrame = Tkinter.Frame(self.mobhelmet1Frame)
                self.mobhelmetCheckButton = Tkinter.Checkbutton(self.mobhelmetFrame, variable=self.mobhelmetCheck, onvalue=True, offvalue=False, height=1)
                self.mobhelmetCheckButton.pack(side='left')

                self.mobhelmetidFrame = Tkinter.Frame(self.mobhelmetFrame)
                mobhelmetidLabel = Tkinter.Label(self.mobhelmetidFrame, text = "Helmet ID: ", width=20)
                self.mobhelmetidEntry = Tkinter.Entry(self.mobhelmetidFrame, textvariable=self.mobhelmetidVar, width=10)
                mobhelmetidLabel.pack(side='left')
                self.mobhelmetidEntry.pack(side='left')
                self.mobhelmetidFrame.pack()

                self.mobhelmetdamageFrame = Tkinter.Frame(self.mobhelmetFrame)
                mobhelmetdamageLabel = Tkinter.Label(self.mobhelmetdamageFrame, text = "Helmet damage value: ", width=20)
                self.mobhelmetdamageEntry = Tkinter.Entry(self.mobhelmetdamageFrame, textvariable=self.mobhelmetdamageVar, width=10)
                mobhelmetdamageLabel.pack(side='left')
                self.mobhelmetdamageEntry.pack(side='left')
                self.mobhelmetdamageFrame.pack()

                self.mobhelmetcountFrame = Tkinter.Frame(self.mobhelmetFrame)
                mobhelmetcountLabel = Tkinter.Label(self.mobhelmetcountFrame, text = "Helmet count: ", width=20)
                self.mobhelmetcountEntry = Tkinter.Entry(self.mobhelmetcountFrame, textvariable=self.mobhelmetcountVar, width=10)
                mobhelmetcountLabel.pack(side='left')
                self.mobhelmetcountEntry.pack(side='left')
                self.mobhelmetcountFrame.pack()

                self.mobhelmetenchantsFrame = Tkinter.Frame(self.mobhelmetFrame)
                mobhelmetenchantsLabel = Tkinter.Label(self.mobhelmetenchantsFrame, text = "Helmet enchants: ", width=20)
                self.mobhelmetenchantsEntry = Tkinter.Entry(self.mobhelmetenchantsFrame, textvariable=self.mobhelmetenchantsVar, width=10)
                mobhelmetenchantsLabel.pack(side='left')
                self.mobhelmetenchantsEntry.pack(side='left')
                self.mobhelmetenchantsFrame.pack()

                self.mobhelmetchanceFrame = Tkinter.Frame(self.mobhelmetFrame)
                mobhelmetchanceLabel = Tkinter.Label(self.mobhelmetchanceFrame, text = "Helmet drop chance: ", width=20)
                self.mobhelmetchanceEntry = Tkinter.Entry(self.mobhelmetchanceFrame, textvariable=self.mobhelmetchanceVar, width=10)
                mobhelmetchanceLabel.pack(side='left')
                self.mobhelmetchanceEntry.pack(side='left')
                self.mobhelmetchanceFrame.pack()

                self.mobhelmetskullownerFrame = Tkinter.Frame(self.mobhelmetFrame)
                mobhelmetskullownerLabel = Tkinter.Label(self.mobhelmetskullownerFrame, text = "Helmet skull owner: ", width=20)
                self.mobhelmetskullownerEntry = Tkinter.Entry(self.mobhelmetskullownerFrame, textvariable=self.mobhelmetskullownerVar, width=10)
                mobhelmetskullownerLabel.pack(side='left')
                self.mobhelmetskullownerEntry.pack(side='left')
                self.mobhelmetskullownerFrame.pack()

                self.mobhelmetnameFrame = Tkinter.Frame(self.mobhelmetdisplayFrame)
                mobhelmetnameLabel = Tkinter.Label(self.mobhelmetnameFrame, text = "Helmet name: ", width=20)
                self.mobhelmetnameEntry = Tkinter.Entry(self.mobhelmetnameFrame, textvariable=self.mobhelmetnameVar, width=10)
                mobhelmetnameLabel.pack(side='left')
                self.mobhelmetnameEntry.pack(side='left')
                self.mobhelmetnameFrame.pack()

                self.mobhelmetloreFrame = Tkinter.Frame(self.mobhelmetdisplayFrame)
                mobhelmetloreLabel = Tkinter.Label(self.mobhelmetloreFrame, text = "Helmet lore: ", width=20)
                self.mobhelmetloreEntry = Tkinter.Entry(self.mobhelmetloreFrame, textvariable=self.mobhelmetloreVar, width=50)
                mobhelmetloreLabel.pack(side='left')
                self.mobhelmetloreEntry.pack(side='left')
                self.mobhelmetloreFrame.pack()

                self.mobhelmetcolorFrame = Tkinter.Frame(self.mobhelmetdisplayFrame)
                mobhelmetcolorLabel = Tkinter.Label(self.mobhelmetcolorFrame, text = "Helmet color: ", width=20)
                self.mobhelmetcolorEntry = Tkinter.Entry(self.mobhelmetcolorFrame, textvariable=self.mobhelmetcolorVar, width=10)
                mobhelmetcolorLabel.pack(side='left')
                self.mobhelmetcolorEntry.pack(side='left')
                self.mobhelmetcolorFrame.pack()

                self.mobchest1Frame = Tkinter.Frame(self.mobequipFrame)
                self.mobchestdisplayFrame = Tkinter.Frame(self.mobchest1Frame)

                self.mobchestFrame = Tkinter.Frame(self.mobchest1Frame)
                self.mobchestCheckButton = Tkinter.Checkbutton(self.mobchestFrame, variable=self.mobchestCheck, onvalue=True, offvalue=False, height=1)
                self.mobchestCheckButton.pack(side='left')

                self.mobchestidFrame = Tkinter.Frame(self.mobchestFrame)
                mobchestidLabel = Tkinter.Label(self.mobchestidFrame, text = "Chest ID: ", width=20)
                self.mobchestidEntry = Tkinter.Entry(self.mobchestidFrame, textvariable=self.mobchestidVar, width=10)
                mobchestidLabel.pack(side='left')
                self.mobchestidEntry.pack(side='left')
                self.mobchestidFrame.pack()

                self.mobchestdamageFrame = Tkinter.Frame(self.mobchestFrame)
                mobchestdamageLabel = Tkinter.Label(self.mobchestdamageFrame, text = "Chest damage value: ", width=20)
                self.mobchestdamageEntry = Tkinter.Entry(self.mobchestdamageFrame, textvariable=self.mobchestdamageVar, width=10)
                mobchestdamageLabel.pack(side='left')
                self.mobchestdamageEntry.pack(side='left')
                self.mobchestdamageFrame.pack()

                self.mobchestcountFrame = Tkinter.Frame(self.mobchestFrame)
                mobchestcountLabel = Tkinter.Label(self.mobchestcountFrame, text = "Chest count: ", width=20)
                self.mobchestcountEntry = Tkinter.Entry(self.mobchestcountFrame, textvariable=self.mobchestcountVar, width=10)
                mobchestcountLabel.pack(side='left')
                self.mobchestcountEntry.pack(side='left')
                self.mobchestcountFrame.pack()

                self.mobchestenchantsFrame = Tkinter.Frame(self.mobchestFrame)
                mobchestenchantsLabel = Tkinter.Label(self.mobchestenchantsFrame, text = "Chest enchants: ", width=20)
                self.mobchestenchantsEntry = Tkinter.Entry(self.mobchestenchantsFrame, textvariable=self.mobchestenchantsVar, width=10)
                mobchestenchantsLabel.pack(side='left')
                self.mobchestenchantsEntry.pack(side='left')
                self.mobchestenchantsFrame.pack()

                self.mobchestchanceFrame = Tkinter.Frame(self.mobchestFrame)
                mobchestchanceLabel = Tkinter.Label(self.mobchestchanceFrame, text = "Chest drop chance: ", width=20)
                self.mobchestchanceEntry = Tkinter.Entry(self.mobchestchanceFrame, textvariable=self.mobchestchanceVar, width=10)
                mobchestchanceLabel.pack(side='left')
                self.mobchestchanceEntry.pack(side='left')
                self.mobchestchanceFrame.pack()

                self.mobchestnameFrame = Tkinter.Frame(self.mobchestdisplayFrame)
                mobchestnameLabel = Tkinter.Label(self.mobchestnameFrame, text = "Chest name: ", width=20)
                self.mobchestnameEntry = Tkinter.Entry(self.mobchestnameFrame, textvariable=self.mobchestnameVar, width=10)
                mobchestnameLabel.pack(side='left')
                self.mobchestnameEntry.pack(side='left')
                self.mobchestnameFrame.pack()

                self.mobchestloreFrame = Tkinter.Frame(self.mobchestdisplayFrame)
                mobchestloreLabel = Tkinter.Label(self.mobchestloreFrame, text = "Chest lore: ", width=20)
                self.mobchestloreEntry = Tkinter.Entry(self.mobchestloreFrame, textvariable=self.mobchestloreVar, width=50)
                mobchestloreLabel.pack(side='left')
                self.mobchestloreEntry.pack(side='left')
                self.mobchestloreFrame.pack()

                self.mobchestcolorFrame = Tkinter.Frame(self.mobchestdisplayFrame)
                mobchestcolorLabel = Tkinter.Label(self.mobchestcolorFrame, text = "Chest color: ", width=20)
                self.mobchestcolorEntry = Tkinter.Entry(self.mobchestcolorFrame, textvariable=self.mobchestcolorVar, width=10)
                mobchestcolorLabel.pack(side='left')
                self.mobchestcolorEntry.pack(side='left')
                self.mobchestcolorFrame.pack()

                self.moblegs1Frame = Tkinter.Frame(self.mobequipFrame)
                self.moblegsdisplayFrame = Tkinter.Frame(self.moblegs1Frame)

                self.moblegsFrame = Tkinter.Frame(self.moblegs1Frame)
                self.moblegsCheckButton = Tkinter.Checkbutton(self.moblegsFrame, variable=self.moblegsCheck, onvalue=True, offvalue=False, height=1)
                self.moblegsCheckButton.pack(side='left')

                self.moblegsidFrame = Tkinter.Frame(self.moblegsFrame)
                moblegsidLabel = Tkinter.Label(self.moblegsidFrame, text = "Legs ID: ", width=20)
                self.moblegsidEntry = Tkinter.Entry(self.moblegsidFrame, textvariable=self.moblegsidVar, width=10)
                moblegsidLabel.pack(side='left')
                self.moblegsidEntry.pack(side='left')
                self.moblegsidFrame.pack()

                self.moblegsdamageFrame = Tkinter.Frame(self.moblegsFrame)
                moblegsdamageLabel = Tkinter.Label(self.moblegsdamageFrame, text = "Legs damage value: ", width=20)
                self.moblegsdamageEntry = Tkinter.Entry(self.moblegsdamageFrame, textvariable=self.moblegsdamageVar, width=10)
                moblegsdamageLabel.pack(side='left')
                self.moblegsdamageEntry.pack(side='left')
                self.moblegsdamageFrame.pack()

                self.moblegscountFrame = Tkinter.Frame(self.moblegsFrame)
                moblegscountLabel = Tkinter.Label(self.moblegscountFrame, text = "Legs count: ", width=20)
                self.moblegscountEntry = Tkinter.Entry(self.moblegscountFrame, textvariable=self.moblegscountVar, width=10)
                moblegscountLabel.pack(side='left')
                self.moblegscountEntry.pack(side='left')
                self.moblegscountFrame.pack()

                self.moblegsenchantsFrame = Tkinter.Frame(self.moblegsFrame)
                moblegsenchantsLabel = Tkinter.Label(self.moblegsenchantsFrame, text = "Legs enchants: ", width=20)
                self.moblegsenchantsEntry = Tkinter.Entry(self.moblegsenchantsFrame, textvariable=self.moblegsenchantsVar, width=10)
                moblegsenchantsLabel.pack(side='left')
                self.moblegsenchantsEntry.pack(side='left')
                self.moblegsenchantsFrame.pack()

                self.moblegschanceFrame = Tkinter.Frame(self.moblegsFrame)
                moblegschanceLabel = Tkinter.Label(self.moblegschanceFrame, text = "Legs drop chance: ", width=20)
                self.moblegschanceEntry = Tkinter.Entry(self.moblegschanceFrame, textvariable=self.moblegschanceVar, width=10)
                moblegschanceLabel.pack(side='left')
                self.moblegschanceEntry.pack(side='left')
                self.moblegschanceFrame.pack()

                self.moblegsnameFrame = Tkinter.Frame(self.moblegsdisplayFrame)
                moblegsnameLabel = Tkinter.Label(self.moblegsnameFrame, text = "Legs name: ", width=20)
                self.moblegsnameEntry = Tkinter.Entry(self.moblegsnameFrame, textvariable=self.moblegsnameVar, width=10)
                moblegsnameLabel.pack(side='left')
                self.moblegsnameEntry.pack(side='left')
                self.moblegsnameFrame.pack()

                self.moblegsloreFrame = Tkinter.Frame(self.moblegsdisplayFrame)
                moblegsloreLabel = Tkinter.Label(self.moblegsloreFrame, text = "Legs lore: ", width=20)
                self.moblegsloreEntry = Tkinter.Entry(self.moblegsloreFrame, textvariable=self.moblegsloreVar, width=50)
                moblegsloreLabel.pack(side='left')
                self.moblegsloreEntry.pack(side='left')
                self.moblegsloreFrame.pack()

                self.moblegscolorFrame = Tkinter.Frame(self.moblegsdisplayFrame)
                moblegscolorLabel = Tkinter.Label(self.moblegscolorFrame, text = "Legs color: ", width=20)
                self.moblegscolorEntry = Tkinter.Entry(self.moblegscolorFrame, textvariable=self.moblegscolorVar, width=10)
                moblegscolorLabel.pack(side='left')
                self.moblegscolorEntry.pack(side='left')
                self.moblegscolorFrame.pack()

                self.mobboots1Frame = Tkinter.Frame(self.mobequipFrame)
                self.mobbootsdisplayFrame = Tkinter.Frame(self.mobboots1Frame)

                self.mobbootsFrame = Tkinter.Frame(self.mobboots1Frame)
                self.mobbootsCheckButton = Tkinter.Checkbutton(self.mobbootsFrame, variable=self.mobbootsCheck, onvalue=True, offvalue=False, height=1)
                self.mobbootsCheckButton.pack(side='left')

                self.mobbootsidFrame = Tkinter.Frame(self.mobbootsFrame)
                mobbootsidLabel = Tkinter.Label(self.mobbootsidFrame, text = "Boots ID: ", width=20)
                self.mobbootsidEntry = Tkinter.Entry(self.mobbootsidFrame, textvariable=self.mobbootsidVar, width=10)
                mobbootsidLabel.pack(side='left')
                self.mobbootsidEntry.pack(side='left')
                self.mobbootsidFrame.pack()

                self.mobbootsdamageFrame = Tkinter.Frame(self.mobbootsFrame)
                mobbootsdamageLabel = Tkinter.Label(self.mobbootsdamageFrame, text = "Boots damage value: ", width=20)
                self.mobbootsdamageEntry = Tkinter.Entry(self.mobbootsdamageFrame, textvariable=self.mobbootsdamageVar, width=10)
                mobbootsdamageLabel.pack(side='left')
                self.mobbootsdamageEntry.pack(side='left')
                self.mobbootsdamageFrame.pack()

                self.mobbootscountFrame = Tkinter.Frame(self.mobbootsFrame)
                mobbootscountLabel = Tkinter.Label(self.mobbootscountFrame, text = "Boots count: ", width=20)
                self.mobbootscountEntry = Tkinter.Entry(self.mobbootscountFrame, textvariable=self.mobbootscountVar, width=10)
                mobbootscountLabel.pack(side='left')
                self.mobbootscountEntry.pack(side='left')
                self.mobbootscountFrame.pack()

                self.mobbootsenchantsFrame = Tkinter.Frame(self.mobbootsFrame)
                mobbootsenchantsLabel = Tkinter.Label(self.mobbootsenchantsFrame, text = "Boots enchants: ", width=20)
                self.mobbootsenchantsEntry = Tkinter.Entry(self.mobbootsenchantsFrame, textvariable=self.mobbootsenchantsVar, width=10)
                mobbootsenchantsLabel.pack(side='left')
                self.mobbootsenchantsEntry.pack(side='left')
                self.mobbootsenchantsFrame.pack()

                self.mobbootschanceFrame = Tkinter.Frame(self.mobbootsFrame)
                mobbootschanceLabel = Tkinter.Label(self.mobbootschanceFrame, text = "Boots drop chance: ", width=20)
                self.mobbootschanceEntry = Tkinter.Entry(self.mobbootschanceFrame, textvariable=self.mobbootschanceVar, width=10)
                mobbootschanceLabel.pack(side='left')
                self.mobbootschanceEntry.pack(side='left')
                self.mobbootschanceFrame.pack()

                self.mobbootsnameFrame = Tkinter.Frame(self.mobbootsdisplayFrame)
                mobbootsnameLabel = Tkinter.Label(self.mobbootsnameFrame, text = "Boots name: ", width=20)
                self.mobbootsnameEntry = Tkinter.Entry(self.mobbootsnameFrame, textvariable=self.mobbootsnameVar, width=10)
                mobbootsnameLabel.pack(side='left')
                self.mobbootsnameEntry.pack(side='left')
                self.mobbootsnameFrame.pack()

                self.mobbootsloreFrame = Tkinter.Frame(self.mobbootsdisplayFrame)
                mobbootsloreLabel = Tkinter.Label(self.mobbootsloreFrame, text = "Boots lore: ", width=20)
                self.mobbootsloreEntry = Tkinter.Entry(self.mobbootsloreFrame, textvariable=self.mobbootsloreVar, width=50)
                mobbootsloreLabel.pack(side='left')
                self.mobbootsloreEntry.pack(side='left')
                self.mobbootsloreFrame.pack()

                self.mobbootscolorFrame = Tkinter.Frame(self.mobbootsdisplayFrame)
                mobbootscolorLabel = Tkinter.Label(self.mobbootscolorFrame, text = "Boots color: ", width=20)
                self.mobbootscolorEntry = Tkinter.Entry(self.mobbootscolorFrame, textvariable=self.mobbootscolorVar, width=10)
                mobbootscolorLabel.pack(side='left')
                self.mobbootscolorEntry.pack(side='left')
                self.mobbootscolorFrame.pack()

                self.mobweaponFrame.pack(side='left')
                self.mobhelmetFrame.pack(side='left')
                self.mobchestFrame.pack(side='left')
                self.moblegsFrame.pack(side='left')
                self.mobbootsFrame.pack(side='left')
                self.mobweapondisplayFrame.pack(side='left')
                self.mobhelmetdisplayFrame.pack(side='left')
                self.mobchestdisplayFrame.pack(side='left')
                self.moblegsdisplayFrame.pack(side='left')
                self.mobbootsdisplayFrame.pack(side='left')
                self.mobweapon1Frame.pack(pady=5)
                self.mobhelmet1Frame.pack(pady=5)
                self.mobchest1Frame.pack(pady=5)
                self.moblegs1Frame.pack(pady=5)
                self.mobboots1Frame.pack(pady=5)

####
                self.spawnerFrame.pack()
                self.baseFrame.pack()
                self.positionFrame.pack()
                self.motionFrame.pack(pady=10)
                self.directionFrame.pack(pady=10)

                self.skeletonFrame.pack()
                self.zombieFrame.pack()
                self.creeperFrame.pack()
                self.endermanFrame.pack()
                self.pigmanFrame.pack()
                self.slimeFrame.pack()
                self.witherbossFrame.pack()
                self.batFrame.pack()
                self.villagerFrame.pack()

                self.golemFrame.pack()
                self.breedFrame.pack()
                self.pigFrame.pack()
                self.sheepFrame.pack()
                self.wolfcatFrame.pack()
                self.wolfFrame.pack()
                self.catFrame.pack()

                self.hostileotherFrame.pack(side='left')
                self.breedableFrame.pack(side='left', padx=25)

                self.thrownpotionFrame.pack()
                self.primedtntFrame.pack()
                self.fallingsandFrame.pack()
                self.xporbFrame.pack()
                self.itemFrame.pack()

                self.allprojectilesFrame.pack()
                self.arrowFrame.pack()

                self.custompotioneffectFrame.pack()
                                
                self.tabbedWindows.add(self.spawnerandbaseFrame, text = "Base tags")
                self.windowCount += 1
                self.tabbedWindows.add(self.positionmotionFrame, text = "Position/Motion")
                self.windowCount += 1
                self.tabbedWindows.add(self.mobspecificFrame, text = "Mob Specific tags")
                self.windowCount += 1
                self.tabbedWindows.add(self.projectileFrame, text = "Projectiles")
                self.windowCount += 1
                self.tabbedWindows.add(self.potionsFrame, text = "Mob Potion Effects")
                self.windowCount += 1
                self.tabbedWindows.add(self.mobequipFrame, text = "Mob Equipment")
                self.windowCount += 1
                self.tabbedWindows.add(self.itemsblocksFrame, text = "Items/Blocks/misc")
                self.windowCount += 1
                self.tabbedWindows.add(self.custompotioneffectFrame, text = "Custom Potion Data")
                self.windowCount += 1
                
                self.tabbedWindows.pack(padx=10)

                self.filenameFrame.pack(pady=7)
                self.createSpawnerButton = ttk.Button(self.root, command=self.createSpawner, text="Create Spawner")
                self.createSpawnerButton.pack(pady=2)
                
        def createSpawner(self):
                isItem = False
                itemData = pynbt.TAG_Compound()
                itemData.name = "Item"
                spawner = Spawner(self.mobBoxSelection.get())
                if self.delayCheck.get():
                        spawner.spawner['Delay'].value = self.delayVar.get()
                if self.minspawndelayCheck.get():
                        spawner.spawner['MinSpawnDelay'].value = self.minspawndelayVar.get()
                if self.maxspawndelayCheck.get():
                        spawner.spawner['MaxSpawnDelay'].value = self.maxspawndelayVar.get()
                if self.spawncountCheck.get():
                        spawner.spawner['SpawnCount'].value = self.spawncountVar.get()
                if self.MaxNearbyEntitiesCheck.get():
                        spawner.spawner.add(pynbt.TAG_Short(name = "MaxNearbyEntities", value = self.MaxNearbyEntitiesVar.get()))
                if self.RequiredPlayerRangeCheck.get():
                        spawner.spawner.add(pynbt.TAG_Short(name = "RequiredPlayerRange", value = self.RequiredPlayerRangeVar.get()))
                if self.SpawnRangeCheck.get():
                        spawner.spawner.add(pynbt.TAG_Short(name = "SpawnRange", value = self.SpawnRangeVar.get()))
                spawnerData = pynbt.TAG_Compound()
                spawnerData.name = "SpawnData"
                positionList = pynbt.TAG_List(name="Pos")
                motionList = pynbt.TAG_List(name="Motion")
                directionList = pynbt.TAG_List(name="direction")
                if self.positionCheck.get():
                        positionList.insert(0, pynbt.TAG_Double(value = self.positionXVar.get()))
                        positionList.insert(1, pynbt.TAG_Double(value = self.positionYVar.get()))
                        positionList.insert(2, pynbt.TAG_Double(value = self.positionZVar.get()))
                        spawnerData.add(positionList)
                if self.motionCheck.get():
                        motionList.insert(0, pynbt.TAG_Double(value = self.motionXVar.get()))
                        motionList.insert(1, pynbt.TAG_Double(value = self.motionYVar.get()))
                        motionList.insert(2, pynbt.TAG_Double(value = self.motionZVar.get()))
                        spawnerData.add(motionList)
                if self.directionCheck.get():
                        directionList.insert(0, pynbt.TAG_Double(value = self.directionXVar.get()))
                        directionList.insert(1, pynbt.TAG_Double(value = self.directionYVar.get()))
                        directionList.insert(2, pynbt.TAG_Double(value = self.directionZVar.get()))
                        spawnerData.add(directionList)
                if self.healthCheck.get():
                        spawnerData.add(pynbt.TAG_Short(name = "Health", value = self.healthVar.get()))
                if self.fireCheck.get():
                        spawnerData.add(pynbt.TAG_Short(name = "Fire", value = self.fireVar.get()))
                if self.airCheck.get():
                        spawnerData.add(pynbt.TAG_Short(name = "Air", value = self.airVar.get()))
                if self.attacktimeCheck.get():
                        spawnerData.add(pynbt.TAG_Short(name = "AttackTime", value = self.attacktimeVar.get()))
                if self.hurttimeCheck.get():
                        spawnerData.add(pynbt.TAG_Short(name = "HurtTime", value = self.hurttimeVar.get()))
                if self.deathtimeCheck.get():
                        spawnerData.add(pynbt.TAG_Short(name = "DeathTime", value = self.deathtimeVar.get()))
                if self.canlootCheck.get():
                        spawnerData.add(pynbt.TAG_Byte(name = "CanPickUpLoot", value = self.canlootVar.get()))
                if self.dimensionCheck.get():
                        spawnerData.add(pynbt.TAG_Int(name = "Dimension", value = self.dimensionVar.get()))
                if self.persistencereqCheck.get():
                        spawnerData.add(pynbt.TAG_Byte(name = "PersistenceRequired", value = self.persistencereqVar.get()))
                if self.invulnerableCheck.get():
                        spawnerData.add(pynbt.TAG_Byte(name = "Invulnerable", value = self.invulnerableVar.get()))
                if self.inloveCheck.get():
                        spawnerData.add(pynbt.TAG_Int(name = "InLove", value = self.inloveVar.get()))
                if self.mobageCheck.get():
                        spawnerData.add(pynbt.TAG_Int(name = "Age", value = self.mobageVar.get()))
                if self.PlayerCreatedCheck.get():
                        spawnerData.add(pynbt.TAG_Byte(name = "PlayerCreated", value = self.PlayerCreatedVar.get()))
                if self.saddleCheck.get():
                        spawnerData.add(pynbt.TAG_Byte(name = "Saddle", value = self.saddleVar.get()))
                if self.shearedCheck.get():
                        spawnerData.add(pynbt.TAG_Byte(name = "Sheared", value = self.shearedVar.get()))
                if self.colorCheck.get():
                        spawnerData.add(pynbt.TAG_Byte(name = "Color", value = self.colorVar.get()))
                if self.poweredCheck.get():
                        spawnerData.add(pynbt.TAG_Byte(name = "powered", value = self.poweredVar.get()))
                if self.creeperfuseCheck.get():
                        spawnerData.add(pynbt.TAG_Short(name = "Fuse", value = self.creeperfuseVar.get()))
                if self.explosionradiusCheck.get():
                        spawnerData.add(pynbt.TAG_Byte(name = "ExplosionRadius", value = self.explosionradiusVar.get()))
                if self.batflagsCheck.get():
                        spawnerData.add(pynbt.TAG_Byte(name = "BatFlags", value = self.batflagsVar.get()))
                if self.skeletontypeCheck.get():
                        spawnerData.add(pynbt.TAG_Byte(name = "SkeletonType", value = self.skeletontypeVar.get()))
                if self.witherinvulCheck.get():
                        spawnerData.add(pynbt.TAG_Int(name = "Invul", value = self.witherinvulVar.get()))
                if self.sizeCheck.get():
                        spawnerData.add(pynbt.TAG_Int(name = "Size", value = self.sizeVar.get()))
                if self.ownerCheck.get():
                        spawnerData.add(pynbt.TAG_String(name = "Owner", value = self.ownerVar.get()))
                if self.sittingCheck.get():
                        spawnerData.add(pynbt.TAG_Byte(name = "Sitting", value = self.sittingVar.get()))
                if self.angryCheck.get():
                        spawnerData.add(pynbt.TAG_Byte(name = "Angry", value = self.angryVar.get()))
                if self.collarcolorCheck.get():
                        spawnerData.add(pynbt.TAG_Byte(name = "CollarColor", value = self.collarcolorVar.get()))
                if self.cattypeCheck.get():
                        spawnerData.add(pynbt.TAG_Int(name = "CatType", value = self.cattypeVar.get()))
                if self.angerCheck.get():
                        spawnerData.add(pynbt.TAG_Short(name = "Anger", value = self.angerVar.get()))
                if self.carriedCheck.get():
                        spawnerData.add(pynbt.TAG_Short(name = "carried", value = self.carriedVar.get()))
                if self.carrieddataCheck.get():
                        spawnerData.add(pynbt.TAG_Short(name = "carriedData", value = self.carrieddataVar.get()))
                if self.professionCheck.get():
                        spawnerData.add(pynbt.TAG_Int(name = "Profession", value = self.professionVar.get()))
                if self.richesCheck.get():
                        spawnerData.add(pynbt.TAG_Int(name = "Riches", value = self.richesVar.get()))
                if self.thrownpotionvalueCheck.get():
                        spawnerData.add(pynbt.TAG_Int(name = "potionValue", value = self.thrownpotionvalueVar.get()))
                if self.fuseCheck.get():
                        spawnerData.add(pynbt.TAG_Byte(name = "Fuse", value = self.fuseVar.get()))
                if self.dataCheck.get():
                        spawnerData.add(pynbt.TAG_Byte(name = "Data", value = self.dataVar.get()))
                if self.ongroundCheck.get():
                        spawnerData.add(pynbt.TAG_Byte(name = "OnGround", value = self.ongroundVar.get()))
                if self.tileCheck.get():
                        spawnerData.add(pynbt.TAG_Byte(name = "Tile", value = self.tileVar.get()))
                if self.timeCheck.get():
                        spawnerData.add(pynbt.TAG_Byte(name = "Time", value = self.timeVar.get()))
                if self.falldistanceCheck.get():
                        spawnerData.add(pynbt.TAG_Float(name = "FallDistance", value = self.falldistanceVar.get()))
                if self.dropitemCheck.get():
                        spawnerData.add(pynbt.TAG_Byte(name = "DropItem", value = self.dropitemVar.get()))
                if self.HurtEntitiesCheck.get():
                        spawnerData.add(pynbt.TAG_Byte(name = "HurtEntities", value = self.HurtEntitiesVar.get()))
                if self.FallHurtMaxCheck.get():
                        spawnerData.add(pynbt.TAG_Int(name = "FallHurtMax", value = self.FallHurtMaxVar.get()))
                if self.FallHurtAmountCheck.get():
                        spawnerData.add(pynbt.TAG_Float(name = "FallHurtAmount", value = self.FallHurtAmountVar.get()))
                if self.valueCheck.get():
                        spawnerData.add(pynbt.TAG_Short(name = "Value", value = self.valueVar.get()))
                if self.xtileCheck.get():
                        spawnerData.add(pynbt.TAG_Short(name = "xTile", value = self.xtileVar.get()))
                if self.ytileCheck.get():
                        spawnerData.add(pynbt.TAG_Short(name = "yTile", value = self.ytileVar.get()))
                if self.ztileCheck.get():
                        spawnerData.add(pynbt.TAG_Short(name = "zTile", value = self.ztileVar.get()))
                if self.intileCheck.get():
                        spawnerData.add(pynbt.TAG_Byte(name = "inTile", value = self.intileVar.get()))
                if self.shakeCheck.get():
                        spawnerData.add(pynbt.TAG_Byte(name = "shake", value = self.shakeVar.get()))
                if self.ingroundCheck.get():
                        spawnerData.add(pynbt.TAG_Byte(name = "inGround", value = self.ingroundVar.get()))
                if self.indataCheck.get():
                        spawnerData.add(pynbt.TAG_Byte(name = "inData", value = self.indataVar.get()))
                if self.pickupCheck.get():
                        spawnerData.add(pynbt.TAG_Byte(name = "pickup", value = self.pickupVar.get()))
                if self.damageCheck.get():
                        spawnerData.add(pynbt.TAG_Double(name = "damage", value = self.damageVar.get()))
                if self.itemageCheck.get():
                        spawnerData.add(pynbt.TAG_Short(name = "Age", value = self.itemageVar.get()))
                if self.idCheck.get():
                        itemData.add(pynbt.TAG_Short(name = "id", value = self.idVar.get()))
                        isItem = True
                if self.damageitemCheck.get():
                        itemData.add(pynbt.TAG_Short(name = "Damage", value = self.damageitemVar.get()))
                        isItem = True
                if self.countCheck.get():
                        itemData.add(pynbt.TAG_Byte(name = "Count", value = self.countVar.get()))
                        isItem = True
                itemtagdata = pynbt.TAG_Compound()
                itemtagdata.name = "tag"
                additemtagdata = False
                itemdisplaydata = pynbt.TAG_Compound()
                itemdisplaydata.name = "display"
                additemdisplaydata = False
                if self.enchantsCheck.get():
                        #itemEnchants = pynbt.TAG_Compound()
                        #itemEnchants.name = "tag"
                        itemenchantList = pynbt.TAG_List(name="ench")
                        itemenchantCount = 0
                        itemenchantData = self.enchantsVar.get().split()
                        while len(itemenchantData) > itemenchantCount:
                                enchant = pynbt.TAG_Compound()
                                enchant.add(pynbt.TAG_Short(name = "id", value = itemenchantData[itemenchantCount]))
                                enchant.add(pynbt.TAG_Short(name = "lvl", value = itemenchantData[itemenchantCount + 1]))
                                itemenchantList.insert(itemenchantCount / 2, enchant)
                                itemenchantCount +=2
                        itemtagdata.add(itemenchantList)
                        additemtagdata = True
                        #itemData.add(itemEnchants)
                if self.itemskullownerCheck.get():
                        itemtagdata.add(pynbt.TAG_String(name = "SkullOwner", value = self.itemskullownerVar.get()))
                        try:
                                itemData["Damage"].value = 3
                        except:
                                itemData.add(pynbt.TAG_Short(name = "Damage", value = 3))
                        additemtagdata = True
                if self.itemcolorCheck.get():
                        itemdisplaydata.add(pynbt.TAG_Int(name = "color", value = self.itemcolorVar.get()))
                        additemdisplaydata = True
                if self.itemnameCheck.get():
                        itemdisplaydata.add(pynbt.TAG_String(name = "Name", value = self.itemnameVar.get()))
                        additemdisplaydata = True
                if self.itemloreCheck.get():
                        itemlorelist = pynbt.TAG_List(name = "Lore")
                        itemloredata = self.itemloreVar.get().split('/n')
                        itemlorecount = 0
                        for lore in itemloredata:
                                itemlorelist.insert(itemlorecount, pynbt.TAG_String(value = lore))
                                itemlorecount += 1
                        itemdisplaydata.add(itemlorelist)
                        additemdisplaydata = True
                if additemdisplaydata:
                        itemtagdata.add(itemdisplaydata)
                        additemtagdata = True                                
                if additemtagdata:
                        itemData.add(itemtagdata)
                        isItem = True
                if self.isvillagerCheck.get():
                        spawnerData.add(pynbt.TAG_Byte(name = "IsVillager", value = self.isvillagerVar.get()))
                if self.isbabyCheck.get():
                        spawnerData.add(pynbt.TAG_Byte(name = "IsBaby", value = self.isbabyVar.get()))
                if self.conversiontimeCheck.get():
                        spawnerData.add(pynbt.TAG_Int(name = "ConversionTime", value = self.conversiontimeVar.get()))
                if self.mobweaponCheck.get() or self.mobhelmetCheck.get() or self.mobchestCheck.get() or self.moblegsCheck.get() or self.mobbootsCheck.get():
                        equipmentList = pynbt.TAG_List(name="Equipment")
                        mobweapon = pynbt.TAG_Compound()
                        mobhelmet = pynbt.TAG_Compound()
                        mobchest = pynbt.TAG_Compound()
                        moblegs = pynbt.TAG_Compound()
                        mobboots = pynbt.TAG_Compound()
                        dropchanceList = pynbt.TAG_List(name="DropChances")
                        mobweaponchance = pynbt.TAG_Float(value = 0.05)
                        mobhelmetchance = pynbt.TAG_Float(value = 0.05)
                        mobchestchance = pynbt.TAG_Float(value = 0.05)
                        moblegschance = pynbt.TAG_Float(value = 0.05)
                        mobbootschance = pynbt.TAG_Float(value = 0.05)
                        if self.mobweaponCheck.get():
                                mobweapon.add(pynbt.TAG_Byte(name = "Count", value = self.mobweaponcountVar.get()))
                                mobweapon.add(pynbt.TAG_Short(name = "id", value = self.mobweaponidVar.get()))
                                mobweapon.add(pynbt.TAG_Short(name = "Damage", value = self.mobweapondamageVar.get()))
                                mobweapontagdata = pynbt.TAG_Compound()
                                mobweapontagdata.name = "tag"
                                addmobweapontagdata = False
                                addmobweapondisplaydata = False
                                mobweapondisplaydata = pynbt.TAG_Compound()
                                mobweapondisplaydata.name = "display"
                                if len(self.mobweaponnameVar.get()) > 0:
                                        mobweapondisplaydata.add(pynbt.TAG_String(name = "Name", value = self.mobweaponnameVar.get()))
                                        addmobweapondisplaydata = True
                                if len(self.mobweaponloreVar.get()) > 0:
                                        mobweaponlorelist = pynbt.TAG_List(name = "Lore")
                                        mobweaponlorecount = 0
                                        mobweaponlore = self.mobweaponloreVar.get().split('/n')
                                        for lore in mobweaponlore:
                                                mobweaponlorelist.insert(mobweaponlorecount, pynbt.TAG_String(value=lore))
                                                mobweaponlorecount += 1
                                        mobweapondisplaydata.add(mobweaponlorelist)
                                        addmobweapondisplaydata = True
                                if self.mobweaponcolorVar.get() >= 0:
                                        mobweapondisplaydata.add(pynbt.TAG_Int(name = "color", value = self.mobweaponcolorVar.get()))
                                        addmobweapondisplaydata = True
                                if addmobweapondisplaydata:
                                        mobweapontagdata.add(mobweapondisplaydata)
                                        addmobweapontagdata = True
                                mobweaponenchantList = pynbt.TAG_List(name="ench")
                                mobweaponenchantCount = 0
                                mobweaponenchantData = self.mobweaponenchantsVar.get().split()
                                while len(mobweaponenchantData) > mobweaponenchantCount:
                                        mobweaponenchant = pynbt.TAG_Compound()
                                        mobweaponenchant.add(pynbt.TAG_Short(name = "id", value = mobweaponenchantData[mobweaponenchantCount]))
                                        mobweaponenchant.add(pynbt.TAG_Short(name = "lvl", value = mobweaponenchantData[mobweaponenchantCount + 1]))
                                        mobweaponenchantList.insert(mobweaponenchantCount / 2, mobweaponenchant)
                                        mobweaponenchantCount +=2
                                if mobweaponenchantCount > 0:
                                        mobweapontagdata.add(mobweaponenchantList)
                                        addmobweapontagdata = True
                                if addmobweapontagdata:
                                        mobweapon.add(mobweapontagdata)
                                mobweaponchance.setValue(self.mobweaponchanceVar.get())
                        if self.mobhelmetCheck.get():
                                mobhelmet.add(pynbt.TAG_Byte(name = "Count", value = self.mobhelmetcountVar.get()))
                                mobhelmet.add(pynbt.TAG_Short(name = "id", value = self.mobhelmetidVar.get()))
                                mobhelmet.add(pynbt.TAG_Short(name = "Damage", value = self.mobhelmetdamageVar.get()))
                                mobhelmettagdata = pynbt.TAG_Compound()
                                mobhelmettagdata.name = "tag"
                                addmobhelmettagdata = False
                                addmobhelmetdisplaydata = False
                                mobhelmetdisplaydata = pynbt.TAG_Compound()
                                mobhelmetdisplaydata.name = "display"
                                if len(self.mobhelmetnameVar.get()) > 0:
                                        mobhelmetdisplaydata.add(pynbt.TAG_String(name = "Name", value = self.mobhelmetnameVar.get()))
                                        addmobhelmetdisplaydata = True
                                if len(self.mobhelmetloreVar.get()) > 0:
                                        mobhelmetlorelist = pynbt.TAG_List(name = "Lore")
                                        mobhelmetlorecount = 0
                                        mobhelmetlore = self.mobhelmetloreVar.get().split('/n')
                                        for lore in mobhelmetlore:
                                                mobhelmetlorelist.insert(mobhelmetlorecount, pynbt.TAG_String(value=lore))
                                                mobhelmetlorecount += 1
                                        mobhelmetdisplaydata.add(mobhelmetlorelist)
                                        addmobhelmetdisplaydata = True
                                if self.mobhelmetcolorVar.get() >= 0:
                                        mobhelmetdisplaydata.add(pynbt.TAG_Int(name = "color", value = self.mobhelmetcolorVar.get()))
                                        addmobhelmetdisplaydata = True
                                if addmobhelmetdisplaydata:
                                        mobhelmettagdata.add(mobhelmetdisplaydata)
                                        addmobhelmettagdata = True
                                mobhelmetenchantList = pynbt.TAG_List(name="ench")
                                mobhelmetenchantCount = 0
                                mobhelmetenchantData = self.mobhelmetenchantsVar.get().split()
                                while len(mobhelmetenchantData) > mobhelmetenchantCount:
                                        mobhelmetenchant = pynbt.TAG_Compound()
                                        mobhelmetenchant.add(pynbt.TAG_Short(name = "id", value = mobhelmetenchantData[mobhelmetenchantCount]))
                                        mobhelmetenchant.add(pynbt.TAG_Short(name = "lvl", value = mobhelmetenchantData[mobhelmetenchantCount + 1]))
                                        mobhelmetenchantList.insert(mobhelmetenchantCount / 2, mobhelmetenchant)
                                        mobhelmetenchantCount +=2
                                if mobhelmetenchantCount > 0:
                                        mobhelmettagdata.add(mobhelmetenchantList)
                                        addmobhelmettagdata = True
                                if len(self.mobhelmetskullownerVar.get()) > 0:
                                        mobhelmettagdata.add(pynbt.TAG_String(name = "SkullOwner", value = self.mobhelmetskullownerVar.get()))
                                        addmobhelmettagdata = True
                                if addmobhelmettagdata:
                                        mobhelmet.add(mobhelmettagdata)
                                mobhelmetchance.setValue(self.mobhelmetchanceVar.get())
                        if self.mobchestCheck.get():
                                mobchest.add(pynbt.TAG_Byte(name = "Count", value = self.mobchestcountVar.get()))
                                mobchest.add(pynbt.TAG_Short(name = "id", value = self.mobchestidVar.get()))
                                mobchest.add(pynbt.TAG_Short(name = "Damage", value = self.mobchestdamageVar.get()))
                                mobchesttagdata = pynbt.TAG_Compound()
                                mobchesttagdata.name = "tag"
                                addmobchesttagdata = False
                                addmobchestdisplaydata = False
                                mobchestdisplaydata = pynbt.TAG_Compound()
                                mobchestdisplaydata.name = "display"
                                if len(self.mobchestnameVar.get()) > 0:
                                        mobchestdisplaydata.add(pynbt.TAG_String(name = "Name", value = self.mobchestnameVar.get()))
                                        addmobchestdisplaydata = True
                                if len(self.mobchestloreVar.get()) > 0:
                                        mobchestlorelist = pynbt.TAG_List(name = "Lore")
                                        mobchestlorecount = 0
                                        mobchestlore = (self.mobchestloreVar.get()).split("/n")
                                        for lore in mobchestlore:
                                                mobchestlorelist.insert(mobchestlorecount, pynbt.TAG_String(value=lore))
                                                mobchestlorecount += 1
                                        mobchestdisplaydata.add(mobchestlorelist)
                                        addmobchestdisplaydata = True
                                if self.mobchestcolorVar.get() >= 0:
                                        mobchestdisplaydata.add(pynbt.TAG_Int(name = "color", value = self.mobchestcolorVar.get()))
                                        addmobchestdisplaydata = True
                                if addmobchestdisplaydata:
                                        mobchesttagdata.add(mobchestdisplaydata)
                                        addmobchesttagdata = True
                                mobchestenchantList = pynbt.TAG_List(name="ench")
                                mobchestenchantCount = 0
                                mobchestenchantData = self.mobchestenchantsVar.get().split()
                                while len(mobchestenchantData) > mobchestenchantCount:
                                        mobchestenchant = pynbt.TAG_Compound()
                                        mobchestenchant.add(pynbt.TAG_Short(name = "id", value = mobchestenchantData[mobchestenchantCount]))
                                        mobchestenchant.add(pynbt.TAG_Short(name = "lvl", value = mobchestenchantData[mobchestenchantCount + 1]))
                                        mobchestenchantList.insert(mobchestenchantCount / 2, mobchestenchant)
                                        mobchestenchantCount +=2
                                if mobchestenchantCount > 0:
                                        mobchesttagdata.add(mobchestenchantList)
                                        addmobchesttagdata = True
                                if addmobchesttagdata:
                                        mobchest.add(mobchesttagdata)
                                mobchestchance.setValue(self.mobchestchanceVar.get())
                        if self.moblegsCheck.get():
                                moblegs.add(pynbt.TAG_Byte(name = "Count", value = self.moblegscountVar.get()))
                                moblegs.add(pynbt.TAG_Short(name = "id", value = self.moblegsidVar.get()))
                                moblegs.add(pynbt.TAG_Short(name = "Damage", value = self.moblegsdamageVar.get()))
                                moblegstagdata = pynbt.TAG_Compound()
                                moblegstagdata.name = "tag"
                                addmoblegstagdata = False
                                addmoblegsdisplaydata = False
                                moblegsdisplaydata = pynbt.TAG_Compound()
                                moblegsdisplaydata.name = "display"
                                if len(self.moblegsnameVar.get()) > 0:
                                        moblegsdisplaydata.add(pynbt.TAG_String(name = "Name", value = self.moblegsnameVar.get()))
                                        addmoblegsdisplaydata = True
                                if len(self.moblegsloreVar.get()) > 0:
                                        moblegslorelist = pynbt.TAG_List(name = "Lore")
                                        moblegslorecount = 0
                                        moblegslore = self.moblegsloreVar.get().split("/n")
                                        for lore in moblegslore:
                                                moblegslorelist.insert(moblegslorecount, pynbt.TAG_String(value=lore))
                                                moblegslorecount += 1
                                        moblegsdisplaydata.add(moblegslorelist)
                                        addmoblegsdisplaydata = True
                                if self.moblegscolorVar.get() >= 0:
                                        moblegsdisplaydata.add(pynbt.TAG_Int(name = "color", value = self.moblegscolorVar.get()))
                                        addmoblegsdisplaydata = True
                                if addmoblegsdisplaydata:
                                        moblegstagdata.add(moblegsdisplaydata)
                                        addmoblegstagdata = True
                                moblegsenchantList = pynbt.TAG_List(name="ench")
                                moblegsenchantCount = 0
                                moblegsenchantData = self.moblegsenchantsVar.get().split()
                                while len(moblegsenchantData) > moblegsenchantCount:
                                        moblegsenchant = pynbt.TAG_Compound()
                                        moblegsenchant.add(pynbt.TAG_Short(name = "id", value = moblegsenchantData[moblegsenchantCount]))
                                        moblegsenchant.add(pynbt.TAG_Short(name = "lvl", value = moblegsenchantData[moblegsenchantCount + 1]))
                                        moblegsenchantList.insert(moblegsenchantCount / 2, moblegsenchant)
                                        moblegsenchantCount +=2
                                if moblegsenchantCount > 0:
                                        moblegstagdata.add(moblegsenchantList)
                                        addmoblegstagdata = True
                                if addmoblegstagdata:
                                        moblegs.add(moblegstagdata)
                                moblegschance.setValue(self.moblegschanceVar.get())
                        if self.mobbootsCheck.get():
                                mobboots.add(pynbt.TAG_Byte(name = "Count", value = self.mobbootscountVar.get()))
                                mobboots.add(pynbt.TAG_Short(name = "id", value = self.mobbootsidVar.get()))
                                mobboots.add(pynbt.TAG_Short(name = "Damage", value = self.mobbootsdamageVar.get()))
                                mobbootstagdata = pynbt.TAG_Compound()
                                mobbootstagdata.name = "tag"
                                addmobbootstagdata = False
                                addmobbootsdisplaydata = False
                                mobbootsdisplaydata = pynbt.TAG_Compound()
                                mobbootsdisplaydata.name = "display"
                                if len(self.mobbootsnameVar.get()) > 0:
                                        mobbootsdisplaydata.add(pynbt.TAG_String(name = "Name", value = self.mobbootsnameVar.get()))
                                        addmobbootsdisplaydata = True
                                if len(self.mobbootsloreVar.get()) > 0:
                                        mobbootslorelist = pynbt.TAG_List(name = "Lore")
                                        mobbootslorecount = 0
                                        mobbootslore = (self.mobbootsloreVar.get()).split('/n')
                                        for lore in mobbootslore:
                                                mobbootslorelist.insert(mobbootslorecount, pynbt.TAG_String(value=lore))
                                                mobbootslorecount += 1
                                        mobbootsdisplaydata.add(mobbootslorelist)
                                        addmobbootsdisplaydata = True
                                if self.mobbootscolorVar.get() >= 0:
                                        mobbootsdisplaydata.add(pynbt.TAG_Int(name = "color", value = self.mobbootscolorVar.get()))
                                        addmobbootsdisplaydata = True
                                if addmobbootsdisplaydata:
                                        mobbootstagdata.add(mobbootsdisplaydata)
                                        addmobbootstagdata = True
                                mobbootsenchantList = pynbt.TAG_List(name="ench")
                                mobbootsenchantCount = 0
                                mobbootsenchantData = self.mobbootsenchantsVar.get().split()
                                while len(mobbootsenchantData) > mobbootsenchantCount:
                                        mobbootsenchant = pynbt.TAG_Compound()
                                        mobbootsenchant.add(pynbt.TAG_Short(name = "id", value = mobbootsenchantData[mobbootsenchantCount]))
                                        mobbootsenchant.add(pynbt.TAG_Short(name = "lvl", value = mobbootsenchantData[mobbootsenchantCount + 1]))
                                        mobbootsenchantList.insert(mobbootsenchantCount / 2, mobbootsenchant)
                                        mobbootsenchantCount +=2
                                if mobbootsenchantCount > 0:
                                        mobbootstagdata.add(mobbootsenchantList)
                                        addmobbootstagdata = True
                                if addmobbootstagdata:
                                        mobboots.add(mobbootstagdata)
                                mobbootschance.setValue(self.mobbootschanceVar.get())
                        equipmentList.insert(0, mobweapon)
                        equipmentList.insert(1, mobboots)
                        equipmentList.insert(2, moblegs)
                        equipmentList.insert(3, mobchest)
                        equipmentList.insert(4, mobhelmet)
                        spawnerData.add(equipmentList)
                        dropchanceList.insert(0, mobweaponchance)
                        dropchanceList.insert(1, mobbootschance)
                        dropchanceList.insert(2, moblegschance)
                        dropchanceList.insert(3, mobchestchance)
                        dropchanceList.insert(4, mobhelmetchance)
                        spawnerData.add(dropchanceList)
                potions = 0
                potionList = pynbt.TAG_List(name="ActiveEffects")
                if self.pspeedCheck.get():
                        pspeed = pynbt.TAG_Compound()
                        pspeed.add(pynbt.TAG_Byte(name = "Amplifier", value = self.pspeedlevelVar.get()))
                        pspeed.add(pynbt.TAG_Byte(name = "Id", value = 1))
                        pspeed.add(pynbt.TAG_Int(name = "Duration", value = self.pspeeddurationVar.get()))
                        pspeed.add(pynbt.TAG_Byte(name = "Ambient", value = self.pspeedambientVar.get()))
                        potionList.insert(potions, pspeed)
                        potions += 1
                if self.pslowCheck.get():
                        pslow = pynbt.TAG_Compound()
                        pslow.add(pynbt.TAG_Byte(name = "Amplifier", value = self.pslowlevelVar.get()))
                        pslow.add(pynbt.TAG_Byte(name = "Id", value = 2))
                        pslow.add(pynbt.TAG_Int(name = "Duration", value = self.pslowdurationVar.get()))
                        pslow.add(pynbt.TAG_Byte(name = "Ambient", value = self.pslowambientVar.get()))
                        potionList.insert(potions, pslow)
                        potions += 1
                if self.phasteCheck.get():
                        phaste = pynbt.TAG_Compound()
                        phaste.add(pynbt.TAG_Byte(name = "Amplifier", value = self.phastelevelVar.get()))
                        phaste.add(pynbt.TAG_Byte(name = "Id", value = 3))
                        phaste.add(pynbt.TAG_Int(name = "Duration", value = self.phastedurationVar.get()))
                        phaste.add(pynbt.TAG_Byte(name = "Ambient", value = self.phasteambientVar.get()))
                        potionList.insert(potions, phaste)
                        potions += 1
                if self.pfatigueCheck.get():
                        pfatigue = pynbt.TAG_Compound()
                        pfatigue.add(pynbt.TAG_Byte(name = "Amplifier", value = self.pfatiguelevelVar.get()))
                        pfatigue.add(pynbt.TAG_Byte(name = "Id", value = 4))
                        pfatigue.add(pynbt.TAG_Int(name = "Duration", value = self.pfatiguedurationVar.get()))
                        pfatigue.add(pynbt.TAG_Byte(name = "Ambient", value = self.pfatigueambientVar.get()))
                        potionList.insert(potions, pfatigue)
                        potions += 1
                if self.pstrengthCheck.get():
                        pstrength = pynbt.TAG_Compound()
                        pstrength.add(pynbt.TAG_Byte(name = "Amplifier", value = self.pstrengthlevelVar.get()))
                        pstrength.add(pynbt.TAG_Byte(name = "Id", value = 5))
                        pstrength.add(pynbt.TAG_Int(name = "Duration", value = self.pstrengthdurationVar.get()))
                        pstrength.add(pynbt.TAG_Byte(name = "Ambient", value = self.pstrengthambientVar.get()))
                        potionList.insert(potions, pstrength)
                        potions += 1
                if self.phealthCheck.get():
                        phealth = pynbt.TAG_Compound()
                        phealth.add(pynbt.TAG_Byte(name = "Amplifier", value = self.phealthlevelVar.get()))
                        phealth.add(pynbt.TAG_Byte(name = "Id", value = 6))
                        phealth.add(pynbt.TAG_Int(name = "Duration", value = self.phealthdurationVar.get()))
                        phealth.add(pynbt.TAG_Byte(name = "Ambient", value = self.phealthambientVar.get()))
                        potionList.insert(potions, phealth)
                        potions += 1
                if self.pdamageCheck.get():
                        pdamage = pynbt.TAG_Compound()
                        pdamage.add(pynbt.TAG_Byte(name = "Amplifier", value = self.pdamagelevelVar.get()))
                        pdamage.add(pynbt.TAG_Byte(name = "Id", value = 7))
                        pdamage.add(pynbt.TAG_Int(name = "Duration", value = self.pdamagedurationVar.get()))
                        pdamage.add(pynbt.TAG_Byte(name = "Ambient", value = self.pdamageambientVar.get()))
                        potionList.insert(potions, pdamage)
                        potions += 1
                if self.pjumpCheck.get():
                        pjump = pynbt.TAG_Compound()
                        pjump.add(pynbt.TAG_Byte(name = "Amplifier", value = self.pjumplevelVar.get()))
                        pjump.add(pynbt.TAG_Byte(name = "Id", value = 8))
                        pjump.add(pynbt.TAG_Int(name = "Duration", value = self.pjumpdurationVar.get()))
                        pjump.add(pynbt.TAG_Byte(name = "Ambient", value = self.pjumpambientVar.get()))
                        potionList.insert(potions, pjump)
                        potions += 1
                if self.pnauseaCheck.get():
                        pnausea = pynbt.TAG_Compound()
                        pnausea.add(pynbt.TAG_Byte(name = "Amplifier", value = self.pnausealevelVar.get()))
                        pnausea.add(pynbt.TAG_Byte(name = "Id", value = 9))
                        pnausea.add(pynbt.TAG_Int(name = "Duration", value = self.pnauseadurationVar.get()))
                        pnausea.add(pynbt.TAG_Byte(name = "Ambient", value = self.pnauseaambientVar.get()))
                        potionList.insert(potions, pnausea)
                        potions += 1
                if self.pregenCheck.get():
                        pregen = pynbt.TAG_Compound()
                        pregen.add(pynbt.TAG_Byte(name = "Amplifier", value = self.pregenlevelVar.get()))
                        pregen.add(pynbt.TAG_Byte(name = "Id", value = 10))
                        pregen.add(pynbt.TAG_Int(name = "Duration", value = self.pregendurationVar.get()))
                        pregen.add(pynbt.TAG_Byte(name = "Ambient", value = self.pregenambientVar.get()))
                        potionList.insert(potions, pregen)
                        potions += 1
                if self.presistCheck.get():
                        presist = pynbt.TAG_Compound()
                        presist.add(pynbt.TAG_Byte(name = "Amplifier", value = self.presistlevelVar.get()))
                        presist.add(pynbt.TAG_Byte(name = "Id", value = 11))
                        presist.add(pynbt.TAG_Int(name = "Duration", value = self.presistdurationVar.get()))
                        presist.add(pynbt.TAG_Byte(name = "Ambient", value = self.presistambientVar.get()))
                        potionList.insert(potions, presist)
                        potions += 1
                if self.pfireresCheck.get():
                        pfireres = pynbt.TAG_Compound()
                        pfireres.add(pynbt.TAG_Byte(name = "Amplifier", value = self.pfirereslevelVar.get()))
                        pfireres.add(pynbt.TAG_Byte(name = "Id", value = 12))
                        pfireres.add(pynbt.TAG_Int(name = "Duration", value = self.pfireresdurationVar.get()))
                        pfireres.add(pynbt.TAG_Byte(name = "Ambient", value = self.pfireresambientVar.get()))
                        potionList.insert(potions, pfireres)
                        potions += 1
                if self.pwaterbrCheck.get():
                        pwaterbr = pynbt.TAG_Compound()
                        pwaterbr.add(pynbt.TAG_Byte(name = "Amplifier", value = self.pwaterbrlevelVar.get()))
                        pwaterbr.add(pynbt.TAG_Byte(name = "Id", value = 13))
                        pwaterbr.add(pynbt.TAG_Int(name = "Duration", value = self.pwaterbrdurationVar.get()))
                        pwaterbr.add(pynbt.TAG_Byte(name = "Ambient", value = self.pwaterbrambientVar.get()))
                        potionList.insert(potions, pwaterbr)
                        potions += 1
                if self.pinvisCheck.get():
                        pinvis = pynbt.TAG_Compound()
                        pinvis.add(pynbt.TAG_Byte(name = "Amplifier", value = self.pinvislevelVar.get()))
                        pinvis.add(pynbt.TAG_Byte(name = "Id", value = 14))
                        pinvis.add(pynbt.TAG_Int(name = "Duration", value = self.pinvisdurationVar.get()))
                        pinvis.add(pynbt.TAG_Byte(name = "Ambient", value = self.pinvisambientVar.get()))
                        potionList.insert(potions, pinvis)
                        potions += 1
                if self.pblindCheck.get():
                        pblind = pynbt.TAG_Compound()
                        pblind.add(pynbt.TAG_Byte(name = "Amplifier", value = self.pblindlevelVar.get()))
                        pblind.add(pynbt.TAG_Byte(name = "Id", value = 15))
                        pblind.add(pynbt.TAG_Int(name = "Duration", value = self.pblinddurationVar.get()))
                        pblind.add(pynbt.TAG_Byte(name = "Ambient", value = self.pblindambientVar.get()))
                        potionList.insert(potions, pblind)
                        potions += 1
                if self.pnightvCheck.get():
                        pnightv = pynbt.TAG_Compound()
                        pnightv.add(pynbt.TAG_Byte(name = "Amplifier", value = self.pnightvlevelVar.get()))
                        pnightv.add(pynbt.TAG_Byte(name = "Id", value = 16))
                        pnightv.add(pynbt.TAG_Int(name = "Duration", value = self.pnightvdurationVar.get()))
                        pnightv.add(pynbt.TAG_Byte(name = "Ambient", value = self.pnightvambientVar.get()))
                        potionList.insert(potions, pnightv)
                        potions += 1
                if self.phungerCheck.get():
                        phunger = pynbt.TAG_Compound()
                        phunger.add(pynbt.TAG_Byte(name = "Amplifier", value = self.phungerlevelVar.get()))
                        phunger.add(pynbt.TAG_Byte(name = "Id", value = 17))
                        phunger.add(pynbt.TAG_Int(name = "Duration", value = self.phungerdurationVar.get()))
                        phunger.add(pynbt.TAG_Byte(name = "Ambient", value = self.phungerambientVar.get()))
                        potionList.insert(potions, phunger)
                        potions += 1
                if self.pweakCheck.get():
                        pweak = pynbt.TAG_Compound()
                        pweak.add(pynbt.TAG_Byte(name = "Amplifier", value = self.pweaklevelVar.get()))
                        pweak.add(pynbt.TAG_Byte(name = "Id", value = 18))
                        pweak.add(pynbt.TAG_Int(name = "Duration", value = self.pweakdurationVar.get()))
                        pweak.add(pynbt.TAG_Byte(name = "Ambient", value = self.pweakambientVar.get()))
                        potionList.insert(potions, pweak)
                        potions += 1
                if self.ppoisonCheck.get():
                        ppoison = pynbt.TAG_Compound()
                        ppoison.add(pynbt.TAG_Byte(name = "Amplifier", value = self.ppoisonlevelVar.get()))
                        ppoison.add(pynbt.TAG_Byte(name = "Id", value = 19))
                        ppoison.add(pynbt.TAG_Int(name = "Duration", value = self.ppoisondurationVar.get()))
                        ppoison.add(pynbt.TAG_Byte(name = "Ambient", value = self.ppoisonambientVar.get()))
                        potionList.insert(potions, ppoison)
                        potions += 1
                if self.pwitherCheck.get():
                        pwither = pynbt.TAG_Compound()
                        pwither.add(pynbt.TAG_Byte(name = "Amplifier", value = self.pwitherlevelVar.get()))
                        pwither.add(pynbt.TAG_Byte(name = "Id", value = 20))
                        pwither.add(pynbt.TAG_Int(name = "Duration", value = self.pwitherdurationVar.get()))
                        pwither.add(pynbt.TAG_Byte(name = "Ambient", value = self.pwitherambientVar.get()))
                        potionList.insert(potions, pwither)
                        potions += 1

                if potions > 0:
                        spawnerData.add(potionList)

                if self.custompotioneffectCheck.get():
                        cpeindex = int(self.colorBox.current())
                        print("index: %s" % (cpeindex))
                        cpedamage = 0
                        if cpeindex < 0:
                                print("Color error... defaulting to 0")
                                cpedamage = 0
                        elif cpeindex == 0:
                                print("using custom damage value")
                                cpedamage = self.effectdamageVar.get()
                        else:
                                if self.splashCheck.get() or self.mobBoxSelection.get() == "ThrownPotion":
                                        cpedamage = self.presetsplashdamagelist[cpeindex]
                                else:
                                        cpedamage = self.presetdamagelist[cpeindex]
                        cpepotion = Potion(cpedamage, self.currenteffects)
                        if self.mobBoxSelection.get() == "ThrownPotion":
                                cpeData = pynbt.TAG_Compound()
                                cpeData.name = "Potion"
                                cpeData.add(pynbt.TAG_Short(name = "Damage", value = cpedamage))
                                cpeData.add(pynbt.TAG_Short(name = "id", value = 373))
                                cpeData.add(cpepotion.getNBT())
                                spawnerData.add(cpeData)
                        elif self.mobBoxSelection.get() == "Item":
                                try:
                                        itemData["Damage"].value = cpedamage
                                except:
                                        itemData.add(pynbt.TAG_Short(name = "Damage", value = cpedamage))
                                itemData.add(cpepotion.getNBT())
                                isItem = True

                if isItem:
                        spawnerData.add(itemData)
                spawner.spawner.add(spawnerData)
                schem = Schematic(spawner.spawner)

                print(schem.schematic.pretty_string())
                schem.schematic.save(filename="./schematics/" + self.filenameVar.get() + ".schematic")
                
        def addEffect(self):
                print("Adding effect to potion")
                effect = PotionEffect(self.effectidVar.get(), self.effectamplifierVar.get(), self.effectdurationVar.get())
                self.currenteffects.append(effect)
                effecttxt = ("ID: %s Level: %s Duration: %s" % (self.effectidVar.get(), self.effectamplifierVar.get(), self.effectdurationVar.get()))
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
                
if __name__ == '__main__':
        root = Tkinter.Tk()
        root.title('Custom Spawner')
        root.wm_geometry('750x750')
        ## Grid sizing behavior in window
        root.grid_rowconfigure(0, weight=1)
        root.grid_columnconfigure(0, weight=1)
        ## Canvas
        cnv = Tkinter.Canvas(root)
        cnv.grid(row=0, column=0, sticky='nswe')
        ## Scrollbars for canvas
        hScroll = Tkinter.Scrollbar(root, orient='horizontal', command=cnv.xview)
        hScroll.grid(row=1, column=0, sticky='we')
        vScroll = Tkinter.Scrollbar(root, orient='vertical', command=cnv.yview)
        vScroll.grid(row=0, column=1, sticky='ns')
        cnv.configure(xscrollcommand=hScroll.set, yscrollcommand=vScroll.set)
        ## Frame in canvas
        frm = Tkinter.Frame(cnv)
        ## This puts the frame in the canvas's scrollable zone
        cnv.create_window(0, 0, window=frm, anchor='nw')
        ## Frame contents
        mywindow = MakeSpawner(frm)
        #for i in range(20):
        #b = Button(frm, text='Button n#%s' % i, width=40)
        #b.pack(side=TOP, padx=2, pady=2)
        ## Update display to get correct dimensions
        frm.update_idletasks()
        ## Configure size of canvas's scrollable zone
        cnv.configure(scrollregion=(0, 0, frm.winfo_width(), frm.winfo_height()))
        ## Go!
        #mywindow = MakeSpawner(root)
	root.mainloop()
