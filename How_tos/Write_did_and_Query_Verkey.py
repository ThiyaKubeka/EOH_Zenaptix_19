import asyncio
import json
import pprint

from indy import pool, ledger, wallet, did
from indy.error import IndyError, ErrorCode

from utils import get_pool_genesis_txn_path, PROTOCOL_VERSION
from Functions import pool_configuration,create_wallet,steward_did_verkey,trust_wallet,trust_anchor_wallet,Build_NYM,CLient_wallet,Client_did_and_verkey,GET_NYM,Clean_Up

pool_name = 'pool'
genesis_file_path = get_pool_genesis_txn_path(pool_name)

async def write_nym_and_query_verkey():
    try: 
        pool_handles =  await pool_configuration()
        wallet_handle = await create_wallet()
        steward_did,steward_verkey = await steward_did_verkey(wallet_handle)
        trust_handles = await trust_wallet()
        trust_anchor_did,trust_anchor_verkey = await trust_anchor_wallet(trust_handles)
        build_nym = await Build_NYM(steward_did,trust_anchor_did,trust_anchor_verkey,pool_handles,wallet_handle)
        Client_handle =  await CLient_wallet()
        client_did,client_verkey = await Client_did_and_verkey(Client_handle)
        get_nym = await GET_NYM(client_did,trust_anchor_did,pool_handles,trust_anchor_verkey)
        clean = await Clean_Up(wallet_handle,pool_handles)
        return steward_did,steward_verkey,trust_anchor_did,trust_anchor_verkey,build_nym,client_did,client_verkey,get_nym,clean
    except IndyError as e:
        print('Error occurred: %s' % e)


def main():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(write_nym_and_query_verkey())    
    loop.close()


if __name__ == '__main__':
    main()