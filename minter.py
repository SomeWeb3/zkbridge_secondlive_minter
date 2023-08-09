import time
from pathlib import Path
from random import randint, shuffle

from eth_account.signers.local import LocalAccount
from eth_typing import ChecksumAddress
from loguru import logger
from web3 import Account, Web3

from abi import BRIDGE_ABI, NFT_ABI
from config import (
    CHAINS_TO_BRIDGE,
    MINT_ADDRESS,
    NFT_BRIDGE,
    ONLY_MINT,
    OTHER_CHAIN_MINT,
    RANDOM_ORDER,
    RPC,
    TIME_TO_SLEEP_BETWEEN_BRIDGES,
    TIME_TO_SLEEP_BETWEEN_WALLETS,
    logger,
)

w3 = Web3(Web3.HTTPProvider(RPC))
nft_contract = w3.eth.contract(w3.to_checksum_address(MINT_ADDRESS), abi=NFT_ABI)
bridge_contract = w3.eth.contract(w3.to_checksum_address(NFT_BRIDGE), abi=BRIDGE_ABI)


def is_claimed(address: ChecksumAddress) -> bool:
    return nft_contract.functions.isClaimed(address).call()


def get_token_id(address: ChecksumAddress) -> int:
    return nft_contract.functions.tokenOfOwnerByIndex(address, 0).call()


def mint(wallet: LocalAccount) -> None:
    """Минт nft."""

    tx_dict = nft_contract.functions.claim().build_transaction(
        {
            "chainId": w3.eth.chain_id,
            "from": wallet.address,
            "gasPrice": w3.to_wei(1.1, "gwei"),
            "nonce": w3.eth.get_transaction_count(wallet.address),
        }
    )

    tx_dict["gas"] = w3.eth.estimate_gas(tx_dict)
    signed_txn = wallet.sign_transaction(tx_dict)
    txn_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
    logger.success(
        f"Mint from {wallet.address}. Tx: https://bscscan.com/tx/{txn_hash.hex()}"
    )


def bridge_nft(wallet: LocalAccount, to: str) -> None:
    """Отправка nft в другие сети."""

    token_id = get_token_id(wallet.address)

    fee = bridge_contract.functions.estimateFee(
        _token=w3.to_checksum_address(MINT_ADDRESS),
        _tokenId=token_id,
        _dstChainId=OTHER_CHAIN_MINT[to]["chain_id"],
        _recipient=wallet.address,
        _adapterParams=OTHER_CHAIN_MINT[to]["adapter_params"],
    ).call()

    tx_dict = bridge_contract.functions.transferNFT(
        _token=w3.to_checksum_address(MINT_ADDRESS),
        _tokenId=token_id,
        _dstChainId=OTHER_CHAIN_MINT[to]["chain_id"],
        _recipient=wallet.address,
        _adapterParams=OTHER_CHAIN_MINT[to]["adapter_params"],
    ).build_transaction(
        {
            "chainId": w3.eth.chain_id,
            "from": wallet.address,
            "value": fee,
            "gasPrice": w3.to_wei(1.1, "gwei"),
            "nonce": w3.eth.get_transaction_count(wallet.address),
        }
    )

    tx_dict["gas"] = w3.eth.estimate_gas(tx_dict)
    signed_txn = wallet.sign_transaction(tx_dict)
    txn_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
    logger.success(
        f"Bridge from {wallet.address} to {to} chain. Tx: https://bscscan.com/tx/{txn_hash.hex()}"
    )


def load_wallets() -> list[LocalAccount]:
    """Загрузка кошельков из текстовика."""

    file = Path("./wallets.txt").open("r")
    return [Account.from_key(line.replace("\n", "")) for line in file.readlines()]


def sleep(between_action: bool = False) -> None:
    """Функция сна."""

    range_ = (
        TIME_TO_SLEEP_BETWEEN_BRIDGES
        if between_action
        else TIME_TO_SLEEP_BETWEEN_WALLETS
    )
    time_to_sleep = randint(*range_)
    logger.info(f"Sleep {time_to_sleep} sec")
    time.sleep(time_to_sleep)


def do_work(wallet: LocalAccount) -> None:
    if not is_claimed(wallet.address):
        try:
            mint(wallet)
        except Exception as ex:
            logger.error(f"Error while mint. Error: {ex}")
    else:
        logger.info(f"Already minted on {wallet.address}")

    if ONLY_MINT:
        return

    try:
        while not is_claimed(wallet.address):
            time.sleep(1)
    except Exception as ex:
        logger.error(f"Error while check mint. Error: {ex}")

    chains_to_bridge = [chain for chain, arg in CHAINS_TO_BRIDGE.items() if arg]
    shuffle(chains_to_bridge)

    for chain in chains_to_bridge:
        try:
            bridge_nft(wallet, chain)
            if chain != chains_to_bridge[-1]:
                sleep(between_action=True)
        except Exception as ex:
            logger.error(f"Error while bridge to {chain}. Error: {ex}")


def main() -> None:
    wallets = load_wallets()
    logger.info(f"Load {len(wallets)} wallets.")

    if RANDOM_ORDER:
        shuffle(wallets)

    for wallet in wallets:
        try:
            do_work(wallet)
            if wallet != wallets[-1]:
                sleep()
        except Exception as ex:
            logger.error(f"Error {ex}")

    logger.info("Finish")


if __name__ == "__main__":
    main()
