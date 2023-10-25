import tkinter as tk
from decimal import *
getcontext().prec = 10

master = tk.Tk()
master.title('EUC')
master.resizable(width=False, height=False)

# --------- #

Hartree_kcalmol = Decimal(627.509)
Hartree_eV = Decimal(27.2116)
cal_J = Decimal(4.184)
eV_nm = Decimal(1239.8)

# --------- #

e1 = tk.Entry(master, font=('Arial', '11'))
e1.grid(row=0, column=0, padx = 1, pady = 1)
l1 = tk.Label(master, text='Hartree', font=('Arial', '11'))
l1.grid(row=0, column=1, padx = 1, pady = 1)
sv1 = tk.StringVar()

e2 = tk.Entry(master, font=('Arial', '11'))
e2.grid(row=1, column=0, padx = 1, pady = 1)
l2 = tk.Label(master, text='kcal/mol', font=('Arial', '11'))
l2.grid(row=1, column=1, padx = 1, pady = 1)
sv2 = tk.StringVar()

e3 = tk.Entry(master, font=('Arial', '11'))
e3.grid(row=2, column=0, padx = 1, pady = 1)
l3 = tk.Label(master, text='kJ/mol', font=('Arial', '11'))
l3.grid(row=2, column=1, padx = 1, pady = 1)
sv3 = tk.StringVar()

e4 = tk.Entry(master, font=('Arial', '11'))
e4.grid(row=3, column=0, padx = 1, pady = 1)
l4 = tk.Label(master, text='eV', font=('Arial', '11'))
l4.grid(row=3, column=1, padx = 1, pady = 1)
sv4 = tk.StringVar()

e5 = tk.Entry(master, font=('Arial', '11'))
e5.grid(row=4, column=0, padx = 1, pady = 1)
l5 = tk.Label(master, text='nm', font=('Arial', '11'))
l5.grid(row=4, column=1, padx = 1, pady = 1)
sv5 = tk.StringVar()

# --------- #

value1 = Decimal('0')
value2 = Decimal('0')
value3 = Decimal('0')
value4 = Decimal('0')
value5 = Decimal('NaN')
sv1.set(str(value1))
sv2.set(str(value2))
sv3.set(str(value3))
sv4.set(str(value4))
sv5.set(str(value5))
e1.config(bg='#FFFFFF')
e2.config(bg='#FFFFFF')
e3.config(bg='#FFFFFF')
e4.config(bg='#FFFFFF')
e5.config(bg='#FFFFFF')
sv1_old = sv1.get()
sv2_old = sv2.get()
sv3_old = sv3.get()
sv4_old = sv4.get()
sv5_old = sv5.get()

# --------- #

def deactivate(self, *args):
    master.focus_set()

def convert1(self, *args):
    global value1, value2, value3, value4, value5
    global sv1_old, sv2_old, sv3_old, sv4_old, sv5_old
    value= sv1.get()
    if sv1_old != value:
        try:
            value1 = Decimal(value)
            value2 = value1 * Hartree_kcalmol
            value3 = value1 * Hartree_kcalmol * cal_J
            value4 = value1 * Hartree_eV
            value5 = eV_nm / value1 / Hartree_eV
            sv1.set(str(value1))
            sv2.set(str(value2))
            sv3.set(str(value3))
            sv4.set(str(value4))
            sv5.set(str(value5))
            e1.config(bg='#D0E5E2')
            e2.config(bg='#FFFFFF')
            e3.config(bg='#FFFFFF')
            e4.config(bg='#FFFFFF')
            e5.config(bg='#FFFFFF')
        except:
            e1.config(bg='#FFD9E8')
    sv1_old = sv1.get()
    sv2_old = sv2.get()
    sv3_old = sv3.get()
    sv4_old = sv4.get()
    sv5_old = sv5.get()

def convert2(self, *args):
    global value1, value2, value3, value4, value5
    global sv1_old, sv2_old, sv3_old, sv4_old, sv5_old
    value= sv2.get()
    if sv2_old != value:
        try:
            value2 = Decimal(value)
            value1 = value2 / Hartree_kcalmol
            value3 = value1 * Hartree_kcalmol * cal_J
            value4 = value1 * Hartree_eV
            value5 = eV_nm / value1 / Hartree_eV
            sv1.set(str(value1))
            sv2.set(str(value2))
            sv3.set(str(value3))
            sv4.set(str(value4))
            sv5.set(str(value5))
            e1.config(bg='#FFFFFF')
            e2.config(bg='#D0E5E2')
            e3.config(bg='#FFFFFF')
            e4.config(bg='#FFFFFF')
            e5.config(bg='#FFFFFF')
        except:
            e2.config(bg='#FFD9E8')
    sv1_old = sv1.get()
    sv2_old = sv2.get()
    sv3_old = sv3.get()
    sv4_old = sv4.get()
    sv5_old = sv5.get()

def convert3(self, *args):
    global value1, value2, value3, value4, value5
    global sv1_old, sv2_old, sv3_old, sv4_old, sv5_old
    value= sv3.get()
    if sv3_old != value:
        try:
            value3 = Decimal(value)
            value1 = value3 / Hartree_kcalmol / cal_J
            value2 = value1 * Hartree_kcalmol
            value4 = value1 * Hartree_eV
            value5 = eV_nm / value1 / Hartree_eV
            sv1.set(str(value1))
            sv2.set(str(value2))
            sv3.set(str(value3))
            sv4.set(str(value4))
            sv5.set(str(value5))
            e1.config(bg='#FFFFFF')
            e2.config(bg='#FFFFFF')
            e3.config(bg='#D0E5E2')
            e4.config(bg='#FFFFFF')
            e5.config(bg='#FFFFFF')
        except:
            e3.config(bg='#FFD9E8')
    sv1_old = sv1.get()
    sv2_old = sv2.get()
    sv3_old = sv3.get()
    sv4_old = sv4.get()
    sv5_old = sv5.get()

def convert4(self, *args):
    global value1, value2, value3, value4, value5
    global sv1_old, sv2_old, sv3_old, sv4_old, sv5_old
    value= sv4.get()
    if sv4_old != value:
        try:
            value4 = Decimal(value)
            value1 = value4 / Hartree_eV
            value2 = value1 * Hartree_kcalmol
            value3 = value1 * Hartree_kcalmol * cal_J
            value5 = eV_nm / value1 / Hartree_eV
            sv1.set(str(value1))
            sv2.set(str(value2))
            sv3.set(str(value3))
            sv4.set(str(value4))
            sv5.set(str(value5))
            e1.config(bg='#FFFFFF')
            e2.config(bg='#FFFFFF')
            e3.config(bg='#FFFFFF')
            e4.config(bg='#D0E5E2')
            e5.config(bg='#FFFFFF')
        except:
            e4.config(bg='#FFD9E8')
    sv1_old = sv1.get()
    sv2_old = sv2.get()
    sv3_old = sv3.get()
    sv4_old = sv4.get()
    sv5_old = sv5.get()

def convert5(self, *args):
    global value1, value2, value3, value4, value5
    global sv1_old, sv2_old, sv3_old, sv4_old, sv5_old
    value= sv5.get()
    if sv5_old != value:
        try:
            value5 = Decimal(value)
            value1 = eV_nm / value5 / Hartree_eV
            value2 = value1 * Hartree_kcalmol
            value3 = value1 * Hartree_kcalmol * cal_J
            value4 = value1 * Hartree_eV
            sv1.set(str(value1))
            sv2.set(str(value2))
            sv3.set(str(value3))
            sv4.set(str(value4))
            sv5.set(str(value5))
            e1.config(bg='#FFFFFF')
            e2.config(bg='#FFFFFF')
            e3.config(bg='#FFFFFF')
            e4.config(bg='#FFFFFF')
            e5.config(bg='#D0E5E2')
        except:
            e5.config(bg='#FFD9E8')
    sv1_old = sv1.get()
    sv2_old = sv2.get()
    sv3_old = sv3.get()
    sv4_old = sv4.get()
    sv5_old = sv5.get()

# --------- #

e1.configure(textvariable=sv1)
e1.bind('<Return>', convert1)
e1.bind('<FocusOut>', convert1)
l1.bind('<ButtonPress>', deactivate)

e2.configure(textvariable=sv2)
e2.bind('<Return>', convert2)
e2.bind('<FocusOut>', convert2)
l2.bind('<ButtonPress>', deactivate)

e3.configure(textvariable=sv3)
e3.bind('<Return>', convert3)
e3.bind('<FocusOut>', convert3)
l3.bind('<ButtonPress>', deactivate)

e4.configure(textvariable=sv4)
e4.bind('<Return>', convert4)
e4.bind('<FocusOut>', convert4)
l4.bind('<ButtonPress>', deactivate)

e5.configure(textvariable=sv5)
e5.bind('<Return>', convert5)
e5.bind('<FocusOut>', convert5)
l5.bind('<ButtonPress>', deactivate)

master.mainloop()