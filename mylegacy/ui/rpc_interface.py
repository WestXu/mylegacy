from mylegacy.cli import rpc
from mylegacy.cli.rpc import client, utils

cli = client.Client("http://main.seed.starcoin.org:9850")


def transfer(sender_private_key: str, payee_adress: str, amount: float):
    return rpc.sign(
        cli,
        sender=rpc.private_key_to_account(sender_private_key),
        script=rpc.transfer(
            payee=utils.account_address(payee_adress),
            amount=int(amount * 1e9),
        ),
    )


def init_legacy(
    sender_private_key: str,
    payee_adress: str,
    total_value: float,
    times: int,
    freq: int,
):
    return rpc.sign(
        cli,
        sender=rpc.private_key_to_account(sender_private_key),
        script=rpc.init_legacy(
            payee=utils.account_address(payee_adress),
            total_value=int(total_value * 1e9),
            times=times,
            freq=freq,
        ),
    )


def redeem(sender_private_key: str, payer_adress: str):
    return rpc.sign(
        cli,
        sender=rpc.private_key_to_account(sender_private_key),
        script=rpc.redeem(
            payer=utils.account_address(payer_adress),
        ),
    )


def show_balance(address: str):
    print(rpc.get_stc_balance(cli, address=utils.account_address(address)))


if __name__ == "__main__":
    from fire import Fire

    Fire(
        {
            'transfer': transfer,
            'init_legacy': init_legacy,
            'redeem': redeem,
        }
    )
