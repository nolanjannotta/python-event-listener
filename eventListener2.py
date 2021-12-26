# import the following dependencies
import json
from web3 import Web3
import asyncio

# add your blockchain connection information
infura_url = ""
web3 = Web3(Web3.HTTPProvider(infura_url))

# get abi
f = open('./ABI/EmitEvent.json')
abi = json.load(f)

# contract instance
Emit_Event_contract = '0x7b9fC3fBE0a4ff099126FcAdA64e70dEc6B4b07B'

contract = web3.eth.contract(address=Emit_Event_contract, abi=abi)


# define function to handle events and print to the console
def handle_event(event):
    
    print(Web3.toJSON(event.args))
    # print(event)
    # and whatever


async def log_loop(filterList, poll_interval):
    while True:
        for NewString in filterList[0].get_new_entries():
            handle_event(NewString)
        for NewNumber in filterList[1].get_new_entries():
            handle_event(NewNumber)
        await asyncio.sleep(poll_interval)




def main():
    
    newNumber_filter = contract.events.NewNumber.createFilter(fromBlock='latest')
    newString_filter = contract.events.NewString.createFilter(fromBlock='latest')
    filterList = [newNumber_filter, newString_filter]
    #block_filter = web3.eth.filter('latest')
    # tx_filter = web3.eth.filter('pending')
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(
            asyncio.gather(
                log_loop(filterList, 2)))
                # log_loop(block_filter, 2),
                # log_loop(tx_filter, 2)))
    finally:
        # close loop to free up system resources
        loop.close()


if __name__ == "__main__":
    main()