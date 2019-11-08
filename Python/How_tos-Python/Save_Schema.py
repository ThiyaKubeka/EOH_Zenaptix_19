import asyncio
import json
import pprint

from indy import pool, ledger, wallet, did, anoncreds
from indy.error import ErrorCode, IndyError

from utils import get_pool_genesis_txn_path, PROTOCOL_VERSION
from Save_Schema_func import write_schema_and_cred_def 

pool_name = 'pool'
wallet_config = json.dumps({"id": "wallet"})
wallet_credentials = json.dumps({"key": "wallet_key"})
genesis_file_path = get_pool_genesis_txn_path(pool_name)

def print_log(value_color="", value_noncolor=""):
    """set the colors for text."""
    HEADER = '\033[92m'
    ENDC = '\033[0m'
    print(HEADER + value_color + ENDC + str(value_noncolor))

async def Schema():
    try: 
        Sche = await write_schema_and_cred_def()

    except IndyError as e:
        print('Error occurred: %s' % e)

    return(Sche)

def main():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(Schema())
    loop.close()


if __name__ == '__main__':
    main()
