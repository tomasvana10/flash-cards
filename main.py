import tkinter as tk
import tkinter.messagebox
from customtkinter import *
import customtkinter as ctk
from PIL import Image
import os
import random
import json
from time import gmtime, strftime
import numpy as np
import sys
import subprocess
 
class App(ctk.CTk):
    def __init__(self, dim, size):
        super().__init__()
        # Basic specifications
        self.geometry(f"{dim[0]}x{dim[1]}")
        self.maxsize(dim[0], dim[1])
        self.minsize(dim[0], dim[1])
        ctk.set_widget_scaling(size)
        ctk.set_default_color_theme("assets/custom_themes/trojan_blue_theme.json")
        self.title("Flash Cards")

        # Frame for main content
        self.frame = ctk.CTkFrame(self)
        self.frame.pack(expand = 1.0, fill = tk.BOTH)

        # Reference to class methods of FlashCardUtils
        self.flashcards = FlashCardUtils(self)

        self.createContent()
        self.createFileMenu()

    def createContent(self):
        # Title label
        self.titleLabel = ctk.CTkLabel(self.frame, text = "Flash cards", font = ctk.CTkFont(family = "Helvetica", 
                                                                                            size = 20, weight = "bold"))
        self.titleLabel.place(relx = 0.5, rely = 0.1, anchor = "c")

        # Available flash cards + option menu
        self.availableCards = [f for f in os.listdir("flash_sets") if f.endswith(".txt")]
        self.flashOptions = ctk.CTkOptionMenu(self.frame, values = self.availableCards)
        self.flashOptions.set("Your flash card sets")
        self.flashOptions.place(relx = 0.5, rely = 0.235, anchor = "c")

        # Button to open the flash card set
        self.openSetButton = ctk.CTkButton(self.frame, text = "Open the selected set", 
                                           command = self.flashcards.handleSetOpen)
        self.bind("<Return>", lambda event = None: self.openSetButton.invoke())
        self.openSetButton.place(relx = 0.5, rely = 0.335, anchor = "c")

        # Images and their respective widgets
        self.cardsImage = ctk.CTkImage(Image.open("assets/flash_cards_vector.png"), size = (140, 140))
        self.placeholderWidget = ctk.CTkLabel(self.frame, text = "", image = self.cardsImage)
        self.placeholderWidget.place(relx = 0.5, rely = 0.67, anchor = "c")
        
        self.folderImage = ctk.CTkImage(Image.open("assets/open_folder.png"), size = (16, 16))
        self.openFolderButton = ctk.CTkButton(self.frame, text = "", image = self.folderImage, 
                                              command = lambda: self.flashcards.openFolder("/flash_sets"),
                                              width = 16)
        self.openFolderButton.place(relx = 0.825, rely = 0.235, anchor = "c")
        
        self.settingsImage = ctk.CTkImage(Image.open("assets/settings.png"), size = (16, 16))
        self.openSettingsButton = ctk.CTkButton(self.frame, text = "", image = self.settingsImage,
                                                command = self.openSettings, width = 16)
        self.openSettingsButton.place(relx = 0.937, rely = 0.05, anchor = "c")

    def createFileMenu(self):
        self.menuBar = tk.Menu()
        self.config(menu = self.menuBar)

        self.mainCascade = tk.Menu(self.menuBar) 
        self.menuBar.add_cascade(label = "More", menu = self.mainCascade)
        self.mainCascade.add_command(label = "Help", command = self.showHelp)
        self.mainCascade.add_separator()
        self.mainCascade.add_command(label = "Exit", command = self.destroy)

    def openSettings(self):
        self.settings = Settings(self)

    def showHelp(self):
        tk.messagebox.showinfo(title = "Help", 
                               message =    "If you are unsure how to add a flash card, open the current "
                                            "working directory you are running this program in, and make a "
                                            "new file under the \"flash_sets\" folder. Name it whatever you "
                                            "want and add .txt to the end. Then, restart the program and your "
                                            "set will appear.")


class FlashCardUtils:
    def __init__(self, master):
        self.master = master
        
    def handleSetOpen(self):
        # If no set selected
        if self.master.flashOptions.get() == "Your flash card sets":
            tk.messagebox.showerror(title = "Error", message = "Please select a flash card set first")
            return
        
        # If the .txt is empty
        if os.path.getsize(f"flash_sets/{self.master.flashOptions.get()}") <= 0:
            tk.messagebox.showerror(title = "Error", message = "Your flash card set is empty")
            return

        # Ensure the .txt file has a multiple of 2 lines
        if self.readFlashCards(self.master.flashOptions.get()) == "error":
            return
        
        # If the flash card set is valid, a toplevel is created
        newFlashCardInstance = NewFlashCardInstance(self.master, self.master.flashOptions.get(), 
                                                    self.readFlashCards(self.master.flashOptions.get()))
        
    def readFlashCards(self, filename):
        try:
            # Store Q and A pairs as a list of dictionaries
            self.flashCards = []
            with open(f"flash_sets/{filename}", 'r') as f:
                self.lines = f.readlines()

            for i in range(0, len(self.lines), 3):
                self.question = self.lines[i].strip()
                self.answer = self.lines[i + 1].strip()
                self.flashCards.append({'Q': self.question, 'A': self.answer})

            return self.flashCards
        except:
            tk.messagebox.showerror(title = "Error", message = "Ensure your .txt file has a multiple of 2 lines")
            return "error"
    
    def compareSets(self, answer, entry):
        answer = answer.casefold()
        entry = entry.casefold()
        
        # Compare flash card answer to user input using Jaccard Index
        self.answerSet = set(answer)
        self.entrySet = set(entry)
        self.intersection = len(self.answerSet & self.entrySet)
        self.union = len(self.answerSet | self.entrySet)

        return self.intersection / self.union if self.union != 0 else 0

    def openFolder(self, subdir):
        self.folderPath = os.getcwd() + subdir
        if sys.platform == "win32":
            os.startfile(self.folderPath)
        elif sys.platform == "darwin":
            subprocess.call(["open", self.folderPath])
        elif sys.platform == "linux":
            os.system('xdg-open "%s"' % self.folderPath)


class NewFlashCardInstance(ctk.CTkToplevel):
    def __init__(self, master, flashname, flashdata):
        super().__init__(master)

        self.geometry("600x450")
        self.maxsize(600, 450)
        self.minsize(600, 450)
        self.title(flashname)

        self.master = master

        # Save reference to flashname and flashdata
        self.flashName = flashname
        self.flashData = flashdata

        # For main content
        self.frame = ctk.CTkFrame(self)
        self.frame.pack(expand = 1.0, fill = tk.BOTH)

        # Detect user pressing enter and handle it based on if the widget is visible
        self.bind("<Return>", lambda event = None: self.handleEnter())

        self.createContent()

    def createContent(self):
        # Title content
        self.titleLabel = ctk.CTkLabel(self.frame, text = f"Flash card set: {self.flashName.replace('.txt', '')}", 
                                        font = ctk.CTkFont(family = "Helvetica", size = 18, weight = "bold"))
        self.titleLabel.place(relx = 0.5, rely = 0.3, anchor = "c")
        self.questionCount = ctk.CTkLabel(self.frame, text = f"{len(self.flashData)} questions", 
                                        font = ctk.CTkFont(family = "Helvetica", size = 14, slant = "italic"))
        self.questionCount.place(relx = 0.5, rely = 0.37, anchor = "c")

        # Write answer or just cycle through cards
        self.answerOptions = ctk.CTkSegmentedButton(self.frame, values = ["Write answers", "Click through"])
        self.answerOptions.set("Write answers")
        self.answerOptions.place(relx = 0.5, rely = 0.5, anchor = "c")

        # Start button
        self.startButton = ctk.CTkButton(self.frame, text = "Start", command = self.generateFlashCardComponents)
        self.startButton.place(relx = 0.3, rely = 0.65, anchor = "c")

        # Exit button
        self.exitButton = ctk.CTkButton(self.frame, text = "Exit", command = self.destroy)
        self.exitButton.place(relx = 0.7, rely = 0.65, anchor = "c")

    def hideContent(self, cardui):
        if not cardui:
            # Main menu content
            self.titleLabel.place_forget()
            self.questionCount.place_forget()
            self.answerOptions.place_forget()
            self.startButton.place_forget()
            self.exitButton.place_forget()
        else:
            # Flash card content
            self.questionFrame.place_forget()
            self.questionBox.place_forget()
            self.continueButton.place_forget()
            self.scoreLabel.place_forget()
            self.finishedButton.place_forget()
            self.finishedLabel.place_forget()
            self.finalScoreLabel.place_forget()

    def insertText(self, text, qtype):
        self.questionBox.configure(state = "normal")
        self.questionBox.delete("0.0", tk.END)
        if qtype == "q":
            self.questionBox.insert("0.0", f"Question: {text}")
        else:
            self.questionBox.insert("0.0", f"Answer: {text}")
        self.questionBox.configure(state = "disabled")

    def handleEnter(self):
        if self.startButton.winfo_ismapped():
            self.startButton.invoke()
            return
        if self.revealButton.winfo_ismapped(): 
            self.revealButton.invoke()
            return
        if self.continueButton.winfo_ismapped():
            self.continueButton.invoke()
            return
        if self.finishedButton.winfo_ismapped():
            self.finishedButton.invoke()
            return
        if self.confirmAnswerButton.winfo_ismapped():
            self.confirmAnswerButton.invoke()
            return

    def generateFlashCardComponents(self):
        # Run this when user starts practicing the flash cards
        self.hideContent(cardui = False) # Hide main content for this toplevel
        self.flashDataCopy = self.flashData.copy() # Allow multiple retries within a single instance
        self.sessionScores = [] # Store data from all flash card repsonses

        # Question box and frame 
        self.questionFrame = ctk.CTkFrame(self.frame, corner_radius = 10, width = 200, height = 200)
        self.questionBox = ctk.CTkTextbox(self.questionFrame, wrap = "word")
        self.questionBox.configure(state = "disabled")
        
        # Buttons to reveal answer, continue, and confirm you are finished
        self.revealButton = ctk.CTkButton(self.frame, text = "Reveal", command = self.revealAnswer)
        self.continueButton = ctk.CTkButton(self.frame, text = "Continue", command = self.generateQuestion)
        self.finishedButton = ctk.CTkButton(self.frame, text = "Finish", command = self.finish)
        self.confirmAnswerButton = ctk.CTkButton(self.frame, text = "Confirm", command = self.revealAnswer)
        
        # Entry to store the user's answer for the current flash card question
        self.answerEntry = ctk.CTkEntry(self.frame, placeholder_text = "Enter your answer")
        
        # Label to display current score, final score and finishing text
        self.finishedLabel = ctk.CTkLabel(self.frame, text = f"You completed {self.flashName.replace('.txt', '')}!", 
                                          font = ctk.CTkFont(family = "Helvetica", size = 18, weight = "bold"))
        self.scoreLabel = ctk.CTkLabel(self.frame, text = "")
        self.finalScoreLabel = ctk.CTkLabel(self.frame)

        self.generateQuestion()

    def generateQuestion(self):
        # First time loading questions
        if len(self.flashDataCopy) == len(self.flashData):
            self.answerEntry.focus()
                
        # Answered all questions
        if len(self.flashDataCopy) == 0:
            self.hideContent(cardui = True)
            self.updateScoresJSON()
            self.finishedButton.place(relx = 0.5, rely = 0.6, anchor = "c")
            self.finishedLabel.place(relx = 0.5, rely = 0.35, anchor = "c")
            self.finalScoreLabel.place(relx = 0.5, rely = 0.45, anchor = "c")
            self.finalScoreLabel.configure(text = f"Average score is: {int(np.mean([record['score'] for record in self.sessionScores])) * 100}%")
            return

        # Remove possible widgets from the revealed answer
        self.scoreLabel.place_forget()
        self.continueButton.place_forget() 
        
        # Choose random question
        self.randomQuestion = random.choice(self.flashDataCopy)
        self.randomQuestionIndex = self.flashDataCopy.index(self.randomQuestion)

        # Place main question content
        self.questionFrame.place(relx = 0.5, rely = 0.4, anchor = "c")
        self.questionBox.place(relx = 0.5, rely = 0.5, anchor = "c")
        self.insertText(self.randomQuestion["Q"], "q")

        # Allow user to either confirm answer or simply continue 
        if self.answerOptions.get() == "Write answers":
            self.answerEntry.place(relx = 0.5, rely = 0.8, anchor = "c")
            self.confirmAnswerButton.place(relx = 0.5, rely = 0.9, anchor = "c")
        else:
            self.revealButton.place(relx = 0.5, rely = 0.8, anchor = "c")

        # Delete question 
        del self.flashDataCopy[self.randomQuestionIndex]

    def revealAnswer(self):
        # Insert the answer
        self.insertText(self.randomQuestion["A"], "a")
        
        if self.answerOptions.get() == "Write answers":
            # Jaccard's index
            self.score = self.master.flashcards.compareSets(self.randomQuestion["A"], self.answerEntry.get())
            # Log score
            self.appendScore(written = True)

            self.answerEntry.delete(0, tk.END)
            self.confirmAnswerButton.place_forget()
            self.answerEntry.place_forget()
            self.scoreLabel.place(relx = 0.5, rely = 0.8, anchor = "c")
            self.scoreLabel.configure(text = f"Accuracy of answer: {int(self.sessionScores[-1]['score'] * 100)}%")

        else:
            # Log score
            self.appendScore(written = False)
            self.revealButton.place_forget()
        
        # Allow user to continue
        self.continueButton.place(relx = 0.5, rely = 0.9, anchor = "c")

    def appendScore(self, written):
        if written:
            self.sessionScores.append({"set": self.flashName, "question": self.randomQuestion['Q'], 
                            "answer": self.randomQuestion['A'], "userAnswer": self.answerEntry.get(),
                            "score": self.score, "timestamp": str(strftime("%Y-%m-%d %H:%M:%S", gmtime()))})
        else:
            self.sessionScores.append({"set": self.flashName, "question": self.randomQuestion['Q'], 
                                       "answer": self.randomQuestion['A'], "userAnswer": self.answerEntry.get(),
                                       "score": "N/A", "timestamp": str(strftime("%Y-%m-%d %H:%M:%S", gmtime()))})

    def finish(self):
        # After user finishes the set of flash cards
        self.hideContent(cardui = True)
        self.createContent()

    def updateScoresJSON(self):
            if os.path.getsize("scores.json") > 0:
                # Extending with more data
                with open("scores.json", "r") as f:
                    self.currentData = json.load(f)

                self.currentData.extend(self.sessionScores)

                with open("scores.json", "w") as f:
                    json.dump(self.currentData, f, indent = 2)

            else:
                # First-time dumping of data
                with open("scores.json", "w") as f:
                    json.dump(self.sessionScores, f, indent = 2)


class Settings(ctk.CTkToplevel):
    def __init__(self, master):
        super().__init__(master)
        
        self.geometry("300x300")
        self.maxsize(300, 300)
        self.minsize(300, 300)
        self.title("Settings")
        
        self.master = master
        
        

if __name__ == "__main__":
    # Start program
    app = App((400, 450), 1.3)
    app.mainloop()