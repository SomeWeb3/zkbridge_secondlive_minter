BRIDGE_ABI = [
    {
        "inputs": [
            {"internalType": "address", "name": "_token", "type": "address"},
            {"internalType": "uint256", "name": "_tokenId", "type": "uint256"},
            {"internalType": "uint16", "name": "_dstChainId", "type": "uint16"},
            {"internalType": "address", "name": "_recipient", "type": "address"},
            {"internalType": "bytes", "name": "_adapterParams", "type": "bytes"},
        ],
        "name": "transferNFT",
        "outputs": [
            {"internalType": "uint64", "name": "currentNonce", "type": "uint64"}
        ],
        "stateMutability": "payable",
        "type": "function",
    },
    {
        "inputs": [
            {"internalType": "address", "name": "_token", "type": "address"},
            {"internalType": "uint256", "name": "_tokenId", "type": "uint256"},
            {"internalType": "uint16", "name": "_dstChainId", "type": "uint16"},
            {"internalType": "address", "name": "_recipient", "type": "address"},
            {"internalType": "bytes", "name": "_adapterParams", "type": "bytes"},
        ],
        "name": "estimateFee",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function",
    },
]
NFT_ABI = [
    {
        "inputs": [{"internalType": "address", "name": "", "type": "address"}],
        "name": "isClaimed",
        "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [
            {"internalType": "address", "name": "owner", "type": "address"},
            {"internalType": "uint256", "name": "index", "type": "uint256"},
        ],
        "name": "tokenOfOwnerByIndex",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [],
        "name": "claim",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "stateMutability": "nonpayable",
        "type": "function",
    },
]
