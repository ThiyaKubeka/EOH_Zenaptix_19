import asyncio
import json
import pprint

from indy import pool, ledger, wallet, did, anoncreds
from indy.error import ErrorCode, IndyError

from utils import open_wallet, get_pool_genesis_txn_path, PROTOCOL_VERSION
from Issue_Cred_func import issue_credential
pool_name = 'pool'
issuer_wallet_config = json.dumps({"id": "issuer_wallet"})
issuer_wallet_credentials = json.dumps({"key": "issuer_wallet_key"})
genesis_file_path = get_pool_genesis_txn_path(pool_name)

def print_log(value_color="", value_noncolor=""):
    """set the colors for text."""
    HEADER = '\033[92m'
    ENDC = '\033[0m'
    print(HEADER + value_color + ENDC + str(value_noncolor))

async def Creds():
    try:
        Issue = await issue_credential()
    
    except IndyError as e:
        print('Error occurred: %s' % e)
    return(Issue)


def main():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(Creds())
    loop.close()


if __name__ == '__main__':
    main()
