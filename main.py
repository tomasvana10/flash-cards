import tkinter as tk
import tkinter.messagebox
from customtkinter import *
import customtkinter as ctk
from PIL import Image
import os
import random

 
class App(ctk.CTk):
    def __init__(self, dim, size):
        super().__init__()
        # Basic specifications
        self.geometry(f"{dim[0]}x{dim[1]}")
        self.maxsize(dim[0], dim[1])
        self.minsize(dim[0], dim[1])
        ctk.set_widget_scaling(size)
        ctk.set_default_color_theme("assets/trojan_blue_theme.json")
        self.title("Flash Cards")

        # Put widgets in here
        self.frame = ctk.CTkFrame(self)
        self.frame.pack(expand = 1.0, fill = tk.BOTH)

        # Reference to class methods of FlashCards
        self.flashcards = FlashCardUtils(self)

        self.createContent()

    def createContent(self):
        # Title label
        self.titleLabel = ctk.CTkLabel(self.frame, text = "Flash cards", font = ctk.CTkFont(family = "Helvetica", 
                                                                                            size = 20))
        self.titleLabel.place(relx = 0.5, rely = 0.1, anchor = "c")

        # Available flash cards + option menu
        self.availableCards = [f for f in os.listdir("flash_sets") if f.endswith(".txt")]
        self.flashOptions = ctk.CTkOptionMenu(self.frame, values = self.availableCards)
        self.flashOptions.set("Your flash card sets")
        self.flashOptions.place(relx = 0.5, rely = 0.235, anchor = "c")

        # Button to open the flash card set
        self.openSetButton = ctk.CTkButton(self.frame, text = "Open the selected set", 
                                            command = self.flashcards.handleSetOpen)
        self.openSetButton.place(relx = 0.5, rely = 0.335, anchor = "c")

        # Vector image for decoration
        self.cardsImage = ctk.CTkImage(Image.open("assets/flash_cards_vector.png"), size = (140, 140))
        self.placeholderWidget = ctk.CTkLabel(self.frame, text = "", image = self.cardsImage)
        self.placeholderWidget.place(relx = 0.5, rely = 0.67, anchor = "c")

        # File menu
        self.menuBar = tk.Menu()
        self.config(menu = self.menuBar)

        self.mainCascade = tk.Menu(self.menuBar) 
        self.menuBar.add_cascade(label = "More", menu = self.mainCascade)
        self.mainCascade.add_command(label = "Help", command = self.showHelp)
        self.mainCascade.add_separator()
        self.mainCascade.add_command(label = "Exit", command = self.destroy)

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
            tk.messagebox.showerror(title = "Error", message = "Ensure your .txt file has a factor of 2 lines")
    
    def compareSets(self, answer, entry):
        # Compare flash card answer to user input using Jaccard Index
        self.answerSet = set(answer)
        self.entrySet = set(entry)
        self.intersection = len(self.answerSet & self.entrySet)
        self.union = len(self.answerSet | self.entrySet)

        return self.intersection / self.union if self.union != 0 else 0


class NewFlashCardInstance(ctk.CTkToplevel):
    def __init__(self, master, flashname, flashdata):
        super().__init__(master)

        self.geometry("600x450")
        self.maxsize(600,450)
        self.minsize(600, 450)
        self.title(flashname)

        self.master = master

        # Save reference to flashname and flashdata
        self.flashName = flashname
        self.flashData = flashdata

        # For main content
        self.frame = ctk.CTkFrame(self)
        self.frame.pack(expand = 1.0, fill = tk.BOTH)

        self.createContent()

    def createContent(self):
        # Title content
        self.titleLabel = ctk.CTkLabel(self.frame, text = f"Flash card set: {self.flashName}", 
                                        font = ctk.CTkFont(family = "Helvetica", size = 18, weight = "bold"))
        self.titleLabel.place(relx = 0.5, rely = 0.3, anchor = "c")
        self.questionCount = ctk.CTkLabel(self.frame, text = f"{len(self.flashData)} questions", 
                                        font = ctk.CTkFont(family = "Helvetica", size = 14, slant = "italic"))
        self.questionCount.place(relx = 0.5, rely = 0.37, anchor = "c")

        # Write answer or just cycle through cards
        self.gameOptions = ctk.CTkSegmentedButton(self.frame, values = ["Write answers", "Do not require answers"])
        self.gameOptions.set("Write answers")
        self.gameOptions.place(relx = 0.5, rely = 0.5, anchor = "c")

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
            self.gameOptions.place_forget()
            self.startButton.place_forget()
            self.exitButton.place_forget()
        else:
            # Flash card content
            self.questionFrame.place_forget()
            self.questionBox.place_forget()
            self.revealButton.place_forget()
            self.continueButton.place_forget()

    def insertText(self, question):
        self.questionBox.configure(state = "normal")
        self.questionBox.delete("0.0", tk.END)
        self.questionBox.insert("0.0", question)
        self.questionBox.configure(state = "disabled")

    def generateFlashCardComponents(self):
        # Run this when user starts practicing the flash cards
        self.hideContent(cardui = False) # Hide main content for this toplevel
        self.flashDataCopy = self.flashData.copy() # Allow multiple retries within a single instance

        # All necessary widgets
        self.questionFrame = ctk.CTkFrame(self.frame, corner_radius = 10, width = 200, height = 200)
        self.questionBox = ctk.CTkTextbox(self.questionFrame, wrap = tk.WORD)
        self.questionBox.configure(state = "disabled")
        self.revealButton = ctk.CTkButton(self.frame, text = "Reveal", command = self.revealAnswer)
        self.continueButton = ctk.CTkButton(self.frame, text = "Continue", command = self.generateQuestion)
        self.finishedButton = ctk.CTkButton(self.frame, text = "Finish", command = self.finish)

        self.generateQuestion()

    def finish(self):
        # After user finishes the set of flash cards
        self.finishedButton.place_forget()
        self.createContent()

    def generateQuestion(self):
        if len(self.flashDataCopy) == 0:
            self.hideContent(cardui = True)
            self.finishedButton.place(relx = 0.5, rely = 0.5, anchor = "c")
            return

        self.continueButton.place_forget() # Remove contiue button and replace it with reveal button
        self.randomQuestion = random.choice(self.flashDataCopy)
        self.randomQuestionIndex = self.flashDataCopy.index(self.randomQuestion)

        self.questionFrame.place(relx = 0.5, rely = 0.4, anchor = "c")
        self.questionBox.place(relx = 0.5, rely = 0.5, anchor = "c")
        self.insertText(self.randomQuestion["Q"])
        self.revealButton.place(relx = 0.5, rely = 0.8, anchor = "c")

        # Delete question 
        del self.flashDataCopy[self.randomQuestionIndex]

    def revealAnswer(self):
        self.insertText(self.randomQuestion["A"])
        self.revealButton.place_forget()
        self.continueButton.place(relx = 0.5, rely = 0.8, anchor = "c")




    

        



        



        





if __name__ == "__main__":
    # Start program
    app = App((400, 450), 1.3)
    app.mainloop()