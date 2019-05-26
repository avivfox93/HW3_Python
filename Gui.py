import tkinter as tk
import matplotlib.pyplot as plt
import threading
import Words

message = 'Please Enter Char \nand Press Start'


class Gui:
    def __init__(self, tinker, root):
        self.tinker = tinker
        self.top = TopWindow(root)
        self.bottom = BottomWindow(root)

    def show(self):
        self.tinker.mainloop()


def _show_word_count():
    words = Words.word_count()
    plt.bar(words.keys(), words.values())
    plt.show()


class BottomWindow:
    def __init__(self, root):
        self._running = False
        self._frame = tk.Frame(root)
        self._init_bottom()
        self._frame.pack(side=tk.BOTTOM, padx=5, pady=5)
        self._words = None

    def _init_bottom(self):
        self._include = tk.BooleanVar()
        self._word = tk.StringVar()
        self._word.set(message)
        self._character = tk.StringVar()
        self._character.trace('w', callback=lambda *args: self._char_limit())
        self._character_text = tk.Entry(self._frame, width=2, textvariable=self._character)
        self._include_checkbox = tk.Checkbutton(self._frame, text='Include?', variable=self._include)
        self._label = tk.Label(self._frame, textvariable=self._word, height=3, width=15)
        self._start_button = tk.Button(self._frame, text='Start', command=self._start_words)
        self._reset_button = tk.Button(self._frame, text='Reset', command=self._reset_words)
        self._stop_button = tk.Button(self._frame, text='Stop', command=self._stop_words)
        tk.Button(self._frame, text='Show Word Graph', command=_show_word_count).grid(column=2, row=5, padx=5, pady=5)
        self._start_button.grid(column=0, row=4, padx=5, pady=5)
        self._reset_button.grid(column=2, row=4, padx=5, pady=5)
        self._stop_button.grid(column=4, row=4, padx=5, pady=5)
        tk.Label(self._frame, text='Char:').grid(column=2, row=1)
        self._character_text.grid(column=2, row=2, pady=5)
        self._include_checkbox.grid(column=2, row=3)
        self._label.grid(column=2, row=0, padx=5, pady=5)
        self._include.set(True)

    def _char_limit(self):
        if len(self._character.get()) > 0:
            self._character.set(self._character.get()[:1])

    def _reset_words(self):
        self._running = False
        self._words = None
        self._word.set(message)

    def _get_char(self):
        return self._character.get()

    def _update_word(self):
        try:
            word = next(self._words)
            if not self._running:
                return
            self._word.set(word)
        except StopIteration:
            self._running = False
            self._words = None
            return
        self._update_word()

    def _stop_words(self):
        self._running = False

    def _start_words(self):
        if self._running:
            return
        if not self._words:
            if not self._get_char():
                return
            self._words = Words.word_generator(self._get_char(), self._include.get())
        self._running = True
        t = threading.Thread(target=self._update_word)
        t.setDaemon(True)
        t.start()


class TopWindow:
    def __init__(self, root, accounts=None):
        if not accounts:
            accounts = []
        self.accounts = accounts
        self._index = 0
        self._frame = tk.Frame(root)
        self._frame.pack(side=tk.TOP)
        self._init_top()
        self._update()

    def _init_top(self):
        self._account_balance_var = tk.StringVar()
        self._account_name_var = tk.StringVar()
        self._account_num_var = tk.StringVar()
        self._next_button = tk.Button(self._frame, text='Next', command=self.next_account, width=9)
        self._prev_button = tk.Button(self._frame, text='Prev', command=self.prev_account, width=9)
        self._deposit = tk.Button(self._frame, text='Deposit', command=lambda *args: self._deposit_withdrawal_window('Deposit'), width=9)
        self._transfer = tk.Button(self._frame, text='Transfer', command=self._transfer_window, width=9)
        self._withdrawal = tk.Button(self._frame, text='Withdrawal', command=lambda *args:self._deposit_withdrawal_window('Withdrawal'), width=9)
        self._account_name_text = tk.Label(self._frame, textvariable=self._account_name_var)
        self._account_balance_label = tk.Label(self._frame, textvariable=self._account_balance_var)
        self._account_num_label = tk.Label(self._frame, textvariable=self._account_num_var)
        tk.Label(self._frame, text='Name: ').grid(column=2, row=0)
        tk.Label(self._frame, text='Balance: ').grid(column=2, row=1)
        tk.Label(self._frame, text='Num: ').grid(column=2, row=2)
        self._account_name_text.grid(column=3, row=0, padx=5, pady=3)
        self._account_balance_label.grid(column=3, row=1, padx=5, pady=3)
        self._account_num_label.grid(column=3, row=2, padx=5, pady=5)
        self._prev_button.grid(column=0, row=3, padx=5, pady=5)
        self._next_button.grid(column=4, row=3, padx=5, pady=5)
        self._transfer.grid(column=4, row=4, padx=5, pady=5)
        self._deposit.grid(column=2, row=4, padx=5, pady=5, columnspan=2)
        self._withdrawal.grid(column=0, row=4, padx=5, pady=5)

    def _transfer_window(self):
        window = tk.Toplevel(self._frame)
        amount_var = tk.StringVar()
        accounts = tk.Listbox(window, height=3)
        for account in self.accounts:
            if account is not self.accounts[self._index]:
                accounts.insert(tk.END, account)
        amount = tk.Entry(window, textvariable=amount_var)
        tk.Label(window, text='To').pack()
        accounts.pack()
        tk.Label(window, text='Amount').pack()
        amount.pack(pady=5, padx=5)

        def callback():
            alert = tk.Toplevel(window)
            to = None
            for a in self.accounts:
                if a.name == accounts.selection_get():
                    to = a
                    break
            if not to or not amount_var.get().isnumeric():
                tk.Label(alert, text='Illegal input!').pack(pady=5, padx=5)
                return
            if self.accounts[self._index].transfer(int(amount_var.get()), to=to):
                self._update()
                window.destroy()
            else:
                tk.Label(alert, text='insufficient Funds!').pack(pady=5, padx=5)
        tk.Button(window, text='OK', command=callback).pack(pady=5, padx=5)

    def _deposit_withdrawal_window(self, action):
        window = tk.Toplevel(self._frame)
        amount_var = tk.StringVar()
        amount = tk.Entry(window, textvariable=amount_var)
        tk.Label(window, text='Amount').pack()
        amount.pack(pady=5, padx=5)

        def callback():
            if not amount_var.get().isnumeric():
                return
            if action == 'Deposit':
                self.accounts[self._index].deposit(int(amount_var.get()))
                self._update()
                window.destroy()
            elif action == 'Withdrawal':
                if not self.accounts[self._index].withdrawal(int(amount_var.get())):
                    alert = tk.Toplevel(window)
                    tk.Label(alert, text='insufficient Funds!').pack(pady=5, padx=5)
                else:
                    self._update()
                    window.destroy()
        tk.Button(window, text='OK', command=callback).pack(pady=5, padx=5)

    def add_account(self, account):
        self.accounts.append(account)
        self._update()

    def add_accounts(self, accounts):
        self.accounts.extend(accounts)
        self._update()

    def next_account(self):
        self._index += 1
        if self._index >= len(self.accounts):
            self._index = len(self.accounts) - 1
        self._update()

    def prev_account(self):
        self._index -= 1
        if self._index < 0:
            self._index = 0
        self._update()

    def _update(self):
        if len(self.accounts) is 0 or not self.accounts[self._index]:
            return
        self._account_name_var.set(self.accounts[self._index].name)
        self._account_balance_var.set(str(self.accounts[self._index].balance))
        self._account_num_var.set(self.accounts[self._index].num)
