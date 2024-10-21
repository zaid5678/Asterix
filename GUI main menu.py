from tkinter import *
import os

class Window(Frame):

    def __init__(self, master = None):

        Frame.__init__(self,master)

        self.master = master

        self.init_window()

    def init_window(self):

        self.master.title("Asterix")

        self.pack(fill=BOTH, expand=1)

        quitButton = Button(self, text="Exit program", command=self.clientExit)

        quitButton.place(x=160, y=200)

        viewLeaderBoardButton = Button(self, text="View leaderboard", command=self.recieveScores)

        viewLeaderBoardButton.place(x=145, y=150)

        startButton = Button(self, text="Start game", command=self.startGame)

        startButton.place(x=160, y=100)
        
    def clientExit(self):
        exit()

    def startGame(self):
        import Main_project.py

    def recieveScores(self):
        from AllMatrixAndVectorOperations import SortAndSearch
        S = SortAndSearch()
        o = open("AllScores.txt", "r")
        print(S.msort(o))

root = Tk()
root.geometry("400x300")

app = Window(root)

root.mainloop()
