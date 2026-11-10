import customtkinter as ctk
from theme import CARD_COLOR, RED, RED_HOVER

class HistoryPage(ctk.CTkScrollableFrame):
    
    def __init__(self,master, on_view, on_delete):
        super().__init__(
            master, fg_color="transparent"
        )
        
        
        # callbacks provided by the main application
        self.on_view = on_view
        self.on_delete = on_delete
        
        
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
            