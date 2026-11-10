import customtkinter as ctk
from theme import(
    CARD_COLOR,ENTRY_COLOR,INACTIVE_COLOR,RED,RED_HOVER
)

class CalculatorPage(ctk.CTkFrame):
    
    def __init__(self, master, on_calculate):
        super().__init__(
            master, corner_radius=12, fg_color=CARD_COLOR
        )
        self.on_calculate = on_calculate

    
    
        #SECTION HEADING
        self.personal_title = ctk.CTkLabel(
            master=self,
            text= "Personal Information",
            font = ("Cascadia Code", 20, "bold")
        )
        self.personal_title.pack(
            anchor="w", padx=20, pady=(20, 10)
        )
        
        #CONTAINER FOR INPUT FIELDS
        self.fields_frame  = ctk.CTkFrame(
            master = self, fg_color="transparent"
        )
        self.fields_frame.pack(
            fill="x", padx=15,pady=(0, 20)
        )
        
        #ALLOWING 3 COLUMNS TO EXPAND EVELY
        self.fields_frame.grid_columnconfigure(
            (0,1,2), weight=1
        )
        #DEFINING INPUT FIELDS
        fields = [
            ("Age", "age", "e.g. 21"),
            ("Weight (kg)", "weight", "e.g. 60"),
            ("Height (cm)", "height", "e.g. 173")
        ]
        self.inputs= {}
        for column, (label_text, key, placeholder) in enumerate(fields):
            label = ctk.CTkLabel(master=self.fields_frame, text=label_text)
            label.grid(
                row=0, column=column, padx=10, pady=(10, 5), sticky="w"
            )
            entry= ctk.CTkEntry(
                master=self.fields_frame, placeholder_text=placeholder,
                height=40, fg_color=ENTRY_COLOR, border_color= "#484850",
                text_color="white", placeholder_text_color="#95959F"
            )
            entry.grid(
                row=1, column=column, padx = 10, sticky="ew"
            )
            self.inputs[key] = entry
        
        #LIFESTYLE AND GOALS SECTION
        self.selection_frame = ctk.CTkFrame(
            master=self, fg_color= "transparent"
        )
        self.selection_frame.pack(
            fill="x", padx=15, pady=(0, 20)
        )
        #CREATE 3 EVENLY SPACED COLUMNS
        self.selection_frame.grid_columnconfigure(
            (0,1,2), weight=1
        )
        
        #DROPWOWN MENU WITH FIELD DEFS
        selection_fields = [
            (
                "Sex (RMR formula)",
                "sex", ["Male", "Female"], "Male"
            ),
            (
                "Activity Level",
                "activity", 
                [
                    "Sedentary",
                    "Lightly Active",
                    "Moderately Active",
                    "Very Active",
                    "Extremely Active"
                ],
                "Moderately Active"
            ),
            (
                "Fitness Goal","goal",
                [
                    "Lose Weight",
                    "Maintain Weight",
                    "Gain Weight"
                ],
                "Maintain Weight"
            )
        ]
        self.selectors = {}
        for column, (label_text, key, values, default) in enumerate(selection_fields):
            
            #FIELD LABEL
            label = ctk.CTkLabel(
                master= self.selection_frame, text=label_text
            )
            label.grid(
                row=0, column=column, padx=10, pady=(10, 5), sticky="w"
            )
            #DROPDOWN MENU
            dropdown = ctk.CTkOptionMenu(
                master= self.selection_frame, values=values,
                height=40, corner_radius=8, fg_color=INACTIVE_COLOR, button_color=RED,
                button_hover_color=RED_HOVER, dropdown_fg_color=CARD_COLOR,
                dropdown_hover_color=RED
            )
            dropdown.grid(
                row=1, column=column, padx=10, sticky="ew"
            )
            #SET INITIAL VALUE
            dropdown.set(default)
            #STORE WIDGET REFERENCE
            self.selectors[key] = dropdown
            
        # CALCULATE BUTTON
        self.calculate_button = ctk.CTkButton(
            master=self,
            text="Calculate Calories",
            height=48,
            corner_radius=8,
            fg_color=RED,
            hover_color=RED_HOVER,
            font=("Cascadia Code", 16, "bold"),
            command=self.submit
        )
        
        self.calculate_button.pack(
            fill="x", padx=25, pady=(0, 25)
        )
    
    
    def submit(self):
        """collect the form data and send it to the appliaction"""
        
        form_data = {
            "age": self.inputs["age"].get(),
            "weight": self.inputs["weight"].get(),
            "height": self.inputs["height"].get(),
            "sex": self.selectors["sex"].get(),
            "activity": self.selectors["activity"].get(),
            "goal":self.selectors["goal"].get()
        }
        
        self.on_calculate(form_data)