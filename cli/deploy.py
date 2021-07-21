from fire import Fire

from move_cli import cli, logger, rprint, shell_run


def deploy(dev_ipc_file, address):
    logger.info("Compiling module...")
    res = cli(
        dev_ipc_file,
        'dev',
        'compile',
        'mylegacy/module/MyLegacy.move',
        '-s',
        address,
        '-o',
        'tmp/',
    )
    compiled_mv_file = res['ok'][0]

    logger.info('Packaging...')
    res = cli(
        dev_ipc_file,
        "dev",
        "package",
        "-n",
        "mylegacy",
        "-o",
        "tmp",
        compiled_mv_file,
    )
    packaged_blob_file = res['ok']['file']

    logger.info('Converting binary to hex...')
    shell_run(["hexdump", "-v", "-e", '1/1 "%02x"', packaged_blob_file])
    print("\nGo deploy it at https://starmask-test-dapp.starcoin.org/")


if __name__ == "__main__":
    Fire(deploy)
