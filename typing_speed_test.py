from tkinter import *
from tkmacosx import Button
from sqlalchemy.orm import declarative_base, Mapped, mapped_column, Session
from sqlalchemy import create_engine, select
window = Tk()
window.title("Typing Speed Test")
window.minsize(width=600, height=700)
bg_color = '#FFF8F0'
bright_br_color = '#C08552'
text_color = '#8C5A3C'
window.config(bg=bg_color)
default_font = ("Arial",26)

base = declarative_base()
#table for the text that we will be rewriting
class PaP_Text(base):
    __tablename__ = "Pride_and_Prejudice"
    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str]
#the current path of the database
engine = create_engine("sqlite:///instance/pnp_text.db")
base.metadata.create_all(engine)
session = Session(engine)
#order by id so we have the right order of the text
pnp_text = select(PaP_Text.text).order_by(PaP_Text.id)
#the outcome comment meaning the text that comments on the result
outcome_comment = {20: "Learn the proper typing technique and practice to improve your speed.", 35: "Better, but still below the average", 50:"That is the average typing speed", 65: "You are above the average!", 80: "You would qualify for any typing job! You are really fast!"}
#the that we are rewriting, each line is added as a separate list elements
pride_and_prejudice = session.execute(pnp_text).scalars().all()
class PNP():
    def __init__(self):
        
        self.time_started = False
        #the text box where we will write our text
        self.text = Text(height=4, width=90, wrap="word", padx=10, pady=10)
        self.text.config(bg='#F9F8F6', fg=text_color, font=("Arial",22), insertbackground=bright_br_color, highlightthickness=2)
        self.text.grid(row=1,column=0)
        # the text number indicating which text we will use to display and rewrite
        self.text_no = 0
        # disable the copy paste to not allow the users to cheat
        for key in ("<Control-c>", "<Control-v>", "<Control-x>", "<Button-3>"):
            self.text.bind(key, lambda e: "break")
        #the count of the words in the already written text
        self.previous_text_count = 0
        #the count of the characters in the already written text
        self.previous_char_count = 0
        # boolean to check if the user just started to type
        self.first_time = True
        # count of the seconds passed
        self.iterations = 5
        #counter to be used for calculating Characters Per Second
        self.counter = 0
        #try again/reset button
        self.try_again_btn = Button(text="Try Again", command=self.reset, bg=bright_br_color, borderless = True)
        self.try_again_btn.config(fg=bg_color, font=("Arial",26, "bold"), state = "disabled")
        self.try_again_btn.grid(row=6,column=0, pady=40)
        self.init_label = Label(text="Start writing the text below", bg=bg_color, bd=0)
        self.init_label.config(font=("Arial", 20, "bold"), bg=bg_color, fg=bright_br_color)
        self.init_label.grid(row=0, column=0, pady=(40, 20))
        self.speed_label = Label(text="Your average speed is 0 WPM", bg=bg_color, bd=0, pady=20)
        self.speed_label.config(font=default_font, bg=bg_color, fg=text_color)
        self.speed_label.grid(row=4, column=0)
        self.cps_label = Label(text="Characters per second: 0", bg=bg_color, bd=0, pady=20)
        self.cps_label.config(font=default_font, bg=bg_color, fg=text_color)
        self.cps_label.grid(row=5, column=0)
        #tag for mistakes
        self.text.tag_config("wrong", foreground="RED")
        self.pap_text = Text(wrap="word", height=6)
        #inserting the text which we will retype in our textbox. we add 1 more text that comes after
        # to let user to see what to type just after he is done with the current text
        self.pap_text.insert("1.0",' '.join(pride_and_prejudice[self.text_no:(self.text_no+2)]))
        self.pap_text.config(font=default_font, state="disabled", bg=bg_color, fg='#4B2E2B', highlightthickness=0)
        self.pap_text.grid(row=2,column=0, padx=60, pady=40)
        self.pap_text.tag_config("current", background="#ffdaa3")
        self.pap_words = pride_and_prejudice[self.text_no].split()
    # reset after the test is done to try again
    def reset(self):
        self.time_started = False
        self.text_no = 0
        self.previous_text_count = 0
        self.previous_char_count = 0
        self.iterations = 5
        self.counter = 0
        self.first_time = True
        self.cps_label.config(text="Characters per second: 0")
        self.speed_label.config(text="Your average speed is 0 WPM")
        self.text.config(state="normal")
        self.text.delete("1.0", "end-1c")
        self.text.after_cancel(self.average_wpm)
        self.text.after_cancel(self.average_cps)
        self.pap_text.config(state="normal") 
        self.pap_text.delete("1.0", "end-1c")
        self.pap_text.insert("1.0", ' '.join(pride_and_prejudice[self.text_no:(self.text_no+2)]))
        self.pap_text.config(state="disabled")
        self.pap_words = pride_and_prejudice[self.text_no].split()  
        self.outcome_label.grid_remove()
        self.try_again_btn.config(state = "disabled")
    #start the timer when user starts to type      
    def start_timer(self, event):
        if not self.time_started:
            #dont include CapsLock, shift or Ctrl as the first key when you start to type
            if not event.keycode in [16,17,18]:
                self.time_started = True
                self.char_per_second()
                self.repeat_task()

    def repeat_task(self):
        final_text = self.text.get("1.0", "end-1c")
        #count the current already typed words + the previous already typed words that are not in the text box
        text_count=len(final_text.split()) + self.previous_text_count
        #skip the first time as there is no text yet written,
        # the key pressed is not counted so you will get 0 as a result
        if self.first_time:
            self.first_time = False
            self.text.after(5000, self.repeat_task)
            return
        #update the speed label and show the average Words Per Minute speed
        self.speed_label.config(text=f"Your average speed is {int(text_count/(self.iterations/60))} WPM")
        #while its not over a minute, keep counting
        if self.iterations < 60:
            self.iterations += 5
            self.average_wpm = self.text.after(5000, self.repeat_task)
        #if its a minute passed, then stop and show the outcome
        # comment with also updated average WPM
        else:
            for value in outcome_comment:
                if value > text_count:
                    self.outcome_label = Label(text=outcome_comment[value], bg=bg_color, bd=0, pady=20)
                    self.outcome_label.config(font=("Arial",30, "bold"), bg=bg_color, fg=bright_br_color)
                    self.outcome_label.grid(row=3,column=0)
                    self.try_again_btn.config(state = "normal")
                    self.text.config(state="disabled")
                    self.time_started = False
                    break
            #although if its 90 or more words per minute,
            # then show this final, best comment about the user
            if text_count >= 90:
                self.outcome_label = Label(text="At this speed, you are probably a gamer, coder, or a genius. That is amazing!", bg=bg_color, bd=0, pady=20)
                self.outcome_label.config(font=("Arial",30, "bold"), bg=bg_color, fg=bright_br_color)
                self.outcome_label.grid(row=3,column=0)
                self.try_again_btn.config(state = "normal")
                self.text.config(state="disabled")
                self.time_started = False

    def char_per_second(self):
        #if time is running, then count and calculate the CPS every 0.1 second
        if self.time_started:
            self.counter += 0.1
            cps = round((len(self.text.get("1.0", "end-1c"))+self.previous_char_count)/self.counter, 1)
            self.cps_label.config(text=f"Characters per second: {cps}")
            self.average_cps = self.text.after(100, self.char_per_second)
    def check_word(self, event):
        self.typed = self.text.get("1.0", "end-1c").split()
        # index of the starting new word that is being retyped
        index = len(self.typed) -1 
        

        self.pap_text.tag_remove("current", "1.0", "end")

        if 0 <= index < len(self.pap_words):
            #find the start and the end of the word of the current word that is being retyped
            start = f"1.{sum(len(w)+1 for w in self.pap_words[:index])}"
            end = f"1.{sum(len(w)+1 for w in self.pap_words[:index+1])-1}"
            self.pap_text.tag_add("current", start, end)

        typing = self.text.get("1.0", "end-1c")
        for i, letter in enumerate(typing):
            #if everything what has top be typed is done
            if i >= len(pride_and_prejudice[self.text_no]):
                #then check if there are no mistakes to allow too continue with typing
                if not self.text.tag_ranges("wrong"):
                    #check the next text
                    self.text_no += 1
                    #count the previous word count
                    self.previous_text_count += len(self.text.get("1.0", "end-1c").split())
                    #count the previous character count
                    self.previous_char_count += len(self.text.get("1.0", "end-1c"))
                    #delete the text from the textbox to start typing the new text 
                    # and to compare it with the shown text that we are rewriting
                    self.text.delete("1.0", "end-1c")
                    self.pap_text.config(state="normal") 
                    # delete the text that we were retyping from 
                    # and insert the new text
                    self.pap_text.delete("1.0", "end-1c")
                    self.pap_text.insert("1.0", ' '.join(pride_and_prejudice[self.text_no:(self.text_no+2)]))
                    self.pap_text.config(state="disabled")
                    self.pap_text.tag_config("current")
                    #assign the new words from the new text to keep the track of the sentences
                    self.pap_words = pride_and_prejudice[self.text_no].split()
                    #and start checking the words to keep the track
                    self.text.bind("<KeyRelease>", pnp.check_word)
                    #break from this for loop with the i, letter
                    break
            #the start and the end of the char
            start = f"1.{i}"
            end = f"1.{i+1}"
            #if the length of textbox typing text is not over the text that we are retyping from
            if i < len(pride_and_prejudice[self.text_no]):
            #if the char is not the same as in the text that we are retyping from
                if letter.lower() != pride_and_prejudice[self.text_no][i].lower():
                    #then add the tag to mark the char as wrong
                    self.text.tag_add("wrong",start,end)

pnp = PNP()
pnp.text.bind("<KeyRelease>", pnp.check_word)
pnp.text.bind("<Key>", pnp.start_timer)

window.mainloop()