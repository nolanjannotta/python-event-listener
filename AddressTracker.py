from web3 import Web3
import time


infura_url_arb_testnet = ""

receiverAddress = ""

targetAddress = ""
_private = ""

web3 = Web3(Web3.HTTPProvider(infura_url_arb_testnet))

class Balance:
    def __init__(self):
        self.balance = web3.eth.get_balance(targetAddress)
        _gas = ((web3.eth.gas_price / 10**9) * 670000 * 10 ** 9)

        if self.balance > _gas:

            print("____________________________________________________________________________")
            print(f"target address has initial balance of: {str(self.balance / 10 **18)}")
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
            print(f"target address funded with: {str(newBalance/ 10 **18)} Eth")
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
    print(f"sent {(_mainBalance - int(_gas)) / 10**18} Eth to {receiverAddress}")
    print(f"target remaining balance: {str(web3.eth.get_balance(targetAddress) / 10**18)}")
    print("____________________________________________________________________________")



def event_loop(poll_interval):
    while True:
        balance.checkChange()
        time.sleep(poll_interval)

def main():
    event_loop(5)


print(f"target address: {targetAddress}")
print(f"receiver address {receiverAddress}")
print("waiting for funding...")


balance = Balance()


if __name__ == "__main__":
    main()