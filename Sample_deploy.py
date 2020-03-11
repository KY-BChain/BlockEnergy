import sys
from fetchai.ledger.api import LedgerApi, TokenApi
from fetchai.ledger.contract import Contract
from fetchai.ledger.crypto import Entity, Address

# The contract we are going to load
contract_name = 'hello.etch'

# Connect the API to the testnet
try:
    api = LedgerApi(network="testnet")
except Exception as e:
    sys.exit(e)

# Load the contract and perform some basic checks on it
try:
    contract_text = open(contract_name, 'r').read()
except IOError as e:
    sys.exit('File not found')

if 0 == len(contract_text):
    print ("Contract is zero length.")
    sys.exit("Invalid contract")

# Private key of the address to deploy from
# WARNING: Unencrypted private keys should not be present in production code
entity = Entity(b'... your private key here ...')
address = Address(entity)

print ("Deploying contract:", contract_name, '\n')
print ("  Owner:", address)
print (" Length:", len(contract_text), "byte(s)")

# Perform the deployment now
try:
    contract = Contract(contract_text, entity)
    gas_fee = 600000
    api.sync(contract.create(api, entity, gas_fee), None, 0)
except Exception as e:
    sys.exit(e);

# Deployed, so we can now announce address and owner
print ("\nContract deployed:\n")
print ("Address:", contract.address)
print ("  Owner:", contract.owner)

# Confirm by querying the contract
print (" Output:", contract.query(api, 'sayHello'))
