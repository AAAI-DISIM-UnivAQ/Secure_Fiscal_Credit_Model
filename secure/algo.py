import base64
import json
from typing import cast

from algosdk import account, error, mnemonic
from algosdk.transaction import PaymentTxn
from algosdk.v2client import algod


# Function to generate an account
def generate_algorand_keypair():
    private_key, address = account.generate_account()
    print(f"My Address: {address}")
    print(f"My Private Key: {private_key}")
    print(f"My Passphrase: {mnemonic.from_private_key(private_key)}" + "\n")


# Function to confirm pending transaction and manage errors
def wait_for_confirmation(
    algod_client: algod.AlgodClient, txid: str, wait_rounds: int = 0, **kwargs
):
    """
    Block until a pending transaction is confirmed by the network.
    Args:
        algod_client (algod.AlgodClient): Instance of the `algod` client
        txid (str): transaction ID
        wait_rounds (int, optional): The number of rounds to block for before
            exiting with an Exception. If not supplied, this will be 1000.
    """
    algod.AlgodClient._assert_json_response(kwargs, "wait_for_confirmation")

    last_round = cast(int, cast(dict, algod_client.status())["last-round"])
    current_round = last_round + 1

    if wait_rounds == 0:
        wait_rounds = 1000

    while True:
        # Check that the `wait_rounds` has not passed
        if current_round > last_round + wait_rounds:
            raise error.ConfirmationTimeoutError(
                f"Wait for transaction id {txid} timed out"
            )

        try:
            tx_info = cast(dict, algod_client.pending_transaction_info(txid, **kwargs))

            # The transaction has been rejected
            if "pool-error" in tx_info and len(tx_info["pool-error"]) != 0:
                raise error.TransactionRejectedError(
                    "Transaction rejected: " + tx_info["pool-error"]
                )

            # The transaction has been confirmed
            if "confirmed-round" in tx_info and tx_info["confirmed-round"] != 0:
                return tx_info
        except error.AlgodHTTPError:
            # Ignore HTTP errors from pending_transaction_info, since it may return 404 if the algod
            # instance is behind a load balancer and the request goes to a different algod than the
            # one we submitted the transaction to
            pass

        # Wait until the block for the `current_round` is confirmed
        algod_client.status_after_block(current_round)

        # Incremenent the `current_round`
        current_round += 1


def send_transaction(private_key, my_address, receiver_address, amount):
    algod_address = "http://localhost:4001"
    algod_token = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
    algod_client = algod.AlgodClient(algod_token, algod_address)

    account_info = algod_client.account_info(my_address)
    print("Account blance: {} microAlgos".format(account_info.get("amount")) + "\n")

    # build txn
    params = algod_client.suggested_params()
    # comment next tu use suggested param
    params.flat_fee = True
    params.fee = 1000
    note = b"hello world"

    unsigned_txn = PaymentTxn(my_address, params, receiver_address, amount, None, note)

    # sign txn
    signed_txn = unsigned_txn.sign(private_key)

    # submit txn
    txid = algod_client.send_transaction(signed_txn)
    print(f"Successfully sent ransaction with txID: {txid}")

    # wait for confirmation
    try:
        confirmed_txn = wait_for_confirmation(algod_client, txid, 4)
    except Exception as err:
        print(err)
        return

    print(f"Txn info: {json.dumps(confirmed_txn, indent=4)}")
    print(
        "Decoded note: {}".format(base64.b64decode(confirmed_txn["txn"]["txn"]["note"]))
    )


# generate_algorand_keypair()

"""
send_transaction("4aEIHnkSYsygwxekEprU+n6+qMZtE6m808Sz14x53RCZleqdY6y551wuoSKVoocqvviwEZpZt95viljoe3ELNA==",
    "TGK6VHLDVS46OXBOUERJLIUHFK7PRMARTJM3PXTPRJMOQ63RBM2CQJBHNI",
    "4YTGV7MY4W5FSJKPN3FGG6IPOBOUJLJFOYO6SEIAO26SNNINIO5FMYFR3E",
    4470881)

send_transaction("FUB4rJF0UuzSJdBGmswps6IbXK6tBodxLOsOB6NyaXzqgjGPCtvM4Sj0cpCOspvln8SE+PuMcRzNW+Ma8CB3xw==",
    "5KBDDDYK3PGOCKHUOKII5MU34WP4JBHY7OGHCHGNLPRRV4BAO7DRMNLBQM",
    "4YTGV7MY4W5FSJKPN3FGG6IPOBOUJLJFOYO6SEIAO26SNNINIO5FMYFR3E",
    387483)

send_transaction("+IVWWBuyRIJKS2CxziOblb6aA8HDfHCUgn3tI9BCWv7QLUARuoVryjidHtQApv80PCH7bS0hj5izfig9ZX12xA==",
    "2AWUAEN2QVV4UOE5D3KABJX7GQ6CD63NFUQY7GFTPYUD2ZL5O3CFFJ3BVY",
    "4YTGV7MY4W5FSJKPN3FGG6IPOBOUJLJFOYO6SEIAO26SNNINIO5FMYFR3E",
    11906767)

send_transaction("i+Usy5wSSrRzTw4EVm4s1vPkr7uX12kPt/SP0AnvM9gOI3ZN0CFlg9t8/+dCokU3uIRiSBbrYELxbgItdnOBnw==",
    "BYRXMTOQEFSYHW3477TUFISFG64IIYSIC3VWAQXRNYBC25TTQGPYMUYLDA",
    "4YTGV7MY4W5FSJKPN3FGG6IPOBOUJLJFOYO6SEIAO26SNNINIO5FMYFR3E",
    1365707)
"""
