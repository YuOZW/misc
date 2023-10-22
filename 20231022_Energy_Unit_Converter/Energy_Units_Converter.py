import tkinter as tk

master = tk.Tk()
master.title('Energy Units Converter')
master.resizable(width=False, height=False)

# --------- #
Hartree_kcalmol = 627.509
Hartree_eV = 27.2116
cal_J = 4.184
eV_nm = 1239.8

# --------- #

e1 = tk.Entry(master, font=('Arial', '11'))
e1.grid(row=0, column=0, padx = 1, pady = 1)
l1 = tk.Label(master, text='Hartree', font=('Arial', '11'))
l1.grid(row=0, column=1, padx = 1, pady = 1)
sv1 = tk.StringVar()
sv1.set('0.0')

e2 = tk.Entry(master, font=('Arial', '11'))
e2.grid(row=1, column=0, padx = 1, pady = 1)
l2 = tk.Label(master, text='kcal/mol', font=('Arial', '11'))
l2.grid(row=1, column=1, padx = 1, pady = 1)
sv2 = tk.StringVar()
sv2.set('0.0')

e3 = tk.Entry(master, font=('Arial', '11'))
e3.grid(row=2, column=0, padx = 1, pady = 1)
l3 = tk.Label(master, text='kJ/mol', font=('Arial', '11'))
l3.grid(row=2, column=1, padx = 1, pady = 1)
sv3 = tk.StringVar()
sv3.set('0.0')

e4 = tk.Entry(master, font=('Arial', '11'))
e4.grid(row=3, column=0, padx = 1, pady = 1)
l4 = tk.Label(master, text='eV', font=('Arial', '11'))
l4.grid(row=3, column=1, padx = 1, pady = 1)
sv4 = tk.StringVar()
sv4.set('0.0')

e5 = tk.Entry(master, font=('Arial', '11'))
e5.grid(row=4, column=0, padx = 1, pady = 1)
l5 = tk.Label(master, text='nm', font=('Arial', '11'))
l5.grid(row=4, column=1, padx = 1, pady = 1)
sv5 = tk.StringVar()
sv5.set('NaN')

# --------- #

def deactivate(self, *args):
    master.focus_set()

def check_value(value):
    try:
        value = float(value)
    except:
        value = 0.0
    return value

def set_values(value):
    sv1.set(str(round(value, 10)))
    sv2.set(str(round(value * Hartree_kcalmol, 10)))
    sv3.set(str(round(value * Hartree_kcalmol * cal_J, 10)))
    sv4.set(str(round(value * Hartree_eV, 10)))
    if value > 10e-10:
        sv5.set(str(round(eV_nm / value / Hartree_eV, 10)))
    else:
        sv5.set('NaN')

def convert1(self, *args):
    value = check_value(sv1.get())
    set_values(value)

def convert2(self, *args):
    value = check_value(sv2.get()) / Hartree_kcalmol
    set_values(value)

def convert3(self, *args):
    value = check_value(sv3.get()) / Hartree_kcalmol / cal_J
    set_values(value)

def convert4(self, *args):
    value = check_value(sv4.get()) / Hartree_eV
    set_values(value)

def convert5(self, *args):
    value = check_value(sv5.get())
    if value > 10e-10:
        value = eV_nm / value / Hartree_eV
    else:
        value = 0.0
    set_values(value)

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