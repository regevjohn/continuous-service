VALIDATOR_ABI = """[
	{
		"constant": false,
		"inputs": [
			{
				"internalType": "string",
				"name": "_file_name",
				"type": "string"
			},
			{
				"internalType": "bytes32",
				"name": "_file_hash",
				"type": "bytes32"
			}
		],
		"name": "add_file_hash",
		"outputs": [],
		"payable": false,
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"constant": true,
		"inputs": [
			{
				"internalType": "string",
				"name": "",
				"type": "string"
			}
		],
		"name": "files_hashes",
		"outputs": [
			{
				"internalType": "bytes32",
				"name": "",
				"type": "bytes32"
			}
		],
		"payable": false,
		"stateMutability": "view",
		"type": "function"
	},
	{
		"constant": true,
		"inputs": [
			{
				"internalType": "bytes32[]",
				"name": "_question",
				"type": "bytes32[]"
			},
			{
				"internalType": "bytes32[]",
				"name": "_answer",
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
		"stateMutability": "view",
		"type": "function"
	},
	{
		"constant": true,
		"inputs": [
			{
				"internalType": "bytes32[]",
				"name": "_question",
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
		"stateMutability": "view",
		"type": "function"
	}
]"""

VALIDATOR_SOL = {
	"linkReferences": {},
	"object": "608060405234801561001057600080fd5b5061076f806100206000396000f3fe608060405234801561001057600080fd5b506004361061004c5760003560e01c80631bf28f831461005157806351428bc0146100e25780636a817626146101c85780636eebe3971461024b575b600080fd5b6100c86004803603602081101561006757600080fd5b810190808035906020019064010000000081111561008457600080fd5b82018360208201111561009657600080fd5b803590602001918460208302840111640100000000831117156100b857600080fd5b909192939192939050505061031a565b604051808215151515815260200191505060405180910390f35b6101ae600480360360408110156100f857600080fd5b810190808035906020019064010000000081111561011557600080fd5b82018360208201111561012757600080fd5b8035906020019184602083028401116401000000008311171561014957600080fd5b90919293919293908035906020019064010000000081111561016a57600080fd5b82018360208201111561017c57600080fd5b8035906020019184602083028401116401000000008311171561019e57600080fd5b90919293919293905050506103fa565b604051808215151515815260200191505060405180910390f35b610249600480360360408110156101de57600080fd5b81019080803590602001906401000000008111156101fb57600080fd5b82018360208201111561020d57600080fd5b8035906020019184600183028401116401000000008311171561022f57600080fd5b909192939192939080359060200190929190505050610531565b005b6103046004803603602081101561026157600080fd5b810190808035906020019064010000000081111561027e57600080fd5b82018360208201111561029057600080fd5b803590602001918460018302840111640100000000831117156102b257600080fd5b91908080601f016020809104026020016040519081016040528093929190818152602001838380828437600081840152601f19601f820116905080830192505050505050509192919290505050610562565b6040518082815260200191505060405180910390f35b60006060610368848480806020026020016040519081016040528093929190818152602001838360200280828437600081840152601f19601f82011690508083019250505050505050610590565b905060608190506000801b6000826040518082805190602001908083835b602083106103a95780518252602082019150602081019050602083039250610386565b6001836020036101000a038019825116818451168082178552505050505050905001915050908152602001604051809103902054146103ed576001925050506103f4565b6000925050505b92915050565b60006060610448868680806020026020016040519081016040528093929190818152602001838360200280828437600081840152601f19601f82011690508083019250505050505050610590565b90506060610496858580806020026020016040519081016040528093929190818152602001838360200280828437600081840152601f19601f82011690508083019250505050505050610590565b905060608290506000816040518082805190602001908083835b602083106104d357805182526020820191506020810190506020830392506104b0565b6001836020036101000a038019825116818451168082178552505050505050905001915050908152602001604051809103902054828051906020012014156105215760019350505050610529565b600093505050505b949350505050565b8060008484604051808383808284378083019250505092505050908152602001604051809103902081905550505050565b6000818051602081018201805184825260208301602085012081835280955050505050506000915090505481565b60606000826000815181106105a157fe5b60200260200101516000602081106105b557fe5b1a60f81b60f81c60ff1690506060816020600286510302016040519080825280601f01601f1916602001820160405280156105ff5781602001600182028038833980820191505090505b509050600080905060008090505b60028651038110156106aa5760008090505b602081101561069c5786600183018151811061063757fe5b6020026020010151816020811061064a57fe5b1a60f81b84848151811061065a57fe5b60200101907effffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff1916908160001a905350600183019250808060010191505061061f565b50808060010191505061060d565b5060008090505b8381101561072e57856001875103815181106106c957fe5b602002602001015181602081106106dc57fe5b1a60f81b8383815181106106ec57fe5b60200101907effffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff1916908160001a90535060018201915080806001019150506106b1565b5081935050505091905056fea265627a7a723158201b04c9a3c13e9a0c3c3761f2b4bd2bd5a6fa074c53fb559f7307a74b2583d04864736f6c63430005110032",
	"opcodes": "PUSH1 0x80 PUSH1 0x40 MSTORE CALLVALUE DUP1 ISZERO PUSH2 0x10 JUMPI PUSH1 0x0 DUP1 REVERT JUMPDEST POP PUSH2 0x76F DUP1 PUSH2 0x20 PUSH1 0x0 CODECOPY PUSH1 0x0 RETURN INVALID PUSH1 0x80 PUSH1 0x40 MSTORE CALLVALUE DUP1 ISZERO PUSH2 0x10 JUMPI PUSH1 0x0 DUP1 REVERT JUMPDEST POP PUSH1 0x4 CALLDATASIZE LT PUSH2 0x4C JUMPI PUSH1 0x0 CALLDATALOAD PUSH1 0xE0 SHR DUP1 PUSH4 0x1BF28F83 EQ PUSH2 0x51 JUMPI DUP1 PUSH4 0x51428BC0 EQ PUSH2 0xE2 JUMPI DUP1 PUSH4 0x6A817626 EQ PUSH2 0x1C8 JUMPI DUP1 PUSH4 0x6EEBE397 EQ PUSH2 0x24B JUMPI JUMPDEST PUSH1 0x0 DUP1 REVERT JUMPDEST PUSH2 0xC8 PUSH1 0x4 DUP1 CALLDATASIZE SUB PUSH1 0x20 DUP2 LT ISZERO PUSH2 0x67 JUMPI PUSH1 0x0 DUP1 REVERT JUMPDEST DUP2 ADD SWAP1 DUP1 DUP1 CALLDATALOAD SWAP1 PUSH1 0x20 ADD SWAP1 PUSH5 0x100000000 DUP2 GT ISZERO PUSH2 0x84 JUMPI PUSH1 0x0 DUP1 REVERT JUMPDEST DUP3 ADD DUP4 PUSH1 0x20 DUP3 ADD GT ISZERO PUSH2 0x96 JUMPI PUSH1 0x0 DUP1 REVERT JUMPDEST DUP1 CALLDATALOAD SWAP1 PUSH1 0x20 ADD SWAP2 DUP5 PUSH1 0x20 DUP4 MUL DUP5 ADD GT PUSH5 0x100000000 DUP4 GT OR ISZERO PUSH2 0xB8 JUMPI PUSH1 0x0 DUP1 REVERT JUMPDEST SWAP1 SWAP2 SWAP3 SWAP4 SWAP2 SWAP3 SWAP4 SWAP1 POP POP POP PUSH2 0x31A JUMP JUMPDEST PUSH1 0x40 MLOAD DUP1 DUP3 ISZERO ISZERO ISZERO ISZERO DUP2 MSTORE PUSH1 0x20 ADD SWAP2 POP POP PUSH1 0x40 MLOAD DUP1 SWAP2 SUB SWAP1 RETURN JUMPDEST PUSH2 0x1AE PUSH1 0x4 DUP1 CALLDATASIZE SUB PUSH1 0x40 DUP2 LT ISZERO PUSH2 0xF8 JUMPI PUSH1 0x0 DUP1 REVERT JUMPDEST DUP2 ADD SWAP1 DUP1 DUP1 CALLDATALOAD SWAP1 PUSH1 0x20 ADD SWAP1 PUSH5 0x100000000 DUP2 GT ISZERO PUSH2 0x115 JUMPI PUSH1 0x0 DUP1 REVERT JUMPDEST DUP3 ADD DUP4 PUSH1 0x20 DUP3 ADD GT ISZERO PUSH2 0x127 JUMPI PUSH1 0x0 DUP1 REVERT JUMPDEST DUP1 CALLDATALOAD SWAP1 PUSH1 0x20 ADD SWAP2 DUP5 PUSH1 0x20 DUP4 MUL DUP5 ADD GT PUSH5 0x100000000 DUP4 GT OR ISZERO PUSH2 0x149 JUMPI PUSH1 0x0 DUP1 REVERT JUMPDEST SWAP1 SWAP2 SWAP3 SWAP4 SWAP2 SWAP3 SWAP4 SWAP1 DUP1 CALLDATALOAD SWAP1 PUSH1 0x20 ADD SWAP1 PUSH5 0x100000000 DUP2 GT ISZERO PUSH2 0x16A JUMPI PUSH1 0x0 DUP1 REVERT JUMPDEST DUP3 ADD DUP4 PUSH1 0x20 DUP3 ADD GT ISZERO PUSH2 0x17C JUMPI PUSH1 0x0 DUP1 REVERT JUMPDEST DUP1 CALLDATALOAD SWAP1 PUSH1 0x20 ADD SWAP2 DUP5 PUSH1 0x20 DUP4 MUL DUP5 ADD GT PUSH5 0x100000000 DUP4 GT OR ISZERO PUSH2 0x19E JUMPI PUSH1 0x0 DUP1 REVERT JUMPDEST SWAP1 SWAP2 SWAP3 SWAP4 SWAP2 SWAP3 SWAP4 SWAP1 POP POP POP PUSH2 0x3FA JUMP JUMPDEST PUSH1 0x40 MLOAD DUP1 DUP3 ISZERO ISZERO ISZERO ISZERO DUP2 MSTORE PUSH1 0x20 ADD SWAP2 POP POP PUSH1 0x40 MLOAD DUP1 SWAP2 SUB SWAP1 RETURN JUMPDEST PUSH2 0x249 PUSH1 0x4 DUP1 CALLDATASIZE SUB PUSH1 0x40 DUP2 LT ISZERO PUSH2 0x1DE JUMPI PUSH1 0x0 DUP1 REVERT JUMPDEST DUP2 ADD SWAP1 DUP1 DUP1 CALLDATALOAD SWAP1 PUSH1 0x20 ADD SWAP1 PUSH5 0x100000000 DUP2 GT ISZERO PUSH2 0x1FB JUMPI PUSH1 0x0 DUP1 REVERT JUMPDEST DUP3 ADD DUP4 PUSH1 0x20 DUP3 ADD GT ISZERO PUSH2 0x20D JUMPI PUSH1 0x0 DUP1 REVERT JUMPDEST DUP1 CALLDATALOAD SWAP1 PUSH1 0x20 ADD SWAP2 DUP5 PUSH1 0x1 DUP4 MUL DUP5 ADD GT PUSH5 0x100000000 DUP4 GT OR ISZERO PUSH2 0x22F JUMPI PUSH1 0x0 DUP1 REVERT JUMPDEST SWAP1 SWAP2 SWAP3 SWAP4 SWAP2 SWAP3 SWAP4 SWAP1 DUP1 CALLDATALOAD SWAP1 PUSH1 0x20 ADD SWAP1 SWAP3 SWAP2 SWAP1 POP POP POP PUSH2 0x531 JUMP JUMPDEST STOP JUMPDEST PUSH2 0x304 PUSH1 0x4 DUP1 CALLDATASIZE SUB PUSH1 0x20 DUP2 LT ISZERO PUSH2 0x261 JUMPI PUSH1 0x0 DUP1 REVERT JUMPDEST DUP2 ADD SWAP1 DUP1 DUP1 CALLDATALOAD SWAP1 PUSH1 0x20 ADD SWAP1 PUSH5 0x100000000 DUP2 GT ISZERO PUSH2 0x27E JUMPI PUSH1 0x0 DUP1 REVERT JUMPDEST DUP3 ADD DUP4 PUSH1 0x20 DUP3 ADD GT ISZERO PUSH2 0x290 JUMPI PUSH1 0x0 DUP1 REVERT JUMPDEST DUP1 CALLDATALOAD SWAP1 PUSH1 0x20 ADD SWAP2 DUP5 PUSH1 0x1 DUP4 MUL DUP5 ADD GT PUSH5 0x100000000 DUP4 GT OR ISZERO PUSH2 0x2B2 JUMPI PUSH1 0x0 DUP1 REVERT JUMPDEST SWAP2 SWAP1 DUP1 DUP1 PUSH1 0x1F ADD PUSH1 0x20 DUP1 SWAP2 DIV MUL PUSH1 0x20 ADD PUSH1 0x40 MLOAD SWAP1 DUP2 ADD PUSH1 0x40 MSTORE DUP1 SWAP4 SWAP3 SWAP2 SWAP1 DUP2 DUP2 MSTORE PUSH1 0x20 ADD DUP4 DUP4 DUP1 DUP3 DUP5 CALLDATACOPY PUSH1 0x0 DUP2 DUP5 ADD MSTORE PUSH1 0x1F NOT PUSH1 0x1F DUP3 ADD AND SWAP1 POP DUP1 DUP4 ADD SWAP3 POP POP POP POP POP POP POP SWAP2 SWAP3 SWAP2 SWAP3 SWAP1 POP POP POP PUSH2 0x562 JUMP JUMPDEST PUSH1 0x40 MLOAD DUP1 DUP3 DUP2 MSTORE PUSH1 0x20 ADD SWAP2 POP POP PUSH1 0x40 MLOAD DUP1 SWAP2 SUB SWAP1 RETURN JUMPDEST PUSH1 0x0 PUSH1 0x60 PUSH2 0x368 DUP5 DUP5 DUP1 DUP1 PUSH1 0x20 MUL PUSH1 0x20 ADD PUSH1 0x40 MLOAD SWAP1 DUP2 ADD PUSH1 0x40 MSTORE DUP1 SWAP4 SWAP3 SWAP2 SWAP1 DUP2 DUP2 MSTORE PUSH1 0x20 ADD DUP4 DUP4 PUSH1 0x20 MUL DUP1 DUP3 DUP5 CALLDATACOPY PUSH1 0x0 DUP2 DUP5 ADD MSTORE PUSH1 0x1F NOT PUSH1 0x1F DUP3 ADD AND SWAP1 POP DUP1 DUP4 ADD SWAP3 POP POP POP POP POP POP POP PUSH2 0x590 JUMP JUMPDEST SWAP1 POP PUSH1 0x60 DUP2 SWAP1 POP PUSH1 0x0 DUP1 SHL PUSH1 0x0 DUP3 PUSH1 0x40 MLOAD DUP1 DUP3 DUP1 MLOAD SWAP1 PUSH1 0x20 ADD SWAP1 DUP1 DUP4 DUP4 JUMPDEST PUSH1 0x20 DUP4 LT PUSH2 0x3A9 JUMPI DUP1 MLOAD DUP3 MSTORE PUSH1 0x20 DUP3 ADD SWAP2 POP PUSH1 0x20 DUP2 ADD SWAP1 POP PUSH1 0x20 DUP4 SUB SWAP3 POP PUSH2 0x386 JUMP JUMPDEST PUSH1 0x1 DUP4 PUSH1 0x20 SUB PUSH2 0x100 EXP SUB DUP1 NOT DUP3 MLOAD AND DUP2 DUP5 MLOAD AND DUP1 DUP3 OR DUP6 MSTORE POP POP POP POP POP POP SWAP1 POP ADD SWAP2 POP POP SWAP1 DUP2 MSTORE PUSH1 0x20 ADD PUSH1 0x40 MLOAD DUP1 SWAP2 SUB SWAP1 KECCAK256 SLOAD EQ PUSH2 0x3ED JUMPI PUSH1 0x1 SWAP3 POP POP POP PUSH2 0x3F4 JUMP JUMPDEST PUSH1 0x0 SWAP3 POP POP POP JUMPDEST SWAP3 SWAP2 POP POP JUMP JUMPDEST PUSH1 0x0 PUSH1 0x60 PUSH2 0x448 DUP7 DUP7 DUP1 DUP1 PUSH1 0x20 MUL PUSH1 0x20 ADD PUSH1 0x40 MLOAD SWAP1 DUP2 ADD PUSH1 0x40 MSTORE DUP1 SWAP4 SWAP3 SWAP2 SWAP1 DUP2 DUP2 MSTORE PUSH1 0x20 ADD DUP4 DUP4 PUSH1 0x20 MUL DUP1 DUP3 DUP5 CALLDATACOPY PUSH1 0x0 DUP2 DUP5 ADD MSTORE PUSH1 0x1F NOT PUSH1 0x1F DUP3 ADD AND SWAP1 POP DUP1 DUP4 ADD SWAP3 POP POP POP POP POP POP POP PUSH2 0x590 JUMP JUMPDEST SWAP1 POP PUSH1 0x60 PUSH2 0x496 DUP6 DUP6 DUP1 DUP1 PUSH1 0x20 MUL PUSH1 0x20 ADD PUSH1 0x40 MLOAD SWAP1 DUP2 ADD PUSH1 0x40 MSTORE DUP1 SWAP4 SWAP3 SWAP2 SWAP1 DUP2 DUP2 MSTORE PUSH1 0x20 ADD DUP4 DUP4 PUSH1 0x20 MUL DUP1 DUP3 DUP5 CALLDATACOPY PUSH1 0x0 DUP2 DUP5 ADD MSTORE PUSH1 0x1F NOT PUSH1 0x1F DUP3 ADD AND SWAP1 POP DUP1 DUP4 ADD SWAP3 POP POP POP POP POP POP POP PUSH2 0x590 JUMP JUMPDEST SWAP1 POP PUSH1 0x60 DUP3 SWAP1 POP PUSH1 0x0 DUP2 PUSH1 0x40 MLOAD DUP1 DUP3 DUP1 MLOAD SWAP1 PUSH1 0x20 ADD SWAP1 DUP1 DUP4 DUP4 JUMPDEST PUSH1 0x20 DUP4 LT PUSH2 0x4D3 JUMPI DUP1 MLOAD DUP3 MSTORE PUSH1 0x20 DUP3 ADD SWAP2 POP PUSH1 0x20 DUP2 ADD SWAP1 POP PUSH1 0x20 DUP4 SUB SWAP3 POP PUSH2 0x4B0 JUMP JUMPDEST PUSH1 0x1 DUP4 PUSH1 0x20 SUB PUSH2 0x100 EXP SUB DUP1 NOT DUP3 MLOAD AND DUP2 DUP5 MLOAD AND DUP1 DUP3 OR DUP6 MSTORE POP POP POP POP POP POP SWAP1 POP ADD SWAP2 POP POP SWAP1 DUP2 MSTORE PUSH1 0x20 ADD PUSH1 0x40 MLOAD DUP1 SWAP2 SUB SWAP1 KECCAK256 SLOAD DUP3 DUP1 MLOAD SWAP1 PUSH1 0x20 ADD KECCAK256 EQ ISZERO PUSH2 0x521 JUMPI PUSH1 0x1 SWAP4 POP POP POP POP PUSH2 0x529 JUMP JUMPDEST PUSH1 0x0 SWAP4 POP POP POP POP JUMPDEST SWAP5 SWAP4 POP POP POP POP JUMP JUMPDEST DUP1 PUSH1 0x0 DUP5 DUP5 PUSH1 0x40 MLOAD DUP1 DUP4 DUP4 DUP1 DUP3 DUP5 CALLDATACOPY DUP1 DUP4 ADD SWAP3 POP POP POP SWAP3 POP POP POP SWAP1 DUP2 MSTORE PUSH1 0x20 ADD PUSH1 0x40 MLOAD DUP1 SWAP2 SUB SWAP1 KECCAK256 DUP2 SWAP1 SSTORE POP POP POP POP JUMP JUMPDEST PUSH1 0x0 DUP2 DUP1 MLOAD PUSH1 0x20 DUP2 ADD DUP3 ADD DUP1 MLOAD DUP5 DUP3 MSTORE PUSH1 0x20 DUP4 ADD PUSH1 0x20 DUP6 ADD KECCAK256 DUP2 DUP4 MSTORE DUP1 SWAP6 POP POP POP POP POP POP PUSH1 0x0 SWAP2 POP SWAP1 POP SLOAD DUP2 JUMP JUMPDEST PUSH1 0x60 PUSH1 0x0 DUP3 PUSH1 0x0 DUP2 MLOAD DUP2 LT PUSH2 0x5A1 JUMPI INVALID JUMPDEST PUSH1 0x20 MUL PUSH1 0x20 ADD ADD MLOAD PUSH1 0x0 PUSH1 0x20 DUP2 LT PUSH2 0x5B5 JUMPI INVALID JUMPDEST BYTE PUSH1 0xF8 SHL PUSH1 0xF8 SHR PUSH1 0xFF AND SWAP1 POP PUSH1 0x60 DUP2 PUSH1 0x20 PUSH1 0x2 DUP7 MLOAD SUB MUL ADD PUSH1 0x40 MLOAD SWAP1 DUP1 DUP3 MSTORE DUP1 PUSH1 0x1F ADD PUSH1 0x1F NOT AND PUSH1 0x20 ADD DUP3 ADD PUSH1 0x40 MSTORE DUP1 ISZERO PUSH2 0x5FF JUMPI DUP2 PUSH1 0x20 ADD PUSH1 0x1 DUP3 MUL DUP1 CODESIZE DUP4 CODECOPY DUP1 DUP3 ADD SWAP2 POP POP SWAP1 POP JUMPDEST POP SWAP1 POP PUSH1 0x0 DUP1 SWAP1 POP PUSH1 0x0 DUP1 SWAP1 POP JUMPDEST PUSH1 0x2 DUP7 MLOAD SUB DUP2 LT ISZERO PUSH2 0x6AA JUMPI PUSH1 0x0 DUP1 SWAP1 POP JUMPDEST PUSH1 0x20 DUP2 LT ISZERO PUSH2 0x69C JUMPI DUP7 PUSH1 0x1 DUP4 ADD DUP2 MLOAD DUP2 LT PUSH2 0x637 JUMPI INVALID JUMPDEST PUSH1 0x20 MUL PUSH1 0x20 ADD ADD MLOAD DUP2 PUSH1 0x20 DUP2 LT PUSH2 0x64A JUMPI INVALID JUMPDEST BYTE PUSH1 0xF8 SHL DUP5 DUP5 DUP2 MLOAD DUP2 LT PUSH2 0x65A JUMPI INVALID JUMPDEST PUSH1 0x20 ADD ADD SWAP1 PUSH31 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF NOT AND SWAP1 DUP2 PUSH1 0x0 BYTE SWAP1 MSTORE8 POP PUSH1 0x1 DUP4 ADD SWAP3 POP DUP1 DUP1 PUSH1 0x1 ADD SWAP2 POP POP PUSH2 0x61F JUMP JUMPDEST POP DUP1 DUP1 PUSH1 0x1 ADD SWAP2 POP POP PUSH2 0x60D JUMP JUMPDEST POP PUSH1 0x0 DUP1 SWAP1 POP JUMPDEST DUP4 DUP2 LT ISZERO PUSH2 0x72E JUMPI DUP6 PUSH1 0x1 DUP8 MLOAD SUB DUP2 MLOAD DUP2 LT PUSH2 0x6C9 JUMPI INVALID JUMPDEST PUSH1 0x20 MUL PUSH1 0x20 ADD ADD MLOAD DUP2 PUSH1 0x20 DUP2 LT PUSH2 0x6DC JUMPI INVALID JUMPDEST BYTE PUSH1 0xF8 SHL DUP4 DUP4 DUP2 MLOAD DUP2 LT PUSH2 0x6EC JUMPI INVALID JUMPDEST PUSH1 0x20 ADD ADD SWAP1 PUSH31 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF NOT AND SWAP1 DUP2 PUSH1 0x0 BYTE SWAP1 MSTORE8 POP PUSH1 0x1 DUP3 ADD SWAP2 POP DUP1 DUP1 PUSH1 0x1 ADD SWAP2 POP POP PUSH2 0x6B1 JUMP JUMPDEST POP DUP2 SWAP4 POP POP POP POP SWAP2 SWAP1 POP JUMP INVALID LOG2 PUSH6 0x627A7A723158 KECCAK256 SHL DIV 0xC9 LOG3 0xC1 RETURNDATACOPY SWAP11 0xC EXTCODECOPY CALLDATACOPY PUSH2 0xF2B4 0xBD 0x2B 0xD5 0xA6 STATICCALL SMOD 0x4C MSTORE8 0xFB SSTORE SWAP16 PUSH20 0x7A74B2583D04864736F6C634300051100320000 ",
	"sourceMap": "114:1670:0:-;;;;8:9:-1;5:2;;;30:1;27;20:12;5:2;114:1670:0;;;;;;;"
}