import asyncio
import os
import random
from asyncio import subprocess
from pathlib import Path

from pytoniq import LiteBalancer, WalletV4R2
from pytoniq_core import WalletMessage, Cell, Address
from pytoniq_core.boc.deserialize import BocError

from .config import BASE_DIR, Config
from .givers import givers

config = Config.init()
provider = LiteBalancer.from_config(config.global_config, trust_level=2)


async def get_pow_params(giver_address: str) -> tuple[int, int, int]:
    response = await provider.run_get_method(giver_address, "get_mining_status", [])
    return response[2], response[0], response[1]


async def mine_boc(gpu_id: int, giver_address: str, seed: int, complexity: int, _: int
                   ) -> tuple[bytes, str] | tuple[None, None]:
    iterations = 9999999999999999

    filename = f"{BASE_DIR}/bocs/{giver_address}.boc"
    command = (
        f"./data/pow-miner-cuda -vv -g {gpu_id} -F 128 "
        f"-t {config.timeout} {config.recipient_address} {seed} "
        f"{complexity} {iterations} {giver_address} {filename}"
    )

    try:
        proc = await asyncio.create_subprocess_shell(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        await asyncio.wait_for(proc.wait(), config.timeout)

    except asyncio.TimeoutError:
        ...

    if Path(filename).exists():
        boc = Path(filename).read_bytes()
        os.remove(filename)
        return boc, giver_address

    return None, None


async def mine_all_gpus() -> tuple[any]:
    tasks, count = [], 0
    giver_address = random.choice(givers)

    for gpu_id in range(config.gpus_count + 1):
        if count == config.gpus_count:
            break

        seed, complexity, iterations = await get_pow_params(giver_address)
        tasks.append(mine_boc(count, giver_address, seed, complexity, iterations))
        count += 1

    return await asyncio.gather(*tasks)


async def create_messages(wallet: WalletV4R2) -> WalletMessage | None:
    for boc, giver_address in await mine_all_gpus():
        if boc is not None:
            try:
                return wallet.create_wallet_internal_message(
                    destination=Address(giver_address),
                    value=int(0.08 * 1e9),
                    body=Cell.from_boc(boc)[0].to_slice().load_ref(),
                )
            except BocError:
                continue
    return None


async def main():
    await provider.start_up()
    wallet = await WalletV4R2.from_mnemonic(provider, config.mnemonics)

    while True:
        try:
            message = await create_messages(wallet)
            if message is not None:
                print(f"Mined! Sending messages...")
                await wallet.raw_transfer(msgs=[message])
                print("Messages sent!")
            else:
                print(f"Not mined. Retrying...")
        except Exception as e:
            print(e)


if __name__ == "__main__":
    asyncio.run(main())
