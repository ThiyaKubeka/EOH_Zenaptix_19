import asyncio
import time
import re
import json
import pprint
import random
from random import *


from indy import crypto, did, wallet,pool,ledger
from indy.error import IndyError, ErrorCode
from utils import get_pool_genesis_txn_path, PROTOCOL_VERSION
from Write_DID_Func import pool_configuration,create_steward_wallet, Steward_did_and_verkey,create_faber_wallet,Faber_did_and_verkey,steward_keys_for_faber,add_to_ledger,print_log



async def prep(Wallet_handle, steward_verkey, steward_verkey_for_faber, msg):
    msg = bytes(msg, "utf-8")
    encrypted = await crypto.auth_crypt(Wallet_handle, steward_verkey, steward_verkey_for_faber, msg)
    #encrypted = await crypto.anon_crypt(steward_verkey, msg)
    print('encrypted = %s' % repr(encrypted))
    with open('message.dat', 'wb') as f:
        f.write(encrypted)
    print('prepping %s' % msg)


async def init():
    
    me = input('Who are you? ').strip()
    if me == 'steward':
        pool_handle = await pool_configuration()
        Wallet_handle = await create_steward_wallet()
        steward_did,steward_verkey = await Steward_did_and_verkey(Wallet_handle)    
        
        faber = input("Faber's DID and verkey? ").strip().split(' ')
        return Wallet_handle, steward_did, steward_verkey,faber[0],faber[1]
    elif me == 'faber':
        pool_handle = await pool_configuration()
        time.sleep(1)
        Wallet_handle = await create_steward_wallet()
        time.sleep(1)
        steward_did,steward_verkey = await Steward_did_and_verkey(Wallet_handle)  
        time.sleep(1)
        steward_did_for_faber,steward_verkey_for_faber = await steward_keys_for_faber(Wallet_handle)  
        time.sleep(1)
        build_nym = await add_to_ledger(Wallet_handle,steward_did,steward_verkey,steward_did_for_faber,steward_verkey_for_faber,pool_handle)
        time.sleep
        print('steward_did and verkey for faber = %s %s' % (steward_did_for_faber, steward_verkey_for_faber))
        steward = input("steward's DID and verkey? ").strip().split(' ')
        return Wallet_handle,steward_did_for_faber ,steward_verkey_for_faber ,steward[0],steward[1]
    return Wallet_handle, steward_did,steward_verkey,steward_did_for_faber,steward_verkey_for_faber

async def send():
     print_log('\n1. REQUESTING..............\n')

async def accept(Wallet_handle):
    print_log('\n1. Accept.\n')

    steward_did_for_faber, steward_verkey_for_faber = await did.create_and_store_my_did(Wallet_handle, "{}")
    nonce = [1,2,3,4,5,6,7,8,9] 
    shuffle(nonce)
    print('steward_did for faber =  %s' % (steward_did_for_faber))
    print('steward_verkey_for_faber = %s'% (steward_verkey_for_faber))      
    print('nonce = %s' % (nonce))
    time.sleep(3)
    print_log('\n1. CREATING WALLET.\n')
    faber_handle = await create_faber_wallet()
    faber_did,faber_verkey = await Faber_did_and_verkey(faber_handle)
    return faber_handle,faber_did,faber_verkey
    

async def reads(Wallet_handle, steward_verkey):
    with open('message.dat', 'rb') as f:
        encrypted = f.read()
    decrypted = await crypto.auth_decrypt(Wallet_handle, steward_verkey, encrypted)
    # decrypted = await crypto.anon_decrypt(wallet_handle, my_vk, encrypted)
    print(decrypted)

    
async def read(Wallet_handle, steward_verkey):
    with open('message.dat', 'rb') as f:
        encrypted = f.read()
    decrypted = await crypto.auth_decrypt(Wallet_handle, steward_verkey, encrypted)
    # decrypted = await crypto.anon_decrypt(wallet_handle, my_vk, encrypted)
    print(decrypted)

async def demo():
    Wallet_handle, steward_did,steward_verkey,steward_did_for_faber,steward_verkey_for_faber = await init()
    

    while True:
        argv = input('> ').strip().split(' ')
        cmd = argv[0].lower()
        rest = ' '.join(argv[1:])
        if re.match(cmd, 'prep'):
            await prep(Wallet_handle, steward_verkey, steward_verkey_for_faber, rest)
        elif re.match(cmd, 'read'):
            await read(Wallet_handle, steward_verkey)
        elif re.match(cmd, 'send'):
            await send()
        elif re.match(cmd, 'accept'):
            await accept(Wallet_handle)
        elif re.match(cmd, 'quit'):
            break
        else:
            print('Huh?')

if __name__ == '__main__':
    try:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(demo())
        time.sleep(1)  # waiting for libindy thread complete
    except KeyboardInterrupt:
        print('')
