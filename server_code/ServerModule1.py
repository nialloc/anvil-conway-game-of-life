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


@anvil.server.callable
def get_data():
    
    cell4 = contract.functions.getCells().call()
    print("cells ", cell4)
    return generate_cells(cell4)

@anvil.server.callable
def step():
    
    private_key = 'c896a57983b43deeb1387dcc567f3c5ec1d955939935c4030da45a3ca8f7140a'
    print('private_key',private_key)

    acct = Account.from_key(private_key)
    caller_address = acct.address

    print('caller_address',caller_address)

    nonce = web3.eth.getTransactionCount(caller_address)
    
    nonce +=1
    
    chainId = 42 #Kovan - 42

    gwei = 1_000_000_000
    gasPrice = 10 * gwei

    caller_balance0 = web3.eth.get_balance(caller_address)

    gasPrice = Web3.toWei(1, 'gwei')

    myblock = contract.functions.getMyBlock().call()

    print('myblock',myblock)
    
    
    # check when the last step was done
    # compare to current block
    # only execute the step if the time is greater than one minute
    myblock = contract.functions.getMyBlock().call()
    current = web3.eth.blockNumber

    GAP = 0 #int(60/4) # Kovan updates every 4 seconds, let's wait for a minute (60)

    target  = myblock + GAP
    print(f"current {current} target {target}")
    
    if current < target :
        print({'code':f'current block is {current}, skipping until block {target}'})    

    txn = contract.functions.step().buildTransaction(
        {
            'chainId' : chainId,
            'nonce': nonce,
            'gasPrice': gasPrice,
        }
    )
    print('txn',txn)

    
    signed_txn = web3.eth.account.sign_transaction(
        txn,
        private_key=private_key
    )

    try: 
        result = web3.eth.sendRawTransaction(signed_txn.rawTransaction)
        print('result',result)
        txn['status'] = 'ok'
    except Exception as e:
        print(type(e))
        print(e)
        txn = {'status':str(e)}

    response = txn

    caller_balance1 = web3.eth.get_balance(caller_address)

    response['block'] = web3.eth.blockNumber
    response['balance_before'] = caller_balance0
    response['balance_after'] = caller_balance1
    response['cost'] = caller_balance0 - caller_balance1
    response['myblock'] = contract.functions.getMyBlock().call()

    return response

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


