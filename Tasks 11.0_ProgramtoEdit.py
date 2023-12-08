
import tkinter as tk
from tkinter import ttk
from tkinter import simpledialog
from tkinter.messagebox import askokcancel, showinfo, WARNING
import sqlite3

class Database():
    
    filename = "QuizData.db"
    def __init__(self):
        self.conn = None

    def connect(self):
        self.conn = sqlite3.connect(self.filename)



class QuestionBanks(Database):
    def __init__(self):
        super().__init__()
        self.getQuestionBanks()

    def getQuestionBanks(self):
        self.connect()
        self.questionBanks = self.conn.execute("Select * from bank").fetchall()
        self.conn.close()
        return self.questionBanks

    def add(self,description):
        self.connect()


    def delBnk(self, bankNo):
        pass

    def updateBnk(self, bankID, description):
        pass


# class Questions
# inherit from main connection
class Questions(Database):
    # initialise from bank no
    def __init__(self, bankNo):
        super().__init__()
        self.bankNo = bankNo

    def get_questions(self):
        self.connect()
        sql = """
               SELECT questionID, question 
               FROM questions
               WHERE bankNo = ? ORDER BY questionID
              """
        questions = self.conn.execute(sql,[self.bankNo] ).fetchall()
        self.conn.close()
        return questions

    def get_total(self):
        return len(self.get_questions())


    def add_question(self, bankNo):
        # re-open database

        # increment using  last max ID number in records

        # insert record

        # update question list
        pass


    def save_question(self, recordNo, question):

        # update_record

        # refresh internal List
        pass

    def del_question(self,recordNo):
        questionID = self.get_questions()[recordNo - 1][0]
        # SQL to delete record from database -


# class Answers
class Answers(Database):
    # initialise from question ID
    def __init__(self, questionID):
        super().__init__()
        self.questionID = questionID

    def getAnswers(self):
        self.connect()
        sql = """
               Select answerId, answer, correct 
               FROM questionAnswers   
               WHERE questionID = ? 
              """
        questAnswers = self.conn.execute(sql, [self.questionID]).fetchall()
        self.conn.close()
        return questAnswers

    def delAnswers(self, questionID):
        self.connect()
        sql = """ 
               DELETE FROM questionAnswers 
               WHERE questionID = ? 
              """
        self.conn.execute(sql, [questionID])
        self.conn.commit()

    def delAnswer(self, answerID):
        self.connect()
        sql = """
               DELETE FROM questionAnswers 
               WHERE answerID = ? 
              """
        self.conn.execute(sql, [answerID])
        self.conn.commit()


    def insAnswer(self, ansText, correct):
        self.connect()
        sql = """
               SELECT MAX(answerID) AS newID 
               FROM questionAnswers
              """
        answerID = self.conn.execute(sql).fetchone()[0] + 1

        sql = """ 
               INSERT INTO questionAnswers  
               VALUES (?,?,?,?)
              """
        self.conn.execute(sql, [answerID, self.questionID, ansText, correct])
        self.conn.commit()

    def updateAnswer(self, answerID, answerText, correct):
        self.connect()
        sql = """ 
               UPDATE questionAnswers 
               SET answer = ?, correct = ? 
               WHERE answerID = ? 
              """
        self.conn.execute(sql, [answerText, correct, answerID])
        self.conn.commit()


class Answers_window(tk.Toplevel):
    def __init__(self, answersObject, treeAnswers, action):
        super().__init__()
        self.answers = answersObject
        self.treeAnswers = treeAnswers
        self.selected = treeAnswers.index(treeAnswers.selection())

        # initialise windows, widgets and events
        self.geometry("350x150+350+300")
        self.title("Possible Answer")
        self.resizable(False, False)
        self.grab_set()
        self.add_widgets(action)

    def insertAnswer(self):
        pass


    def updateAnswer(self):
        pass

    def cancel(self):
        self.destroy()

    def add_widgets(self, action):

        self.columnconfigure(1, weight=3)
        # text & correct
        self.frmtxtEntry = tk.Frame(self, padx=20, pady=20)
        self.frmtxtEntry.grid(row=0, column=1)
        self.frmDialogueBtns = tk.Frame(self, padx=10)
        self.frmDialogueBtns.grid(row=1, column=1)
        # used for checkbox
        self.correct = tk.IntVar()
        # if new button was added then enter details
        # call insertAnswer
        if action == "add":
            entryText = "Add possible answer here"
            self.ansOK = tk.Button(self.frmDialogueBtns, text="OK", command=self.insertAnswer)
            self.correct.set(0)
        # edit button selected
        # call updateAnswer
        elif action == "edt":
            answersList = self.answers.getAnswers()
            entryText = answersList[self.selected][1]
            self.ansOK = tk.Button(self.frmDialogueBtns, text="OK", command=self.updateAnswer)
            correct_value = self.answers.getAnswers()[self.selected][2]
            self.correct.set(correct_value)

        self.txtAnswer = tk.Text(self.frmtxtEntry, width=40, height=3, font=("Arial", 10))
        self.txtAnswer.insert("1.0", entryText)
        self.txtAnswer.grid(row=0, column = 0, sticky="N" )
        self.chkCorrect = tk.Checkbutton(self.frmtxtEntry, text="Correct?", variable = self.correct, onvalue=1, offvalue=0)
        self.ansCancel = tk.Button(self.frmDialogueBtns, text="Cancel", command= self.cancel)
        self.ansCancel.grid(row=2, column=2)
        self.ansOK.grid(row=2, column=1)
        self.chkCorrect.grid(row=1, column=0, padx=20)


# class display bank questions
# inherit from Toplevel class
class Questions_window(tk.Toplevel):
    def __init__(self, bankNo):
        # initialise from Toplevel
        super().__init__()

        # set record and bank number
        self.recordNo = 1
        self.bankNo = bankNo

        # initialise windows, widgets and events
        self.geometry("650x350+350+300")
        self.title("Questions")
        self.resizable(True, True)
        self.grab_set()
        self.initialise_grid(4,4)
        self.add_widgts()

        # instantiate questions, using bankNo selected
        self.questions = Questions(self.bankNo)
        self.display_question()

    def display_question(self):
        # clear textbox
        self.txtQuestion.delete(1.0, tk.END)
        # only display question if there are questions
        if self.questions.get_questions():
            self.txtQuestion.config(state="normal")
            self.lblQuestionno.config(text="Question No: " + str(self.recordNo))
            self.txtQuestion.insert("1.0", self.questions.get_questions()[self.recordNo - 1][1])
            self.display_answers()
        else:
            self.lblQuestionno.config(text="No Questions")
            self.txtQuestion.insert("1.0", "Need to click ADD as no questions")
            # disable for entry
            self.txtQuestion.config(state="disabled")

    def display_answers(self):
        pass

    def initialise_grid(self,col_size, row_size):
        for col in range (col_size):
            self.rowconfigure(col, weight=1)
        for row in range (row_size):
            self.columnconfigure(row, weight=1)

    def first(self):
        # goto first record in list
        pass

    def previous(self):
        # check if there is a previous record
        pass

    def next(self):
        # Check if not at end of records
        pass

    def last(self):
        # set record no to last record in list
        self.recordNo = len(self.questions.get_questions())
        self.display_question()


    def add(self):
        # increment recordNo from last record and clear textbox
        # create new question, insert into database
        # refresh record
        pass

    def delete(self):
        # check if any questions to delete
        if self.questions.get_questions():
            # confirm deletion

                # del question  ## for Answers Tasks and question Answers
                # get question ID from questions list

                # if last record then change record no to previous
                # get total number of questions, before deleting records.
                # delete record
                # was it at last record? If so, go to previous

                # update record to display (one in front or previous)
                self.display_question()
        else:
            tk.messagebox.showwarning(message="No questions to delete!")


    def save(self):
        pass

    def ansAdd(self):
        pass

    def ansDel(self):
        pass

    def ansEdtFunction(self,event=None):
        pass

    def add_widgts(self):
        # navigation button frame
        self.frmNavigation =  tk.Frame(self, padx= 20)
        self.frmNavigation.grid(row=2, column=0)
        self.first = tk.Button(self.frmNavigation, text="<<", command=self.first)
        self.first.grid(row=0, column=0)
        self.previous = tk.Button(self.frmNavigation, text="<", command=self.previous)
        self.previous.grid(row=0, column=1)
        self.next = tk.Button(self.frmNavigation,text=">", command=self.next)
        self.next.grid(row=0, column=2)
        self.last = tk.Button(self.frmNavigation, text=">>", command=self.last)
        self.last.grid(row=0, column=3)
        self.add = tk.Button(self.frmNavigation, text="Add", command=self.add)
        self.add.grid(row=0, column=4)
        self.delete = tk.Button(self.frmNavigation, text="Del", command=self.delete)
        self.delete.grid(row=0, column=5)
        self.delete = tk.Button(self.frmNavigation, text="Save", command=self.save)
        self.delete.grid(row=0, column=6)
        # Answers frame + buttons:

        #labels and text box
        self.questionFrame = tk.Frame(self, padx=20)
        self.questionFrame.grid(row=0, column = 0)
        self.lblQuestionno = tk.Label(self.questionFrame, font= ("Arial",12))
        self.lblAnswers = tk.Label(self.questionFrame, text = "Answers", font=("Arial", 12))
        self.txtQuestion = tk.Text(self.questionFrame, width= 40, height=10, font = ("Arial",10))
        self.lblQuestionno.grid(row=0, column=0, sticky="W")
        self.txtQuestion.grid(row=1, column=0)
        self.lblAnswers.grid(row=0, column=1)

        #answers
        columns = ("description", "correct")
        self.treeAnswers = ttk.Treeview(self.questionFrame, columns=columns, show="headings", height=7)
        self.treeAnswers.heading("description", text="Description")
        self.treeAnswers.heading("correct", text="Correct?")
        self.treeAnswers.column("description", width=200, stretch=tk.NO)
        self.treeAnswers.column("correct", width=60, stretch=tk.NO)
        self.treeAnswers.grid(row=1, column=1, padx = 30)
        # allow double click on listbox
        self.treeAnswers.bind('<Double-Button-1>', self.ansEdtFunction)

class Main(tk.Tk):
    # Create main Window on initialisation
    def __init__ (self):
        super().__init__()
        # initialise window
        self.title("Quiz Program")
        self.geometry('600x400')
        self.initialise_grid(3,3)

        # instantiate question Banks
        self.questionBanks = QuestionBanks()

        # add remaning window elements
        self.widgets()
        self.buttons()
        self.binding_events()

    def initialise_grid(self,col_size, row_size):
        for col in range (col_size):
            self.rowconfigure(col, weight=1)
        for row in range (row_size):
            self.columnconfigure(row, weight=1)

    def check_bank_selected(self):
        select = False
        if self.treeBank.selection():
            select = True
        else:
           a =  tk.messagebox.showerror(title="error", message="No bank selected")
        return select

    def viewQuestions(self, event):

        if self.treeBank.selection():
            selected_bank = self.treeBank.selection()[0] 
            bank_details = self.treeBank.item(selected_bank)['values']
            bank_id = bank_details[0]
            question_window = Questions_window(bank_id)
            question_window.grab_set()
        else:
            tk.messagebox.showwarning("Warning", "Please select a bank to view questions.")




    def binding_events(self):
        # add events to objects
        # allow double click on listbox
        self.treeBank.bind('<Double-Button-1>', self.viewQuestions)

    def populate_bankTree(self):
        # clear tree / listbox
        self.treeBank.delete(*self.treeBank.get_children())
        # add to Tree (Listbox) by iterating through records
        for record in self.questionBanks.getQuestionBanks():
            self.treeBank.insert('', tk.END, values =record )


    def addBank(self):

        description = simpledialog.askstring("New Bank", "Enter new bank description")
        print(description)
        if description:
            conn = sqlite3.connect('QuizData.db')
            cursor = conn.cursor()
            cursor.execute("INSERT INTO bank (description) VALUES(?)", (description,))
            conn.commit()
            conn.close()

            self.populate_bankTree()  

    def delBank(self):
            selected_bank = self.treeBank.selection()[0]
            bank_details = self.treeBank.item(selected_bank)['values']
            bank_id = bank_details[0] 
            if askokcancel("Delete", "Are you sure you want to delete this bank?"):
                conn = sqlite3.connect('QuizData.db')
                cursor = conn.cursor()
                cursor.execute("DELETE FROM bank WHERE id = ? ", (bank_id,))
                conn.commit()
                conn.close()
               
                self.populate_bankTree()  
        else:
            tk.messagebox.showwarning("Warning", "Please select a bank to delete.")


    def edtBank(self):
      
        if self.treeBank.selection():
            selected_bank = self.treeBank.selection()[0]
            bank_details = self.treeBank.item(selected_bank)['values']
            bank_id = bank_details[0]
            description = bank_details[1]  

            
            new_description = simpledialog.askstring("Edit Bank", "Edit bank description", initialvalue=description)
            if new_description and new_description != description:
                self.questionBanks.updateBnk(bank_id, new_description)
                self.populate_bankTree()
                conn = sqlite3.connect('QuizData.db')
                cursor = conn.cursor()
                cursor.execute("INSERT FROM bank WHERE id = ? ", (new_description, bank_id,))
                conn.commit()
                conn.close()
               
                self.populate_bankTree()
        else:
            tk.messagebox.showwarning("Warning", "Please select a bank to edit.")

            

    def buttons(self):
        self.frame_buttons = tk.Frame(self, padx= 20)
        self.frame_buttons.grid(row=2, column=1)
        self.view_questions = tk.Button (self.frame_buttons, text="View", command=lambda: self.viewQuestions(0))
        self.view_questions.grid(row=0,column=0)
        self.add_bank = tk.Button (self.frame_buttons, text="Add", command=self.addBank)
        self.add_bank.grid(row=0,column= 1)
        self.del_bank = tk.Button(self.frame_buttons, text="Del", command=self.delBank)
        self.del_bank.grid(row=0,column = 2)
        self.edt_bank = tk.Button(self.frame_buttons, text="Edt", command=self.edtBank)
        self.edt_bank.grid(row=0, column=3)

    def widgets(self):
        # label heading
        self.lblQuestionBank = tk.Label(self, text="Question Bank", font= ("Arial",25) )
        self.lblQuestionBank.grid(row=0, column=0, columnspan=3)

        # treeview
        columns = ("bankNo", "description")
        self.treeBank = ttk.Treeview(self, columns = columns, show="headings")
        self.treeBank.heading ("bankNo", text="Bank No")
        self.treeBank.heading ("description", text ="Description")
        self.treeBank.column("bankNo", width=80, stretch=tk.NO)
        self.treeBank.column("description", width=400, stretch=tk.NO)
        self.treeBank.grid(row = 1, column= 0, columnspan=3)
        self.populate_bankTree()

# Complete program as of 27/12/22
# by G. Bradshaw
# call loop method to run program
# continually checking for events

quiz_prog = Main()
quiz_prog.mainloop()






