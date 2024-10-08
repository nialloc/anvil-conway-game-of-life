from ._anvil_designer import Form1Template
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server

import random
import time

class Form1(Form1Template):

    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

        # Any code you write here will run when the form opens.
        self.rows = 32
        self.cols = 32
        self.cell_width = 12
        self.cell_height = 12
        self.reset_board()
        
        button_width = 100
        self.button_reset.width = button_width
        self.button_start.width = button_width
        self.button_stop.width = button_width
        self.button_step.width = button_width
        

       
        
    def show_board(self):
        c = self.canvas_1
#         c.background = "#FFF0F0"

        av = 0
        if self.stepCount !=  0 :
            av = int(self.totalTime / self.stepCount)
            
        Debug = True
        if Debug:
            text = f"Step Count: {self.stepCount} time taken: {self.timeTaken} ms Average: {av}"
        else:
            text = f"Step Count: {self.stepCount}"
        
        self.label_stepCount.text = text
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
    
    def button_step_click(self, **event_args):
        self.step_board()
        self.show_board()

    def button_reset_click(self, **event_args):
        self.reset_board()
        self.show_board()
        
    def reset_board(self):
        self.board = [int(round(random.random())) for x in range(self.rows*self.cols)]
        self.timer_1.interval = 0
        
        self.stepCount = 0 # how many steps have we done?
        self.timeTaken = 0 # time in milliseconds taken per step
        self.totalTime = 0 # total time taken
        
        
    def get(self,pos):
        pos = pos % len(self.board)
        return self.board[pos]
        
    def set(self,pos,value):
        self.new_board[pos] = value
            
    def step_board(self):
        
        t0 = time.time()
        
        self.new_board = [0 for x in range(len(self.board))]
        
        self.stepCount += 1
        
        for pos,value in enumerate(self.board):

            col = int(pos % self.cols)
            row = int(pos / self.cols)
        
            count = 0
            
            cols = self.cols
            rows = self.rows

            get = self.get
            set = self.set
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
                
        self.board = self.new_board    
        t1 = time.time()
        
        self.timeTaken = int(1000*(t1-t0))  # time in milliseconds
        self.totalTime += self.timeTaken
        

    def timer_1_tick(self, **event_args):
        self.step_board()
        self.show_board()

    def button_stop_click(self, **event_args):

        self.timer_1.interval = 0

    def button_start_click(self, **event_args):
        self.timer_1.interval = 0.1

    def form_show(self, **event_args):
        self.show_board()

    def canvas_1_mouse_down(self, x, y, button, **event_args):
        #print(x,y,button, event_args)
        row = int(y / self.cell_width)
        col = int(x / self.cell_height)
        
        # ignore off board clicks
        if row < 0 or row >= self.rows :
            return
        if col < 0 or col >= self.cols:
            return
        pos = col + row * self.cols
        # flip it
        self.board[pos] = not self.board[pos]
        #print(f"row {row} col {col} pos {pos} cell {self.board[pos]}")
        self.show_board()

