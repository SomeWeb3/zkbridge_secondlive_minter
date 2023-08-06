import time
from pathlib import Path
from random import randint, shuffle

from eth_account.signers.local import LocalAccount
from loguru import logger
from web3 import Account, Web3

TIME_TO_SLEEP = (50, 100)
RANDOM_ORDER = True  # True / False
RPC = "https://rpc.ankr.com/bsc"
MINT_ADDRESS = "0x8fc516dcdcc1f25f9c1352fdbdc8f3b4e164e596"
DATA = "0x4e71d92d0000000000000000000000000000000000000000000000000000000000000000"


logger.add("log/debug.log")


w3 = Web3(Web3.HTTPProvider(RPC))


def mint(wallet: LocalAccount) -> None:
    """Минт nft."""

    tx_dict = {
        "chainId": w3.eth.chain_id,
        "from": wallet.address,
        "to": w3.to_checksum_address(MINT_ADDRESS),
        "gasPrice": w3.to_wei(1.1, "gwei"),
        "nonce": w3.eth.get_transaction_count(wallet.address),
        "data": DATA,
    }

    tx_dict["gas"] = w3.eth.estimate_gas(tx_dict)
    signed_txn = wallet.sign_transaction(tx_dict)
    txn_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
    logger.success(
        f"Mint from {wallet.address}. Tx: https://bscscan.com/tx/{txn_hash.hex()}"
    )


def load_wallets() -> list[LocalAccount]:
    """Загрузка кошельков из текстовика."""

    file = Path("./wallets.txt").open()
    return [Account.from_key(line.replace("\n", "")) for line in file.readlines()]


def main():
    wallets = load_wallets()
    logger.info(f"Load {len(wallets)} wallets.")

    if RANDOM_ORDER:
        shuffle(wallets)

    for wallet in wallets:
        try:
            mint(wallet)
            if wallet != wallets[-1]:
                time_to_sleep = randint(*TIME_TO_SLEEP)
                logger.info(f"Sleep {time_to_sleep} sec")
                time.sleep(time_to_sleep)
        except Exception as ex:
            logger.error(f"Error {ex}")
    logger.info("Finish")


if __name__ == "__main__":
    main()
