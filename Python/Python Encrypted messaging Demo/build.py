
import asyncio
import json
import pprint
import random

from indy import pool, ledger, wallet, did
from indy.error import IndyError, ErrorCode
from Write_DID_Func import print_log
from utils import get_pool_genesis_txn_path, PROTOCOL_VERSION

pool_name = 'pool'
genesis_file_path = get_pool_genesis_txn_path(pool_name)

pool_s = 'pool'

async def pools():
    await pool.set_protocol_version(PROTOCOL_VERSION)

    
    pool_config = json.dumps({'genesis_txn': str(genesis_file_path)})
   

    try:
        await pool.create_pool_ledger_config(config_name=pool_s, config=pool_config)
    except IndyError as ex:
            if ex.error_code == ErrorCode.PoolLedgerConfigAlreadyExistsError:
                pass
    
    pooles = await pool.open_pool_ledger(config_name=pool_s, config=None)
    return pooles
async def clos(pooles):
    
    
        await pool.set_protocol_version(PROTOCOL_VERSION)

     
        pool_config = json.dumps({'genesis_txn': str(genesis_file_path)})
        print_log('\n1. Close pool.\n')

        try:
            await pool.close_pool_ledger(pooles)
        except IndyError as ex:
         if ex.error_code == ErrorCode.PoolLedgerInvalidPoolHandle:
             pass
    

async def Faber(): 
    wallet_config = json.dumps({"id": "wallet_faber_f"})
    wallet_credentials = json.dumps({"key": "wallet_key_faber_f"})
    # 1. Create Wallet and Get Wallet Handle
    
   
    try:  
        await wallet.create_wallet(wallet_config, wallet_credentials)
    except IndyError as ex:
        if ex.error_code == ErrorCode.WalletAlreadyExistsError:
            pass
 
    try:
        faber = await wallet.open_wallet(wallet_config, wallet_credentials)
    except IndyError as ex:
        if ex.error_code == ErrorCode.WalletAlreadyOpenedError:
            pass
    
    return faber
async def fab_keys(faber):
    
    
    Faber_did, Faber_verkey = await did.create_and_store_my_did(faber, "{}")
   
    print ('Faber Did and verkey = %s %s' % (Faber_did,Faber_verkey))   
    return Faber_did, Faber_verkey
async def add_ledger(Wallet_handle,steward_did,steward_verkey,Faber_did,Faber_verkey,pooles):

        print_log('\n7. Building NYM request to add faber did and verkey to the ledger\n')
        nym_transaction_request = await ledger.build_nym_request(submitter_did=steward_did,
                                                                 target_did= Faber_did,
                                                                 ver_key=Faber_verkey,
                                                                 alias=None,
                                                                 role='TRUST_ANCHOR')
        print_log('NYM transaction request: ')
        pprint.pprint(json.loads(nym_transaction_request))

        
        print_log('\n8. Sending NYM request to the ledger\n')
        nym_transaction_response = await ledger.sign_and_submit_request(pool_handle=pooles,
                                                                        wallet_handle=Wallet_handle,
                                                                        submitter_did=steward_did,
                                                                        request_json=nym_transaction_request)
        print_log('NYM transaction response: ')
        pprint.pprint(json.loads(nym_transaction_response))

        return(nym_transaction_request,nym_transaction_response)

