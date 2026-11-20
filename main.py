from csv import Error
from email.errors import MessageError

import re
from shutil import register_unpack_format
import sqlite3
from database import initialize_database, save_calculation, get_calculations, delete_calculation
import customtkinter as ctk
from tkinter import messagebox
from validation import validate_inputs
from theme import (
    BG_COLOR, SIDEBAR_COLOR, CARD_COLOR, ENTRY_COLOR, RED, RED_HOVER,INACTIVE_COLOR
)
from ui.calculator_page import CalculatorPage
from ui.results_page import ResultsPage
from ui.history_page import HistoryPage
from calculator import calculate_calories, calculate_macros



# setting the apperance of the application
ctk.set_appearance_mode("dark")  
#ctk.set_default_color_theme("blue")

class calorie_wise_app(ctk.CTk):
    
    def delete_saved_calculation(self, record_id):
        """delete a saved calculation after user confirmation"""
        
        #asking for confirmation before deleting
        confirmed = messagebox.askyesno(
            "Delete Calculation",
            f"You sure you wanna delete calculation #{record_id}?\n\n"
        )
        
        if not confirmed:
            return
        
        #DELETE THE RECORD FROM SQLite
        try:
            deleted = delete_calculation(record_id)
            
            if not deleted:
                messagebox.showwarning("Not found", "this calculation no longer exist")
                
            #RELOADING THE HISTORY PAGE
            records = get_calculations()
            self.history_page.show_records(records)
            
            #clearing results if the currently dipslayteed record was deleted
            if deleted and self.displayed_saved_id == record_id:
                self.results_page.clear_results()
                self.latest_calculation = None
                self.displayed_saved_id = None
            
        except sqlite3.Error as e:
            messagebox.showerror(
                "Database error",f"could not update calculation history:\n{e}"
            )
            
    
    
    
    def view_saved_calculation(self, record):
        """display a saved calculation in the results dashboard"""
        
        #update calorie results using stored databaes values
        self.results_page.set_results(
            results=record, activity=record["activity"],
            goal=record["goal"]
        )
        
        #update the saved macro information
        self.results_page.set_macros(macros=record,target_calories=record["target"])
        
        #navigate to the Results page
        self.show_page("Results")
        
        # prevent saving an already saved record again
        self.results_page.save_button.configure(
            state="disabled",text="Already Saved"
        )
    
        self.displayed_saved_id = record["id"]
    
    
    #
    def save_current_calculation(self):
        """save the most recent calculation to SQLite"""
        
        #ensuring a calculation has been performed 
        calculation = getattr(self,"latest_calculation",None)
        
        if calculation is None:
            messagebox.showwarning("No Calculation","Please calculate your calories first")
            return
        
        # attempty to save the calculation
        try:
            record_id = save_calculation(calculation)
        except (sqlite3.Error, KeyError) as error:
            messagebox.showerror("Database Error", f"Could not save calculation:\n{error}")
            return
        
        self.displayed_saved_id = record_id
        
        # prevent saving the same result repeatedly
        self.results_page.save_button.configure(state="disabled",text="Calculation Saved")
        messagebox.showinfo("Success",f"Calculation saved successfully\n Record ID: {record_id}")
        
            
        
    
    
    
    def show_page(self, page):
        #UPDATE THE PAE HEADING
        self.content_title.configure(text=page)
        
        #HIDE ALL PAGES BEFORE DISPLAYING THE SELECTED ONE
        self.calculator_page.pack_forget()
        self.results_page.pack_forget()
        self.history_page.pack_forget()
        
        if page == "Calculator":
            self.description.configure(
                text="Calculate your daily calorie requirements"
            )
            
            self.calculator_page.pack(fill="x", pady=(25,0))
        elif page == "Results":
            self.description.configure(
                text="Your individual daily calorie estimates"
            )
            self.results_page.pack(
                fill="both", expand=True, pady=(25,0)
            )
        elif page == "History":
            self.description.configure(text="Your previous calculations")
            
            # Retriving saved calculations
            try:
                records = get_calculations()
            except sqlite3.Error as e:
                messagebox.showerror("Database Error",
                                     f"Could not load history:\n{e}")
                return
            
            # Generating the history cards
            self.history_page.show_records(records)
            
            # Displaying the history page
            self.history_page.pack(
                fill="both",expand=True, pady=(25,0)
            )
            
            
        #HIGHLIGHT THE SELECTED NAVIGATION BUTTON
        for name, button in self.nav_buttons.items():
            button.configure(
                fg_color=RED if name == page else INACTIVE_COLOR
            )
    
    
    
            
    def validate_form(self, form_data):
        """VALIDATE THE CALCULATOR FORM BEFORE PERFORMING CALCULATIONS"""
        
        #RETRIVE DROPDOWN SELECTIONS FROM THE FORM DATA
        age_text =  form_data["age"]
        weight_text = form_data["weight"]
        height_text = form_data["height"]
        
        try:
            #validate andconvert he values
            age, weight, height = validate_inputs(
                age_text, weight_text, height_text
            )
        except ValueError as e:
            #DISPLAY VALIDATION ERROR
            messagebox.showerror("Invalid input", str(e))
            return
        
        #RETRIVE DROPDOWN SELECTIONS
        sex = form_data["sex"]
        activity = form_data["activity"]
        goal = form_data["goal"]
        
        #PERFORM CALORIE CALCULATIONS
        try:
            results = calculate_calories(
                age=age, weight=weight, height=height,
                sex=sex, activity=activity, goal=goal
            )
            
            macros = calculate_macros(
                target_calories =results["target"],    
                weight =weight, goal=goal
            )
            
            
            
        except ValueError as e:
            messagebox.showerror("Calculation Error", str(e))
            return
        
        #STORE THE MOST RECENT CALCULATION
        self.latest_calculation = {
            "age": age,
            "weight": weight,
            "height": height,
            "sex": sex,
            "activity": activity,
            "goal": goal,
            **results,
            **macros
        }
        
        self.displayed_saved_id = None
        
        #UPDATE THE RESULTS DASHBORAD
        self.results_page.set_results(
            results=results, activity=activity, goal=goal
        )
        
        self.results_page.set_macros(
            macros=macros, target_calories=results["target"]
        )
        
        #AUTOMATICALLY SWITCH TO RESULTS
        self.show_page("Results")
            
            
    #INNININT
    def __init__(self):
        super().__init__()
        self.configure(fg_color= BG_COLOR)

        # configuring the main window
        self.title("Calorie intake calculator")
        self.geometry("1000x700")
        self.minsize(800, 600)
        
        #configuring the main grid layout
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(0, minsize=220)
        self.grid_rowconfigure(0, weight=1)
        
        #SIDEBAR
        self.sidebar = ctk.CTkFrame(
            self,
            width=220,
            corner_radius=0,
            fg_color=SIDEBAR_COLOR
        )
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_propagate(False)
        
        #APPLICATION TITLE
        self.sidebar_title = ctk.CTkLabel(
            self.sidebar, text = "Calorie wise",
            font =("Cascadia Code", 24, "bold")
        )
        self.sidebar_title.pack(pady=(30,40))
        
        #NAVIGATION BUTTONS
        pages = ["Calculator", "Results","History"]
        self.nav_buttons = {}
        
        for page in pages:
            button = ctk.CTkButton(
                self.sidebar, text=page, 
                height=42, corner_radius=8,
                fg_color=RED if page == "Calculator" else INACTIVE_COLOR,
                hover_color=RED_HOVER, text_color="white",
                command = lambda p=page: self.show_page(p)
            )
            button.pack(padx=15, pady=8, fill="x")
            self.nav_buttons[page] = button
        
        
        
        #MAIN CONTENT AREA
        self.content = ctk.CTkFrame(self, fg_color="transparent")
        self.content.grid(
            row=0, column=1, sticky="nsew", padx=30, pady=30
        )
        
        #page heading
        self.content_title = ctk.CTkLabel(
            master=self.content, text="Calculator",
            font=("Cascadia Code", 30, "bold")
        )
        self.content_title.pack(anchor="w", pady=(0, 10))
        
        #PAGE DESCRIPTION
        self.description = ctk.CTkLabel(
            master = self.content,
            text="Calculate your daily calorie requirements", 
            font = ("Cascadia Code", 15)
        )
        self.description.pack(anchor="w", pady=(0, 10))
        
        
        #CALCULATOR PAGE
        self.calculator_page = CalculatorPage(
            master=self.content,
            on_calculate=self.validate_form
        )
        self.calculator_page.pack(fill="x",pady=(25,0))
        
        
        #RESULTS PAGE
        self.results_page = ResultsPage(master=self.content, on_save=self.save_current_calculation)
        
        # History Page
        self.history_page =HistoryPage(
            master=self.content, on_view= self.view_saved_calculation,
            on_delete=self.delete_saved_calculation
        )
        
        self.displayed_saved_id = None
        
        
        
        
        
        
        
        
if __name__ == "__main__":
    initialize_database()
    
    app = calorie_wise_app()
    app.mainloop()
