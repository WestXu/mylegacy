import json
import subprocess
from pathlib import Path
from typing import List, Union

from loguru import logger
from rich import print as rprint


def shell_run(
    args: List[str], show_stdout=True, show_stderr=True
) -> subprocess.CompletedProcess:
    try:
        return subprocess.run(
            args,
            check=True,
            text=True,
            stdout=None if show_stdout else subprocess.PIPE,
            stderr=None if show_stderr else subprocess.PIPE,
        )
    except subprocess.CalledProcessError as e:
        logger.error(f':\n{e.stderr}')
        raise


def cli(connect: Union[str, Path], command: str, *args) -> dict:
    shell_run_args = [
        './starcoin-artifacts/starcoin',
        '--connect',
        str(connect),
        command,
    ] + list(args)

    logger.debug('starcoin% ' + ' '.join(shell_run_args[3:]))

    res = shell_run(
        shell_run_args,
        show_stdout=False,
        show_stderr=False,
    )
    if 'failed' in res.stderr:
        raise ValueError(f"{res.stderr}\n{res.stdout}")
    try:
        return json.loads(res.stdout)
    except json.decoder.JSONDecodeError:
        raise ValueError(f"Can't decode as json: \n{res.stdout}")


if __name__ == "__main__":
    print(
        cli('/tmp/59824f61bbebb8ed4d866d05fb88f315/dev/starcoin.ipc', 'account', 'list')
    )
