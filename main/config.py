from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

import requests
from environs import Env

BASE_DIR = Path(__file__).resolve().parent.parent


@dataclass
class Config:
    global_config: dict
    mnemonics: str
    recipient_address: str
    gpus_count: int

    timeout: int
    iterations: int
    givers_count: int
    boost_factor: int

    @classmethod
    def init(cls) -> Config:
        env = Env()
        env.read_env(f"{BASE_DIR}/.env")

        try:
            with open(f"{BASE_DIR}/data/global-config.json", "r") as file:
                global_config = json.load(file)
        except FileNotFoundError:
            global_config = requests.get('https://ton.org/global-config.json').json()

        return cls(
            global_config=global_config,
            mnemonics=env.str("MNEMONICS"),
            recipient_address=env.str("RECIPIENT_ADDRESS"),
            gpus_count=env.int("GPUS_COUNT"),

            timeout=env.int("TIMEOUT"),
            iterations=env.int("ITERATIONS"),
            givers_count=env.int("GIVERS_COUNT"),
            boost_factor=env.int("BOOST_FACTOR"),
        )
