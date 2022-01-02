# import the following dependencies
import json
from web3 import Web3
import asyncio

# add your blockchain connection information
# infura_url_kovan = "https://kovan.infura.io/v3/0469beb7178d48eb9c95721158062ea2"
infura_url_mainnet = "https://mainnet.infura.io/v3/0469beb7178d48eb9c95721158062ea2"

web3 = Web3(Web3.HTTPProvider(infura_url_mainnet))

# get abi
# f = open('./ABI/EmitEvent.json')
# abi = json.load(f)

f = open('./ABI/DaiToken.json')
abi = json.load(f)

# contract instance
Emit_Event_contract = '0x7b9fC3fBE0a4ff099126FcAdA64e70dEc6B4b07B'
Dai_Token_contract = "0x6B175474E89094C44Da98b954EedeAC495271d0F"

# contract = web3.eth.contract(address=Emit_Event_contract, abi=abi)
dai_contract = web3.eth.contract(address = Dai_Token_contract, abi=abi)
# block = web3.eth.get_block('latest')

class Block_Number:

    def __init__(self):
        self.currentBlock = web3.eth.get_block('latest')

    def updateBlock(self):
        self.newBlock = web3.eth.get_block('latest')
        # print(self.newBlock)
        if self.newBlock.number > self.currentBlock.number:
            self.currentBlock = self.newBlock
            print("Current block: #" + str(self.currentBlock.number))

block = Block_Number()


# define function to handle events and print to the console
def handle_event(event):
    block.updateBlock()
    print("from", event.args.src, event.event, "amount:", event.args.wad / 10**18)







async def log_loop(filterList, poll_interval):
    

    while True:
        for Transfer in filterList[0].get_new_entries():
            handle_event(Transfer)
        for Approval in filterList[1].get_new_entries():
            handle_event(Approval)
        await asyncio.sleep(poll_interval)




def main():
    
    Approval_filter = dai_contract.events.Approval.createFilter(fromBlock='latest')
    Transfer_filter = dai_contract.events.Transfer.createFilter(fromBlock='latest')
    filterList = [Approval_filter, Transfer_filter]
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