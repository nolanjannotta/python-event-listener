from web3 import Web3
import json
import time


apiURL = "https://kovan.infura.io/v3/0469beb7178d48eb9c95721158062ea2"
account = "0xc623cAA847a077029624dEc1374a8f8C4d25035d"
contractAddress = "0x7b9fC3fBE0a4ff099126FcAdA64e70dEc6B4b07B"


web3 = Web3(Web3.HTTPProvider(apiURL))


f = open('./ABI/EmitEvent.json')
abi = json.load(f)

# contract instance
EmitEvent = web3.eth.contract(address=contractAddress, abi=abi)

# filter for contract address
block_filter = web3.eth.filter({'fromBlock':'latest', 'address':contractAddress})


balance = web3.eth.getBalance(account)


# event object
newString_Event = EmitEvent.events.NewString()
newNumber_Event = EmitEvent.events.NewNumber()

def handle_event(event):
    
    receipt = web3.eth.waitForTransactionReceipt(event['transactionHash'])
    result = newString_Event.processReceipt(receipt)
    # print(result[0]['args']) 
    print(receipt)
    
def event_loop(event_filter, poll_interval):
    while True:
        for event in event_filter.get_new_entries():
            handle_event(event)
            time.sleep(poll_interval)

print("listening for events...")
event_loop(block_filter, 2)