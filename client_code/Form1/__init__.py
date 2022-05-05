from ._anvil_designer import Form1Template
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


import random

class Form1(Form1Template):

    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

        # Any code you write here will run when the form opens.
        self.rows = 32
        self.cols = 32
        self.width = 20
        self.height = 20
        self.reset_board()
        
    def show_board(self):
        c = self.canvas_1
        c.background = "#FFF000"

        for index,value in enumerate(self.board):

            col = int(index % self.cols)
            row = int(index / self.cols)
            
            x = col * self.width
            y = row * self.width
            width = self.width
            height = self.height
            if value == 1:
                c.stroke_style("#FF0000")
                c.fill_rect(x, y, width, height)
            else:
                c.stroke_style("#FFFFFF")
                c.fill_rect(x, y, width, height)
    
    def button_2_click(self, **event_args):
        """This method is called when the button is clicked"""
        self.show_board()

    def button_1_click(self, **event_args):
        """This method is called when the button is clicked"""
        self.reset_board()
        self.show_board()
        
    def reset_board(self):
        self.board = [int(round(random.random())) for x in range(self.rows*self.cols)]
       


