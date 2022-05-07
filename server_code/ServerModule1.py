import anvil.secrets
import anvil.tables as tables
import anvil.tables.query as q
from anvil import URLMedia
from anvil.tables import app_tables
import anvil.server


from web3 import Web3, HTTPProvider
from web3.eth import Account

import json

rows = 32
cols = 32


@anvil.server.callable
def get_data():
    
    print('starting..')
    provider = 'https://mainnet.infura.io/v3/c6b8365838284f7b819a7faa839a2392'
    provider = 'https://kovan.infura.io/v3/c6b8365838284f7b819a7faa839a2392'
    web3 = Web3(HTTPProvider(provider))
    print("web3 version",web3.version)
 
    # do this a a test of connectivity
    print('block', web3.eth.blockNumber)    

    deployed_contract_address = '0x51B92cef4C0847EF552e4129a28d817c26a4A053'

    #compiler_contract_path = 'GameOfLife.json'
    url = anvil.server.get_app_origin() + "/_/theme/GameOfLife.json"
    file_contents = URLMedia(url).get_bytes()
    contract_json = json.loads(file_contents)
    contract_abi = contract_json['abi']

    deployed_contract_address=Web3.toChecksumAddress(deployed_contract_address)
    print('deployed contract address',deployed_contract_address)
    
    contract = web3.eth.contract(
        address=deployed_contract_address, 
        abi=contract_abi,
        )
    
    cell4 = contract.functions.getCells().call()
    print("cells ", cell4)
    
    return generate_cells(cell4)


def generate_cells(cell4):
    cells = [0 for x in range(rows*cols)]
    index = 0
    for row in range(rows):
        for col in range(cols):
            pos = (col + row*cols) % (rows*cols)
            i = int(pos / 256)
            j = pos % 256
            #print(row,col,pos,i,j,cells[i])
            if (cell4[i] >> j) & 0x01:
                cells[index] = 1
            else:
                cells[index] = 0

            index += 1
    return cells
    