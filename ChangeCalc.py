#!/usr/bin/python3
# -*- coding: utf-8 -*-

################################################################
#
# A futtatáshoz Python 3 szükséges. Az importált modulok az
# alaptelepítés részei. Tesztelve Linuxon, Windowson.
#
################################################################

import urllib.request as ureq
import xml.etree.ElementTree as et
import tkinter as tk
import tkinter.ttk as ttk

################################################################
#
# A calculateHUF függvény végzi a szerény matekot, ami a
# keresztreferencia alapján a devizából forintot számol.
# A Combobox aktuálisan kiválasztott eleme alapján kikeresi a
# szótárból a hozzá tartozó váltási értéket, valamint kikeresi
# a HUF váltási értékét.
#
# myCash : a felhasználó által bevitt deviza mennyiség
# selectedCurrency : a Comboboxban kiválasztott devizanem
# rateFX : EUR/deviza keresztreferencia érték
# rateHUF : EUR/HUF keresztreferencia érték
# myHUF : a foritban kifejezett pénzmennyiség
#
################################################################

def calculateHUF():
	try:
		myCash = float(entry1.get())
	except:
		pass
	else:
		selectedCurrency = combobox1.get()
		rateFx = float(currencies.get(selectedCurrency))
		rateHUF = float(currencies.get('HUF'))
		myHUF = int((myCash/rateFx) * rateHUF)
		label1.config(text = str(myHUF) + ' Ft')


################################################################
#
# A GUI felépítése.
#
################################################################

top = tk.Tk()
top.title('Deviza kalkulátor')

frame1 = tk.LabelFrame(top, text = '')
frame1.pack(fill = 'both', expand = 'yes')

entry1 = tk.Entry(frame1, font = ('', 24), justify = 'right', width = 16)
entry1.grid(column = 1, row = 0, padx = 8, pady = 8)

icon = tk.PhotoImage(file = r"pix/exaile-icon48.png")
button1 = tk.Button(frame1, command = calculateHUF, image = icon)
button1.grid(column = 0, row = 1)

label1 = tk.Label(frame1, anchor = 'e', background = 'white',
                  font = ('', 24), text = '0 Ft', width = 16)
label1.grid(column = 1, row = 1, padx = 8, pady = 8)

label2 = tk.Label(frame1, anchor = 'e', font = ('', 8),
                  text = 'Válasszon devizanemet és adja meg az összeget.',
                  width = 48)
label2.grid(column = 1, row = 2, padx = 8, pady = 8)


################################################################
#
# Az XML letöltése és feldolgozása.
#
# A kódblokk csak akkor fut, ha a letöltés sikeres. A letöltött
# XML-t az urllib és az ElementTree segítségével dolgozza fel.
# Sikertelen letöltés esetén a program a státusz sorban jelzi, a
# Combobox pedig egyetlen, '-' értéket mutat.
#
# A program szűri az adott névtérben a tételeket, mivel lesznek
# számunkra feleslegesek. Ezek 'None'-ként kerülnének a szótárba.
#
# A devizanemek rövidítéseit és az aktuális váltási értékeket
# kulcs és érték formában adja vissza, ezért szótárba teszi.
# 
# url : a cél URL
# document : a megnyitandó XML kezelője
# eurofxref : a megnyitott XML tartalma
# root : az XML tartalma struktúrába szervezve
# cube : ciklusváltozó, végigmegy a megfelelő elemeken
# currencies : szótár a devizanem és keresztref érték párosoknak
# currency : devizanem attribútum
# rate : keresztref érték
#
################################################################

url='https://www.ecb.europa.eu/stats/eurofxref/eurofxref-daily.xml'

try:
	with ureq.urlopen(url) as document:
		eurofxref = document.read()
		root = et.fromstring(eurofxref)
		currencies = {}
		node = './/{http://www.ecb.int/vocabulary/2002-08-01/eurofxref}Cube'
		for cube in root.findall(node):
			currency = cube.attrib.get('currency')
			if str(currency) != 'None':
				rate = cube.attrib.get('rate')
				currencies[currency] = rate
except :
	label2.config(text = 'Sikertelen XML letöltés.')


################################################################
#
# A Combobox elemeinek listáját mindenképp létrehozza. Ha vannak
# valódi deviza adatok azzal, ha nincsenek egy '-' karakterrel
# tölti fel. Ezután elkészíti a Comboboxot, valamint beállítja
# kiválasztottnak a legelső elemet.
#
# comboboxItems	: lista a Combobox elemeinek
# k	: ciklusváltozó. végigmegy a currencies szótár elemein
#
################################################################

comboboxItems = []
try:
	for k in currencies:
		comboboxItems.append(k)
except:
	comboboxItems.append('-')

combobox1 = ttk.Combobox(frame1, font = ('', 24), justify = 'center',
                         values = comboboxItems, width = 5)
combobox1.grid(column = 0, row = 0, padx = 8, pady = 8)

try:
	combobox1.current(0)
except:
	pass

# A fő loop indítása
top.mainloop()

### Script vége. ###
