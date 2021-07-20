from fire import Fire

from move_cli import cli, rprint
from time import sleep


def deploy(ipc_file):
    res = cli(
        ipc_file,
        'dev',
        'compile',
        'myinstallments/module/MyInstallments.move',
        '-o',
        'tmp/',
    )
    compiled_mv_file = res['ok'][0]

    res = cli(ipc_file, 'account', 'unlock')
    address = res['ok']['address']

    payee_address = cli(ipc_file, 'account', 'create', '-p', 'Bob')['ok']['address']

    cli(ipc_file, 'dev', 'get-coin', '-v', '1000000')
    cli(ipc_file, 'dev', 'deploy', compiled_mv_file, '-b')

    cli(
        ipc_file,
        'account',
        'execute-function',
        '--function',
        f'{address}::MyInstallments::init_installments',
        '--arg',
        payee_address,
        '--arg',
        '100',
        '--arg',
        '10',
        '-b',
    )
    cli(
        ipc_file,
        'account',
        'execute-function',
        '--function',
        f'{address}::MyInstallments::pay',
        '-b',
    )
    rprint(
        cli(
            ipc_file,
            'state',
            'get',
            'resource',
            address,
            f'{address}::MyInstallments::Installments',
        )
    )
    rprint(cli(ipc_file, 'account', 'show', address))
    rprint(cli(ipc_file, 'account', 'show', payee_address))


if __name__ == "__main__":
    Fire(deploy)
