import asyncio
import json
import pprint
import random
import mongo

from pymongo import MongoClient
from indy import pool, ledger, wallet, did
from indy.error import IndyError, ErrorCode

from utils import get_pool_genesis_txn_path, PROTOCOL_VERSION

pool_name = 'pool'
genesis_file_path = get_pool_genesis_txn_path(pool_name)

pool_s = 'pool'

client = MongoClient('localhost',27017)

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

async def wall_config():   
    config = client['steward-config']
    configs = config.configs
    print(configs)
    print(config)
    configer = {'wallet_config' :'wallet_credentials'}
    wallet_config = json.dumps({"id": "wallet"})
    wallet_credentials = json.dumps({"key": "wallet_key"})
    configs.insert_one(configer) 
    return wallet_config ,wallet_credentials,configs,configer

async def create_steward_wallet(wallet_config ,wallet_credentials,configs,configer):
    configs.find_one(configer) 
    print_log('\n. Create steward wallet.\n')   
    wallet_config ,wallet_credentials = await wall_config()
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
    usr = client['steward-dets']
    stewards = usr.stewards
    print(usr)
    print(stewards)
    try:
        steward = {'name':'steward'}
        steward['did'],steward['verkey'] = await did.create_and_store_my_did(Wallet_handle, "{}")
        stewards.insert_one(steward)
    except IndyError as ex:
            if ex.error_code == ErrorCode.DidAlreadyExistsError:
                pass
        
    print_log('Steward DID: ', steward['did'])
    print_log('Steward Verkey: ', steward['verkey'])
    return steward['did'], steward['verkey']

async def faber_config():
    config_faber = client['steward-config']
    configes = config_faber.configes
    wallet_config_faber = json.dumps({"id": "wallet_faber"})
    wallet_credentials_faber = json.dumps({"key": "wallet_key_faber"})
    return wallet_config_faber , wallet_credentials_faber,config_faber,configes

async def create_faber_wallet(wallet_config_faber , wallet_credentials_faber,config_faber,configes):
    wallet_config_faber , wallet_credentials_faber = await faber_config()

    
   
    try:  
        await wallet.create_wallet(wallet_config_faber, wallet_credentials_faber)
    except IndyError as ex:
        if ex.error_code == ErrorCode.WalletAlreadyExistsError:
            pass
    print_log('\n. Open Faber Wallet and Get Handle.\n')
    try:
        faber_handle = await wallet.open_wallet(wallet_config_faber, wallet_credentials_faber)
    except IndyError as ex:
        if ex.error_code == ErrorCode.WalletAlreadyOpenedError:
            pass
    
    return faber_handle



async def Faber_did_and_verkey(faber_handle):

        user = client['faber-dets']
        fabers = user.fabers
        print(user)
        print(fabers)
        try:
           Faber_did, Faber_verkey = await did.create_and_store_my_did(faber_handle, "{}")
           fabers.insert_one(fabers)
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

