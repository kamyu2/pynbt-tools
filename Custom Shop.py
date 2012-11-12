#!/usr/bin/env python
"""
Create schematic of a villager with custom shop options.
"""
import os, sys
import Tkinter, tkFileDialog, ttk
import struct

import pynbt

class Item:
        def __init__(self, count, i, damage, enchants=None, name=None, lore=None):
                self.count = count
                self.id = i
                self.damage = damage
                self.enchants = enchants
                self.name = name
                self.lore = lore

class Offer:
        def __init__(self, maxuses, uses, sell, buyA, buyB=None):
                self.maxuses = maxuses
                self.uses = uses
                self.sell = sell
                self.buyA = buyA
                self.buyB = buyB

        def getNBT(self):
                offer = pynbt.TAG_Compound()
                offer.add(pynbt.TAG_Int(name = "maxUses", value = self.maxuses))
                offer.add(pynbt.TAG_Int(name = "uses", value = self.uses))
                buyAtag = pynbt.TAG_Compound()
                buyAtag.name = "buy"
                buyAtag.add(pynbt.TAG_Byte(name = "Count", value = self.buyA.count))
                buyAtag.add(pynbt.TAG_Short(name = "Damage", value = self.buyA.damage))
                buyAtag.add(pynbt.TAG_Short(name = "id", value = self.buyA.id))
                offer.add(buyAtag)
                if self.buyB is not None:
                        buyBtag = pynbt.TAG_Compound()
                        buyBtag.name = "buyB"
                        buyBtag.add(pynbt.TAG_Byte(name = "Count", value = self.buyB.count))
                        buyBtag.add(pynbt.TAG_Short(name = "Damage", value = self.buyB.damage))
                        buyBtag.add(pynbt.TAG_Short(name = "id", value = self.buyB.id))
                        offer.add(buyBtag)
                selltag = pynbt.TAG_Compound()
                selltag.name = "sell"
                selltag.add(pynbt.TAG_Byte(name = "Count", value = self.sell.count))
                selltag.add(pynbt.TAG_Short(name = "Damage", value = self.sell.damage))
                selltag.add(pynbt.TAG_Short(name = "id", value = self.sell.id))
                itemTag = pynbt.TAG_Compound()
                itemTag.name = "tag"
                addTag = False
                if self.sell.enchants is not None:
                        enchantList = pynbt.TAG_List(name="ench")
                        enchantCount = 0
                        enchantData = self.sell.enchants.split()
                        while len(enchantData) > enchantCount:
                                enchant = pynbt.TAG_Compound()
                                enchant.add(pynbt.TAG_Short(name = "id", value = enchantData[enchantCount]))
                                enchant.add(pynbt.TAG_Short(name = "lvl", value = enchantData[enchantCount + 1]))
                                enchantList.insert(enchantCount / 2, enchant)
                                enchantCount +=2
                        if enchantCount > 0:
                                itemTag.add(enchantList)
                                addTag = True
                display = pynbt.TAG_Compound()
                display.name = "display"
                addDisplay = False
                if self.sell.name is not None:
                        if len(self.sell.name) > 0:
                                display.add(pynbt.TAG_String(name="Name", value=self.sell.name))
                                addDisplay = True
                if self.sell.lore is not None:
                        if len(self.sell.lore) > 0:
                                lorelist = pynbt.TAG_List(name="Lore")
                                lorecount = 0
                                for line in self.sell.lore:
                                        lorelist.insert(lorecount, pynbt.TAG_String(value=line))
                                        lorecount += 1
                                display.add(lorelist)
                                addDisplay = True                                        
                if addDisplay:
                        itemTag.add(display)
                        addTag = True
                if addTag:
                        selltag.add(itemTag)
                offer.add(selltag)
                return offer
                
class Villager:
        def __init__(self, profession, riches, invulnerable, offers):
                self.CanPickUpLoot = 0
                self.OnGround = 1
                self.Air = 300
                self.AttackTime = 0
                self.DeathTime = 0
                self.Fire = -1
                self.Health = 20
                self.HurtTime = 0
                self.Age = 0
                self.Dimension = 0
                self.Profession = profession
                self.Riches = riches
                self.Invulnerable = invulnerable
                self.FallDistance = 0
                self.id = "Villager"
                self.offers = offers

        def getNBT(self):
                vill = pynbt.TAG_Compound()
                vill.add(pynbt.TAG_Byte(name = "CanPickUpLoot", value = self.CanPickUpLoot))
                vill.add(pynbt.TAG_Byte(name = "OnGround", value = self.OnGround))
                vill.add(pynbt.TAG_Short(name = "Air", value = self.Air))
                vill.add(pynbt.TAG_Short(name = "AttackTime", value = self.AttackTime))
                vill.add(pynbt.TAG_Short(name = "DeathTime", value = self.DeathTime))
                vill.add(pynbt.TAG_Short(name = "Fire", value = self.Fire))
                vill.add(pynbt.TAG_Short(name = "Health", value = self.Health))
                vill.add(pynbt.TAG_Short(name = "HurtTime", value = self.HurtTime))
                vill.add(pynbt.TAG_Int(name = "Age", value = self.Age))
                vill.add(pynbt.TAG_Int(name = "Dimension", value = self.Dimension))
                vill.add(pynbt.TAG_Int(name = "Profession", value = self.Profession))
                vill.add(pynbt.TAG_Int(name = "Riches", value = self.Riches))
                if self.Invulnerable:
                        vill.add(pynbt.TAG_Byte(name = "Invulnerable", value = 1))
                vill.add(pynbt.TAG_Float(name = "FallDistance", value = self.FallDistance))
                vill.add(pynbt.TAG_String(name = "id", value = self.id))
                drops = pynbt.TAG_List(name = "DropChances")
                equip = pynbt.TAG_List(name = "Equipment")
                index = 0
                while index < 5:
                        drops.insert(index, pynbt.TAG_Float(value = 0.05))
                        equip.insert(index, pynbt.TAG_Compound())
                        index += 1
                vill.add(drops)
                vill.add(equip)
                motion = pynbt.TAG_List(name = "Motion")
                motion.insert(0, pynbt.TAG_Double(value = 0))
                motion.insert(1, pynbt.TAG_Double(value = 0))
                motion.insert(2, pynbt.TAG_Double(value = 0))
                vill.add(motion)
                position = pynbt.TAG_List(name = "Pos")
                position.insert(0, pynbt.TAG_Double(value = 0.5))
                position.insert(1, pynbt.TAG_Double(value = 0))
                position.insert(2, pynbt.TAG_Double(value = 0.5))
                vill.add(position)
                rotation = pynbt.TAG_List(name = "Rotation")
                rotation.insert(0, pynbt.TAG_Float(value = 0))
                rotation.insert(1, pynbt.TAG_Float(value = 0))
                vill.add(rotation)
                offerstag = pynbt.TAG_Compound()
                offerstag.name = "Offers"
                recipies = pynbt.TAG_List(name = "Recipes")
                index = 0
                for offer in self.offers:
                        recipies.insert(index, offer.getNBT())
                        index += 1
                offerstag.add(recipies)
                vill.add(offerstag)
                return vill
                
class Schematic:
        def __init__(self, villager):
                villagerList = pynbt.TAG_List(name = "Entities", list_type = pynbt.TAG_Compound)
                villagerList.insert(0, villager)
                block_data = [0]*2
                self.schematic = pynbt.TAG_Compound()
                self.schematic.name = "Schematic"
                self.schematic.add(pynbt.TAG_Short(name = "Width", value = 1))
                self.schematic.add(pynbt.TAG_Short(name = "Length", value = 1))
                self.schematic.add(pynbt.TAG_Short(name = "Height", value = 2))
                self.schematic.add(pynbt.TAG_String(name = "Materials", value = "Alpha"))
                self.schematic.add(pynbt.TAG_Byte_Array(name = "Blocks", value = bytearray(buffer(struct.pack('b'*len(block_data), *block_data)))))
                self.schematic.add(pynbt.TAG_Byte_Array(name = "Data", value = bytearray(buffer(struct.pack('b'*len(block_data), *block_data)))))
                self.schematic.add(villagerList)
                self.schematic.add(pynbt.TAG_List(name = "TileEntities", list_type = pynbt.TAG_Compound))
                
class CustomVillager:
        def __init__(self, frame):
                self.root = frame
                
                self.currentoffers = []
                self.currentlore = []

                self.professionlist = ["Farmer", "Librarian", "Priest", "Blacksmith", "Butcher", "Generic (green)"]

                professionFrame = Tkinter.Frame(self.root)
                professionLabel = Tkinter.Label(professionFrame, text="Profession:", width=15)
                self.professionVar = Tkinter.StringVar()
                self.professionBox = ttk.Combobox(professionFrame, textvariable=self.professionVar, state='readonly')
                self.professionBox['values'] = self.professionlist
                self.professionBox.current(0)
                professionLabel.pack(side='left')
                self.professionBox.pack(side='left')
                professionFrame.pack(pady=5)

                richesFrame = Tkinter.Frame(self.root)
                richesLabel = Tkinter.Label(richesFrame, text="Riches:", width=15)
                self.richesVar = Tkinter.IntVar(value=0)
                self.richesEntry = Tkinter.Entry(richesFrame, textvariable=self.richesVar, width=10)
                richesLabel.pack(side='left')
                self.richesEntry.pack(side='left')
                richesFrame.pack(pady=5)

                invulnerableFrame = Tkinter.Frame(self.root)
                invulnerableLabel = Tkinter.Label(invulnerableFrame, text="Invulnerable", width=12)
                self.invulnerableCheck = Tkinter.BooleanVar(value=False)
                self.invulnerableCheckButton = Tkinter.Checkbutton(invulnerableFrame, variable=self.invulnerableCheck, onvalue=True, offvalue=False, height=1)
                self.invulnerableCheckButton.pack(side='left')
                invulnerableLabel.pack(side='left')
                invulnerableFrame.pack(pady=5)

                offersFrame = Tkinter.Frame(self.root, bd=1, relief='sunken')
                offersLabel = Tkinter.Label(offersFrame, text="Offer/s", width=8)
                offersLabel.pack()

                maxusesFrame = Tkinter.Frame(offersFrame)
                maxusesLabel = Tkinter.Label(maxusesFrame, text="Max uses:", width=15)
                self.maxusesVar = Tkinter.IntVar(value=7)
                self.maxusesEntry = Tkinter.Entry(maxusesFrame, textvariable=self.maxusesVar, width=10)
                maxusesLabel.pack(side='left')
                self.maxusesEntry.pack(side='left')
                maxusesFrame.pack()

                usesFrame = Tkinter.Frame(offersFrame)
                usesLabel = Tkinter.Label(usesFrame, text="Current uses:", width=15)
                self.usesVar = Tkinter.IntVar(value=0)
                self.usesEntry = Tkinter.Entry(usesFrame, textvariable=self.usesVar, width=10)
                usesLabel.pack(side='left')
                self.usesEntry.pack(side='left')
                usesFrame.pack()

                vendoritemsFrame = Tkinter.Frame(offersFrame)
##buy A
                buyAFrame = Tkinter.Frame(vendoritemsFrame, bd=1, relief='sunken')
                buyALabel = Tkinter.Label(buyAFrame, text="Buy A", width=6)
                buyALabel.pack()
                
                buyAcountFrame = Tkinter.Frame(buyAFrame)
                buyAcountLabel = Tkinter.Label(buyAcountFrame, text="Count:", width=15)
                self.buyAcountVar = Tkinter.IntVar(value=1)
                self.buyAcountEntry = Tkinter.Entry(buyAcountFrame, textvariable=self.buyAcountVar, width=10)
                buyAcountLabel.pack(side='left')
                self.buyAcountEntry.pack(side='left')
                buyAcountFrame.pack()

                buyAidFrame = Tkinter.Frame(buyAFrame)
                buyAidLabel = Tkinter.Label(buyAidFrame, text="Id:", width=15)
                self.buyAidVar = Tkinter.IntVar(value=0)
                self.buyAidEntry = Tkinter.Entry(buyAidFrame, textvariable=self.buyAidVar, width=10)
                buyAidLabel.pack(side='left')
                self.buyAidEntry.pack(side='left')
                buyAidFrame.pack()

                buyAdamageFrame = Tkinter.Frame(buyAFrame)
                buyAdamageLabel = Tkinter.Label(buyAdamageFrame, text="Damage:", width=15)
                self.buyAdamageVar = Tkinter.IntVar(value=0)
                self.buyAdamageEntry = Tkinter.Entry(buyAdamageFrame, textvariable=self.buyAdamageVar, width=10)
                buyAdamageLabel.pack(side='left')
                self.buyAdamageEntry.pack(side='left')
                buyAdamageFrame.pack()

                buyAFrame.pack(side='left', padx=5, pady=5)
##buy B
                buyBFrame = Tkinter.Frame(vendoritemsFrame, bd=1, relief='sunken')
                buyBLabel = Tkinter.Label(buyBFrame, text="Buy B", width=6)
                buyBLabel.pack()

                self.buyBCheckVar = Tkinter.BooleanVar(value=False)
                self.buyBCheckButton = Tkinter.Checkbutton(buyBFrame, variable=self.buyBCheckVar, onvalue=True, offvalue=False, height=1)
                self.buyBCheckButton.pack(side='left')


                buyBcountFrame = Tkinter.Frame(buyBFrame)
                buyBcountLabel = Tkinter.Label(buyBcountFrame, text="Count:", width=15)
                self.buyBcountVar = Tkinter.IntVar(value=1)
                self.buyBcountEntry = Tkinter.Entry(buyBcountFrame, textvariable=self.buyBcountVar, width=10)
                buyBcountLabel.pack(side='left')
                self.buyBcountEntry.pack(side='left')
                buyBcountFrame.pack()

                buyBidFrame = Tkinter.Frame(buyBFrame)
                buyBidLabel = Tkinter.Label(buyBidFrame, text="Id:", width=15)
                self.buyBidVar = Tkinter.IntVar(value=0)
                self.buyBidEntry = Tkinter.Entry(buyBidFrame, textvariable=self.buyBidVar, width=10)
                buyBidLabel.pack(side='left')
                self.buyBidEntry.pack(side='left')
                buyBidFrame.pack()

                buyBdamageFrame = Tkinter.Frame(buyBFrame)
                buyBdamageLabel = Tkinter.Label(buyBdamageFrame, text="Damage:", width=15)
                self.buyBdamageVar = Tkinter.IntVar(value=0)
                self.buyBdamageEntry = Tkinter.Entry(buyBdamageFrame, textvariable=self.buyBdamageVar, width=10)
                buyBdamageLabel.pack(side='left')
                self.buyBdamageEntry.pack(side='left')
                buyBdamageFrame.pack()

                buyBFrame.pack(side='left', padx=5, pady=5)
##sell
                sellFrame = Tkinter.Frame(vendoritemsFrame, bd=1, relief='sunken')
                sellLabel = Tkinter.Label(sellFrame, text="Sell", width=6)
                sellLabel.pack()

                sellcountFrame = Tkinter.Frame(sellFrame)
                sellcountLabel = Tkinter.Label(sellcountFrame, text="Count:", width=15)
                self.sellcountVar = Tkinter.IntVar(value=1)
                self.sellcountEntry = Tkinter.Entry(sellcountFrame, textvariable=self.sellcountVar, width=10)
                sellcountLabel.pack(side='left')
                self.sellcountEntry.pack(side='left')
                sellcountFrame.pack()

                sellidFrame = Tkinter.Frame(sellFrame)
                sellidLabel = Tkinter.Label(sellidFrame, text="Id:", width=15)
                self.sellidVar = Tkinter.IntVar(value=0)
                self.sellidEntry = Tkinter.Entry(sellidFrame, textvariable=self.sellidVar, width=10)
                sellidLabel.pack(side='left')
                self.sellidEntry.pack(side='left')
                sellidFrame.pack()

                selldamageFrame = Tkinter.Frame(sellFrame)
                selldamageLabel = Tkinter.Label(selldamageFrame, text="Damage:", width=15)
                self.selldamageVar = Tkinter.IntVar(value=0)
                self.selldamageEntry = Tkinter.Entry(selldamageFrame, textvariable=self.selldamageVar, width=10)
                selldamageLabel.pack(side='left')
                self.selldamageEntry.pack(side='left')
                selldamageFrame.pack()

                sellenchantsFrame = Tkinter.Frame(sellFrame)
                sellenchantsLabel = Tkinter.Label(sellenchantsFrame, text="Enchant/s:", width=15)
                self.sellenchantsVar = Tkinter.StringVar(value="")
                self.sellenchantsEntry = Tkinter.Entry(sellenchantsFrame, textvariable=self.sellenchantsVar, width=10)
                sellenchantsLabel.pack(side='left')
                self.sellenchantsEntry.pack(side='left')
                sellenchantsFrame.pack()

                sellnameFrame = Tkinter.Frame(sellFrame)
                sellnameLabel = Tkinter.Label(sellnameFrame, text="Name:", width=5)
                self.sellnameVar = Tkinter.StringVar(value="")
                self.sellnameEntry = Tkinter.Entry(sellnameFrame, textvariable=self.sellnameVar, width=30)
                sellnameLabel.pack(side='left')
                self.sellnameEntry.pack(side='left')
                sellnameFrame.pack()

                sellLoreFrame = Tkinter.Frame(sellFrame)
                sellLoreLabel = Tkinter.Label(sellLoreFrame, text="Lore:", width=5)
                self.sellLoreVar = Tkinter.StringVar(value="")
                self.sellLoreEntry = Tkinter.Entry(sellLoreFrame, textvariable=self.sellLoreVar, width=30)
                sellLoreLabel.pack(side='left')
                self.sellLoreEntry.pack(side='left')
                sellLoreFrame.pack(pady=5)
                lorebuttonandlistFrame = Tkinter.Frame(sellFrame)
                lorebuttonFrame = Tkinter.Frame(lorebuttonandlistFrame)
                self.addLoreButton = Tkinter.Button(lorebuttonFrame, command=self.addLore, text="Add lore")
                self.removeLoreButton = Tkinter.Button(lorebuttonFrame, command=self.removeLore, text="Remove lore")
                self.removeallLoreButton = Tkinter.Button(lorebuttonFrame, command=self.removeallLore, text="Remove all")
                self.addLoreButton.pack(pady=5)
                self.removeLoreButton.pack(pady=5)
                self.removeallLoreButton.pack(pady=5)
                lorebuttonFrame.pack(side='left')
                self.loreList = Tkinter.Listbox(lorebuttonandlistFrame, selectmode='SINGLE', width=30)
                self.loreList.pack(padx=5, side='left', fill='y', expand=1)
                lorebuttonandlistFrame.pack()

                sellFrame.pack(side='left', padx=5, pady=5)

                vendoritemsFrame.pack(pady=5)
##offer buttons/list
                offerbuttonandlistFrame = Tkinter.Frame(offersFrame)
                offerbuttonFrame = Tkinter.Frame(offerbuttonandlistFrame)
                self.addOfferButton = Tkinter.Button(offerbuttonFrame, command=self.addOffer, text="Add offer", width=15, height=2)
                self.removeOfferButton = Tkinter.Button(offerbuttonFrame, command=self.removeOffer, text="Remove offer", width=15, height=2)
                self.removealloffersButton = Tkinter.Button(offerbuttonFrame, command=self.removeallOffers, text="Remove all", width=15, height=2)
                self.addOfferButton.pack(pady=5)
                self.removeOfferButton.pack(pady=5)
                self.removealloffersButton.pack(pady=5)
                offerbuttonFrame.pack(side='left')
                self.offerList = Tkinter.Listbox(offerbuttonandlistFrame, selectmode='SINGLE', width=60)
                self.offerList.pack(padx=5, side='left', fill='y', expand=1)
                offerbuttonandlistFrame.pack(pady=5)
                
                offersFrame.pack(pady=5)
##filename stuff
                self.filenameVar = Tkinter.StringVar(value="temp")
                filenameFrame = Tkinter.Frame(self.root)
                filenameLabel1 = Tkinter.Label(filenameFrame, text = "Filename: ", width=15)
                self.filenameEntry = Tkinter.Entry(filenameFrame, textvariable=self.filenameVar, width=30)
                filenameLabel2 = Tkinter.Label(filenameFrame, text = ".schematic", width=15)
                filenameLabel1.pack(side='left')
                self.filenameEntry.pack(side='left')
                filenameLabel2.pack(side='left')
                filenameFrame.pack()
                self.createShopButton = Tkinter.Button(self.root, command=self.createShop, text="Create shop schematic", width=20, height=2)
                self.createShopButton.pack(pady=5)

        def addOffer(self):
                itembuyA = Item(self.buyAcountVar.get(), self.buyAidVar.get(), self.buyAdamageVar.get())
                cl = []
                for l in self.currentlore:
                        cl.append(l)
                itemsell = Item(self.sellcountVar.get(), self.sellidVar.get(), self.selldamageVar.get(), self.sellenchantsVar.get(), self.sellnameVar.get(), cl)
                offer = None
                offertxt = ("MaxUses: %s Uses: %s" % (self.maxusesVar.get(), self.usesVar.get()))
                offertxt += (" Sell: %s Count: %s Id: %s Damage: %s" % (self.sellnameVar.get(), self.sellcountVar.get(), self.sellidVar.get(), self.selldamageVar.get()))
                offertxt += (" BuyA: Count: %s Id: %s Damage: %s" % (self.buyAcountVar.get(), self.buyAidVar.get(), self.buyAdamageVar.get()))
                if self.buyBCheckVar.get():
                        itembuyB = Item(self.buyBcountVar.get(), self.buyBidVar.get(), self.buyBdamageVar.get())
                        offertxt += (" BuyB: Count: %s Id: %s Damage: %s" % (self.buyBcountVar.get(), self.buyBidVar.get(), self.buyBdamageVar.get()))
                        offer = Offer(self.maxusesVar.get(), self.usesVar.get(), itemsell, itembuyA, itembuyB)
                else:
                        offer = Offer(self.maxusesVar.get(), self.usesVar.get(), itemsell, itembuyA)
                self.currentoffers.append(offer)
                self.offerList.insert(self.offerList.size(), offertxt)

        def removeOffer(self):
                selection = self.offerList.curselection()
                if len(selection) > 0:
                        self.currentoffers.pop(int(selection[0]))
                        self.offerList.delete(selection)

        def removeallOffers(self):
                self.currentoffers = []
                self.offerList.delete(0,'end')

        def addLore(self):
                self.currentlore.append(self.sellLoreVar.get())
                self.loreList.insert(self.loreList.size(), self.sellLoreVar.get())

        def removeLore(self):
                selection = self.loreList.curselection()
                if len(selection) > 0:
                        self.currentlore.pop(int(selection[0]))
                        self.loreList.delete(selection)

        def removeallLore(self):
                self.currentlore = []
                self.loreList.delete(0,'end')

        def createShop(self):
                if len(self.currentoffers) > 0:
                        index = int(self.professionBox.current())
                        profession = 0
                        if index < 0:
                                print("Profession error... defaulting to 0")
                                profession = 0
                        else:
                                profession = index
                        villager = Villager(profession, self.richesVar.get(), self.invulnerableCheck.get(), self.currentoffers)
                        schem = Schematic(villager.getNBT())
                        print(schem.schematic.pretty_string())
                        schem.schematic.save(filename="./schematics/" + self.filenameVar.get() + ".schematic")
                else:
                        print("No offers in list...")
                        
if __name__ == '__main__':
        root = Tkinter.Tk()
        root.title('Custom Shop')
        root.wm_geometry('680x710')
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
        mywindow = CustomVillager(frm)
        ## Update display to get correct dimensions
        frm.update_idletasks()
        ## Configure size of canvas's scrollable zone
        cnv.configure(scrollregion=(0, 0, frm.winfo_width(), frm.winfo_height()))
	root.mainloop()


