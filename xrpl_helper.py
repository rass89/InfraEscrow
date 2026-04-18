import os
import hashlib
import xrpl
from xrpl.clients import JsonRpcClient
from xrpl.wallet import Wallet
from xrpl.transaction import submit_and_wait
from datetime import datetime, timedelta
from xrpl.utils import datetime_to_ripple_time
from xrpl.models.transactions import (
    CredentialCreate, 
    CredentialAccept, 
    EscrowCreate, 
    EscrowFinish
)
from xrpl.asyncio.transaction import XRPLReliableSubmissionException

# Back to the stable, fast Testnet
client = JsonRpcClient("https://s.altnet.rippletest.net:51234")

def issue_credential(issuer_seed, subject_address):
    issuer_wallet = Wallet.from_seed(issuer_seed)
    cert_hex = "5374727563747572616C5F43657274".ljust(64, '0') 
    
    tx = CredentialCreate(
        account=issuer_wallet.address,
        subject=subject_address,
        credential_type=cert_hex
    )
    
    try:
        response = submit_and_wait(tx, client, issuer_wallet)
        return response.result["hash"]
    except XRPLReliableSubmissionException as e:
        if "tecDUPLICATE" in str(e):
            return "ALREADY_ISSUED"
        raise e

def accept_credential(inspector_seed, issuer_address):
    inspector_wallet = Wallet.from_seed(inspector_seed)
    cert_hex = "5374727563747572616C5F43657274".ljust(64, '0') 
    
    tx = CredentialAccept(
        account=inspector_wallet.address,
        issuer=issuer_address,
        credential_type=cert_hex
    )
    
    try:
        response = submit_and_wait(tx, client, inspector_wallet)
        return response.result["hash"]
    except XRPLReliableSubmissionException as e:
        if "tecDUPLICATE" in str(e):
            return "ALREADY_ACCEPTED"
        raise e
    

def accept_credential(inspector_seed, issuer_address):
    inspector_wallet = Wallet.from_seed(inspector_seed)
    cert_hex = "5374727563747572616C5F43657274".ljust(64, '0') 
    
    tx = CredentialAccept(
        account=inspector_wallet.address,
        issuer=issuer_address,
        credential_type=cert_hex
    )
    
    try:
        response = submit_and_wait(tx, client, inspector_wallet)
        return response.result["hash"]
    except XRPLReliableSubmissionException as e:
        if "tecDUPLICATE" in str(e):
            return "ALREADY_ACCEPTED"
        raise e

def create_inspection_escrow(funder_seed, inspector_address, amount_xrp=50):
    funder_wallet = Wallet.from_seed(funder_seed)
    preimage = os.urandom(32)
    condition_hex = hashlib.sha256(preimage).hexdigest().upper()
    formatted_condition = "A0258020" + condition_hex + "810120"
    
    cancel_date = datetime.now() + timedelta(days=1) 
    cancel_ripple_time = datetime_to_ripple_time(cancel_date)
    
    # Wrap the logic in an EscrowCreate object
    tx = EscrowCreate(
        account=funder_wallet.address,
        destination=inspector_address,
        amount=xrpl.utils.xrp_to_drops(amount_xrp),
        condition=formatted_condition,
        cancel_after=cancel_ripple_time
    )
    
    response = submit_and_wait(tx, client, funder_wallet)
    sequence = response.result["tx_json"]["Sequence"]
    
    return {
        "hash": response.result["hash"], 
        "sequence": sequence, 
        "condition": condition_hex, 
        "preimage": preimage.hex()
    }

def release_escrow(funder_address, sequence, condition_hex, preimage_hex, trigger_seed):
    trigger_wallet = Wallet.from_seed(trigger_seed)
    formatted_condition = "A0258020" + condition_hex + "810120"
    formatted_fulfillment = "A0228020" + preimage_hex
    
    # Wrap the logic in an EscrowFinish object
    tx = EscrowFinish(
        account=trigger_wallet.address,
        owner=funder_address,
        offer_sequence=sequence,
        condition=formatted_condition,
        fulfillment=formatted_fulfillment
    )
    
    response = submit_and_wait(tx, client, trigger_wallet)
    return response.result["hash"]