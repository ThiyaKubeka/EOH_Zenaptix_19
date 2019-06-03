import asyncio
import json
import pprint

from indy import pool, ledger, wallet, did
from indy.error import IndyError, ErrorCode

from src.utils import get_pool_genesis_txn_path, PROTOCOL_VERSION
from Write_DID_Func import write_nym_and_query_verkey

wallet_handle = 'wallet_handle'
pool_handle = 'pool_handle'
steward_did =  'steward_did'
steward_verkey = 'steward_verkey'
trust_anchor = 'trust_anchor'
trust_anchor_did = 'trust_anchor_did'
trust_anchor_verkey = 'trust_anchor_verkey'
Init = 'Init'
pool_config = 'pool_config'
pool_name = 'pool'
genesis_file_path = get_pool_genesis_txn_path(pool_name)

wallet_config = json.dumps({"id": "wallet"})
wallet_credentials = json.dumps({"key": "wallet_key"})

def print_log(value_color="", value_noncolor=""):
    """set the colors for text."""
    HEADER = '\033[92m'
    ENDC = '\033[0m'
    print(HEADER + value_color + ENDC + str(value_noncolor))


async def how_tos():
    try: 
         Init = await write_nym_and_query_verkey()

         return(Init)

    except IndyError as e:
        print('Error occurred: %s' % e)


def main():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(how_tos())
    loop.close()


if __name__ == '__main__':
    main()
