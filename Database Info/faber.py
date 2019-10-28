import asyncio
import time
import re
import json
import pprint
import random
from random import *

from pymongo import MongoClient
from indy import crypto, did, wallet,pool,ledger
from indy.error import IndyError, ErrorCode
from utils import get_pool_genesis_txn_path, PROTOCOL_VERSION
from functions import pool_configuration,create_steward_wallet, Steward_did_and_verkey,create_faber_wallet,Faber_did_and_verkey,steward_keys_for_faber,add_to_ledger,print_log,add_faber_ledger,pools,pool_close

client = MongoClient('localhost',27017)


async def faberr():
    try:

        faber_handle = await create_faber_wallet()
        user = client['faber-dets']
        fabers = user.fabers
        print(user)
        print(fabers)
        try:
            print_log('\n Generate and store steward DID and verkey for faber\n')
            faber = {'name':'steward'}
            faber_did, faber_verkey = await did.create_and_store_my_did(faber_handle, "{}")
            fabers.insert_one(faber)
        except IndyError as ex:
            if ex.error_code == ErrorCode.DidAlreadyExistsError:
                pass
        print ('faber_did and verkey = %s %s' % (faber_did, faber_verkey))  

    except IndyError as e:
        print('Error occurred: %s' % e)


def main():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(faberr())
    loop.close()


if __name__ == '__main__':
    main()

   