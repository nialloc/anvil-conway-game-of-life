from ._anvil_designer import Form2Template
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class Form2(Form2Template):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

        self.cols = 32
        self.rows = 32
        self.cell_width = 16
        self.cell_height = 16
        self.board = [0 for x in range(self.cols*self.rows)]
        print('ll')
           
    def button_get_click(self, **event_args):
        """This method is called when the button is clicked"""
        data = anvil.server.call('get_data')
        self.board = data
        self.show_board()
        
    def show_board(self):
        c = self.canvas_1
#         c.background = "#FFF0F0"

        for index,value in enumerate(self.board):

            col = int(index % self.cols)
            row = int(index / self.cols)
            
            x = col * self.cell_width
            y = row * self.cell_height
            width = self.cell_width
            height = self.cell_height
            if value == 1:
#                 c.fill_style("#FF0000")
                c.fill_rect(x, y, width, height)
            else:
#                 c.fill_style("#FFFFFF")
                c.clear_rect(x, y, width, height)
        


