#These steps only include steps up to the point of generating and storing the trust anchor DID and verkey. The latter is stored in the same wallet as that for the steward


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

async def inputs():
    me = input('Who are you? ').strip()

    wallet_config = '{"id": "%s-wallet"}' % me
    wallet_credentials = '{"key": "%s-wallet-key"}' % me

    return(me)

async def create_steward_wallet(me):
    print_log('\n. Create steward wallet.\n')   
    wallet_config = '{"id": "%s-wallet"}' % me
    wallet_credentials = '{"key": "%s-wallet-key"}' % me

    print_log('\n. Open Steward Wallet and Get Handle.\n')
    try:
        await wallet.create_wallet(wallet_config, wallet_credentials)
    except:
        pass
    Wallet_handle = await wallet.open_wallet(wallet_config, wallet_credentials)
    print('wallet = %s' % Wallet_handle)
    return (Wallet_handle)

async def Steward_did_and_verkey(Wallet_handle):
    print_log('\n. Generate and store steward DID and verkey\n')
    
    steward_did, steward_verkey = await did.create_and_store_my_did(Wallet_handle, "{}")
   
       
    return steward_did, steward_verkey


async def create_faber_wallet(me):
    wallet_config = '{"id": "%s-wallet_faber"}' % me
    wallet_credentials = '{"key": "%s-wallet-key_faber"}' % me

    # 1. Create Wallet and Get Wallet Handle
    
    print_log('\n. Create faber wallet.\n')          

    try:  
        await wallet.create_wallet(wallet_config, wallet_credentials)
    except IndyError:
        await wallet.delete_wallet(wallet_config, wallet_credentials)
        await wallet.create_wallet(wallet_config, wallet_credentials)

    print_log('\n. Open Faber Wallet and Get Handle.\n')
    faber_handle = await wallet.open_wallet(wallet_config, wallet_credentials)

    return faber_handle



async def Faber_did_and_verkey(faber_handle):

        print_log('\n. Generate and store Faber did and verkey.\n')
        try:
           Faber_did, Faber_verkey = await did.create_and_store_my_did(faber_handle, "{}")
        except IndyError as ex:
            if ex.error_code == ErrorCode.DidAlreadyExistsError:
                pass

        print ('faber_did and verkey = %s %s' % (Faber_did, Faber_verkey))
        return Faber_did , Faber_verkey