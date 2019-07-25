#These steps only include steps up to the point of generating and storing the trust anchor DID and verkey. The latter is stored in the same wallet as that for the steward


import asyncio
import json
import pprint
import random

from indy import pool, ledger, wallet, did
from indy.error import IndyError, ErrorCode

from utils import get_pool_genesis_txn_path, PROTOCOL_VERSION

pool_name = 'pool'
genesis_file_path = get_pool_genesis_txn_path(pool_name)

pool_s = 'pool'


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

async def pool_close(pool_handle):
    
    
        await pool.set_protocol_version(PROTOCOL_VERSION)

     
        pool_config = json.dumps({'genesis_txn': str(genesis_file_path)})
        print_log('\n1. Close pool.\n')

        try:
            await pool.close_pool_ledger(pool_handle)
        except IndyError as ex:
         if ex.error_code == ErrorCode.PoolLedgerInvalidPoolHandle:
             pass
    

async def create_steward_wallet():
    print_log('\n. Create steward wallet.\n')   
    wallet_config = json.dumps({"id": "wallet"})
    wallet_credentials = json.dumps({"key": "wallet_key"})
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
   
    print('steward_did and verkey = %s %s' % (steward_did, steward_verkey))   
    return steward_did, steward_verkey


async def create_faber_wallet():
    wallet_config = json.dumps({"id": "wallet_faber"})
    wallet_credentials = json.dumps({"key": "wallet_key_faber"})
    # 1. Create Wallet and Get Wallet Handle
    
   
    try:  
        await wallet.create_wallet(wallet_config, wallet_credentials)
    except IndyError as ex:
        if ex.error_code == ErrorCode.WalletAlreadyExistsError:
            pass
    print_log('\n. Open Faber Wallet and Get Handle.\n')
    try:
        faber_handle = await wallet.open_wallet(wallet_config, wallet_credentials)
    except IndyError as ex:
        if ex.error_code == ErrorCode.WalletAlreadyOpenedError:
            pass
    
    return faber_handle



async def Faber_did_and_verkey(faber_handle):

      
        try:
           Faber_did, Faber_verkey = await did.create_and_store_my_did(faber_handle, "{}")
        except IndyError as ex:
            if ex.error_code == ErrorCode.DidAlreadyExistsError:
                pass

        print ('faber_did and verkey = %s %s' % (Faber_did, Faber_verkey))
        return Faber_did , Faber_verkey

async def steward_keys_for_faber(Wallet_handle):
   
    print_log('\n Generate and store steward DID and verkey for faber\n')
    
    steward_did_for_faber, steward_verkey_for_faber = await did.create_and_store_my_did(Wallet_handle, "{}")
   
    print ('steward_did_for_faber and verkey = %s %s' % (steward_did_for_faber, steward_verkey_for_faber))   
    return steward_did_for_faber, steward_verkey_for_faber

async def add_to_ledger(Wallet_handle,steward_did,steward_verkey,steward_did_for_faber,steward_verkey_for_faber,pool_handle):

        print_log('\n7. Building NYM request to add steward did and verkey for faber to the ledger\n')
        nym_transaction_request = await ledger.build_nym_request(submitter_did=steward_did,
                                                                 target_did= steward_did_for_faber,
                                                                 ver_key=steward_verkey_for_faber,
                                                                 alias=None,
                                                                 role='TRUST_ANCHOR')
        print_log('NYM transaction request: ')
        pprint.pprint(json.loads(nym_transaction_request))

        
        print_log('\n8. Sending NYM request to the ledger\n')
        nym_transaction_response = await ledger.sign_and_submit_request(pool_handle=pool_handle,
                                                                        wallet_handle=Wallet_handle,
                                                                        submitter_did=steward_did,
                                                                        request_json=nym_transaction_request)
        print_log('NYM transaction response: ')
        pprint.pprint(json.loads(nym_transaction_response))

        return(nym_transaction_request,nym_transaction_response)

async def pools():
    await pool.set_protocol_version(PROTOCOL_VERSION)

    
    pool_config = json.dumps({'genesis_txn': str(genesis_file_path)})
   

    try:
        await pool.create_pool_ledger_config(config_name=pool_s, config=pool_config)
    except IndyError as ex:
            if ex.error_code == ErrorCode.PoolLedgerConfigAlreadyExistsError:
                pass
    try:
        pooles = await pool.open_pool_ledger(config_name=pool_s, config=None)
    except IndyError as ex:
            if ex.error_code == ErrorCode.PoolLedgerInvalidPoolHandle:
                pass
    return pooles


async def add_faber_ledger(Wallet_handle,steward_did,steward_verkey,faber_did,faber_verkey,pooles):

        print_log('\n7. Building NYM request to add faber did and verkey to the ledger\n')
        nym_transaction_request = await ledger.build_nym_request(submitter_did=steward_did,
                                                                 target_did= faber_did,
                                                                 ver_key=faber_verkey,
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

