from loguru import logger

logger.add("log/debug.log")

TIME_TO_SLEEP_BETWEEN_WALLETS = (60, 100)  # Границы задержки между кошельками
TIME_TO_SLEEP_BETWEEN_BRIDGES = (25, 50)  # Границы задержки между бриджами

RANDOM_ORDER = True  # True / False, случайный порядок кошельков при выполнении
ONLY_MINT = False  # True - Только минт, без отправки в другие сети. False - минт и отправка в сети, выбранные ниже

CHAINS_TO_BRIDGE = {
    "arb": True,  # Включение и выключение сетей при бридже
    "scroll": True,  # True / False
    "combo": True,
    "opbnb": True,
}
RPC = "https://rpc.ankr.com/bsc"

MINT_ADDRESS = "0x8fc516dcdcc1f25f9c1352fdbdc8f3b4e164e596"
NFT_BRIDGE = "0x4d4b02D4d4188A1d0Cf3D8290e9481321B94d864"

OTHER_CHAIN_MINT = {
    "arb": {
        "chain_id": 8,
        "adapter_params": "0x00010000000000000000000000000000000000000000000000000000000000055730",
    },
    "scroll": {
        "chain_id": 114,
        "adapter_params": "0x",
    },
    "combo": {
        "chain_id": 120,
        "adapter_params": "0x",
    },
    "opbnb": {
        "chain_id": 116,
        "adapter_params": "0x",
    },
}
