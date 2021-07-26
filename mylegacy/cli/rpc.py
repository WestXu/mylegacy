from cryptography.hazmat.primitives.asymmetric.ed25519 import (
    Ed25519PrivateKey,
    Ed25519PublicKey,
)
from starcoin import bcs
from starcoin import serde_types as st
from starcoin import starcoin_stdlib as stdlib
from starcoin import starcoin_types as types
from starcoin.sdk import auth_key, client, local_account, utils
from starcoin.starcoin_types import (
    AccountAddress,
    Identifier,
    ModuleId,
    ScriptFunction,
    TransactionPayload__ScriptFunction,
)


def sign(
    cli: client.Client,
    sender: local_account.LocalAccount,
    script: TransactionPayload__ScriptFunction,
):
    seq_num = cli.get_account_sequence(
        "0x" + sender.account_address.bcs_serialize().hex()
    )

    # expired after 12 hours
    expiration_timestamp_secs = int(cli.node_info().get('now_seconds')) + 43200

    raw_txn = types.RawTransaction(
        sender=sender.account_address,
        sequence_number=seq_num,
        payload=script,
        max_gas_amount=10000000,
        gas_unit_price=1,
        gas_token_code="0x1::STC::STC",
        expiration_timestamp_secs=expiration_timestamp_secs,
        chain_id=types.ChainId(st.uint8(251)),
    )

    txn = sender.sign(raw_txn)
    return cli.submit(txn)


def transfer(
    payee: AccountAddress,
    amount: st.uint128,
) -> TransactionPayload__ScriptFunction:
    return stdlib.encode_peer_to_peer_v2_script_function(
        token_type=utils.currency_code("STC"),
        payee=payee,
        amount=amount,
    )


def init_legacy(
    payee: AccountAddress,
    total_value: int,
    times: int,
    freq: int,
) -> TransactionPayload__ScriptFunction:
    return TransactionPayload__ScriptFunction(
        value=ScriptFunction(
            module=ModuleId(
                address=utils.account_address("0xe11eA1971774192FD96bA7FCA842128F"),
                name=Identifier("MyLegacy"),
            ),
            function=Identifier("init_legacy"),
            ty_args=[],
            args=[
                bcs.serialize(payee, AccountAddress),
                bcs.serialize(total_value, st.uint64),
                bcs.serialize(times, st.uint64),
                bcs.serialize(freq, st.uint64),
            ],
        )
    )


def redeem(payer: AccountAddress) -> TransactionPayload__ScriptFunction:
    return TransactionPayload__ScriptFunction(
        value=ScriptFunction(
            module=ModuleId(
                address=utils.account_address("0xe11eA1971774192FD96bA7FCA842128F"),
                name=Identifier("MyLegacy"),
            ),
            function=Identifier("redeem"),
            ty_args=[],
            args=[
                bcs.serialize(payer, AccountAddress),
            ],
        )
    )


def private_key_to_account(private_key_hex: str) -> local_account.LocalAccount:
    private_key = Ed25519PrivateKey.from_private_bytes(bytes.fromhex(private_key_hex))
    return local_account.LocalAccount(private_key)


def public_key_to_address(
    payee_public_key_hex: str,
) -> AccountAddress:
    pk = Ed25519PublicKey.from_public_bytes(bytes.fromhex(payee_public_key_hex))
    payee_auth_key = auth_key.AuthKey.from_public_key(pk)
    payee_address = payee_auth_key.account_address()
    return payee_address


def get_stc_balance(cli: client.Client, address: AccountAddress) -> int:
    return cli.get_account_token(utils.account_address_hex(address), "STC", "STC")
