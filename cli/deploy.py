from fire import Fire

from move_cli import cli, rprint
from time import sleep


def deploy(ipc_file):
    res = cli(
        ipc_file,
        'dev',
        'compile',
        'mylegacy/module/MyLegacy.move',
        '-o',
        'tmp/',
    )
    compiled_mv_file = res['ok'][0]

    res = cli(ipc_file, 'account', 'unlock')
    contract_adress = res['ok']['address']

    payer_address = cli(ipc_file, 'account', 'create', '-p', 'Alice')['ok']['address']
    cli(ipc_file, 'account', 'unlock', '-p', 'Alice', payer_address)

    payee_address = cli(ipc_file, 'account', 'create', '-p', 'Bob')['ok']['address']
    cli(ipc_file, 'account', 'unlock', '-p', 'Bob', payee_address)

    cli(ipc_file, 'dev', 'get-coin', '-v', '10')
    cli(ipc_file, 'dev', 'deploy', compiled_mv_file, '-b')

    cli(ipc_file, 'dev', 'get-coin', '-v', '10', payer_address)
    cli(
        ipc_file,
        'account',
        'execute-function',
        '--function',
        f'{contract_adress}::MyLegacy::init_legacy',
        '-s',
        payer_address,
        '--arg',
        payee_address,
        '--arg',
        '100',
        '--arg',
        '10',
        '-b',
    )

    rprint(
        cli(
            ipc_file,
            'state',
            'get',
            'resource',
            payer_address,
            f'{contract_adress}::MyLegacy::Legacy',
        )
    )

    cli(ipc_file, 'dev', 'get-coin', '-v', '10', payee_address)

    cli(
        ipc_file,
        'account',
        'execute-function',
        '--function',
        f'{contract_adress}::MyLegacy::redeem',
        '-s',
        payee_address,
        '--arg',
        payer_address,
        '-b',
    )
    rprint(
        cli(
            ipc_file,
            'state',
            'get',
            'resource',
            payer_address,
            f'{contract_adress}::MyLegacy::Legacy',
        )
    )
    rprint(cli(ipc_file, 'account', 'show', payer_address))
    rprint(cli(ipc_file, 'account', 'show', payee_address))


if __name__ == "__main__":
    Fire(deploy)
