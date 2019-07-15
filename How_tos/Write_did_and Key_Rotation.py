import asyncio
import json
import pprint

from indy import pool, ledger, wallet, did
from indy.error import IndyError, ErrorCode

from utils import get_pool_genesis_txn_path, PROTOCOL_VERSION
from code import rotate_key_on_the_ledger 
from Write_DID_Func import write_nym_and_query_verkey

pool_name = 'pool'
genesis_file_path = get_pool_genesis_txn_path(pool_name)

wallet_config = json.dumps({"id": "wallet"})
wallet_credentials = json.dumps({"key": "wallet_key"})

def print_log(value_color="", value_noncolor=""):
    """set the colors for text."""
    HEADER = '\033[92m'
    ENDC = '\033[0m'
    print(HEADER + value_color + ENDC + str(value_noncolor))

async def Mod():
    try: 
        write = await write_nym_and_query_verkey()
        Key = await rotate_key_on_the_ledger()


    except IndyError as e:
        print('Error occurred: %s' % e)
    return(write , Key)


def main():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(Mod())
    loop.close()


if __name__ == '__main__':
    main()

