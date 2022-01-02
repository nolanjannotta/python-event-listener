from web3 import Web3
import time


infura_url_arb_testnet = "https://arb-rinkeby.g.alchemy.com/v2/9aCVAvacX6YjA7kBIVIVJ1iEBTB-criR"

receiverAddress = "0x86449BFCa17bbAe097db76Ff5873F4522738a54B"

targetAddress = "0xCC6ceC5a5A8Cf40F4F605DD0d8c77cFA8A6Ac60c"
_private = "3df016d230d339e1f9cf9ad60fdbad2e86a83d4fdecfa714ae1b879eb3f8770f"

web3 = Web3(Web3.HTTPProvider(infura_url_arb_testnet))

class Balance:

    
    def __init__(self):
        self.balance = web3.eth.get_balance(targetAddress)
        _gas = ((web3.eth.gas_price / 10**9) * 670000 * 10 ** 9)

        if self.balance > _gas:
            print("____________________________________________________________________________")
            print("target address has initial balance of: " + str(self.balance / 10 **18))
            print("withdrawing...")
            createTransaction()
            self.balance = web3.eth.get_balance(targetAddress)
            # print("target's remaining balance: " + str(web3.eth.get_balance(targetAddress) / 10**18)) 
            


    def checkChange(self):
        newBalance = web3.eth.get_balance(targetAddress)
        if newBalance > self.balance:
            print("                        **new activity detected**")
            print("____________________________________________________________________________")
            print("")
            print("target address funded with: " + str(newBalance/ 10 **18) + " Eth")
            print("withdrawing...")
            createTransaction()
            self.balance = web3.eth.get_balance(targetAddress)




def createTransaction():
    _mainBalance = web3.eth.get_balance(targetAddress)
    _gas = ((web3.eth.gas_price / 10**9) * 670000 * 10 ** 9)
    signed_txn = web3.eth.account.signTransaction({
        'from': targetAddress,
        'to': receiverAddress,
        'gas': 670000,
        'gasPrice': web3.eth.gas_price,
        'value': _mainBalance - int(_gas),
        'nonce': web3.eth.getTransactionCount(targetAddress),
    },
    _private)
    
    txn_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
    web3.eth.wait_for_transaction_receipt(txn_hash, timeout=12, poll_latency=0.1)
    print("sent ", (_mainBalance - int(_gas)) / 10**18, "Eth to", receiverAddress)
    print("target remaining balance: " + str(web3.eth.get_balance(targetAddress) / 10**18))
    print("____________________________________________________________________________")

             

    






def event_loop(poll_interval):
    while True:
        balance.checkChange()
        time.sleep(poll_interval)


def main():
    event_loop(5)


print("target address:", targetAddress)
print("receiver address", receiverAddress)
print("waiting for funding...")


balance = Balance()


if __name__ == "__main__":
    
    main()