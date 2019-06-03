import asyncio
import json
import pprint
import asyncio
import time
import re
from indy.error import IndyError, ErrorCode
from indy import pool, ledger, wallet, did, crypto
from prep import prep , init ,read 



wallet_handle = 'wallet_handle'
my_vk = 'my_vk'
their_vk = 'their_vk'
msg = 'msg'


wallet_config = 'wallet_config'
wallet_credentials = 'wallet_credentials'


async def all(wallet_handle,my_vk,their_vk,msg,my_did,their_did):

    pre = await prep(wallet_handle, my_vk, their_vk, msg)
    wal = await init()
    rea = await read(wallet_handle, my_vk)    

    return(pre,wal,rea)
    
async def demo():
    wallet_handle, my_did, my_vk, their_did, their_vk = await init()

    while True:
        argv = input('> ').strip().split(' ')
        cmd = argv[0].lower()
        rest = ' '.join(argv[1:])
        if re.match(cmd, 'prep'):
            await prep(wallet_handle, my_vk, their_vk, rest)
        elif re.match(cmd, 'read'):
            await read(wallet_handle, my_vk)
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