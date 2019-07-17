import asyncio
import json
import pprint
import random
from indy import pool, ledger, wallet, did
from indy.error import IndyError, ErrorCode
from pool_func import pool_configuration, request


from utils import get_pool_genesis_txn_path, PROTOCOL_VERSION

pool_name = 'pool'
genesis_file_path = get_pool_genesis_txn_path(pool_name)

async def write():
    try:
        await pool_configuration()
        await request()

    except IndyError as e:
        print('Error occurred: %s' % e)


def main():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(write())
    loop.close()


if __name__ == '__main__':
    main()
    