import asyncio
import json
import pprint
import random

from indy import pool, ledger, wallet, did
from indy.error import IndyError, ErrorCode

from utils import get_pool_genesis_txn_path, PROTOCOL_VERSION

pool_no = 'pool'
pool_s ='pool'
genesis_file_path = get_pool_genesis_txn_path(pool_no)




def print_log(value_color="", value_noncolor=""):
    """set the colors for text."""
    HEADER = '\033[92m'
    ENDC = '\033[0m'
    print(HEADER + value_color + ENDC + str(value_noncolor))

async def pool_configurat():


    await pool.set_protocol_version(PROTOCOL_VERSION)

    
    pool_config = json.dumps({'genesis_txn': str(genesis_file_path)})
   

    try:
        await pool.create_pool_ledger_config(config_name=pool_no, config=pool_config)
    except IndyError as ex:
            if ex.error_code == ErrorCode.PoolLedgerConfigAlreadyExistsError:
                pass
    try:
        pole = await pool.open_pool_ledger(config_name=pool_no, config=None)
    except IndyError as ex:
            if ex.error_code == ErrorCode.PoolLedgerInvalidPoolHandle:
                pass
    return pole


async def  wal(): 
    
    wallet_config = json.dumps({"id": "wallet_respons"})
    wallet_credentials = json.dumps({"key": "wallet_key_respons"})
    
    try:
        await wallet.create_wallet(wallet_config, wallet_credentials)
    except IndyError:
        await wallet.delete_wallet(wallet_config, wallet_credentials)
        await wallet.create_wallet(wallet_config, wallet_credentials)
    Wal = await wallet.open_wallet(wallet_config, wallet_credentials)
 
    return (Wal)
async def Client(Wal):
        try:
           F_did,F_verkey = await did.create_and_store_my_did(Wal, "{}")
        except IndyError as ex:
            if ex.error_code == ErrorCode.DidAlreadyExistsError:
                pass

        print ('faber_did and verkey = %s %s' % (F_did, F_verkey))
        return F_did , F_verkey

async def add_faber_to_ledger(Wallet_handle,steward_did,steward_verkey,F_did,F_verkey,pole):

        print_log('\n7. Building NYM request to add faber did and verkey to the ledger as a TRUST ANCHOR\n')
        nym_transaction_request = await ledger.build_nym_request(submitter_did=steward_did,
                                                                 target_did= F_did,
                                                                 ver_key=F_verkey,
                                                                 alias=None,
                                                                 role='TRUST_ANCHOR')
        print_log('NYM transaction request: ')
        pprint.pprint(json.loads(nym_transaction_request))

        
        print_log('\n8. Sending NYM request to the ledger\n')
        nym_transaction_response = await ledger.sign_and_submit_request(pool_handle=pole,
                                                                        wallet_handle=Wallet_handle,
                                                                        submitter_did=steward_did,
                                                                        request_json=nym_transaction_request)
        print_log('NYM transaction response: ')
        pprint.pprint(json.loads(nym_transaction_response))

        return(nym_transaction_request,nym_transaction_response)

async def faber_steward():
    wallet_config = json.dumps({"id": "wallet_faber_S"})
    wallet_credentials = json.dumps({"key": "wallet_key_faber_S"})
    # 1. Create Wallet and Get Wallet Handle
    
   
    try:  
        await wallet.create_wallet(wallet_config, wallet_credentials)
    except IndyError as ex:
        if ex.error_code == ErrorCode.WalletAlreadyExistsError:
            pass
    print_log('\n. Open Faber Wallet and Get Handle.\n')
    try:
        faber_handle_for = await wallet.open_wallet(wallet_config, wallet_credentials)
    except IndyError as ex:
        if ex.error_code == ErrorCode.WalletAlreadyOpenedError:
            pass
    
    return faber_handle_for



async def Faber_did_and_verkey_for_steward(faber_handle_for):

      
        try:
           Faber_did_for_steward, Faber_verkey_for_steward = await did.create_and_store_my_did(faber_handle_for, "{}")
        except IndyError as ex:
            if ex.error_code == ErrorCode.DidAlreadyExistsError:
                pass

        print ('faber_did and verkey for steward= %s %s' % (Faber_did_for_steward, Faber_verkey_for_steward))
        return Faber_did_for_steward , Faber_verkey_for_steward


