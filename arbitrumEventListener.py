# import the following dependencies
import json
from web3 import Web3
import asyncio

# add your blockchain connection information
# infura_url_kovan = "https://kovan.infura.io/v3/0469beb7178d48eb9c95721158062ea2"
infura_url_mainnet = "https://mainnet.infura.io/v3/0469beb7178d48eb9c95721158062ea2"
infura_url_arb_testnet = "https://arb-rinkeby.g.alchemy.com/v2/9aCVAvacX6YjA7kBIVIVJ1iEBTB-criR"

web3 = Web3(Web3.HTTPProvider(infura_url_arb_testnet))

# get abi
f = open('./ABI/EmitEvent.json')
abi = json.load(f)

# f = open('./ABI/DaiToken.json')
# abi = json.load(f)

# contract instance
Emit_Event_contract = '0x7b9fC3fBE0a4ff099126FcAdA64e70dEc6B4b07B'
Dai_Token_contract = "0x6B175474E89094C44Da98b954EedeAC495271d0F"
Emit_Event_contract_arbtest = "0x1D4FEc7bA1D6e4b5628EaCEc907f16201Be399F4"


# contract = web3.eth.contract(address=Emit_Event_contract, abi=abi)
dai_contract = web3.eth.contract(address = Emit_Event_contract_arbtest, abi=abi)

block = web3.eth.get_block('latest')


blockNumber = block.number

def handle_block_number(currentNumber):
    newBlock = web3.eth.get_block('latest')
    if newBlock.number != currentNumber:
        blockNumber = newBlock.number
        print(blockNumber)
        return(blockNumber)

# define function to handle events and print to the console
def handle_event(event):
    # print("from", event.args.src, event.event, "amount:", event.args.wad / 10**18)
    # handle_block_number(blockNumber)
    # print(block.number)
    print(Web3.toJSON(event.args))
    # print(event.args.src)
    # and whatever






async def log_loop(filterList, poll_interval):
    

    while True:
        for NewString in filterList[0].get_new_entries():
            handle_event(NewString)
        for NewNumber in filterList[1].get_new_entries():
            handle_event(NewNumber)
        await asyncio.sleep(poll_interval)




def main():
    
    NewString_filter = dai_contract.events.NewString.createFilter(fromBlock='latest')
    NewNumber_filter = dai_contract.events.NewNumber.createFilter(fromBlock='latest')
    filterList = [NewString_filter, NewNumber_filter]
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