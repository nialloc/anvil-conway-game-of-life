from ._anvil_designer import Form1Template
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

import anvil.server

import random

class Form1(Form1Template):

    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

        # Any code you write here will run when the form opens.
        self.rows = 32
        self.cols = 32
        self.width = 16
        self.height = 16
        self.reset_board()
        
    def show_board(self):
        c = self.canvas_1
#         c.background = "#FFF0F0"

        for index,value in enumerate(self.board):

            col = int(index % self.cols)
            row = int(index / self.cols)
            
            x = col * self.width
            y = row * self.width
            width = self.width
            height = self.height
            if value == 1:
#                 c.fill_style("#FF0000")
                c.fill_rect(x, y, width, height)
            else:
#                 c.fill_style("#FFFFFF")
                c.clear_rect(x, y, width, height)
    
    def button_2_click(self, **event_args):
        """This method is called when the button is clicked"""
                
        self.step_board()
        self.show_board()

    def button_1_click(self, **event_args):
        """This method is called when the button is clicked"""
        self.timer_1.interval = 0
        self.reset_board()
        self.show_board()
        
    def reset_board(self):
        self.board = [int(round(random.random())) for x in range(self.rows*self.cols)]
       
    def step_board(self):
        new_board = [0 for x in range(len(self.board))]
        
        def get(pos):
            pos = pos % len(self.board)
            return self.board[pos]
        
        def set(pos,value):
            new_board[pos] = value
        
        for pos,value in enumerate(self.board):

            col = int(pos % self.cols)
            row = int(pos / self.cols)
        
            # ignore the edges for the mo
#             if col == 0 or col == self.cols-1 or row == 0 or row == self.rows-1:
#                 continue
                
            count = 0
            
            cols = self.cols
            rows = self.rows

            # count_neighbours - count the number of cells that are direct neighbours   
            count += get(pos - cols - 1);  #(row-1,col-1); 
            count += get(pos - cols);      #(row-1,col  );
            count += get(pos - cols + 1);  #(row-1,col+1);
                
            count += get(pos - 1); #(row,col-1);
            count += get(pos + 1); #(row,col+1);
            count += get(pos + cols -1); #(row+1,col-1);
            count += get(pos + cols); #(row+1,col  );
            count += get(pos + cols + 1); #(row+1,col+1);
            # if current cell is alive
            if (get(pos) == 1) :
                if (count > 3) :
                    set(pos,0);
                elif (count == 2 or count == 3) :
                    set(pos,1);
                elif (count < 2) :
                    set(pos,0);
            else: #// dead cell
                if (count == 3) :
                    set(pos,1);
                
        self.board = new_board    

    def timer_1_tick(self, **event_args):
        """This method is called Every [interval] seconds. Does not trigger if [interval] is 0."""
        self.step_board()
        self.show_board()

    def button_stop_click(self, **event_args):
        """This method is called when the button is clicked"""
        self.timer_1.interval = 0

    def button_start_click(self, **event_args):
        """This method is called when the button is clicked"""
        self.timer_1.interval = 0.1



