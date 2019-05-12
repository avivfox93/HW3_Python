import tkinter as tk
import Bank
import Gui

a = Bank.Account(name='mishu1', balance=1250, num='12345')
b = Bank.Account(name='mishu2', balance=700, num='58304')
c = Bank.Account(name='mishu3', balance=2150, num='10385')
a.deposit(500)

root = tk.Tk()
root.geometry('300x450')
main_gui = Gui.Gui(tk, root=root)
main_gui.top.add_accounts(accounts=[a, b, c])
main_gui.show()
