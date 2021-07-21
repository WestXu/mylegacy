from fire import Fire

from move_cli import cli, logger, rprint


def deploy(ipc_file):
    logger.info("Compiling module...")
    res = cli(
        ipc_file,
        'dev',
        'compile',
        'mylegacy/module/MyLegacy.move',
        '-o',
        'tmp/',
    )
    compiled_mv_file = res['ok'][0]

    logger.info("Unlocking contract adress...")
    res = cli(ipc_file, 'account', 'unlock')
    contract_adress = res['ok']['address']

    logger.info("Creating payer account named Alice...")
    payer_address = cli(ipc_file, 'account', 'create', '-p', 'Alice')['ok']['address']
    logger.info("Unlocking Alice...")
    cli(ipc_file, 'account', 'unlock', '-p', 'Alice', payer_address)

    logger.info("Creating payee account named Bob...")
    payee_address = cli(ipc_file, 'account', 'create', '-p', 'Bob')['ok']['address']
    logger.info("Unlocking Bob...")
    cli(ipc_file, 'account', 'unlock', '-p', 'Bob', payee_address)

    logger.info("Contract address getting coin...")
    cli(ipc_file, 'dev', 'get-coin', '-v', '10')

    logger.info("Deploying contract to contract adress...")
    cli(ipc_file, 'dev', 'deploy', compiled_mv_file, '-b')

    logger.info("Payer Alice address getting coin...")
    cli(ipc_file, 'dev', 'get-coin', '-v', '10', payer_address)

    logger.info("Payer Alice init_legacy to Bob...")
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
        '--arg',
        '10',
        '-b',
    )

    logger.info("Showing payer Alice's legacy...")
    rprint(
        cli(
            ipc_file,
            'state',
            'get',
            'resource',
            payer_address,
            f'{contract_adress}::MyLegacy::Legacy',
        )['ok']['json']
    )

    logger.info("Payee Bob address getting coin...")
    cli(ipc_file, 'dev', 'get-coin', '-v', '10', payee_address)

    logger.info("Payee Bob redeeming his legacy...")
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

    logger.info("Showing again payer Alice's legacy...")
    rprint(
        cli(
            ipc_file,
            'state',
            'get',
            'resource',
            payer_address,
            f'{contract_adress}::MyLegacy::Legacy',
        )['ok']['json']
    )

    logger.info("Showing payer Alice's account...")
    rprint(cli(ipc_file, 'account', 'show', payer_address))

    logger.info("Showing payee Bob's account...")
    rprint(cli(ipc_file, 'account', 'show', payee_address))


if __name__ == "__main__":
    Fire(deploy)
