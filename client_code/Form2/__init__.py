from ._anvil_designer import Form2Template
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

import anvil.js

from anvil.js.window import document
from anvil.js.window import Web3

class Form2(Form2Template):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

        # Any code you write here will run when the form opens.
        web3 = Web3
        
        print("web3.version",Web3.version)
        print("provider",Web3.givenProvider)
        
        print(web3.modules)
        
        print(web3.keys())
        print(dir(web3))
        address = anvil.js.call_js('InitialiseWeb3')
        print(address)
           