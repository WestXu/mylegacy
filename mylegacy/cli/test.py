from fire import Fire

from move_cli import cli, logger, rprint


def deploy(connect):
    logger.info("Creating contract account named White...")
    contract_address = cli(connect, 'account', 'create', '-p', 'White')['ok']['address']
    logger.info("Unlocking White...")
    cli(connect, 'account', 'unlock', '-p', 'White', contract_address)

    logger.info("Compiling module...")
    res = cli(
        connect,
        'dev',
        'compile',
        'mylegacy/module/MyLegacy.move',
        '-s',
        contract_address,
        '-o',
        'tmp/',
    )
    compiled_mv_file = res['ok'][0]

    logger.info("Contract address getting coin...")
    cli(connect, 'dev', 'get-coin', '-v', '100', contract_address)

    logger.info("Deploying contract to contract address...")
    cli(connect, 'dev', 'deploy', compiled_mv_file, '-b')

    logger.info("Creating payer account named Alice...")
    payer_address = cli(connect, 'account', 'create', '-p', 'Alice')['ok']['address']
    logger.info("Unlocking Alice...")
    cli(connect, 'account', 'unlock', '-p', 'Alice', payer_address)

    logger.info("Creating payee account named Bob...")
    payee_address = cli(connect, 'account', 'create', '-p', 'Bob')['ok']['address']
    logger.info("Unlocking Bob...")
    cli(connect, 'account', 'unlock', '-p', 'Bob', payee_address)

    logger.info("Payer Alice address getting coin...")
    cli(connect, 'dev', 'get-coin', '-v', '100', payer_address)

    logger.info("Payer Alice init_legacy to Bob...")
    cli(
        connect,
        'account',
        'execute-function',
        '--function',
        f'{contract_address}::MyLegacy::init_legacy',
        '-s',
        payer_address,
        '--arg',
        payee_address,
        '--arg',
        '1000000000',
        '--arg',
        '10',
        '--arg',
        '10',
        '-b',
    )

    logger.info("Showing payer Alice's legacy...")
    rprint(
        cli(
            connect,
            'state',
            'get',
            'resource',
            payer_address,
            f'{contract_address}::MyLegacy::Legacy',
        )['ok']['json']
    )

    logger.info("Payee Bob address getting coin...")
    cli(connect, 'dev', 'get-coin', '-v', '100', payee_address)

    logger.info("Payee Bob redeeming his legacy...")
    cli(
        connect,
        'account',
        'execute-function',
        '--function',
        f'{contract_address}::MyLegacy::redeem',
        '-s',
        payee_address,
        '--arg',
        payer_address,
        '-b',
    )

    logger.info("Showing again payer Alice's legacy...")
    rprint(
        cli(
            connect,
            'state',
            'get',
            'resource',
            payer_address,
            f'{contract_address}::MyLegacy::Legacy',
        )['ok']['json']
    )

    logger.info("Showing payer Alice's account...")
    rprint(cli(connect, 'account', 'show', payer_address)['ok']['balances'])

    logger.info("Showing payee Bob's account...")
    rprint(cli(connect, 'account', 'show', payee_address)['ok']['balances'])


if __name__ == "__main__":
    Fire(deploy)
