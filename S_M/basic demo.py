import asyncio
import time
import re
import json
import pprint


from indy import crypto, did, wallet
from indy.error import IndyError, ErrorCode
from utils import get_pool_genesis_txn_path, PROTOCOL_VERSION
from Write_DID_Func import create_steward_wallet, Steward_did_and_verkey,inputs,create_faber_wallet,Faber_did_and_verkey

async def prep(Wallet_handle, steward_verkey, faber_verkey, msg):
    msg = bytes(msg, "utf-8")
    encrypted = await crypto.auth_crypt(Wallet_handle, steward_verkey, faber_verkey, msg)
    #encrypted = await crypto.anon_crypt(steward_verkey, msg)
    print('encrypted = %s' % repr(encrypted))
    with open('message.dat', 'wb') as f:
        f.write(encrypted)
    print('prepping %s' % msg)


async def init():
    me = await inputs()
    if me == 'steward':
        Wallet_handle = await create_steward_wallet(me)
        steward_did,steward_verkey = await Steward_did_and_verkey(Wallet_handle)
    
        print('steward_did and verkey = %s %s' % (steward_did, steward_verkey))

        faber = input("Faber's DID and verkey? ").strip().split(' ')
        return Wallet_handle, steward_did, steward_verkey,faber[0],faber[1]
    elif me == 'faber':
        
        faber_handle = await create_faber_wallet(me)
        faber_did,faber_verkey = await Faber_did_and_verkey(faber_handle)
        steward = input("steward's DID and verkey? ").strip().split(' ')
        
        return faber_handle,faber_did ,faber_verkey ,steward[0] ,steward[1]
    return Wallet_handle, steward_did,steward_verkey,faber_did,faber_verkey

async def read(Wallet_handle, steward_verkey):
    with open('message.dat', 'rb') as f:
        encrypted = f.read()
    decrypted = await crypto.auth_decrypt(Wallet_handle, steward_verkey, encrypted)
    # decrypted = await crypto.anon_decrypt(wallet_handle, my_vk, encrypted)
    print(decrypted)

async def demo():
    Wallet_handle, steward_did,steward_verkey,faber_did,faber_verkey = await init()
    

    while True:
        argv = input('> ').strip().split(' ')
        cmd = argv[0].lower()
        rest = ' '.join(argv[1:])
        if re.match(cmd, 'prep'):
            await prep(Wallet_handle, steward_verkey, faber_verkey, rest)
        elif re.match(cmd, 'read'):
            await read(Wallet_handle, steward_verkey)
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
