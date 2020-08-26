VALIDATOR_ABI = '''[
    {
        "constant": true,
        "inputs": [
            {
                "internalType": "bytes32[]",
                "name": "question",
                "type": "bytes32[]"
            },
            {
                "internalType": "bytes32[]",
                "name": "answer",
                "type": "bytes32[]"
            }
        ],
        "name": "is_answer_correct",
        "outputs": [
            {
                "internalType": "bool",
                "name": "",
                "type": "bool"
            }
        ],
        "payable": false,
        "stateMutability": "pure",
        "type": "function"
    },
    {
        "constant": true,
        "inputs": [
            {
                "internalType": "bytes32[]",
                "name": "question",
                "type": "bytes32[]"
            }
        ],
        "name": "is_valid_question",
        "outputs": [
            {
                "internalType": "bool",
                "name": "",
                "type": "bool"
            }
        ],
        "payable": false,
        "stateMutability": "pure",
        "type": "function"
    }
]'''
VALIDATOR_SOL = {
    "linkReferences": {},
    "object": "608060405234801561001057600080fd5b506104f3806100206000396000f3fe608060405234801561001057600080fd5b50600436106100365760003560e01c80631bf28f831461003b57806351428bc0146100cc575b600080fd5b6100b26004803603602081101561005157600080fd5b810190808035906020019064010000000081111561006e57600080fd5b82018360208201111561008057600080fd5b803590602001918460208302840111640100000000831117156100a257600080fd5b90919293919293905050506101b2565b604051808215151515815260200191505060405180910390f35b610198600480360360408110156100e257600080fd5b81019080803590602001906401000000008111156100ff57600080fd5b82018360208201111561011157600080fd5b8035906020019184602083028401116401000000008311171561013357600080fd5b90919293919293908035906020019064010000000081111561015457600080fd5b82018360208201111561016657600080fd5b8035906020019184602083028401116401000000008311171561018857600080fd5b90919293919293905050506101e5565b604051808215151515815260200191505060405180910390f35b60006003838390501480156101dd57506000801b838360008181106101d357fe5b9050602002013514155b905092915050565b600060028383905014610260576040517f08c379a000000000000000000000000000000000000000000000000000000000815260040180806020018281038252601a8152602001807f416e73776572206c656e6774682073686f756c6420626520322e00000000000081525060200191505060405180910390fd5b600061027e8686600081811061027257fe5b905060200201356104b1565b9050600061029e8787600181811061029257fe5b905060200201356104b1565b905060006102be888860028181106102b257fe5b905060200201356104b1565b905060006102de878760008181106102d257fe5b905060200201356104b1565b905060006102fe888860018181106102f257fe5b905060200201356104b1565b905060008190506000821215610315578160000390505b60008290506000620f424090505b6001600a838161032f57fe5b0513801561033d5750600181135b1561036157600a828161034c57fe5b059150600a818161035957fe5b059050610323565b60008185888a0302878b020102905060008286898b0302888c60000302010290506000858312801561039557508560000383135b806103ad575085821280156103ac57508560000382135b5b9050606060076040519080825280602002602001820160405280156103e15781602001602082028038833980820191505090505b5090508b816000815181106103f257fe5b6020026020010181815250508a8160018151811061040c57fe5b602002602001018181525050898160028151811061042657fe5b602002602001018181525050888160038151811061044057fe5b602002602001018181525050878160048151811061045a57fe5b602002602001018181525050838160058151811061047457fe5b602002602001018181525050828160068151811061048e57fe5b602002602001018181525050819c50505050505050505050505050949350505050565b60008160001c905091905056fea265627a7a72315820a9e912b8c8f6735edd269586990e2c40e066dd6af0dae606585391086d1dbe3a64736f6c63430005110032",
    "opcodes": "PUSH1 0x80 PUSH1 0x40 MSTORE CALLVALUE DUP1 ISZERO PUSH2 0x10 JUMPI PUSH1 0x0 DUP1 REVERT JUMPDEST POP PUSH2 0x4F3 DUP1 PUSH2 0x20 PUSH1 0x0 CODECOPY PUSH1 0x0 RETURN INVALID PUSH1 0x80 PUSH1 0x40 MSTORE CALLVALUE DUP1 ISZERO PUSH2 0x10 JUMPI PUSH1 0x0 DUP1 REVERT JUMPDEST POP PUSH1 0x4 CALLDATASIZE LT PUSH2 0x36 JUMPI PUSH1 0x0 CALLDATALOAD PUSH1 0xE0 SHR DUP1 PUSH4 0x1BF28F83 EQ PUSH2 0x3B JUMPI DUP1 PUSH4 0x51428BC0 EQ PUSH2 0xCC JUMPI JUMPDEST PUSH1 0x0 DUP1 REVERT JUMPDEST PUSH2 0xB2 PUSH1 0x4 DUP1 CALLDATASIZE SUB PUSH1 0x20 DUP2 LT ISZERO PUSH2 0x51 JUMPI PUSH1 0x0 DUP1 REVERT JUMPDEST DUP2 ADD SWAP1 DUP1 DUP1 CALLDATALOAD SWAP1 PUSH1 0x20 ADD SWAP1 PUSH5 0x100000000 DUP2 GT ISZERO PUSH2 0x6E JUMPI PUSH1 0x0 DUP1 REVERT JUMPDEST DUP3 ADD DUP4 PUSH1 0x20 DUP3 ADD GT ISZERO PUSH2 0x80 JUMPI PUSH1 0x0 DUP1 REVERT JUMPDEST DUP1 CALLDATALOAD SWAP1 PUSH1 0x20 ADD SWAP2 DUP5 PUSH1 0x20 DUP4 MUL DUP5 ADD GT PUSH5 0x100000000 DUP4 GT OR ISZERO PUSH2 0xA2 JUMPI PUSH1 0x0 DUP1 REVERT JUMPDEST SWAP1 SWAP2 SWAP3 SWAP4 SWAP2 SWAP3 SWAP4 SWAP1 POP POP POP PUSH2 0x1B2 JUMP JUMPDEST PUSH1 0x40 MLOAD DUP1 DUP3 ISZERO ISZERO ISZERO ISZERO DUP2 MSTORE PUSH1 0x20 ADD SWAP2 POP POP PUSH1 0x40 MLOAD DUP1 SWAP2 SUB SWAP1 RETURN JUMPDEST PUSH2 0x198 PUSH1 0x4 DUP1 CALLDATASIZE SUB PUSH1 0x40 DUP2 LT ISZERO PUSH2 0xE2 JUMPI PUSH1 0x0 DUP1 REVERT JUMPDEST DUP2 ADD SWAP1 DUP1 DUP1 CALLDATALOAD SWAP1 PUSH1 0x20 ADD SWAP1 PUSH5 0x100000000 DUP2 GT ISZERO PUSH2 0xFF JUMPI PUSH1 0x0 DUP1 REVERT JUMPDEST DUP3 ADD DUP4 PUSH1 0x20 DUP3 ADD GT ISZERO PUSH2 0x111 JUMPI PUSH1 0x0 DUP1 REVERT JUMPDEST DUP1 CALLDATALOAD SWAP1 PUSH1 0x20 ADD SWAP2 DUP5 PUSH1 0x20 DUP4 MUL DUP5 ADD GT PUSH5 0x100000000 DUP4 GT OR ISZERO PUSH2 0x133 JUMPI PUSH1 0x0 DUP1 REVERT JUMPDEST SWAP1 SWAP2 SWAP3 SWAP4 SWAP2 SWAP3 SWAP4 SWAP1 DUP1 CALLDATALOAD SWAP1 PUSH1 0x20 ADD SWAP1 PUSH5 0x100000000 DUP2 GT ISZERO PUSH2 0x154 JUMPI PUSH1 0x0 DUP1 REVERT JUMPDEST DUP3 ADD DUP4 PUSH1 0x20 DUP3 ADD GT ISZERO PUSH2 0x166 JUMPI PUSH1 0x0 DUP1 REVERT JUMPDEST DUP1 CALLDATALOAD SWAP1 PUSH1 0x20 ADD SWAP2 DUP5 PUSH1 0x20 DUP4 MUL DUP5 ADD GT PUSH5 0x100000000 DUP4 GT OR ISZERO PUSH2 0x188 JUMPI PUSH1 0x0 DUP1 REVERT JUMPDEST SWAP1 SWAP2 SWAP3 SWAP4 SWAP2 SWAP3 SWAP4 SWAP1 POP POP POP PUSH2 0x1E5 JUMP JUMPDEST PUSH1 0x40 MLOAD DUP1 DUP3 ISZERO ISZERO ISZERO ISZERO DUP2 MSTORE PUSH1 0x20 ADD SWAP2 POP POP PUSH1 0x40 MLOAD DUP1 SWAP2 SUB SWAP1 RETURN JUMPDEST PUSH1 0x0 PUSH1 0x3 DUP4 DUP4 SWAP1 POP EQ DUP1 ISZERO PUSH2 0x1DD JUMPI POP PUSH1 0x0 DUP1 SHL DUP4 DUP4 PUSH1 0x0 DUP2 DUP2 LT PUSH2 0x1D3 JUMPI INVALID JUMPDEST SWAP1 POP PUSH1 0x20 MUL ADD CALLDATALOAD EQ ISZERO JUMPDEST SWAP1 POP SWAP3 SWAP2 POP POP JUMP JUMPDEST PUSH1 0x0 PUSH1 0x2 DUP4 DUP4 SWAP1 POP EQ PUSH2 0x260 JUMPI PUSH1 0x40 MLOAD PUSH32 0x8C379A000000000000000000000000000000000000000000000000000000000 DUP2 MSTORE PUSH1 0x4 ADD DUP1 DUP1 PUSH1 0x20 ADD DUP3 DUP2 SUB DUP3 MSTORE PUSH1 0x1A DUP2 MSTORE PUSH1 0x20 ADD DUP1 PUSH32 0x416E73776572206C656E6774682073686F756C6420626520322E000000000000 DUP2 MSTORE POP PUSH1 0x20 ADD SWAP2 POP POP PUSH1 0x40 MLOAD DUP1 SWAP2 SUB SWAP1 REVERT JUMPDEST PUSH1 0x0 PUSH2 0x27E DUP7 DUP7 PUSH1 0x0 DUP2 DUP2 LT PUSH2 0x272 JUMPI INVALID JUMPDEST SWAP1 POP PUSH1 0x20 MUL ADD CALLDATALOAD PUSH2 0x4B1 JUMP JUMPDEST SWAP1 POP PUSH1 0x0 PUSH2 0x29E DUP8 DUP8 PUSH1 0x1 DUP2 DUP2 LT PUSH2 0x292 JUMPI INVALID JUMPDEST SWAP1 POP PUSH1 0x20 MUL ADD CALLDATALOAD PUSH2 0x4B1 JUMP JUMPDEST SWAP1 POP PUSH1 0x0 PUSH2 0x2BE DUP9 DUP9 PUSH1 0x2 DUP2 DUP2 LT PUSH2 0x2B2 JUMPI INVALID JUMPDEST SWAP1 POP PUSH1 0x20 MUL ADD CALLDATALOAD PUSH2 0x4B1 JUMP JUMPDEST SWAP1 POP PUSH1 0x0 PUSH2 0x2DE DUP8 DUP8 PUSH1 0x0 DUP2 DUP2 LT PUSH2 0x2D2 JUMPI INVALID JUMPDEST SWAP1 POP PUSH1 0x20 MUL ADD CALLDATALOAD PUSH2 0x4B1 JUMP JUMPDEST SWAP1 POP PUSH1 0x0 PUSH2 0x2FE DUP9 DUP9 PUSH1 0x1 DUP2 DUP2 LT PUSH2 0x2F2 JUMPI INVALID JUMPDEST SWAP1 POP PUSH1 0x20 MUL ADD CALLDATALOAD PUSH2 0x4B1 JUMP JUMPDEST SWAP1 POP PUSH1 0x0 DUP2 SWAP1 POP PUSH1 0x0 DUP3 SLT ISZERO PUSH2 0x315 JUMPI DUP2 PUSH1 0x0 SUB SWAP1 POP JUMPDEST PUSH1 0x0 DUP3 SWAP1 POP PUSH1 0x0 PUSH3 0xF4240 SWAP1 POP JUMPDEST PUSH1 0x1 PUSH1 0xA DUP4 DUP2 PUSH2 0x32F JUMPI INVALID JUMPDEST SDIV SGT DUP1 ISZERO PUSH2 0x33D JUMPI POP PUSH1 0x1 DUP2 SGT JUMPDEST ISZERO PUSH2 0x361 JUMPI PUSH1 0xA DUP3 DUP2 PUSH2 0x34C JUMPI INVALID JUMPDEST SDIV SWAP2 POP PUSH1 0xA DUP2 DUP2 PUSH2 0x359 JUMPI INVALID JUMPDEST SDIV SWAP1 POP PUSH2 0x323 JUMP JUMPDEST PUSH1 0x0 DUP2 DUP6 DUP9 DUP11 SUB MUL DUP8 DUP12 MUL ADD MUL SWAP1 POP PUSH1 0x0 DUP3 DUP7 DUP10 DUP12 SUB MUL DUP9 DUP13 PUSH1 0x0 SUB MUL ADD MUL SWAP1 POP PUSH1 0x0 DUP6 DUP4 SLT DUP1 ISZERO PUSH2 0x395 JUMPI POP DUP6 PUSH1 0x0 SUB DUP4 SGT JUMPDEST DUP1 PUSH2 0x3AD JUMPI POP DUP6 DUP3 SLT DUP1 ISZERO PUSH2 0x3AC JUMPI POP DUP6 PUSH1 0x0 SUB DUP3 SGT JUMPDEST JUMPDEST SWAP1 POP PUSH1 0x60 PUSH1 0x7 PUSH1 0x40 MLOAD SWAP1 DUP1 DUP3 MSTORE DUP1 PUSH1 0x20 MUL PUSH1 0x20 ADD DUP3 ADD PUSH1 0x40 MSTORE DUP1 ISZERO PUSH2 0x3E1 JUMPI DUP2 PUSH1 0x20 ADD PUSH1 0x20 DUP3 MUL DUP1 CODESIZE DUP4 CODECOPY DUP1 DUP3 ADD SWAP2 POP POP SWAP1 POP JUMPDEST POP SWAP1 POP DUP12 DUP2 PUSH1 0x0 DUP2 MLOAD DUP2 LT PUSH2 0x3F2 JUMPI INVALID JUMPDEST PUSH1 0x20 MUL PUSH1 0x20 ADD ADD DUP2 DUP2 MSTORE POP POP DUP11 DUP2 PUSH1 0x1 DUP2 MLOAD DUP2 LT PUSH2 0x40C JUMPI INVALID JUMPDEST PUSH1 0x20 MUL PUSH1 0x20 ADD ADD DUP2 DUP2 MSTORE POP POP DUP10 DUP2 PUSH1 0x2 DUP2 MLOAD DUP2 LT PUSH2 0x426 JUMPI INVALID JUMPDEST PUSH1 0x20 MUL PUSH1 0x20 ADD ADD DUP2 DUP2 MSTORE POP POP DUP9 DUP2 PUSH1 0x3 DUP2 MLOAD DUP2 LT PUSH2 0x440 JUMPI INVALID JUMPDEST PUSH1 0x20 MUL PUSH1 0x20 ADD ADD DUP2 DUP2 MSTORE POP POP DUP8 DUP2 PUSH1 0x4 DUP2 MLOAD DUP2 LT PUSH2 0x45A JUMPI INVALID JUMPDEST PUSH1 0x20 MUL PUSH1 0x20 ADD ADD DUP2 DUP2 MSTORE POP POP DUP4 DUP2 PUSH1 0x5 DUP2 MLOAD DUP2 LT PUSH2 0x474 JUMPI INVALID JUMPDEST PUSH1 0x20 MUL PUSH1 0x20 ADD ADD DUP2 DUP2 MSTORE POP POP DUP3 DUP2 PUSH1 0x6 DUP2 MLOAD DUP2 LT PUSH2 0x48E JUMPI INVALID JUMPDEST PUSH1 0x20 MUL PUSH1 0x20 ADD ADD DUP2 DUP2 MSTORE POP POP DUP2 SWAP13 POP POP POP POP POP POP POP POP POP POP POP POP POP SWAP5 SWAP4 POP POP POP POP JUMP JUMPDEST PUSH1 0x0 DUP2 PUSH1 0x0 SHR SWAP1 POP SWAP2 SWAP1 POP JUMP INVALID LOG2 PUSH6 0x627A7A723158 KECCAK256 0xA9 0xE9 SLT 0xB8 0xC8 0xF6 PUSH20 0x5EDD269586990E2C40E066DD6AF0DAE606585391 ADDMOD PUSH14 0x1DBE3A64736F6C63430005110032 ",
    "sourceMap": "112:1410:0:-;;;;8:9:-1;5:2;;;30:1;27;20:12;5:2;112:1410:0;;;;;;;"
}