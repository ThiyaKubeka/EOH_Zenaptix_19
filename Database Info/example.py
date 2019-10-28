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


async def example():
    try: 
        try:
            Wallet_handle = await create_steward_wallet()
        
            print_log('\n5. Generate and store steward DID and verkey\n')
            steward_seed = '000000000000000000000000Steward1'
            did_json = json.dumps({'seed': steward_seed})
        except IndyError as ex:
            if ex.error_code == ErrorCode.WalletAlreadyExistsError:
                pass
            usr = client['steward-dets']
            stewards = usr.stewards
            print(usr)
            print(stewards)
        try:
            steward = {'name': 'steward'}
            steward['did'], steward['verkey'] = await did.create_and_store_my_did(Wallet_handle, did_json)
            stewards.insert_one(steward)
        except IndyError as ex:
            if ex.error_code == ErrorCode.DidAlreadyExistsError:
                pass
        
        print_log('Steward DID: ', steward['did'])
        print_log('Steward Verkey: ', steward['verkey'])
        
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
   
        print ('steward_did_for_faber and verkey = %s %s' % (faber_did, faber_verkey))   
    




    except IndyError as e:
        print('Error occurred: %s' % e)


def main():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(example())
    loop.close()


if __name__ == '__main__':
    main()

   