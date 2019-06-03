#These steps only include steps up to the point of generating and storing the trust anchor DID and verkey. The latter is stored in the same wallet as that for the steward


import asyncio
import json
import pprint

from indy import pool, ledger, wallet, did
from indy.error import IndyError, ErrorCode

from src.utils import get_pool_genesis_txn_path, PROTOCOL_VERSION

pool_name = 'pool'
genesis_file_path = get_pool_genesis_txn_path(pool_name)

wallet_config = json.dumps({"id": "wallet"})
wallet_credentials = json.dumps({"key": "wallet_key"})

def print_log(value_color="", value_noncolor=""):
    """set the colors for text."""
    HEADER = '\033[92m'
    ENDC = '\033[0m'
    print(HEADER + value_color + ENDC + str(value_noncolor))


async def write_nym_and_query_verkey():
    try:
        await pool.set_protocol_version(PROTOCOL_VERSION)

     
        pool_config = json.dumps({'genesis_txn': str(genesis_file_path)})
        print_log('\n1. Create new pool ledger configuration to connect to ledger.\n')

        try:
            await pool.create_pool_ledger_config(config_name=pool_name, config=pool_config)
        except IndyError as ex:
            if ex.error_code == ErrorCode.PoolLedgerConfigAlreadyExistsError:
                pass 
        print_log('\n2. Open ledger and get handle\n')
        pool_handle = await pool.open_pool_ledger(config_name=pool_name, config=None)
          
        print_log('\n3. Create new identity wallet\n')
        try:  
            await wallet.create_wallet(wallet_config, wallet_credentials)
        except IndyError:
            await wallet.delete_wallet(wallet_config, wallet_credentials)
            await wallet.create_wallet(wallet_config, wallet_credentials)

        print_log('\n4. Open identity wallet and get handle\n')
        wallet_handle = await wallet.open_wallet(wallet_config, wallet_credentials)


        print_log('\n5. Generate and store steward DID and verkey\n')

        steward_seed = '000000000000000000000000Steward1'
        did_json = json.dumps({'seed': steward_seed})
    
        steward_did, steward_verkey = await did.create_and_store_my_did(wallet_handle, did_json)
        print_log('Steward DID: ', steward_did)
        print_log('Steward Verkey: ', steward_verkey)
       

     
        
           
        #The Below is going to be stored in the wallet created. In this tutorial all the DID's and verkeys are stored in one wallet for the sake of convinience.    
        

        
        print_log('\n6. Generating and storing trust anchor DID and verkey\n')
        try:
            trust_anchor_did, trust_anchor_verkey = await did.create_and_store_my_did(wallet_handle, "{}")
        except IndyError as ex:
            if ex.error_code == ErrorCode.DidAlreadyExistsError:
                pass

        print_log('Trust anchor DID: ', trust_anchor_did)
        print_log('Trust anchor Verkey: ', trust_anchor_verkey)
        

    except IndyError as e:
        print('Error occurred: %s' % e)


def main():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(write_nym_and_query_verkey())
    loop.close()


if __name__ == '__main__':
    main()
