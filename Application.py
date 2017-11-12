from tkinter import Tk, Frame, Label, Button, LEFT, Entry, DISABLED

import _thread

from Main import Main


class Application:
    def __init__(self, master=None):
        self.fontePadrao = ("Arial", "10")
        self.primeiroContainer = Frame(master)
        self.primeiroContainer["pady"] = 10
        self.primeiroContainer.pack()

        self.segundoContainer = Frame(master)
        self.segundoContainer["padx"] = 20
        self.segundoContainer.pack()

        self.terceiroContainer = Frame(master)
        self.terceiroContainer["padx"] = 20
        self.terceiroContainer.pack()

        self.quartoContainer = Frame(master)
        self.quartoContainer["pady"] = 20
        self.quartoContainer.pack()

        self.titulo = Label(self.primeiroContainer, text="Defina um termo para análise")
        self.titulo["font"] = ("Arial", "10", "bold")
        self.titulo.pack()

        self.termLabel = Label(self.segundoContainer, text="Termo", font=self.fontePadrao)
        self.termLabel.pack(side=LEFT)

        self.term = Entry(self.segundoContainer)
        self.term["width"] = 30
        self.term["font"] = self.fontePadrao
        self.term.pack(side=LEFT)

        self.startButton = Button(self.terceiroContainer)
        self.startButton["text"] = "Buscar"
        self.startButton["font"] = ("Calibri", "8")
        self.startButton["width"] = 12
        self.startButton["command"] = self.start
        self.startButton.pack()

        self.logsLabel = Label(self.terceiroContainer, text="Logs", font=self.fontePadrao)
        self.logsLabel["font"] = ("Arial", "10", "bold")
        self.logsLabel.pack(side=LEFT)

        self.logs = Label(self.quartoContainer, text="", font=self.fontePadrao)
        self.logs.pack(side=LEFT)

    def start(self):
        self.startButton.configure(state=DISABLED)
        term = self.term.get()
        self.log("Processo Iniciado:")
        main = Main(term, self)
        _thread.start_new_thread(main.run, ())

    def log(self, message):
        self.logs["text"] = self.logs["text"] + "\n" + message


root = Tk()
Application(root)
root.mainloop()
