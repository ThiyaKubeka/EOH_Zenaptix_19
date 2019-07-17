import asyncio
import json
import pprint
import random
from indy import pool, ledger, wallet, did
from indy.error import IndyError, ErrorCode

from utils import get_pool_genesis_txn_path, PROTOCOL_VERSION

pool_name = 'pool'
genesis_file_path = get_pool_genesis_txn_path(pool_name)




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
        except IndyError:
            await pool.delete_pool_ledger_config(config_name=pool_name)
            await pool.create_pool_ledger_config(config_name=pool_name, config=pool_config)
        print_log('\n2. Open ledger and get handle\n')
        pool_handle = await pool.open_pool_ledger(config_name=pool_name, config=None)
        return(pool_handle)
        
async def request():        
        a = str(random.randint(0,9))
        for x in range(9):
                        a= a + str(random.randint(0,9))
     
        steward_did_for_faber = 'did_for_faber'
        connection_request = {steward_did_for_faber: json.dumps({'did':steward_did_for_faber, 'nonce':a})} 
        print(x)

        return(connection_request)

