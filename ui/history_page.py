import enum

import customtkinter as ctk
from theme import CARD_COLOR, RED, RED_HOVER

class HistoryPage(ctk.CTkScrollableFrame):
    
    def __init__(self,master, on_view=None, on_delete=None):
        super().__init__(
            master,fg_color="transparent"
        )
        # callbacks provided by the main application
        self.on_view=on_view
        self.on_delete= on_delete
        
    
        
        
        #container for saved calculation cards
        self.cards_container = ctk.CTkFrame(
            master=self, fg_color="transparent"
        )
        self.cards_container.pack(fill="x")
        
        
    def show_records(self, records):
        """display saved calculations as indivual cards"""
        
        #remove previously displayed cards
        for widget in self.cards_container.winfo_children():
            widget.destroy()
            
        #handle an empty database
        if not records:
            empty_label = ctk.CTkLabel(
                master=self.cards_container,
                text="No saved calculations yet",font=("Cascadia Code", 16)
            )
            empty_label.pack(pady=40)
            return

        #generate 1 card per databaser record
        for record in records:
            
            card = ctk.CTkFrame(
                master=self.cards_container,fg_color= CARD_COLOR, corner_radius=12
            )
            card.pack(fill="x", pady=(0,15))
            
            title=ctk.CTkLabel(
                master=card, text=f"Calculation #{record['id']}",
                font=("Cascadia Code", 17, "bold")
            )
            
            
            title.pack(anchor="w", padx=20, pady=(20,5))
            
            calories= ctk.CTkLabel(
                master=card, text=f"{record['target']:,.0f} kcal/day",
                font=("Cascadia Code",26,"bold"),text_color=RED
            )
            
            calories.pack(anchor="w", padx=20)
            
            goal=ctk.CTkLabel(
                master=card,text=record["goal"]
            )
            
            goal.pack(anchor="w", padx=20,pady=(0,15))
            
            #SAVED DATE
            date_label = ctk.CTkLabel(
                master=card, text=f"Saved: {record['created_at']} UTC",
                text_color='#AFAFB8',font=("Cascadia Code",12)
            )
            date_label.pack(anchor="w",padx=20,pady=(0,15))
            
            
            # MACRO CONTAINER
            macro_frame = ctk.CTkFrame(master=card, fg_color="transparent")
            macro_frame.pack(fill="x",padx=20, pady=(0,20))
            
            # 3 equally sized columns
            macro_frame.grid_columnconfigure((0,1,2), weight=1)
            
            macro_fields = [
                ("Protein","protein"),
                ("Carbs","carbs"),
                ("Fat","fat")
            ]
            
            for column, (name, key) in enumerate(macro_fields):
                
                #container for 1 macro
                macro_item = ctk.CTkFrame(
                    master=macro_frame, fg_color="transparent"
                )
                macro_item.grid(row=0, column=column, sticky="ew")
                
                #MACRO NAME
                name_label = ctk.CTkLabel(
                    master=macro_item, text=name, text_color="#AFAFB8"
                )
                name_label.pack(anchor="w")
                
                #read the stored value
                grams = record[key]
                
                value_text = (
                    f"{grams:.0f} g" if grams is not None else "N/A"
                )
                
                #MACRO AMOUNT
                value_label = ctk.CTkLabel(
                    master=macro_item,text=value_text, 
                    font=("Cascadia Code",16, "bold")
                )
                value_label.pack(anchor="w")
              
              
                
            # ACTION BUTTONS CONTAINER
            buttons_frame = ctk.CTkFrame(
                master=card, fg_color="transparent"
            )
            buttons_frame.pack(
                fill="x",padx=20,pady=(0,20)
            )
                
                
            
            #VIEW DETAILS BUTTON
            view_button = ctk.CTkButton(
                master=buttons_frame,
                text="View Details", height=40,
                corner_radius=8, fg_color=RED, hover_color=RED_HOVER,
                font=("Cascadia Code",13,"bold"),
                command=lambda saved_record=record: self.on_view(saved_record)
            )
            view_button.pack(
                side="left",fill="x", expand=True, padx=(0,10)
            )
            
            #DELETE CALCULATION BUTTONS
            delete_button = ctk.CTkButton(
                master=buttons_frame, text="Delete",
                width=110, height=40, corner_radius=8,
                fg_color="#303036",hover_color="#A61D24",
                text_color="#FF6565",font=("Cascadia Code",13,"bold"),
                command=lambda record_id=record["id"]: self.on_delete(record_id)
            )
            
            delete_button.pack(side="right")
            