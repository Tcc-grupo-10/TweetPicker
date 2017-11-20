from tkinter import Tk, Frame, Label, Button, LEFT, Entry, DISABLED, Scrollbar, RIGHT, Text, INSERT, END
import _thread
from Main import Main


class Application:
    def __init__(self, master=None):
        self.fontePadrao = ("Arial", "10")
        self.primeiroContainer = Frame(master)
        self.primeiroContainer["pady"] = 10
        self.primeiroContainer.pack(fill="x")

        self.segundoContainer = Frame(master)
        self.segundoContainer["padx"] = 20
        self.segundoContainer.pack()

        self.terceiroContainer = Frame(master)
        self.terceiroContainer["padx"] = 10
        self.terceiroContainer.pack(fill="x")

        self.quartoContainer = Frame(master)
        self.quartoContainer["pady"] = 0
        self.quartoContainer.pack(fill="both")

        self.titulo = Label(self.primeiroContainer, text="Defina um termo para análise:")
        self.titulo["font"] = ("Arial", "20", "bold")
        self.titulo.pack()

        self.termLabel = Label(self.segundoContainer, text="Termo", font=self.fontePadrao)
        self.termLabel.pack(side=LEFT)

        self.term = Entry(self.segundoContainer)
        self.term["width"] = 30
        self.term["font"] = self.fontePadrao
        self.term.pack(side=LEFT)

        self.startButton = Button(self.segundoContainer)
        self.startButton["text"] = "Buscar"
        self.startButton["font"] = ("Calibri", "8")
        self.startButton["width"] = 12
        self.startButton["command"] = self.start
        self.startButton.pack()

        self.logsLabel = Label(self.terceiroContainer, text="Logs", font=self.fontePadrao)
        self.logsLabel["font"] = ("Arial", "15", "bold")
        self.logsLabel.pack(side=LEFT)

        txt_frm = Frame(self.quartoContainer, width=50, height=150)
        txt_frm.pack(fill="x", expand=True)
        txt_frm.grid_propagate(False)
        txt_frm.grid_rowconfigure(0, weight=1)
        txt_frm.grid_columnconfigure(0, weight=1)

        self.txt = Text(txt_frm, borderwidth=3, relief="sunken")
        self.txt.config(font=("consolas", 12), undo=True, wrap='word')
        self.txt.grid(row=0, column=0, sticky="nsew", padx=2, pady=2)

        scrollb = Scrollbar(txt_frm, command=self.txt.yview)
        scrollb.grid(row=0, column=1, sticky='nsew')
        self.txt['yscrollcommand'] = scrollb.set

    def start(self):
        self.startButton.configure(state=DISABLED)
        _thread.start_new_thread(self.start_thead, ())

    def start_thead(self):
        term = self.term.get()
        self.txt.insert(END, "Processo Iniciado:")
        self.txt.see("end")
        main = Main(term, self)
        _thread.start_new_thread(main.run, ())

    def log(self, message):
        self.txt.insert(END, "\n" + message)
        self.txt.see("end")


root = Tk()
root.title("Analisador de Tweets")
root.minsize(width=700, height=300)
root.resizable(width=False, height=False)
Application(root)
root.mainloop()
