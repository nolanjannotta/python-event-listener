from web3 import Web3
import json
import time


apiURL = ""
account = "0xc623cAA847a077029624dEc1374a8f8C4d25035d"
contractAddress = "0x4f430Cb75D906EB18E1D4eC6104202237818Bc3C"


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

def handle_event(event):
    receipt = web3.eth.waitForTransactionReceipt(event['transactionHash'])
    result = newString_Event.processReceipt(receipt)
    print(result[0]['args']) 

def event_loop(event_filter, poll_interval):
    while True:
        for event in event_filter.get_new_entries():
            handle_event(event)
            time.sleep(poll_interval)

print("listening for events...")
event_loop(block_filter, 2)