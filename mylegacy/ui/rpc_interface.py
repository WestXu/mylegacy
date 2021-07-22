from mylegacy.cli import rpc
from mylegacy.cli.rpc import client, AccountAddress


def transfer(sender_private_key: str, payee_adress: str, amount: float):
    return rpc.transfer(
        cli,
        sender=rpc.private_key_to_account(sender_private_key),
        payee=AccountAddress.from_hex(payee_adress),
        amount=int(amount * 1e9),
    )


def init_legacy(
    sender_private_key: str,
    payee_adress: str,
    total_value: float,
    times: int,
    freq: int,
):
    return rpc.init_legacy(
        cli,
        sender=rpc.private_key_to_account(sender_private_key),
        payee=AccountAddress.from_hex(payee_adress),
        total_value=int(total_value * 1e9),
        times=times,
        freq=freq,
    )


def redeem(sender_private_key: str, payer_adress: str):
    return rpc.redeem(
        cli,
        sender=rpc.private_key_to_account(sender_private_key),
        payer=AccountAddress.from_hex(payer_adress),
    )


def show_balance(address: str):
    print(rpc.get_stc_balance(cli, address=AccountAddress.from_hex(address)))


if __name__ == "__main__":
    from fire import Fire

    cli = client.Client("http://barnard.seed.starcoin.org:9850")

    Fire([transfer, init_legacy, redeem])
