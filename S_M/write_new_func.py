import asyncio
import json
import pprint

from indy import pool, ledger, wallet, did
from indy.error import IndyError, ErrorCode

from utils import get_pool_genesis_txn_path, PROTOCOL_VERSION

pool_name = 'pool'
genesis_file_path = get_pool_genesis_txn_path(pool_name)



def print_log(value_color="", value_noncolor=""):
    """set the colors for text."""
    HEADER = '\033[92m'
    ENDC = '\033[0m'
    print(HEADER + value_color + ENDC + str(value_noncolor))

async def pool_config():

    await pool.set_protocol_version(PROTOCOL_VERSION)

    
    print_log('\n1. Creates a new local pool ledger configuration that is used '
                'later when connecting to ledger.\n')
    pool_config = json.dumps({'genesis_txn': str(genesis_file_path)})
    try:
        await pool.create_pool_ledger_config(config_name=pool_name, config=pool_config)
    except IndyError as ex:
        if ex.error_code == ErrorCode.PoolLedgerConfigAlreadyExistsError:
            pass

    
    print_log('\n2. Open pool ledger and get handle from libindy\n')
    pool_handle = await pool.open_pool_ledger(config_name=pool_name, config=None)
    return (pool_handle)

async def Create_steward_wallet():

    print_log('\n3. Creating steward wallet\n')
    wallet_config = json.dumps({"id": "wallet"})
    wallet_credentials = json.dumps({"key": "wallet_key"})

    try:
        await wallet.create_wallet(wallet_config, wallet_credentials)
    except:
        pass
    wallet_handle = await wallet.open_wallet(wallet_config, wallet_credentials)
    print('wallet = %s' % wallet_handle)

    return(wallet_handle)

async def steward_keys(wallet_handle):
    print_log('\n4. Generating and Storing Steward DID and verkey\n')

    steward_did, steward_verkey = await did.create_and_store_my_did(wallet_handle, "{}")
    

    print('Steward DID and verkey = %s %s '% (steward_did,steward_verkey))
  

    return(steward_did,steward_verkey)

async def create_faber_wallet(): 
    print_log('\n3. Creating faber wallet\n')
    wallet_config = json.dumps({"id": "wallet_faber"})
    wallet_credentials = json.dumps({"key": "wallet_key_faber"})

    try:
        await wallet.create_wallet(wallet_config, wallet_credentials)
    except:
        pass
    faber_handle = await wallet.open_wallet(wallet_config, wallet_credentials)
    print('wallet = %s' % faber_handle)

    return(faber_handle)
async def faber_keys(faber_handle):
    print_log('\n6. Generating and storing trust anchor DID and verkey\n')
    faber_did, faber_verkey = await did.create_and_store_my_did(faber_handle, "{}")
    print('Steward DID and verkey = %s %s '% (faber_did,faber_verkey))
    return(faber_did,faber_verkey)
     


    
