import enum
from pydoc import text
from sqlite3 import SQLITE_IOERR_LOCK

import customtkinter as ctk
from theme import CARD_COLOR, RED

class ResultsPage(ctk.CTkScrollableFrame):
    def __init__(self, master, on_save):
        super().__init__(master, fg_color="transparent")
        self.on_save = on_save

        #DAILY CALORIE TARGET CARD
        self.target_card = ctk.CTkFrame(
            master=self,
            fg_color="#291719", border_width=1, border_color="#793439",
            corner_radius=14
        )
        self.target_card.pack(fill="x", pady=(0,20))
        
        #CARD TITLE
        self.target_title = ctk.CTkLabel(
            master=self.target_card, text="DAILY CALORIE TARGET",
            font=("Cascadia Code", 15, "bold"),
            text_color="#E9B8B8"
        )
        self.target_title.pack(anchor="w", padx=25, pady=(25,5))
        
        #IMPO
        #CALORIE TARGET VALUE
        self.target_value = ctk.CTkLabel(
            master=self.target_card, text="-- kcal/day",
            font=("Cascadia Code", 36, "bold"), text_color="#FF4D4D"
        )
        self.target_value.pack(anchor="w", padx=25, pady=(0,5))
        
        
        #FITNESS GOAL AND ACTIVITY INFORMATION
        self.goal_info = ctk.CTkLabel(
            master=self.target_card,
            text="Complete calc to see results",
            font=("Cascadia Code",13), text_color="#C9A9A9"
        )
        self.goal_info.pack(anchor="w", padx=25, pady=(0,25))
        
        
        #SECONDARY METRICS SECTION
        self.metrics_frame = ctk.CTkFrame(
            master=self, fg_color="transparent"
        )
        self.metrics_frame.pack(
            fill="x", pady=(0,20)
        )
        
        # 2 EQUALLY SIZED COLUMNS
        self.metrics_frame.grid_columnconfigure((0, 1), weight=1)
        metrics =[
            ("Resting Metabolic Rate", "rmr"),
            ("Maintenance Calories", "tdee")
        ]
        self.metric_values = {}
        
        for column, (title, key) in enumerate(metrics):
            
            card = ctk.CTkFrame(
                master=self.metrics_frame, fg_color=CARD_COLOR,
                corner_radius=12
            )
            card.grid(
                row=0, column=column, padx=(0,10) if column == 0 else (10, 0),
                sticky="nsew"
            )
            
            #METRIC TITLE
            label = ctk.CTkLabel(
                master=card, text=title, font=("Cascadia Code", 13),
                text_color="#B9B9C3"
            )
            label.pack(anchor="w", padx=20, pady=(20, 10))
            
            #DYNAMIC METRIC VALUES
            value = ctk.CTkLabel(
                master=card, text="--",
                font=("Cascadia Code", 26, "bold"), text_color="white"
            )
            value.pack(anchor="w", padx=20)
            
            
            #UNITS
            units = ctk.CTkLabel(
                master=card, text="kcal/day", text_color="#B9B9C3"
            )
            units.pack(anchor="w", padx=20, pady=(0, 20))
            self.metric_values[key] = value
            
            
        #CALCULATION DETAILS SECTION
        self.details_card = ctk.CTkFrame(
            master=self, fg_color=CARD_COLOR, corner_radius=12
        )
        self.details_card.pack(fill="x")
        
        #SECTION HEADING
        details_title = ctk.CTkLabel(master=self.details_card,
                                     text="Calculation Details",
                                     font=("Cascadia Code", 18, "bold"))
        details_title.pack(anchor="w", padx=25, pady=(20, 15))
        
        details = [
            ("Activity Level", "activity"),
            ("Activity Multiplier", "multiplier"),
            ("Goal Adjustment", "adjustment")
        ]
        self.detail_values = {}
        for title, key in details:
            
            row = ctk.CTkFrame(
                master=self.details_card,
                fg_color="transparent"
            )
            row.pack(fill="x", padx=25, pady=8)
            
            #LEFT SIDE: DESCRIPTION
            name_label = ctk.CTkLabel(
                master=row, text=title, text_color="#B9B9C3"
            )
            name_label.pack(side="left")
            
            #RIGHT SIDE: VALUE
            value_label = ctk.CTkLabel(
                master=row, text="--", text_color="white"
            )
            value_label.pack(side="right")
            
            self.detail_values[key] = value_label
            
        #MACRO SECTION
        self.macros_frame = ctk.CTkFrame(
            master=self, fg_color=CARD_COLOR, corner_radius=12
        )
        self.macros_frame.pack(fill="x", pady=(20,0))
        
        #SECTION TITLE
        self.macro_title = ctk.CTkLabel(
            master=self.macros_frame,
            text="Macro Breakdown", font=("Cascadia Code",18,"bold")
            
        )
        self.macro_title.pack(
            anchor="w",padx=25,pady=(20,5)
        )
        
        #SECTION DESCRIPTION
        self.macros_description = ctk.CTkLabel(
            master=self.macros_frame,
            text="Personalized daily macro targets",
            text_color="#B9B9C3"
        )
        self.macros_description.pack(
            anchor="w",padx=25,pady=(0,15)
        )
        
        #CONTAINER FOR 3 MACRO CARDS
        self.macro_grid = ctk.CTkFrame(
            master=self.macros_frame, fg_color="transparent"
        )
        self.macro_grid.pack(
            fill="x",padx=20, pady=(0,20)
        )
        self.macro_grid.grid_columnconfigure((0,1,2),weight=1)
        
        #MACRO DEFINITIONS
        macro_fields = [
            ("Protein", "protein", "#E34A4F"),
            ("Carbs", "carbs", "#C13C43"),
            ("Fat", "fat", "#9B3339")
        ]
        
        #STORE REFERENCES TO DYNAMIC WIDGETS
        self.macro_values = {}
        self.macro_percentages = {}
        self.macro_bars = {}
        
        for column, (name, key, color) in enumerate(macro_fields):
            
            card = ctk.CTkFrame(
                master=self.macro_grid, fg_color="#29292F",
                corner_radius=10
            )
            card.grid(
                row=0, column=column, padx=5, sticky="nsew"
            )
            
            title = ctk.CTkLabel(
                master=card, text=name, text_color="#B9B9C3"
            )
            title.pack(
                anchor="w", padx=15, pady=(15,5)
            )
            
            value = ctk.CTkLabel(
                master=card, text="-- g", font=("Cascadia Code",24,"bold")
            )
            value.pack(
                anchor="w",padx=15
            )
            
            percentage = ctk.CTkLabel(
                master=card, text="--% of calories",
                text_color="#B9B9C3"
            )
            percentage.pack(
                anchor="w", padx=15, pady=(0,10)
            )
            
            progress = ctk.CTkProgressBar(
                master=card, height=7,
                fg_color="#39393F", progress_color=color

            )
            progress.pack(
                fill="x", padx=15, pady=(0,15)
            )
            progress.set(0)
            
            self.macro_values[key] = value
            self.macro_percentages[key] = percentage
            self.macro_bars[key] = progress
            
        #SAVING CALCULATION BUTTON
        self.save_button = ctk.CTkButton(
            master=self,text="Save Calculation", font=("Cascadia Code", 16, "bold"),
            height=48,corner_radius=8,fg_color="#A61D24",state="disabled",command=self.on_save
        )
        self.save_button.pack(
            fill="x",pady=(20,25)
        )
            
    
    def clear_results(self):
        """reset the results dashboard to its initial state"""
        #reset the daily calorie target
        self.target_value.configure(text="-- kcal/day")
        self.goal_info.configure(text="Complete a calculation to see your results")
        
        #reset RMR and TDEE
        for label in self.metric_values.values():
            label.configure(text="--")
            
        #reset calculation details
        for label in self.detail_values.values():
            label.configure(text="--")
        
        #reset macros
        for key in self.macro_values:
            self.macro_values[key].configure(text="-- g")
            self.macro_percentages[key].configure(text="--% of calories")
            self.macro_bars[key].set(0)
            
        #disabling saving until another calculation is made
        self.save_button.configure(state="disabled", text="Save Calculation")
        #resotres the dashboard to the state it ad before the user performed and calc
    
    
    
            
    def set_results(self, results, activity, goal):
        """Update dashboard with calculated values"""
        
        #MAIN CALORIE TARGET
        self.target_value.configure(
            text=f'{results["target"]:,.0f} kcal/day'
        )
        
        self.goal_info.configure(
            text=f"{goal} | {activity}"
        )
        
        #RMR AND TDEE
        self.metric_values["rmr"].configure(
            text=f'{results["rmr"]:,.0f}'
        )
        self.metric_values["tdee"].configure(
            text=f'{results["tdee"]:,.0f}'
        )
        
        
        #ACTIVITY INFORMATION
        self.detail_values["activity"].configure(
            text=activity
        )
        
        self.detail_values["multiplier"].configure(
            text=f'{results["activity_factor"]:.3f}x'
        )
        
        #GOAL ADJUSTEMENT PERCENTAGE
        adjustment = round((results["goal_factor"]-1)*100)
        adjustment_text = (
            f"{adjustment:+d}%" if adjustment != 0 else "0%"
        )
        self.detail_values["adjustment"].configure(
            text=adjustment_text
        )
        
        #ENABLE SAVING FOR HTE NEWLY CALCULATED RESULT
        self.save_button.configure(state="normal",text="Save Calculation")
        
        
    def set_macros(self, macros, target_calories):
        """UPDATE THE MCARO DASHBOARD"""
        
        if target_calories <=0:
            raise ValueError("Invalid calorie target")
        
        calorie_factors = {
            "protein": 4,
            "carbs": 4,
            "fat": 9
        }
        
        for key, kcal_per_gram in calorie_factors.items():
            
            grams = macros[key]
            
            #PERCENTAGE OF TOTAL DAILY CALORIES
            fraction = (grams * kcal_per_gram) / target_calories
            
            #DISPLAY RECOMMENDED GRAMS
            self.macro_values[key].configure(
                text=f"{grams:,.0f} g"
            )
            
            #DISPLAY CALORIE PERCENTAGE
            self.macro_percentages[key].configure(
                text=f"{fraction * 100:.0f}% of calories"
            )
            
            #UPDATE THE VISAUL PROGERSS BAR
            self.macro_bars[key].set(
                max(0, min(1, fraction))
            )
            