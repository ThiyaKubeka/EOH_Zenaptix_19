import asyncio
import json
import pprint
import random

from indy import pool, ledger, wallet, did
from indy.error import IndyError, ErrorCode

from utils import get_pool_genesis_txn_path, PROTOCOL_VERSION

pool_na = 'pool'
pool_n = 'pool'
genesis_file_path = get_pool_genesis_txn_path(pool_na)




def print_log(value_color="", value_noncolor=""):
    """set the colors for text."""
    HEADER = '\033[92m'
    ENDC = '\033[0m'
    print(HEADER + value_color + ENDC + str(value_noncolor))

async def  wall(): 
    
    wallet_config = json.dumps({"id": "wallet_response"})
    wallet_credentials = json.dumps({"key": "wallet_key_response"})
    
    try:
        await wallet.create_wallet(wallet_config, wallet_credentials)
    except IndyError:
        await wallet.delete_wallet(wallet_config, wallet_credentials)
        await wallet.create_wallet(wallet_config, wallet_credentials)
    Wall_handles = await wallet.open_wallet(wallet_config, wallet_credentials)
 
    return (Wall_handles)

async def keys(Wall_handles):
    Did_for_steward,Verkey_for_steward = await did.create_and_store_my_did(Wall_handles, "{}")
   
       
    return Did_for_steward, Verkey_for_steward


async def pool_config():


    await pool.set_protocol_version(PROTOCOL_VERSION)

    
    pool_config = json.dumps({'genesis_txn': str(genesis_file_path)})
   

    try:
        await pool.create_pool_ledger_config(config_name=pool_na, config=pool_config)
    except IndyError as ex:
            if ex.error_code == ErrorCode.PoolLedgerConfigAlreadyExistsError:
                pass
    
    pool_ = await pool.open_pool_ledger(config_name=pool_na, config=None)
    return pool_
async def close(pool_):
    await pool.set_protocol_version(PROTOCOL_VERSION)

     
    pool_config = json.dumps({'genesis_txn': str(genesis_file_path)})
    print_log('\n1. Close pool.\n')

    try:
        await pool.close_pool_ledger(pool_)
    except IndyError as ex:
        if ex.error_code == ErrorCode.PoolLedgerInvalidPoolHandle:
            pass

async def pool_con():


    await pool.set_protocol_version(PROTOCOL_VERSION)

    
    pool_config = json.dumps({'genesis_txn': str(genesis_file_path)})
   

    try:
        await pool.create_pool_ledger_config(config_name=pool_n, config=pool_config)
    except IndyError as ex:
            if ex.error_code == ErrorCode.PoolLedgerConfigAlreadyExistsError:
                pass
    
    poole = await pool.open_pool_ledger(config_name=pool_n, config=None)
    return poole   

async def add_faber_to_ledger(Wallet_handle,steward_did,steward_verkey,faber_did,faber_verkey,pool_):

        print_log('\n7. Building NYM request to add faber did and verkey to the ledger\n')
        nym_transaction_request = await ledger.build_nym_request(submitter_did=steward_did,
                                                                 target_did= faber_did,
                                                                 ver_key=faber_verkey,
                                                                 alias=None,
                                                                 role='TRUST_ANCHOR')
        print_log('NYM transaction request: ')
        pprint.pprint(json.loads(nym_transaction_request))

        
        print_log('\n8. Sending NYM request to the ledger\n')
        nym_transaction_response = await ledger.sign_and_submit_request(pool_handle=pool_,
                                                                        wallet_handle=Wallet_handle,
                                                                        submitter_did=steward_did,
                                                                        request_json=nym_transaction_request)
        print_log('NYM transaction response: ')
        pprint.pprint(json.loads(nym_transaction_response))

        return(nym_transaction_request,nym_transaction_response)
