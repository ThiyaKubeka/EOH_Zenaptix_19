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
from Write_DID_Func import pool_configuration,create_steward_wallet, Steward_did_and_verkey,create_faber_wallet,Faber_did_and_verkey,steward_keys_for_faber,add_to_ledger,print_log,add_faber_ledger,pools,pool_close
from steward_wallet import wall, keys, add_faber_to_ledger,pool_config,close,pool_con
from new import pool_configurat, wal, Client,faber_steward, Faber_did_and_verkey_for_steward
from build import fab_keys,Faber,pools,add_ledger,clos

async def prep(Wallet_handle, steward_verkey,faber_verkey_for_steward, msg):
    msg = bytes(msg, "utf-8")
    encrypted = await crypto.auth_crypt(Wallet_handle, steward_verkey, faber_verkey_for_steward, msg)
    #encrypted = await crypto.anon_crypt(steward_verkey, msg)
    print('encrypted = %s' % repr(encrypted))
    with open('message.dat', 'wb') as f:
        f.write(encrypted)
    print('prepping %s' % msg)


async def init():
    print_log('\n. pool\n')
    print_log('\n. Relation\n')
    print_log('\n1. Steward\n')
    print_log('\n Welcome To The Sovrin Community\n')
    time.sleep
    print_log('\n1. Steward\n')
    print_log('\n2. Faber College\n')
    me = input('Please Select: ').strip()
    if me == '1':
        pool_handle = await pool_configuration()
       
        Wallet_handle = await create_steward_wallet()
        steward_did,steward_verkey = await Steward_did_and_verkey(Wallet_handle)    
        steward_did_for_faber,steward_verkey_for_faber = await steward_keys_for_faber(Wallet_handle) 
        time.sleep(1) 
        print_log('\n Add Steward DID and verkey for faber to the ledger\n')
        build_nym = await add_to_ledger(Wallet_handle,steward_did,steward_verkey,steward_did_for_faber,steward_verkey_for_faber,pool_handle)
        closes = await pool_close(pool_handle)
        faber = input("Faber's DID and verkey? ").strip().split(' ')
        return Wallet_handle, steward_did, steward_verkey,faber[0],faber[1]
    elif me == '2':
        #pool_handle = await pool_configuration()
        #close = await pool_config(pool_handle)
        faber_handle_for = await faber_steward()
        print('faber handle = %s' % faber_handle_for)
        faber_did_for_steward,faber_verkey_for_steward = await Faber_did_and_verkey_for_steward(faber_handle_for)
        #time.sleep(1)
        #W#allet_handle = await create_steward_wallet()
        #time.sleep(1)
        #steward_did,steward_verkey = await Steward_did_and_verkey(Wallet_handle)  
        #time.sleep(1)
        #steward_did_for_faber,steward_verkey_for_faber = await steward_keys_for_faber(Wallet_handle)  
        #time.sleep(1)
        #build_nym = await add_to_ledger(Wallet_handle,steward_did,steward_verkey,steward_did_for_faber,steward_verkey_for_faber,pool_handle)
        #time.sleep
        #print('faber did and verkey = %s %s' % (faber_did, faber_verkey))
        steward = input("steward's DID and verkey? ").strip().split(' ')
        return faber_handle_for,faber_did_for_steward ,faber_verkey_for_steward ,steward[0],steward[1]
    return Wallet_handle, steward_did,steward_verkey,faber_did_for_steward,faber_verkey_for_steward

async def sent():
  print_log('\n Details sent\n')  
async def thanks():
    print_log('\n ONBOARDING COMPLETE\n')
    print_log('\n THANK YOU\n')

async def sending():
    print_log('\n1. Sending connection response..............\n')



async def send():
     print_log('\n1. REQUESTING..............\n')

async def approve():
    
    print_log('\n1. connection response\n')
    Wall_handles = await wall()
    Did_for_steward,Verkey_for_steward = await keys(Wall_handles)
    nonce = [1,2,3,4,5,6,7,8,9] 
    shuffle(nonce)
    print('did for steward  =  %s' % (Did_for_steward))
    print('verkey for steward = %s'% (Verkey_for_steward))      
    print('nonce = %s' % (nonce))

async def Query(faber_handle):
    faber_did,faber_verkey = await Faber_did_and_verkey(faber_handle)


async def accept(Wallet_handle):
    print_log('\n1. Accept connection request\n')
    print_log('\n2. Decline connection request\n')
    me = input('Please Select: ').strip()
    if me == '1':
        steward_did_for_faber, steward_verkey_for_faber = await did.create_and_store_my_did(Wallet_handle, "{}")
        nonce = [1,2,3,4,5,6,7,8,9] 
        shuffle(nonce)
        print('steward did for faber =  %s' % (steward_did_for_faber))
        print('steward verkey for faber = %s'% (steward_verkey_for_faber))      
        print('nonce = %s' % (nonce))
        time.sleep(3)
        print_log('\n. Proceed to create wallet?.\n')
        print_log('\n1. Yes.\n')
        print_log('\n2. No.\n')
        me = input('Please Select: ').strip()
        if me == '1':
            print_log('\n1. CREATING WALLET.\n')
            faber_handle = await create_faber_wallet()
            print('faber handle = %s' % faber_handle)
            faber_did,faber_verkey = await Faber_did_and_verkey(faber_handle)
        else:
            print('bye')
        return faber_handle  
    else:
        print('bye')
    return faber_handle,faber_did,faber_verkey
    
async def trust_a():
    print_log('\n Sending new Did and verkey to steward\n')
    Wal = await wal()
    print('faber handle = %s' % Wal)
    F_did,F_verkey = await Client(Wal)

    return F_did,F_verkey,Wal

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
    
    Wallet_handle, steward_did,steward_verkey,faber_did_for_steward,faber_verkey_for_steward = await init()

   

        
    

    while True:
        argv = input('> ').strip().split(' ')
        cmd = argv[0].lower()
        rest = ' '.join(argv[1:])
        if re.match(cmd, 'prep'):
            await prep(Wallet_handle, steward_verkey, faber_verkey_for_steward, rest)
        elif re.match(cmd, 'read'):
            await read(Wallet_handle, steward_verkey)
        elif re.match(cmd, 'send'):
            await send()
        elif re.match(cmd, 'recieve'):
            await accept(Wallet_handle)
        elif re.match(cmd, 'sending'):
            await sending()
        elif re.match(cmd, 'approve'):
            print_log('\n1. Accept connection response.\n')
            print_log('\n2. Decline. connection response\n')
            me = input('Please Select: ').strip()
            if me == '1':
                await approve()
            else:
                print('bye')
            time.sleep(1)


            print_log('\n PREPARING TO BUILD NYM....\n')
          
            pooles = await pools()
            faber = await Faber()
            print('faber handle = %s' % faber)
            Faber_did,Faber_verkey = await Faber_did_and_verkey(faber)
            build = await add_ledger(Wallet_handle,steward_did,steward_verkey,Faber_did,Faber_verkey,pooles)
            closs = await clos(pooles)
           
        elif re.match(cmd, 'get'):
          faber_handle = await create_faber_wallet()
          faber_did,faber_verkey = await Faber_did_and_verkey(faber_handle)

        elif re.match(cmd, 'i'):
             await trust_a()    
        elif re.match(cmd, 'ok'):
             await sent()

        elif re.match(cmd, 'query'):
            pole = await pool_configurat()
            Wal = await wal()
            print('faber handle = %s' % Wal)
            F_did,F_verkey = await Client(Wal)
            time.sleep(1)
            print_log('\n. Preparing to give Faber college role of Trust Anchor.\n')
            time.sleep(1)
            build = await add_faber_ledger(Wallet_handle,steward_did,steward_verkey,F_did,F_verkey,pole)
            time.sleep(0.8)

        elif re.match(cmd, 'done'):
            await thanks()
            break
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
