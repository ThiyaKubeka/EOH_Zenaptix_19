#These steps only include steps up to the point of generating and storing the trust anchor DID and verkey. The latter is stored in the same wallet as that for the steward


import asyncio
import json
import pprint

from indy import pool, ledger, wallet, did
from indy.error import IndyError, ErrorCode

from utils import get_pool_genesis_txn_path, PROTOCOL_VERSION

pool_name = 'pool'
genesis_file_path = get_pool_genesis_txn_path(pool_name)

wallet_config = json.dumps({"id": "wallet"})
wallet_credentials = json.dumps({"key": "wallet_key"})

def print_log(value_color="", value_noncolor=""):
    """set the colors for text."""
    HEADER = '\033[92m'
    ENDC = '\033[0m'
    print(HEADER + value_color + ENDC + str(value_noncolor))


async def pool_configuration():
    
    
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
        return pool_handle

async def create_steward_wallet():

    print_log('\n3. Create Steward Wallet\n')
    try:  
        await wallet.create_wallet(wallet_config, wallet_credentials)
    except IndyError:
        await wallet.delete_wallet(wallet_config, wallet_credentials)
        await wallet.create_wallet(wallet_config, wallet_credentials)

    print_log('\n4. Open Steward Wallet and Get Handle.\n')
    wallet_handle = await wallet.open_wallet(wallet_config, wallet_credentials)

    return wallet_handle

async def Steward_did_and_verkey(wallet_handle):
        print_log('\n5. Generate and store steward DID and verkey\n')
    
        steward_seed = '000000000000000000000000Steward1'
        did_json = json.dumps({'seed': steward_seed})
    
        steward_did, steward_verkey = await did.create_and_store_my_did(wallet_handle, did_json)
        
        print_log('Steward DID: ', steward_did)
        print_log('Steward Verkey: ', steward_verkey)

        return steward_did, steward_verkey


async def create_faber_wallet():
    wallet_config = json.dumps({"id": "wallet_faber"})
    wallet_credentials = json.dumps({"key": "wallet_key_faber"})
    print_log('\n1. Create faber wallet.\n')          

    try:  
            await wallet.create_wallet(wallet_config, wallet_credentials)
    except IndyError:
        await wallet.delete_wallet(wallet_config, wallet_credentials)
        await wallet.create_wallet(wallet_config, wallet_credentials)

    print_log('\n2. Open Faber Wallet and Get Handle.\n')
    Faber_handle = await wallet.open_wallet(wallet_config, wallet_credentials)

    return Faber_handle



async def Faber_did_and_verkey(Faber_handle):

        print_log('\n3. Generate and store Faber did and verkey.\n')
        try:
           Faber_did, Faber_verkey = await did.create_and_store_my_did(Faber_handle, "{}")
        except IndyError as ex:
            if ex.error_code == ErrorCode.DidAlreadyExistsError:
                pass

        print_log('Faber DID: ', Faber_did)
        print_log('Faber Verkey: ', Faber_verkey)
        return Faber_did , Faber_verkey

