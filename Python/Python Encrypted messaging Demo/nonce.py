
import asyncio
import json
import pprint
import random

from random import *

from indy import pool, ledger, wallet, did
from indy.error import IndyError, ErrorCode

from utils import get_pool_genesis_txn_path, PROTOCOL_VERSION
from Write_DID_Func import create_steward_wallet

pool_name = 'pool'
genesis_file_path = get_pool_genesis_txn_path(pool_name)




def print_log(value_color="", value_noncolor=""):
    """set the colors for text."""
    HEADER = '\033[92m'
    ENDC = '\033[0m'
    print(HEADER + value_color + ENDC + str(value_noncolor))

async def accept():
    wallet_config = json.dumps({"id": "wallet"})
    wallet_credentials = json.dumps({"key": "wallet_key"})
    try:
        print_log('\n1. Accept.\n')
        try:
            await wallet.create_wallet(wallet_config, wallet_credentials)
        except IndyError:
            await wallet.delete_wallet(wallet_config, wallet_credentials)
            await wallet.create_wallet(wallet_config, wallet_credentials)
        Wallet_handle = await wallet.open_wallet(wallet_config, wallet_credentials)
        steward_did_for_faber, steward_verkey_for_faber = await did.create_and_store_my_did(Wallet_handle, "{}")
        nonce = [1,2,3,4,5,6,7,8,9] 
        shuffle(nonce)
        print('steward_did for faber =  %s' % (steward_did_for_faber))
        print('steward_verkey_for_faber = %s'% (steward_verkey_for_faber)) 
               
        print('nonce = %s' % (nonce))
    except IndyError as e:
        print('Error occurred: %s' % e)


def main():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(accept())
    loop.close()


if __name__ == '__main__':
    main()
