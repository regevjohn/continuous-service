import web3
import time
import eth_account.messages
import web3.contract
import random
import json
from ChunkedFilesValidator import *
from eth_keys import keys

w3 = web3.Web3(web3.HTTPProvider("http://127.0.0.1:7545"))

BLOCKLEN = 1024
APPEAL_PERIOD = 10  # the appeal period in blocks.
SUBSCRIPTION_COST = 10 ** 18
SUBSCRIPTION_PERIOD = 100
MAX_QUERIES = 1
SUBSCRIPTION_ABI = '''[
    {
        "inputs": [
            {
                "internalType": "address payable",
                "name": "_costumer",
                "type": "address"
            },
            {
                "internalType": "uint256",
                "name": "_appeal_period_len",
                "type": "uint256"
            },
            {
                "internalType": "uint256",
                "name": "_cost",
                "type": "uint256"
            },
            {
                "internalType": "uint256",
                "name": "_blocks_per_service",
                "type": "uint256"
            },
            {
                "internalType": "address",
                "name": "_validator",
                "type": "address"
            },
            {
                "internalType": "uint256",
                "name": "_max_queries",
                "type": "uint256"
            }
        ],
        "payable": false,
        "stateMutability": "nonpayable",
        "type": "constructor"
    },
    {
        "payable": true,
        "stateMutability": "payable",
        "type": "fallback"
    },
    {
        "constant": false,
        "inputs": [],
        "name": "activate",
        "outputs": [],
        "payable": true,
        "stateMutability": "payable",
        "type": "function"
    },
    {
        "constant": false,
        "inputs": [
            {
                "internalType": "bytes32[]",
                "name": "question",
                "type": "bytes32[]"
            },
            {
                "internalType": "bytes32[]",
                "name": "questions_hashes",
                "type": "bytes32[]"
            },
            {
                "internalType": "uint256",
                "name": "unanswered",
                "type": "uint256"
            },
            {
                "internalType": "uint8",
                "name": "v",
                "type": "uint8"
            },
            {
                "internalType": "bytes32",
                "name": "r",
                "type": "bytes32"
            },
            {
                "internalType": "bytes32",
                "name": "s",
                "type": "bytes32"
            }
        ],
        "name": "appeal",
        "outputs": [],
        "payable": false,
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "constant": true,
        "inputs": [],
        "name": "appeal_period_len",
        "outputs": [
            {
                "internalType": "uint256",
                "name": "",
                "type": "uint256"
            }
        ],
        "payable": false,
        "stateMutability": "view",
        "type": "function"
    },
    {
        "constant": true,
        "inputs": [],
        "name": "blocks_per_service",
        "outputs": [
            {
                "internalType": "uint256",
                "name": "",
                "type": "uint256"
            }
        ],
        "payable": false,
        "stateMutability": "view",
        "type": "function"
    },
    {
        "constant": true,
        "inputs": [],
        "name": "can_exec_demand",
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
        "inputs": [],
        "name": "cost",
        "outputs": [
            {
                "internalType": "uint256",
                "name": "",
                "type": "uint256"
            }
        ],
        "payable": false,
        "stateMutability": "view",
        "type": "function"
    },
    {
        "constant": true,
        "inputs": [],
        "name": "customer",
        "outputs": [
            {
                "internalType": "address payable",
                "name": "",
                "type": "address"
            }
        ],
        "payable": false,
        "stateMutability": "view",
        "type": "function"
    },
    {
        "constant": false,
        "inputs": [
            {
                "internalType": "bytes32[]",
                "name": "question",
                "type": "bytes32[]"
            },
            {
                "internalType": "bytes32[]",
                "name": "questions_hashes",
                "type": "bytes32[]"
            },
            {
                "internalType": "uint256",
                "name": "unanswered",
                "type": "uint256"
            },
            {
                "internalType": "uint8",
                "name": "v",
                "type": "uint8"
            },
            {
                "internalType": "bytes32",
                "name": "r",
                "type": "bytes32"
            },
            {
                "internalType": "bytes32",
                "name": "s",
                "type": "bytes32"
            },
            {
                "internalType": "bytes32[]",
                "name": "answer",
                "type": "bytes32[]"
            }
        ],
        "name": "demand_signature",
        "outputs": [],
        "payable": false,
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "constant": false,
        "inputs": [
            {
                "internalType": "bytes32[]",
                "name": "questions_hashes",
                "type": "bytes32[]"
            },
            {
                "internalType": "uint256",
                "name": "unanswered",
                "type": "uint256"
            },
            {
                "internalType": "uint8",
                "name": "v",
                "type": "uint8"
            },
            {
                "internalType": "bytes32",
                "name": "r",
                "type": "bytes32"
            },
            {
                "internalType": "bytes32",
                "name": "s",
                "type": "bytes32"
            }
        ],
        "name": "dismiss",
        "outputs": [],
        "payable": false,
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "constant": false,
        "inputs": [],
        "name": "exec_demand",
        "outputs": [],
        "payable": false,
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "constant": true,
        "inputs": [],
        "name": "get_answer_demanded",
        "outputs": [
            {
                "internalType": "bytes32[]",
                "name": "",
                "type": "bytes32[]"
            }
        ],
        "payable": false,
        "stateMutability": "view",
        "type": "function"
    },
    {
        "constant": true,
        "inputs": [],
        "name": "get_answer_resolved",
        "outputs": [
            {
                "internalType": "bytes32[]",
                "name": "",
                "type": "bytes32[]"
            }
        ],
        "payable": false,
        "stateMutability": "view",
        "type": "function"
    },
    {
        "constant": true,
        "inputs": [],
        "name": "get_end_of_service_block",
        "outputs": [
            {
                "internalType": "uint256",
                "name": "",
                "type": "uint256"
            }
        ],
        "payable": false,
        "stateMutability": "view",
        "type": "function"
    },
    {
        "constant": true,
        "inputs": [],
        "name": "get_other_owner",
        "outputs": [
            {
                "internalType": "address",
                "name": "",
                "type": "address"
            }
        ],
        "payable": false,
        "stateMutability": "view",
        "type": "function"
    },
    {
        "constant": true,
        "inputs": [],
        "name": "get_question_appealed",
        "outputs": [
            {
                "internalType": "bytes32[]",
                "name": "",
                "type": "bytes32[]"
            }
        ],
        "payable": false,
        "stateMutability": "view",
        "type": "function"
    },
    {
        "constant": true,
        "inputs": [],
        "name": "get_question_demanded",
        "outputs": [
            {
                "internalType": "bytes32[]",
                "name": "",
                "type": "bytes32[]"
            }
        ],
        "payable": false,
        "stateMutability": "view",
        "type": "function"
    },
    {
        "constant": true,
        "inputs": [],
        "name": "get_question_hashes_demanded",
        "outputs": [
            {
                "internalType": "bytes32[]",
                "name": "",
                "type": "bytes32[]"
            }
        ],
        "payable": false,
        "stateMutability": "view",
        "type": "function"
    },
    {
        "constant": true,
        "inputs": [],
        "name": "get_r_appealed",
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
        "inputs": [],
        "name": "get_r_provided",
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
        "inputs": [],
        "name": "get_s_appealed",
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
        "inputs": [],
        "name": "get_s_provided",
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
        "inputs": [],
        "name": "get_start_of_service_block",
        "outputs": [
            {
                "internalType": "uint256",
                "name": "",
                "type": "uint256"
            }
        ],
        "payable": false,
        "stateMutability": "view",
        "type": "function"
    },
    {
        "constant": true,
        "inputs": [],
        "name": "get_unanswered_demanded",
        "outputs": [
            {
                "internalType": "uint256",
                "name": "",
                "type": "uint256"
            }
        ],
        "payable": false,
        "stateMutability": "view",
        "type": "function"
    },
    {
        "constant": true,
        "inputs": [],
        "name": "get_v_appealed",
        "outputs": [
            {
                "internalType": "uint8",
                "name": "",
                "type": "uint8"
            }
        ],
        "payable": false,
        "stateMutability": "view",
        "type": "function"
    },
    {
        "constant": true,
        "inputs": [],
        "name": "get_v_provided",
        "outputs": [
            {
                "internalType": "uint8",
                "name": "",
                "type": "uint8"
            }
        ],
        "payable": false,
        "stateMutability": "view",
        "type": "function"
    },
    {
        "constant": true,
        "inputs": [],
        "name": "get_validator_address",
        "outputs": [
            {
                "internalType": "address",
                "name": "",
                "type": "address"
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
                "name": "question",
                "type": "bytes32[]"
            }
        ],
        "name": "hash_question",
        "outputs": [
            {
                "internalType": "bytes32",
                "name": "",
                "type": "bytes32"
            }
        ],
        "payable": false,
        "stateMutability": "pure",
        "type": "function"
    },
    {
        "constant": true,
        "inputs": [],
        "name": "is_active",
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
        "inputs": [],
        "name": "is_customer_appealing",
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
        "inputs": [],
        "name": "is_provider_demanding",
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
        "inputs": [],
        "name": "max_queries",
        "outputs": [
            {
                "internalType": "uint256",
                "name": "",
                "type": "uint256"
            }
        ],
        "payable": false,
        "stateMutability": "view",
        "type": "function"
    },
    {
        "constant": false,
        "inputs": [
            {
                "internalType": "bytes32[]",
                "name": "questions_hashes",
                "type": "bytes32[]"
            },
            {
                "internalType": "uint256",
                "name": "unanswered",
                "type": "uint256"
            },
            {
                "internalType": "uint8",
                "name": "v",
                "type": "uint8"
            },
            {
                "internalType": "bytes32",
                "name": "r",
                "type": "bytes32"
            },
            {
                "internalType": "bytes32",
                "name": "s",
                "type": "bytes32"
            }
        ],
        "name": "overflow",
        "outputs": [],
        "payable": false,
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "constant": false,
        "inputs": [
            {
                "internalType": "bytes32[]",
                "name": "questions_hashes",
                "type": "bytes32[]"
            },
            {
                "internalType": "uint256",
                "name": "unanswered",
                "type": "uint256"
            },
            {
                "internalType": "uint8",
                "name": "v",
                "type": "uint8"
            },
            {
                "internalType": "bytes32",
                "name": "r",
                "type": "bytes32"
            },
            {
                "internalType": "bytes32",
                "name": "s",
                "type": "bytes32"
            }
        ],
        "name": "provide_signature",
        "outputs": [],
        "payable": false,
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "constant": true,
        "inputs": [],
        "name": "provider",
        "outputs": [
            {
                "internalType": "address payable",
                "name": "",
                "type": "address"
            }
        ],
        "payable": false,
        "stateMutability": "view",
        "type": "function"
    },
    {
        "constant": false,
        "inputs": [
            {
                "internalType": "bytes32[]",
                "name": "answer",
                "type": "bytes32[]"
            }
        ],
        "name": "resolve",
        "outputs": [],
        "payable": false,
        "stateMutability": "nonpayable",
        "type": "function"
    },
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
                "name": "questions_hashes",
                "type": "bytes32[]"
            },
            {
                "internalType": "uint256",
                "name": "unanswered",
                "type": "uint256"
            },
            {
                "internalType": "uint8",
                "name": "v",
                "type": "uint8"
            },
            {
                "internalType": "bytes32",
                "name": "r",
                "type": "bytes32"
            },
            {
                "internalType": "bytes32",
                "name": "s",
                "type": "bytes32"
            }
        ],
        "name": "try_appeal",
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
        "inputs": [],
        "name": "validator",
        "outputs": [
            {
                "internalType": "contract Validator",
                "name": "",
                "type": "address"
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
                "name": "questions_hashes",
                "type": "bytes32[]"
            },
            {
                "internalType": "uint256",
                "name": "unanswered",
                "type": "uint256"
            },
            {
                "internalType": "uint8",
                "name": "v",
                "type": "uint8"
            },
            {
                "internalType": "bytes32",
                "name": "r",
                "type": "bytes32"
            },
            {
                "internalType": "bytes32",
                "name": "s",
                "type": "bytes32"
            },
            {
                "internalType": "address",
                "name": "signerPubKey",
                "type": "address"
            }
        ],
        "name": "verifySig",
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
        "constant": false,
        "inputs": [
            {
                "internalType": "address payable",
                "name": "dest_address",
                "type": "address"
            }
        ],
        "name": "withdraw_funds",
        "outputs": [],
        "payable": false,
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "constant": true,
        "inputs": [],
        "name": "withdraw_funds_amount",
        "outputs": [
            {
                "internalType": "uint256",
                "name": "",
                "type": "uint256"
            }
        ],
        "payable": false,
        "stateMutability": "view",
        "type": "function"
    }
]'''
SUBSCRIPTION_SOL = {
    "linkReferences": {},
    "object": "60806040523480156200001157600080fd5b5060405162004be738038062004be78339818101604052620000379190810190620001b1565b336000806101000a81548173ffffffffffffffffffffffffffffffffffffffff021916908373ffffffffffffffffffffffffffffffffffffffff16021790555085600160006101000a81548173ffffffffffffffffffffffffffffffffffffffff021916908373ffffffffffffffffffffffffffffffffffffffff16021790555084600381905550836004819055508260058190555081600260006101000a81548173ffffffffffffffffffffffffffffffffffffffff021916908373ffffffffffffffffffffffffffffffffffffffff160217905550806006819055506000600c819055506000600a819055506000601581905550600060078190555060006008819055506000600b819055506000600d60006101000a81548160ff021916908315150217905550505050505050620002e7565b6000815190506200017d8162000299565b92915050565b6000815190506200019481620002b3565b92915050565b600081519050620001ab81620002cd565b92915050565b60008060008060008060c08789031215620001cb57600080fd5b6000620001db89828a0162000183565b9650506020620001ee89828a016200019a565b95505060406200020189828a016200019a565b94505060606200021489828a016200019a565b93505060806200022789828a016200016c565b92505060a06200023a89828a016200019a565b9150509295509295509295565b600062000254826200026f565b9050919050565b600062000268826200026f565b9050919050565b600073ffffffffffffffffffffffffffffffffffffffff82169050919050565b6000819050919050565b620002a48162000247565b8114620002b057600080fd5b50565b620002be816200025b565b8114620002ca57600080fd5b50565b620002d8816200028f565b8114620002e457600080fd5b50565b6148f080620002f76000396000f3fe60806040526004361061023b5760003560e01c80636d3f89981161012e57806393c3da8c116100ab578063d914e4e01161006f578063d914e4e0146108c9578063e5f03799146108f4578063eecb5ded14610931578063f13bd54c1461095c578063fbac9443146109875761023b565b806393c3da8c146107f4578063b0433e941461081f578063b107d50c1461084a578063bfae1d0f14610875578063d14867fe1461089e5761023b565b806376c3d965116100f257806376c3d9651461071f5780638463eedd146107485780638ab6fad1146107735780638f0c1a141461079e5780638f145525146107c95761023b565b80636d3f89981461065e5780636ddf2254146106895780637317d73f146106b257806373398395146106dd57806375b6a366146106f45761023b565b80631c08fbc6116101bc5780633a5381b5116101805780633a5381b51461058b5780634e621157146105b6578063630c24a1146105df5780636b34c8c21461060a5780636b5e332a146106335761023b565b80631c08fbc6146104a25780631cc368f8146104df5780631e550b131461050a57806324ed685d146105355780632804b2c0146105605761023b565b8063121273b911610203578063121273b9146103bb57806313faede6146103e457806314e1306c1461040f5780631595be3a1461043a5780631a8012e4146104775761023b565b8063057489fa14610307578063085d4883146103305780630bc2fde31461035b5780630f15f4c0146103865780631177f72d14610390575b600160009054906101000a900473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff163373ffffffffffffffffffffffffffffffffffffffff1614156102a65734600860008282540192505081905550610305565b6000809054906101000a900473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff163373ffffffffffffffffffffffffffffffffffffffff16141561030057600080fd5b600080fd5b005b34801561031357600080fd5b5061032e600480360361032991908101906133f2565b6109b2565b005b34801561033c57600080fd5b50610345610c7c565b6040516103529190614237565b60405180910390f35b34801561036757600080fd5b50610370610ca1565b60405161037d9190614303565b60405180910390f35b61038e610cab565b005b34801561039c57600080fd5b506103a5610e04565b6040516103b29190614303565b60405180910390f35b3480156103c757600080fd5b506103e260048036036103dd9190810190613437565b610e0e565b005b3480156103f057600080fd5b506103f961119d565b60405161040691906145de565b60405180910390f35b34801561041b57600080fd5b506104246111a3565b604051610431919061428d565b60405180910390f35b34801561044657600080fd5b50610461600480360361045c919081019061367f565b6111fb565b60405161046e9190614303565b60405180910390f35b34801561048357600080fd5b5061048c611230565b60405161049991906142e8565b60405180910390f35b3480156104ae57600080fd5b506104c960048036036104c49190810190613779565b61123c565b6040516104d691906142e8565b60405180910390f35b3480156104eb57600080fd5b506104f4611322565b604051610501919061421c565b60405180910390f35b34801561051657600080fd5b5061051f611510565b60405161052c91906142e8565b60405180910390f35b34801561054157600080fd5b5061054a611527565b60405161055791906145de565b60405180910390f35b34801561056c57600080fd5b5061057561152d565b6040516105829190614237565b60405180910390f35b34801561059757600080fd5b506105a0611553565b6040516105ad9190614363565b60405180910390f35b3480156105c257600080fd5b506105dd60048036036105d891908101906135ed565b611579565b005b3480156105eb57600080fd5b506105f46119a4565b60405161060191906145de565b60405180910390f35b34801561061657600080fd5b50610631600480360361062c91908101906135ed565b6119aa565b005b34801561063f57600080fd5b50610648611e08565b60405161065591906145de565b60405180910390f35b34801561066a57600080fd5b50610673611e12565b604051610680919061428d565b60405180910390f35b34801561069557600080fd5b506106b060048036036106ab91908101906133c9565b611e6a565b005b3480156106be57600080fd5b506106c7612121565b6040516106d49190614303565b60405180910390f35b3480156106e957600080fd5b506106f261212b565b005b34801561070057600080fd5b506107096122d4565b60405161071691906142e8565b60405180910390f35b34801561072b57600080fd5b50610746600480360361074191908101906134fa565b6122f9565b005b34801561075457600080fd5b5061075d612710565b60405161076a91906145f9565b60405180910390f35b34801561077f57600080fd5b50610788612727565b604051610795919061428d565b60405180910390f35b3480156107aa57600080fd5b506107b361277f565b6040516107c091906145de565b60405180910390f35b3480156107d557600080fd5b506107de612789565b6040516107eb91906145f9565b60405180910390f35b34801561080057600080fd5b506108096127a0565b604051610816919061421c565b60405180910390f35b34801561082b57600080fd5b506108346127ca565b6040516108419190614303565b60405180910390f35b34801561085657600080fd5b5061085f6127d4565b60405161086c91906145de565b60405180910390f35b34801561088157600080fd5b5061089c600480360361089791908101906135ed565b6127de565b005b3480156108aa57600080fd5b506108b3612a70565b6040516108c0919061428d565b60405180910390f35b3480156108d557600080fd5b506108de612ac8565b6040516108eb91906145de565b60405180910390f35b34801561090057600080fd5b5061091b600480360361091691908101906136c0565b612cdd565b60405161092891906142e8565b60405180910390f35b34801561093d57600080fd5b50610946613047565b604051610953919061428d565b60405180910390f35b34801561096857600080fd5b5061097161309f565b60405161097e91906145de565b60405180910390f35b34801561099357600080fd5b5061099c6130a5565b6040516109a991906142e8565b60405180910390f35b600d60009054906101000a900460ff16610a01576040517f08c379a00000000000000000000000000000000000000000000000000000000081526004016109f89061449e565b60405180910390fd5b610a09611230565b610a48576040517f08c379a0000000000000000000000000000000000000000000000000000000008152600401610a3f9061457e565b60405180910390fd5b6000809054906101000a900473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff163373ffffffffffffffffffffffffffffffffffffffff161480610af05750600160009054906101000a900473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff163373ffffffffffffffffffffffffffffffffffffffff16145b610b2f576040517f08c379a0000000000000000000000000000000000000000000000000000000008152600401610b26906144fe565b60405180910390fd5b600260009054906101000a900473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff166351428bc0600e84846040518463ffffffff1660e01b8152600401610b8f939291906142af565b60206040518083038186803b158015610ba757600080fd5b505afa158015610bbb573d6000803e3d6000fd5b505050506040513d601f19601f82011682018060405250610bdf919081019061381a565b610c1e576040517f08c379a0000000000000000000000000000000000000000000000000000000008152600401610c159061443e565b60405180910390fd5b600a54600c819055506004546007600082825401925050819055506004546008600082825403925050819055506000600d60006101000a81548160ff021916908315150217905550818160119190610c779291906131eb565b505050565b6000809054906101000a900473ffffffffffffffffffffffffffffffffffffffff1681565b6000601454905090565b610cb3611230565b15610cf3576040517f08c379a0000000000000000000000000000000000000000000000000000000008152600401610cea906144de565b60405180910390fd5b600160009054906101000a900473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff163373ffffffffffffffffffffffffffffffffffffffff1614610d83576040517f08c379a0000000000000000000000000000000000000000000000000000000008152600401610d7a9061451e565b60405180910390fd5b3460086000828254019250508190555060045460085410610e02576004546008600082825403925050819055506004546007600082825401925050819055506005544301600c8190555043600981905550600c54600a81905550600c546015819055506000600d60006101000a81548160ff0219169083151502179055505b565b6000601c54905090565b600d60009054906101000a900460ff1615610e5e576040517f08c379a0000000000000000000000000000000000000000000000000000000008152600401610e55906144be565b60405180910390fd5b610e66611230565b610ea5576040517f08c379a0000000000000000000000000000000000000000000000000000000008152600401610e9c9061457e565b60405180910390fd5b600160009054906101000a900473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff163373ffffffffffffffffffffffffffffffffffffffff1614610f35576040517f08c379a0000000000000000000000000000000000000000000000000000000008152600401610f2c9061451e565b60405180910390fd5b610fc5888880806020026020016040519081016040528093929190818152602001838360200280828437600081840152601f19601f82011690508083019250505050505050878780806020026020016040519081016040528093929190818152602001838360200280828437600081840152601f19601f8201169050808301925050505050505086868686612cdd565b611004576040517f08c379a0000000000000000000000000000000000000000000000000000000008152600401610ffb906143be565b60405180910390fd5b600080905060006110558a8a80806020026020016040519081016040528093929190818152602001838360200280828437600081840152601f19601f820116905080830192505050505050506111fb565b9050600086898990500390505b888890508110156110975788888281811061107957fe5b9050602002013582141561108c57600192505b600181019050611062565b50816110d8576040517f08c379a00000000000000000000000000000000000000000000000000000000081526004016110cf9061445e565b60405180910390fd5b6001600d60006101000a81548160ff0219169083151502179055508787600f91906111049291906131eb565b508560108190555084601260006101000a81548160ff021916908360ff16021790555083601381905550826014819055506003544301600c54111561114f576003544301600c819055505b6004546007600082825403925050819055506004546008600082825401925050819055508989600e91906111849291906131eb565b50858888905003600b8190555050505050505050505050565b60045481565b6060601a8054806020026020016040519081016040528092919081815260200182805480156111f157602002820191906000526020600020905b8154815260200190600101908083116111dd575b5050505050905090565b6000808260405160200161120f91906141a6565b60405160208183030381529060405280519060200120905080915050919050565b600043600c5411905090565b600080878730604051602001611254939291906141bd565b60405160208183030381529060405280519060200120905060008160405160200161127f91906141f6565b6040516020818303038152906040528051906020012090508373ffffffffffffffffffffffffffffffffffffffff16600182898989604051600081526020016040526040516112d1949392919061431e565b6020604051602081039080840390855afa1580156112f3573d6000803e3d6000fd5b5050506020604051035173ffffffffffffffffffffffffffffffffffffffff1614925050509695505050505050565b60008060009054906101000a900473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff163373ffffffffffffffffffffffffffffffffffffffff1614806113cc5750600160009054906101000a900473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff163373ffffffffffffffffffffffffffffffffffffffff16145b61140b576040517f08c379a0000000000000000000000000000000000000000000000000000000008152600401611402906144fe565b60405180910390fd5b600160009054906101000a900473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff163373ffffffffffffffffffffffffffffffffffffffff16141561148a576000809054906101000a900473ffffffffffffffffffffffffffffffffffffffff16905061150d565b6000809054906101000a900473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff163373ffffffffffffffffffffffffffffffffffffffff16141561150957600160009054906101000a900473ffffffffffffffffffffffffffffffffffffffff16905061150d565b3090505b90565b6000600d60009054906101000a900460ff16905090565b60035481565b600160009054906101000a900473ffffffffffffffffffffffffffffffffffffffff1681565b600260009054906101000a900473ffffffffffffffffffffffffffffffffffffffff1681565b600d60009054906101000a900460ff166115c8576040517f08c379a00000000000000000000000000000000000000000000000000000000081526004016115bf9061449e565b60405180910390fd5b6115d0611230565b61160f576040517f08c379a00000000000000000000000000000000000000000000000000000000081526004016116069061457e565b60405180910390fd5b6000809054906101000a900473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff163373ffffffffffffffffffffffffffffffffffffffff1614806116b75750600160009054906101000a900473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff163373ffffffffffffffffffffffffffffffffffffffff16145b6116f6576040517f08c379a00000000000000000000000000000000000000000000000000000000081526004016116ed906144fe565b60405180910390fd5b611767868680806020026020016040519081016040528093929190818152602001838360200280828437600081840152601f19601f8201169050808301925050505050505085858585600160009054906101000a900473ffffffffffffffffffffffffffffffffffffffff1661123c565b6117a6576040517f08c379a000000000000000000000000000000000000000000000000000000000815260040161179d906143fe565b60405180910390fd5b838686905003600b54116117c157838686905003600b819055505b611860600f80548060200260200160405190810160405280929190818152602001828054801561181057602002820191906000526020600020905b8154815260200190600101908083116117fc575b5050505050601054888880806020026020016040519081016040528093929190818152602001838360200280828437600081840152601f19601f82011690508083019250505050505050876130bc565b806119075750611905868680806020026020016040519081016040528093929190818152602001838360200280828437600081840152601f19601f8201169050808301925050505050505085600f8054806020026020016040519081016040528092919081815260200182805480156118f857602002820191906000526020600020905b8154815260200190600101908083116118e4575b50505050506010546130bc565b155b611946576040517f08c379a000000000000000000000000000000000000000000000000000000000815260040161193d9061455e565b60405180910390fd5b600a54600c819055506004546007600082825401925050819055506004546008600082825403925050819055506000600d60006101000a81548160ff0219169083151502179055506011600061199c9190613238565b505050505050565b60055481565b601660009054906101000a900460ff166119f9576040517f08c379a00000000000000000000000000000000000000000000000000000000081526004016119f0906145be565b60405180910390fd5b611a01611230565b611a40576040517f08c379a0000000000000000000000000000000000000000000000000000000008152600401611a379061457e565b60405180910390fd5b6000809054906101000a900473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff163373ffffffffffffffffffffffffffffffffffffffff161480611ae85750600160009054906101000a900473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff163373ffffffffffffffffffffffffffffffffffffffff16145b611b27576040517f08c379a0000000000000000000000000000000000000000000000000000000008152600401611b1e906144fe565b60405180910390fd5b611b98868680806020026020016040519081016040528093929190818152602001838360200280828437600081840152601f19601f8201169050808301925050505050505085858585600160009054906101000a900473ffffffffffffffffffffffffffffffffffffffff1661123c565b611bd7576040517f08c379a0000000000000000000000000000000000000000000000000000000008152600401611bce906143fe565b60405180910390fd5b60008090506000611c376017805480602002602001604051908101604052809291908181526020018280548015611c2d57602002820191906000526020600020905b815481526020019060010190808311611c19575b50505050506111fb565b905060008090505b868989905003811015611c7657888882818110611c5857fe5b90506020020135821415611c6b57600192505b600181019050611c3f565b5081611cb7576040517f08c379a0000000000000000000000000000000000000000000000000000000008152600401611cae9061437e565b60405180910390fd5b611d566018805480602002602001604051908101604052809291908181526020018280548015611d0657602002820191906000526020600020905b815481526020019060010190808311611cf2575b50505050506019548a8a80806020026020016040519081016040528093929190818152602001838360200280828437600081840152601f19601f82011690508083019250505050505050896130bc565b611d95576040517f08c379a0000000000000000000000000000000000000000000000000000000008152600401611d8c9061447e565b60405180910390fd5b6000601660006101000a81548160ff021916908315150217905550858888905003600b81905550878760189190611dcd9291906131eb565b508560198190555084601b60006101000a81548160ff021916908360ff16021790555083601c8190555082601d819055505050505050505050565b6000600c54905090565b60606011805480602002602001604051908101604052809291908181526020018280548015611e6057602002820191906000526020600020905b815481526020019060010190808311611e4c575b5050505050905090565b6000809054906101000a900473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff163373ffffffffffffffffffffffffffffffffffffffff161480611f125750600160009054906101000a900473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff163373ffffffffffffffffffffffffffffffffffffffff16145b611f51576040517f08c379a0000000000000000000000000000000000000000000000000000000008152600401611f48906144fe565b60405180910390fd5b6000809054906101000a900473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff163373ffffffffffffffffffffffffffffffffffffffff161415612037576000600754905043600c54118015611fcb5750600d60009054906101000a900460ff16155b15611fda576004546007540390505b806007600082825403925050819055508173ffffffffffffffffffffffffffffffffffffffff166108fc829081150290604051600060405180830381858888f19350505050158015612030573d6000803e3d6000fd5b505061211e565b600160009054906101000a900473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff163373ffffffffffffffffffffffffffffffffffffffff16141561211d576000600854905043600c541180156120b15750600d60009054906101000a900460ff165b156120c0576004546008540390505b806008600082825403925050819055508173ffffffffffffffffffffffffffffffffffffffff166108fc829081150290604051600060405180830381858888f19350505050158015612116573d6000803e3d6000fd5b505061211e565b5b50565b6000601354905090565b601660009054906101000a900460ff1661217a576040517f08c379a0000000000000000000000000000000000000000000000000000000008152600401612171906145be565b60405180910390fd5b6000809054906101000a900473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff163373ffffffffffffffffffffffffffffffffffffffff1614806122225750600160009054906101000a900473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff163373ffffffffffffffffffffffffffffffffffffffff16145b612261576040517f08c379a0000000000000000000000000000000000000000000000000000000008152600401612258906144fe565b60405180910390fd5b6122696122d4565b156122d25743600c8190555043600a81905550600d60009054906101000a900460ff16156122d1576004546007600082825401925050819055506004546008600082825403925050819055506000600d60006101000a81548160ff0219169083151502179055505b5b565b600043601554111580156122f45750601660009054906101000a900460ff165b905090565b601660009054906101000a900460ff1615612349576040517f08c379a00000000000000000000000000000000000000000000000000000000081526004016123409061459e565b60405180910390fd5b612351611230565b612390576040517f08c379a00000000000000000000000000000000000000000000000000000000081526004016123879061457e565b60405180910390fd5b6000809054906101000a900473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff163373ffffffffffffffffffffffffffffffffffffffff161461241f576040517f08c379a00000000000000000000000000000000000000000000000000000000081526004016124169061451e565b60405180910390fd5b600260009054906101000a900473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff166351428bc08b8b85856040518563ffffffff1660e01b81526004016124809493929190614252565b60206040518083038186803b15801561249857600080fd5b505afa1580156124ac573d6000803e3d6000fd5b505050506040513d601f19601f820116820180604052506124d0919081019061381a565b61250f576040517f08c379a00000000000000000000000000000000000000000000000000000000081526004016125069061443e565b60405180910390fd5b612580888880806020026020016040519081016040528093929190818152602001838360200280828437600081840152601f19601f8201169050808301925050505050505087878787600160009054906101000a900473ffffffffffffffffffffffffffffffffffffffff1661123c565b6125bf576040517f08c379a00000000000000000000000000000000000000000000000000000000081526004016125b6906143fe565b60405180910390fd5b600080905060006126108c8c80806020026020016040519081016040528093929190818152602001838360200280828437600081840152601f19601f820116905080830192505050505050506111fb565b90506000888b8b90500390505b8a8a9050811015612652578a8a8281811061263457fe5b9050602002013582141561264757600192505b60018101905061261d565b5081612693576040517f08c379a000000000000000000000000000000000000000000000000000000000815260040161268a9061441e565b60405180910390fd5b6001601660006101000a81548160ff0219169083151502179055508989601891906126bf9291906131eb565b50876019819055508b8b601791906126d89291906131eb565b508383601a91906126ea9291906131eb565b506003544301601581905550878a8a905003600b81905550505050505050505050505050565b6000601b60009054906101000a900460ff16905090565b6060601880548060200260200160405190810160405280929190818152602001828054801561277557602002820191906000526020600020905b815481526020019060010190808311612761575b5050505050905090565b6000601954905090565b6000601260009054906101000a900460ff16905090565b6000600260009054906101000a900473ffffffffffffffffffffffffffffffffffffffff16905090565b6000601d54905090565b6000600954905090565b6127e6611230565b612825576040517f08c379a000000000000000000000000000000000000000000000000000000000815260040161281c9061457e565b60405180910390fd5b6000809054906101000a900473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff163373ffffffffffffffffffffffffffffffffffffffff1614806128cd5750600160009054906101000a900473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff163373ffffffffffffffffffffffffffffffffffffffff16145b61290c576040517f08c379a0000000000000000000000000000000000000000000000000000000008152600401612903906144fe565b60405180910390fd5b61297d868680806020026020016040519081016040528093929190818152602001838360200280828437600081840152601f19601f8201169050808301925050505050505085858585600160009054906101000a900473ffffffffffffffffffffffffffffffffffffffff1661123c565b6129bc576040517f08c379a00000000000000000000000000000000000000000000000000000000081526004016129b3906143fe565b60405180910390fd5b60065484878790500311612a05576040517f08c379a00000000000000000000000000000000000000000000000000000000081526004016129fc9061453e565b60405180910390fd5b600d60009054906101000a900460ff1615612a5a576004546007600082825401925050819055506004546008600082825403925050819055506000600d60006101000a81548160ff0219169083151502179055505b43600c8190555043600a81905550505050505050565b6060600e805480602002602001604051908101604052809291908181526020018280548015612abe57602002820191906000526020600020905b815481526020019060010190808311612aaa575b5050505050905090565b60008060009054906101000a900473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff163373ffffffffffffffffffffffffffffffffffffffff161480612b725750600160009054906101000a900473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff163373ffffffffffffffffffffffffffffffffffffffff16145b612bb1576040517f08c379a0000000000000000000000000000000000000000000000000000000008152600401612ba8906144fe565b60405180910390fd5b6000809054906101000a900473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff163373ffffffffffffffffffffffffffffffffffffffff161415612c43576000600754905043600c54118015612c2b5750600d60009054906101000a900460ff16155b15612c3a576004546007540390505b80915050612cda565b600160009054906101000a900473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff163373ffffffffffffffffffffffffffffffffffffffff161415612cd5576000600854905043600c54118015612cbd5750600d60009054906101000a900460ff165b15612ccc576004546008540390505b80915050612cda565b600090505b90565b6000600d60009054906101000a900460ff1615612d2f576040517f08c379a0000000000000000000000000000000000000000000000000000000008152600401612d26906144be565b60405180910390fd5b612d37611230565b612d76576040517f08c379a0000000000000000000000000000000000000000000000000000000008152600401612d6d9061457e565b60405180910390fd5b600160009054906101000a900473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff163373ffffffffffffffffffffffffffffffffffffffff1614612e06576040517f08c379a0000000000000000000000000000000000000000000000000000000008152600401612dfd9061451e565b60405180910390fd5b84865103600b541115612e4e576040517f08c379a0000000000000000000000000000000000000000000000000000000008152600401612e459061439e565b60405180910390fd5b600260009054906101000a900473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16631bf28f83886040518263ffffffff1660e01b8152600401612ea9919061428d565b60206040518083038186803b158015612ec157600080fd5b505afa158015612ed5573d6000803e3d6000fd5b505050506040513d601f19601f82011682018060405250612ef9919081019061381a565b612f38576040517f08c379a0000000000000000000000000000000000000000000000000000000008152600401612f2f906143de565b60405180910390fd5b612f688686868686600160009054906101000a900473ffffffffffffffffffffffffffffffffffffffff1661123c565b612fa7576040517f08c379a0000000000000000000000000000000000000000000000000000000008152600401612f9e906143fe565b60405180910390fd5b60008090506000612fb7896111fb565b905060008789510390505b8851811015612ff657888181518110612fd757fe5b6020026020010151821415612feb57600192505b600181019050612fc2565b5081613037576040517f08c379a000000000000000000000000000000000000000000000000000000000815260040161302e9061441e565b60405180910390fd5b6001925050509695505050505050565b6060601780548060200260200160405190810160405280929190818152602001828054801561309557602002820191906000526020600020905b815481526020019060010190808311613081575b5050505050905090565b60065481565b6000601660009054906101000a900460ff16905090565b60008060008060008090505b8789510381101561314e578881815181106130df57fe5b602002602001015192506000935060008090505b868851038110156131305787818151811061310a57fe5b60200260200101519250828414156131255760019450613130565b6001810190506130f3565b50836131435760009450505050506131e3565b6001810190506130c8565b5060008789510390505b88518110156131da5788818151811061316d57fe5b602002602001015192506000935060008090505b87518110156131bc5787818151811061319657fe5b60200260200101519250828414156131b157600194506131bc565b600181019050613181565b50836131cf5760009450505050506131e3565b600181019050613158565b50600193505050505b949350505050565b828054828255906000526020600020908101928215613227579160200282015b8281111561322657823582559160200191906001019061320b565b5b5090506132349190613259565b5090565b50805460008255906000526020600020908101906132569190613259565b50565b61327b91905b8082111561327757600081600090555060010161325f565b5090565b90565b60008135905061328d81614823565b92915050565b6000813590506132a28161483a565b92915050565b60008083601f8401126132ba57600080fd5b8235905067ffffffffffffffff8111156132d357600080fd5b6020830191508360208202830111156132eb57600080fd5b9250929050565b600082601f83011261330357600080fd5b813561331661331182614641565b614614565b9150818183526020840193506020810190508385602084028201111561333b57600080fd5b60005b8381101561336b5781613351888261338a565b84526020840193506020830192505060018101905061333e565b5050505092915050565b60008151905061338481614851565b92915050565b60008135905061339981614868565b92915050565b6000813590506133ae8161487f565b92915050565b6000813590506133c381614896565b92915050565b6000602082840312156133db57600080fd5b60006133e984828501613293565b91505092915050565b6000806020838503121561340557600080fd5b600083013567ffffffffffffffff81111561341f57600080fd5b61342b858286016132a8565b92509250509250929050565b60008060008060008060008060c0898b03121561345357600080fd5b600089013567ffffffffffffffff81111561346d57600080fd5b6134798b828c016132a8565b9850985050602089013567ffffffffffffffff81111561349857600080fd5b6134a48b828c016132a8565b965096505060406134b78b828c0161339f565b94505060606134c88b828c016133b4565b93505060806134d98b828c0161338a565b92505060a06134ea8b828c0161338a565b9150509295985092959890939650565b60008060008060008060008060008060e08b8d03121561351957600080fd5b60008b013567ffffffffffffffff81111561353357600080fd5b61353f8d828e016132a8565b9a509a505060208b013567ffffffffffffffff81111561355e57600080fd5b61356a8d828e016132a8565b9850985050604061357d8d828e0161339f565b965050606061358e8d828e016133b4565b955050608061359f8d828e0161338a565b94505060a06135b08d828e0161338a565b93505060c08b013567ffffffffffffffff8111156135cd57600080fd5b6135d98d828e016132a8565b92509250509295989b9194979a5092959850565b60008060008060008060a0878903121561360657600080fd5b600087013567ffffffffffffffff81111561362057600080fd5b61362c89828a016132a8565b9650965050602061363f89828a0161339f565b945050604061365089828a016133b4565b935050606061366189828a0161338a565b925050608061367289828a0161338a565b9150509295509295509295565b60006020828403121561369157600080fd5b600082013567ffffffffffffffff8111156136ab57600080fd5b6136b7848285016132f2565b91505092915050565b60008060008060008060c087890312156136d957600080fd5b600087013567ffffffffffffffff8111156136f357600080fd5b6136ff89828a016132f2565b965050602087013567ffffffffffffffff81111561371c57600080fd5b61372889828a016132f2565b955050604061373989828a0161339f565b945050606061374a89828a016133b4565b935050608061375b89828a0161338a565b92505060a061376c89828a0161338a565b9150509295509295509295565b60008060008060008060c0878903121561379257600080fd5b600087013567ffffffffffffffff8111156137ac57600080fd5b6137b889828a016132f2565b96505060206137c989828a0161339f565b95505060406137da89828a016133b4565b94505060606137eb89828a0161338a565b93505060806137fc89828a0161338a565b92505060a061380d89828a0161327e565b9150509295509295509295565b60006020828403121561382c57600080fd5b600061383a84828501613375565b91505092915050565b600061384f8383613a30565b60208301905092915050565b60006138678383613a4e565b60208301905092915050565b61387c81614712565b82525050565b61389361388e82614712565b6147be565b82525050565b6138a281614700565b82525050565b60006138b483856146be565b93507f07ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff8311156138e357600080fd5b6020830292506138f4838584614795565b82840190509392505050565b600061390b8261468e565b61391581856146be565b935061392083614669565b8060005b838110156139515781516139388882613843565b9750613943836146a4565b925050600181019050613924565b5085935050505092915050565b60006139698261468e565b61397381856146cf565b935061397e83614669565b8060005b838110156139af578151613996888261385b565b97506139a1836146a4565b925050600181019050613982565b5085935050505092915050565b60006139c782614699565b6139d181856146be565b93506139dc83614679565b8060005b83811015613a14576139f1826147f6565b6139fb8882613843565b9750613a06836146b1565b9250506001810190506139e0565b5085935050505092915050565b613a2a81614724565b82525050565b613a3981614730565b82525050565b613a4881614730565b82525050565b613a5781614730565b82525050565b613a6e613a6982614730565b6147d0565b82525050565b613a7d81614771565b82525050565b6000613a90601c836146eb565b91507f19457468657265756d205369676e6564204d6573736167653a0a3332000000006000830152601c82019050919050565b6000613ad0602f836146da565b91507f5175657374696f6e206973206e6f7420696e2074686520616e7377657265642060008301527f6861736865732070726f766964656400000000000000000000000000000000006020830152604082019050919050565b6000613b366039836146da565b91507f43616e27742061707065616c206f6e206c65737320616e73776572656420717560008301527f657374696f6e73207468616e2073686f776e206265666f7265000000000000006020830152604082019050919050565b6000613b9c600f836146da565b91507f436f756c646e27742061707065616c00000000000000000000000000000000006000830152602082019050919050565b6000613bdc6019836146da565b91507f5175657374696f6e2073686f756c642062652076616c69642e000000000000006000830152602082019050919050565b6000613c1c601f836146da565b91507f48617368657320617265206e6f74207369676e656420636f72726563746c79006000830152602082019050919050565b6000613c5c6031836146da565b91507f5175657374696f6e206973206e6f7420696e2074686520756e616e737765726560008301527f64206861736865732070726f76696465640000000000000000000000000000006020830152604082019050919050565b6000613cc2601d836146da565b91507f416e737765722073686f756c64206d61746368207175657374696f6e2e0000006000830152602082019050919050565b6000613d02602f836146da565b91507f7175657374696f6e2061707065616c6564206d75737420626520696e20756e6160008301527f6e737765726564206861736865737300000000000000000000000000000000006020830152604082019050919050565b6000613d68602a836146da565b91507f43616e27742070726f76696465206f6c646572206f7220646966666572656e7460008301527f207369676e6174757265000000000000000000000000000000000000000000006020830152604082019050919050565b6000613dce602c836146da565b91507f43616e27742075736520746869732066756e6374696f6e207768696c65206e6f60008301527f742061707065616c696e672e00000000000000000000000000000000000000006020830152604082019050919050565b6000613e346028836146da565b91507f43616e27742075736520746869732066756e6374696f6e207768696c6520617060008301527f7065616c696e672e0000000000000000000000000000000000000000000000006020830152604082019050919050565b6000613e9a6024836146da565b91507f43616e27742075736520746869732066756e6374696f6e207768656e2061637460008301527f6976652e000000000000000000000000000000000000000000000000000000006020830152604082019050919050565b6000613f006025836146da565b91507f4f6e6c7920616e206f776e65722063616e2063616c6c20746869732066756e6360008301527f74696f6e2e0000000000000000000000000000000000000000000000000000006020830152604082019050919050565b6000613f666029836146da565b91507f4f6e6c792074686520636f7374756d65722063616e2063616c6c20746869732060008301527f66756e6374696f6e2e00000000000000000000000000000000000000000000006020830152604082019050919050565b6000613fcc6017836146da565b91507f6469646e74207265616368206d617820717565726965730000000000000000006000830152602082019050919050565b600061400c601c836146da565b91507f6469736d6973732077697468206f6c646572207369676e6174757265000000006000830152602082019050919050565b600061404c6028836146da565b91507f43616e27742075736520746869732066756e6374696f6e207768656e206e6f7460008301527f206163746976652e0000000000000000000000000000000000000000000000006020830152604082019050919050565b60006140b26028836146da565b91507f43616e27742075736520746869732066756e6374696f6e207768696c6520646560008301527f6d616e64696e672e0000000000000000000000000000000000000000000000006020830152604082019050919050565b6000614118602c836146da565b91507f43616e27742075736520746869732066756e6374696f6e207768696c65206e6f60008301527f742064656d616e64696e672e00000000000000000000000000000000000000006020830152604082019050919050565b61417a8161475a565b82525050565b61419161418c8261475a565b6147ec565b82525050565b6141a081614764565b82525050565b60006141b2828461395e565b915081905092915050565b60006141c9828661395e565b91506141d58285614180565b6020820191506141e58284613882565b601482019150819050949350505050565b600061420182613a83565b915061420d8284613a5d565b60208201915081905092915050565b60006020820190506142316000830184613899565b92915050565b600060208201905061424c6000830184613873565b92915050565b6000604082019050818103600083015261426d8186886138a8565b905081810360208301526142828184866138a8565b905095945050505050565b600060208201905081810360008301526142a78184613900565b905092915050565b600060408201905081810360008301526142c981866139bc565b905081810360208301526142de8184866138a8565b9050949350505050565b60006020820190506142fd6000830184613a21565b92915050565b60006020820190506143186000830184613a3f565b92915050565b60006080820190506143336000830187613a3f565b6143406020830186614197565b61434d6040830185613a3f565b61435a6060830184613a3f565b95945050505050565b60006020820190506143786000830184613a74565b92915050565b6000602082019050818103600083015261439781613ac3565b9050919050565b600060208201905081810360008301526143b781613b29565b9050919050565b600060208201905081810360008301526143d781613b8f565b9050919050565b600060208201905081810360008301526143f781613bcf565b9050919050565b6000602082019050818103600083015261441781613c0f565b9050919050565b6000602082019050818103600083015261443781613c4f565b9050919050565b6000602082019050818103600083015261445781613cb5565b9050919050565b6000602082019050818103600083015261447781613cf5565b9050919050565b6000602082019050818103600083015261449781613d5b565b9050919050565b600060208201905081810360008301526144b781613dc1565b9050919050565b600060208201905081810360008301526144d781613e27565b9050919050565b600060208201905081810360008301526144f781613e8d565b9050919050565b6000602082019050818103600083015261451781613ef3565b9050919050565b6000602082019050818103600083015261453781613f59565b9050919050565b6000602082019050818103600083015261455781613fbf565b9050919050565b6000602082019050818103600083015261457781613fff565b9050919050565b600060208201905081810360008301526145978161403f565b9050919050565b600060208201905081810360008301526145b7816140a5565b9050919050565b600060208201905081810360008301526145d78161410b565b9050919050565b60006020820190506145f36000830184614171565b92915050565b600060208201905061460e6000830184614197565b92915050565b6000604051905081810181811067ffffffffffffffff8211171561463757600080fd5b8060405250919050565b600067ffffffffffffffff82111561465857600080fd5b602082029050602081019050919050565b6000819050602082019050919050565b60008190508160005260206000209050919050565b600081519050919050565b600081549050919050565b6000602082019050919050565b6000600182019050919050565b600082825260208201905092915050565b600081905092915050565b600082825260208201905092915050565b600081905092915050565b6000819050919050565b600061470b8261473a565b9050919050565b600061471d8261473a565b9050919050565b60008115159050919050565b6000819050919050565b600073ffffffffffffffffffffffffffffffffffffffff82169050919050565b6000819050919050565b600060ff82169050919050565b600061477c82614783565b9050919050565b600061478e8261473a565b9050919050565b82818337600083830152505050565b60006147b76147b283614816565b6146f6565b9050919050565b60006147c9826147da565b9050919050565b6000819050919050565b60006147e582614809565b9050919050565b6000819050919050565b600061480282546147a4565b9050919050565b60008160601b9050919050565b60008160001c9050919050565b61482c81614700565b811461483757600080fd5b50565b61484381614712565b811461484e57600080fd5b50565b61485a81614724565b811461486557600080fd5b50565b61487181614730565b811461487c57600080fd5b50565b6148888161475a565b811461489357600080fd5b50565b61489f81614764565b81146148aa57600080fd5b5056fea365627a7a72315820dc05e4e158a538e1b5741a373d911fe531827e01d1a10cb626a9adee6b6d17c86c6578706572696d656e74616cf564736f6c63430005110040",
    "opcodes": "PUSH1 0x80 PUSH1 0x40 MSTORE CALLVALUE DUP1 ISZERO PUSH3 0x11 JUMPI PUSH1 0x0 DUP1 REVERT JUMPDEST POP PUSH1 0x40 MLOAD PUSH3 0x4BE7 CODESIZE SUB DUP1 PUSH3 0x4BE7 DUP4 CODECOPY DUP2 DUP2 ADD PUSH1 0x40 MSTORE PUSH3 0x37 SWAP2 SWAP1 DUP2 ADD SWAP1 PUSH3 0x1B1 JUMP JUMPDEST CALLER PUSH1 0x0 DUP1 PUSH2 0x100 EXP DUP2 SLOAD DUP2 PUSH20 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF MUL NOT AND SWAP1 DUP4 PUSH20 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF AND MUL OR SWAP1 SSTORE POP DUP6 PUSH1 0x1 PUSH1 0x0 PUSH2 0x100 EXP DUP2 SLOAD DUP2 PUSH20 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF MUL NOT AND SWAP1 DUP4 PUSH20 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF AND MUL OR SWAP1 SSTORE POP DUP5 PUSH1 0x3 DUP2 SWAP1 SSTORE POP DUP4 PUSH1 0x4 DUP2 SWAP1 SSTORE POP DUP3 PUSH1 0x5 DUP2 SWAP1 SSTORE POP DUP2 PUSH1 0x2 PUSH1 0x0 PUSH2 0x100 EXP DUP2 SLOAD DUP2 PUSH20 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF MUL NOT AND SWAP1 DUP4 PUSH20 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF AND MUL OR SWAP1 SSTORE POP DUP1 PUSH1 0x6 DUP2 SWAP1 SSTORE POP PUSH1 0x0 PUSH1 0xC DUP2 SWAP1 SSTORE POP PUSH1 0x0 PUSH1 0xA DUP2 SWAP1 SSTORE POP PUSH1 0x0 PUSH1 0x15 DUP2 SWAP1 SSTORE POP PUSH1 0x0 PUSH1 0x7 DUP2 SWAP1 SSTORE POP PUSH1 0x0 PUSH1 0x8 DUP2 SWAP1 SSTORE POP PUSH1 0x0 PUSH1 0xB DUP2 SWAP1 SSTORE POP PUSH1 0x0 PUSH1 0xD PUSH1 0x0 PUSH2 0x100 EXP DUP2 SLOAD DUP2 PUSH1 0xFF MUL NOT AND SWAP1 DUP4 ISZERO ISZERO MUL OR SWAP1 SSTORE POP POP POP POP POP POP POP PUSH3 0x2E7 JUMP JUMPDEST PUSH1 0x0 DUP2 MLOAD SWAP1 POP PUSH3 0x17D DUP2 PUSH3 0x299 JUMP JUMPDEST SWAP3 SWAP2 POP POP JUMP JUMPDEST PUSH1 0x0 DUP2 MLOAD SWAP1 POP PUSH3 0x194 DUP2 PUSH3 0x2B3 JUMP JUMPDEST SWAP3 SWAP2 POP POP JUMP JUMPDEST PUSH1 0x0 DUP2 MLOAD SWAP1 POP PUSH3 0x1AB DUP2 PUSH3 0x2CD JUMP JUMPDEST SWAP3 SWAP2 POP POP JUMP JUMPDEST PUSH1 0x0 DUP1 PUSH1 0x0 DUP1 PUSH1 0x0 DUP1 PUSH1 0xC0 DUP8 DUP10 SUB SLT ISZERO PUSH3 0x1CB JUMPI PUSH1 0x0 DUP1 REVERT JUMPDEST PUSH1 0x0 PUSH3 0x1DB DUP10 DUP3 DUP11 ADD PUSH3 0x183 JUMP JUMPDEST SWAP7 POP POP PUSH1 0x20 PUSH3 0x1EE DUP10 DUP3 DUP11 ADD PUSH3 0x19A JUMP JUMPDEST SWAP6 POP POP PUSH1 0x40 PUSH3 0x201 DUP10 DUP3 DUP11 ADD PUSH3 0x19A JUMP JUMPDEST SWAP5 POP POP PUSH1 0x60 PUSH3 0x214 DUP10 DUP3 DUP11 ADD PUSH3 0x19A JUMP JUMPDEST SWAP4 POP POP PUSH1 0x80 PUSH3 0x227 DUP10 DUP3 DUP11 ADD PUSH3 0x16C JUMP JUMPDEST SWAP3 POP POP PUSH1 0xA0 PUSH3 0x23A DUP10 DUP3 DUP11 ADD PUSH3 0x19A JUMP JUMPDEST SWAP2 POP POP SWAP3 SWAP6 POP SWAP3 SWAP6 POP SWAP3 SWAP6 JUMP JUMPDEST PUSH1 0x0 PUSH3 0x254 DUP3 PUSH3 0x26F JUMP JUMPDEST SWAP1 POP SWAP2 SWAP1 POP JUMP JUMPDEST PUSH1 0x0 PUSH3 0x268 DUP3 PUSH3 0x26F JUMP JUMPDEST SWAP1 POP SWAP2 SWAP1 POP JUMP JUMPDEST PUSH1 0x0 PUSH20 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF DUP3 AND SWAP1 POP SWAP2 SWAP1 POP JUMP JUMPDEST PUSH1 0x0 DUP2 SWAP1 POP SWAP2 SWAP1 POP JUMP JUMPDEST PUSH3 0x2A4 DUP2 PUSH3 0x247 JUMP JUMPDEST DUP2 EQ PUSH3 0x2B0 JUMPI PUSH1 0x0 DUP1 REVERT JUMPDEST POP JUMP JUMPDEST PUSH3 0x2BE DUP2 PUSH3 0x25B JUMP JUMPDEST DUP2 EQ PUSH3 0x2CA JUMPI PUSH1 0x0 DUP1 REVERT JUMPDEST POP JUMP JUMPDEST PUSH3 0x2D8 DUP2 PUSH3 0x28F JUMP JUMPDEST DUP2 EQ PUSH3 0x2E4 JUMPI PUSH1 0x0 DUP1 REVERT JUMPDEST POP JUMP JUMPDEST PUSH2 0x48F0 DUP1 PUSH3 0x2F7 PUSH1 0x0 CODECOPY PUSH1 0x0 RETURN INVALID PUSH1 0x80 PUSH1 0x40 MSTORE PUSH1 0x4 CALLDATASIZE LT PUSH2 0x23B JUMPI PUSH1 0x0 CALLDATALOAD PUSH1 0xE0 SHR DUP1 PUSH4 0x6D3F8998 GT PUSH2 0x12E JUMPI DUP1 PUSH4 0x93C3DA8C GT PUSH2 0xAB JUMPI DUP1 PUSH4 0xD914E4E0 GT PUSH2 0x6F JUMPI DUP1 PUSH4 0xD914E4E0 EQ PUSH2 0x8C9 JUMPI DUP1 PUSH4 0xE5F03799 EQ PUSH2 0x8F4 JUMPI DUP1 PUSH4 0xEECB5DED EQ PUSH2 0x931 JUMPI DUP1 PUSH4 0xF13BD54C EQ PUSH2 0x95C JUMPI DUP1 PUSH4 0xFBAC9443 EQ PUSH2 0x987 JUMPI PUSH2 0x23B JUMP JUMPDEST DUP1 PUSH4 0x93C3DA8C EQ PUSH2 0x7F4 JUMPI DUP1 PUSH4 0xB0433E94 EQ PUSH2 0x81F JUMPI DUP1 PUSH4 0xB107D50C EQ PUSH2 0x84A JUMPI DUP1 PUSH4 0xBFAE1D0F EQ PUSH2 0x875 JUMPI DUP1 PUSH4 0xD14867FE EQ PUSH2 0x89E JUMPI PUSH2 0x23B JUMP JUMPDEST DUP1 PUSH4 0x76C3D965 GT PUSH2 0xF2 JUMPI DUP1 PUSH4 0x76C3D965 EQ PUSH2 0x71F JUMPI DUP1 PUSH4 0x8463EEDD EQ PUSH2 0x748 JUMPI DUP1 PUSH4 0x8AB6FAD1 EQ PUSH2 0x773 JUMPI DUP1 PUSH4 0x8F0C1A14 EQ PUSH2 0x79E JUMPI DUP1 PUSH4 0x8F145525 EQ PUSH2 0x7C9 JUMPI PUSH2 0x23B JUMP JUMPDEST DUP1 PUSH4 0x6D3F8998 EQ PUSH2 0x65E JUMPI DUP1 PUSH4 0x6DDF2254 EQ PUSH2 0x689 JUMPI DUP1 PUSH4 0x7317D73F EQ PUSH2 0x6B2 JUMPI DUP1 PUSH4 0x73398395 EQ PUSH2 0x6DD JUMPI DUP1 PUSH4 0x75B6A366 EQ PUSH2 0x6F4 JUMPI PUSH2 0x23B JUMP JUMPDEST DUP1 PUSH4 0x1C08FBC6 GT PUSH2 0x1BC JUMPI DUP1 PUSH4 0x3A5381B5 GT PUSH2 0x180 JUMPI DUP1 PUSH4 0x3A5381B5 EQ PUSH2 0x58B JUMPI DUP1 PUSH4 0x4E621157 EQ PUSH2 0x5B6 JUMPI DUP1 PUSH4 0x630C24A1 EQ PUSH2 0x5DF JUMPI DUP1 PUSH4 0x6B34C8C2 EQ PUSH2 0x60A JUMPI DUP1 PUSH4 0x6B5E332A EQ PUSH2 0x633 JUMPI PUSH2 0x23B JUMP JUMPDEST DUP1 PUSH4 0x1C08FBC6 EQ PUSH2 0x4A2 JUMPI DUP1 PUSH4 0x1CC368F8 EQ PUSH2 0x4DF JUMPI DUP1 PUSH4 0x1E550B13 EQ PUSH2 0x50A JUMPI DUP1 PUSH4 0x24ED685D EQ PUSH2 0x535 JUMPI DUP1 PUSH4 0x2804B2C0 EQ PUSH2 0x560 JUMPI PUSH2 0x23B JUMP JUMPDEST DUP1 PUSH4 0x121273B9 GT PUSH2 0x203 JUMPI DUP1 PUSH4 0x121273B9 EQ PUSH2 0x3BB JUMPI DUP1 PUSH4 0x13FAEDE6 EQ PUSH2 0x3E4 JUMPI DUP1 PUSH4 0x14E1306C EQ PUSH2 0x40F JUMPI DUP1 PUSH4 0x1595BE3A EQ PUSH2 0x43A JUMPI DUP1 PUSH4 0x1A8012E4 EQ PUSH2 0x477 JUMPI PUSH2 0x23B JUMP JUMPDEST DUP1 PUSH4 0x57489FA EQ PUSH2 0x307 JUMPI DUP1 PUSH4 0x85D4883 EQ PUSH2 0x330 JUMPI DUP1 PUSH4 0xBC2FDE3 EQ PUSH2 0x35B JUMPI DUP1 PUSH4 0xF15F4C0 EQ PUSH2 0x386 JUMPI DUP1 PUSH4 0x1177F72D EQ PUSH2 0x390 JUMPI JUMPDEST PUSH1 0x1 PUSH1 0x0 SWAP1 SLOAD SWAP1 PUSH2 0x100 EXP SWAP1 DIV PUSH20 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF AND PUSH20 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF AND CALLER PUSH20 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF AND EQ ISZERO PUSH2 0x2A6 JUMPI CALLVALUE PUSH1 0x8 PUSH1 0x0 DUP3 DUP3 SLOAD ADD SWAP3 POP POP DUP2 SWAP1 SSTORE POP PUSH2 0x305 JUMP JUMPDEST PUSH1 0x0 DUP1 SWAP1 SLOAD SWAP1 PUSH2 0x100 EXP SWAP1 DIV PUSH20 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF AND PUSH20 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF AND CALLER PUSH20 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF AND EQ ISZERO PUSH2 0x300 JUMPI PUSH1 0x0 DUP1 REVERT JUMPDEST PUSH1 0x0 DUP1 REVERT JUMPDEST STOP JUMPDEST CALLVALUE DUP1 ISZERO PUSH2 0x313 JUMPI PUSH1 0x0 DUP1 REVERT JUMPDEST POP PUSH2 0x32E PUSH1 0x4 DUP1 CALLDATASIZE SUB PUSH2 0x329 SWAP2 SWAP1 DUP2 ADD SWAP1 PUSH2 0x33F2 JUMP JUMPDEST PUSH2 0x9B2 JUMP JUMPDEST STOP JUMPDEST CALLVALUE DUP1 ISZERO PUSH2 0x33C JUMPI PUSH1 0x0 DUP1 REVERT JUMPDEST POP PUSH2 0x345 PUSH2 0xC7C JUMP JUMPDEST PUSH1 0x40 MLOAD PUSH2 0x352 SWAP2 SWAP1 PUSH2 0x4237 JUMP JUMPDEST PUSH1 0x40 MLOAD DUP1 SWAP2 SUB SWAP1 RETURN JUMPDEST CALLVALUE DUP1 ISZERO PUSH2 0x367 JUMPI PUSH1 0x0 DUP1 REVERT JUMPDEST POP PUSH2 0x370 PUSH2 0xCA1 JUMP JUMPDEST PUSH1 0x40 MLOAD PUSH2 0x37D SWAP2 SWAP1 PUSH2 0x4303 JUMP JUMPDEST PUSH1 0x40 MLOAD DUP1 SWAP2 SUB SWAP1 RETURN JUMPDEST PUSH2 0x38E PUSH2 0xCAB JUMP JUMPDEST STOP JUMPDEST CALLVALUE DUP1 ISZERO PUSH2 0x39C JUMPI PUSH1 0x0 DUP1 REVERT JUMPDEST POP PUSH2 0x3A5 PUSH2 0xE04 JUMP JUMPDEST PUSH1 0x40 MLOAD PUSH2 0x3B2 SWAP2 SWAP1 PUSH2 0x4303 JUMP JUMPDEST PUSH1 0x40 MLOAD DUP1 SWAP2 SUB SWAP1 RETURN JUMPDEST CALLVALUE DUP1 ISZERO PUSH2 0x3C7 JUMPI PUSH1 0x0 DUP1 REVERT JUMPDEST POP PUSH2 0x3E2 PUSH1 0x4 DUP1 CALLDATASIZE SUB PUSH2 0x3DD SWAP2 SWAP1 DUP2 ADD SWAP1 PUSH2 0x3437 JUMP JUMPDEST PUSH2 0xE0E JUMP JUMPDEST STOP JUMPDEST CALLVALUE DUP1 ISZERO PUSH2 0x3F0 JUMPI PUSH1 0x0 DUP1 REVERT JUMPDEST POP PUSH2 0x3F9 PUSH2 0x119D JUMP JUMPDEST PUSH1 0x40 MLOAD PUSH2 0x406 SWAP2 SWAP1 PUSH2 0x45DE JUMP JUMPDEST PUSH1 0x40 MLOAD DUP1 SWAP2 SUB SWAP1 RETURN JUMPDEST CALLVALUE DUP1 ISZERO PUSH2 0x41B JUMPI PUSH1 0x0 DUP1 REVERT JUMPDEST POP PUSH2 0x424 PUSH2 0x11A3 JUMP JUMPDEST PUSH1 0x40 MLOAD PUSH2 0x431 SWAP2 SWAP1 PUSH2 0x428D JUMP JUMPDEST PUSH1 0x40 MLOAD DUP1 SWAP2 SUB SWAP1 RETURN JUMPDEST CALLVALUE DUP1 ISZERO PUSH2 0x446 JUMPI PUSH1 0x0 DUP1 REVERT JUMPDEST POP PUSH2 0x461 PUSH1 0x4 DUP1 CALLDATASIZE SUB PUSH2 0x45C SWAP2 SWAP1 DUP2 ADD SWAP1 PUSH2 0x367F JUMP JUMPDEST PUSH2 0x11FB JUMP JUMPDEST PUSH1 0x40 MLOAD PUSH2 0x46E SWAP2 SWAP1 PUSH2 0x4303 JUMP JUMPDEST PUSH1 0x40 MLOAD DUP1 SWAP2 SUB SWAP1 RETURN JUMPDEST CALLVALUE DUP1 ISZERO PUSH2 0x483 JUMPI PUSH1 0x0 DUP1 REVERT JUMPDEST POP PUSH2 0x48C PUSH2 0x1230 JUMP JUMPDEST PUSH1 0x40 MLOAD PUSH2 0x499 SWAP2 SWAP1 PUSH2 0x42E8 JUMP JUMPDEST PUSH1 0x40 MLOAD DUP1 SWAP2 SUB SWAP1 RETURN JUMPDEST CALLVALUE DUP1 ISZERO PUSH2 0x4AE JUMPI PUSH1 0x0 DUP1 REVERT JUMPDEST POP PUSH2 0x4C9 PUSH1 0x4 DUP1 CALLDATASIZE SUB PUSH2 0x4C4 SWAP2 SWAP1 DUP2 ADD SWAP1 PUSH2 0x3779 JUMP JUMPDEST PUSH2 0x123C JUMP JUMPDEST PUSH1 0x40 MLOAD PUSH2 0x4D6 SWAP2 SWAP1 PUSH2 0x42E8 JUMP JUMPDEST PUSH1 0x40 MLOAD DUP1 SWAP2 SUB SWAP1 RETURN JUMPDEST CALLVALUE DUP1 ISZERO PUSH2 0x4EB JUMPI PUSH1 0x0 DUP1 REVERT JUMPDEST POP PUSH2 0x4F4 PUSH2 0x1322 JUMP JUMPDEST PUSH1 0x40 MLOAD PUSH2 0x501 SWAP2 SWAP1 PUSH2 0x421C JUMP JUMPDEST PUSH1 0x40 MLOAD DUP1 SWAP2 SUB SWAP1 RETURN JUMPDEST CALLVALUE DUP1 ISZERO PUSH2 0x516 JUMPI PUSH1 0x0 DUP1 REVERT JUMPDEST POP PUSH2 0x51F PUSH2 0x1510 JUMP JUMPDEST PUSH1 0x40 MLOAD PUSH2 0x52C SWAP2 SWAP1 PUSH2 0x42E8 JUMP JUMPDEST PUSH1 0x40 MLOAD DUP1 SWAP2 SUB SWAP1 RETURN JUMPDEST CALLVALUE DUP1 ISZERO PUSH2 0x541 JUMPI PUSH1 0x0 DUP1 REVERT JUMPDEST POP PUSH2 0x54A PUSH2 0x1527 JUMP JUMPDEST PUSH1 0x40 MLOAD PUSH2 0x557 SWAP2 SWAP1 PUSH2 0x45DE JUMP JUMPDEST PUSH1 0x40 MLOAD DUP1 SWAP2 SUB SWAP1 RETURN JUMPDEST CALLVALUE DUP1 ISZERO PUSH2 0x56C JUMPI PUSH1 0x0 DUP1 REVERT JUMPDEST POP PUSH2 0x575 PUSH2 0x152D JUMP JUMPDEST PUSH1 0x40 MLOAD PUSH2 0x582 SWAP2 SWAP1 PUSH2 0x4237 JUMP JUMPDEST PUSH1 0x40 MLOAD DUP1 SWAP2 SUB SWAP1 RETURN JUMPDEST CALLVALUE DUP1 ISZERO PUSH2 0x597 JUMPI PUSH1 0x0 DUP1 REVERT JUMPDEST POP PUSH2 0x5A0 PUSH2 0x1553 JUMP JUMPDEST PUSH1 0x40 MLOAD PUSH2 0x5AD SWAP2 SWAP1 PUSH2 0x4363 JUMP JUMPDEST PUSH1 0x40 MLOAD DUP1 SWAP2 SUB SWAP1 RETURN JUMPDEST CALLVALUE DUP1 ISZERO PUSH2 0x5C2 JUMPI PUSH1 0x0 DUP1 REVERT JUMPDEST POP PUSH2 0x5DD PUSH1 0x4 DUP1 CALLDATASIZE SUB PUSH2 0x5D8 SWAP2 SWAP1 DUP2 ADD SWAP1 PUSH2 0x35ED JUMP JUMPDEST PUSH2 0x1579 JUMP JUMPDEST STOP JUMPDEST CALLVALUE DUP1 ISZERO PUSH2 0x5EB JUMPI PUSH1 0x0 DUP1 REVERT JUMPDEST POP PUSH2 0x5F4 PUSH2 0x19A4 JUMP JUMPDEST PUSH1 0x40 MLOAD PUSH2 0x601 SWAP2 SWAP1 PUSH2 0x45DE JUMP JUMPDEST PUSH1 0x40 MLOAD DUP1 SWAP2 SUB SWAP1 RETURN JUMPDEST CALLVALUE DUP1 ISZERO PUSH2 0x616 JUMPI PUSH1 0x0 DUP1 REVERT JUMPDEST POP PUSH2 0x631 PUSH1 0x4 DUP1 CALLDATASIZE SUB PUSH2 0x62C SWAP2 SWAP1 DUP2 ADD SWAP1 PUSH2 0x35ED JUMP JUMPDEST PUSH2 0x19AA JUMP JUMPDEST STOP JUMPDEST CALLVALUE DUP1 ISZERO PUSH2 0x63F JUMPI PUSH1 0x0 DUP1 REVERT JUMPDEST POP PUSH2 0x648 PUSH2 0x1E08 JUMP JUMPDEST PUSH1 0x40 MLOAD PUSH2 0x655 SWAP2 SWAP1 PUSH2 0x45DE JUMP JUMPDEST PUSH1 0x40 MLOAD DUP1 SWAP2 SUB SWAP1 RETURN JUMPDEST CALLVALUE DUP1 ISZERO PUSH2 0x66A JUMPI PUSH1 0x0 DUP1 REVERT JUMPDEST POP PUSH2 0x673 PUSH2 0x1E12 JUMP JUMPDEST PUSH1 0x40 MLOAD PUSH2 0x680 SWAP2 SWAP1 PUSH2 0x428D JUMP JUMPDEST PUSH1 0x40 MLOAD DUP1 SWAP2 SUB SWAP1 RETURN JUMPDEST CALLVALUE DUP1 ISZERO PUSH2 0x695 JUMPI PUSH1 0x0 DUP1 REVERT JUMPDEST POP PUSH2 0x6B0 PUSH1 0x4 DUP1 CALLDATASIZE SUB PUSH2 0x6AB SWAP2 SWAP1 DUP2 ADD SWAP1 PUSH2 0x33C9 JUMP JUMPDEST PUSH2 0x1E6A JUMP JUMPDEST STOP JUMPDEST CALLVALUE DUP1 ISZERO PUSH2 0x6BE JUMPI PUSH1 0x0 DUP1 REVERT JUMPDEST POP PUSH2 0x6C7 PUSH2 0x2121 JUMP JUMPDEST PUSH1 0x40 MLOAD PUSH2 0x6D4 SWAP2 SWAP1 PUSH2 0x4303 JUMP JUMPDEST PUSH1 0x40 MLOAD DUP1 SWAP2 SUB SWAP1 RETURN JUMPDEST CALLVALUE DUP1 ISZERO PUSH2 0x6E9 JUMPI PUSH1 0x0 DUP1 REVERT JUMPDEST POP PUSH2 0x6F2 PUSH2 0x212B JUMP JUMPDEST STOP JUMPDEST CALLVALUE DUP1 ISZERO PUSH2 0x700 JUMPI PUSH1 0x0 DUP1 REVERT JUMPDEST POP PUSH2 0x709 PUSH2 0x22D4 JUMP JUMPDEST PUSH1 0x40 MLOAD PUSH2 0x716 SWAP2 SWAP1 PUSH2 0x42E8 JUMP JUMPDEST PUSH1 0x40 MLOAD DUP1 SWAP2 SUB SWAP1 RETURN JUMPDEST CALLVALUE DUP1 ISZERO PUSH2 0x72B JUMPI PUSH1 0x0 DUP1 REVERT JUMPDEST POP PUSH2 0x746 PUSH1 0x4 DUP1 CALLDATASIZE SUB PUSH2 0x741 SWAP2 SWAP1 DUP2 ADD SWAP1 PUSH2 0x34FA JUMP JUMPDEST PUSH2 0x22F9 JUMP JUMPDEST STOP JUMPDEST CALLVALUE DUP1 ISZERO PUSH2 0x754 JUMPI PUSH1 0x0 DUP1 REVERT JUMPDEST POP PUSH2 0x75D PUSH2 0x2710 JUMP JUMPDEST PUSH1 0x40 MLOAD PUSH2 0x76A SWAP2 SWAP1 PUSH2 0x45F9 JUMP JUMPDEST PUSH1 0x40 MLOAD DUP1 SWAP2 SUB SWAP1 RETURN JUMPDEST CALLVALUE DUP1 ISZERO PUSH2 0x77F JUMPI PUSH1 0x0 DUP1 REVERT JUMPDEST POP PUSH2 0x788 PUSH2 0x2727 JUMP JUMPDEST PUSH1 0x40 MLOAD PUSH2 0x795 SWAP2 SWAP1 PUSH2 0x428D JUMP JUMPDEST PUSH1 0x40 MLOAD DUP1 SWAP2 SUB SWAP1 RETURN JUMPDEST CALLVALUE DUP1 ISZERO PUSH2 0x7AA JUMPI PUSH1 0x0 DUP1 REVERT JUMPDEST POP PUSH2 0x7B3 PUSH2 0x277F JUMP JUMPDEST PUSH1 0x40 MLOAD PUSH2 0x7C0 SWAP2 SWAP1 PUSH2 0x45DE JUMP JUMPDEST PUSH1 0x40 MLOAD DUP1 SWAP2 SUB SWAP1 RETURN JUMPDEST CALLVALUE DUP1 ISZERO PUSH2 0x7D5 JUMPI PUSH1 0x0 DUP1 REVERT JUMPDEST POP PUSH2 0x7DE PUSH2 0x2789 JUMP JUMPDEST PUSH1 0x40 MLOAD PUSH2 0x7EB SWAP2 SWAP1 PUSH2 0x45F9 JUMP JUMPDEST PUSH1 0x40 MLOAD DUP1 SWAP2 SUB SWAP1 RETURN JUMPDEST CALLVALUE DUP1 ISZERO PUSH2 0x800 JUMPI PUSH1 0x0 DUP1 REVERT JUMPDEST POP PUSH2 0x809 PUSH2 0x27A0 JUMP JUMPDEST PUSH1 0x40 MLOAD PUSH2 0x816 SWAP2 SWAP1 PUSH2 0x421C JUMP JUMPDEST PUSH1 0x40 MLOAD DUP1 SWAP2 SUB SWAP1 RETURN JUMPDEST CALLVALUE DUP1 ISZERO PUSH2 0x82B JUMPI PUSH1 0x0 DUP1 REVERT JUMPDEST POP PUSH2 0x834 PUSH2 0x27CA JUMP JUMPDEST PUSH1 0x40 MLOAD PUSH2 0x841 SWAP2 SWAP1 PUSH2 0x4303 JUMP JUMPDEST PUSH1 0x40 MLOAD DUP1 SWAP2 SUB SWAP1 RETURN JUMPDEST CALLVALUE DUP1 ISZERO PUSH2 0x856 JUMPI PUSH1 0x0 DUP1 REVERT JUMPDEST POP PUSH2 0x85F PUSH2 0x27D4 JUMP JUMPDEST PUSH1 0x40 MLOAD PUSH2 0x86C SWAP2 SWAP1 PUSH2 0x45DE JUMP JUMPDEST PUSH1 0x40 MLOAD DUP1 SWAP2 SUB SWAP1 RETURN JUMPDEST CALLVALUE DUP1 ISZERO PUSH2 0x881 JUMPI PUSH1 0x0 DUP1 REVERT JUMPDEST POP PUSH2 0x89C PUSH1 0x4 DUP1 CALLDATASIZE SUB PUSH2 0x897 SWAP2 SWAP1 DUP2 ADD SWAP1 PUSH2 0x35ED JUMP JUMPDEST PUSH2 0x27DE JUMP JUMPDEST STOP JUMPDEST CALLVALUE DUP1 ISZERO PUSH2 0x8AA JUMPI PUSH1 0x0 DUP1 REVERT JUMPDEST POP PUSH2 0x8B3 PUSH2 0x2A70 JUMP JUMPDEST PUSH1 0x40 MLOAD PUSH2 0x8C0 SWAP2 SWAP1 PUSH2 0x428D JUMP JUMPDEST PUSH1 0x40 MLOAD DUP1 SWAP2 SUB SWAP1 RETURN JUMPDEST CALLVALUE DUP1 ISZERO PUSH2 0x8D5 JUMPI PUSH1 0x0 DUP1 REVERT JUMPDEST POP PUSH2 0x8DE PUSH2 0x2AC8 JUMP JUMPDEST PUSH1 0x40 MLOAD PUSH2 0x8EB SWAP2 SWAP1 PUSH2 0x45DE JUMP JUMPDEST PUSH1 0x40 MLOAD DUP1 SWAP2 SUB SWAP1 RETURN JUMPDEST CALLVALUE DUP1 ISZERO PUSH2 0x900 JUMPI PUSH1 0x0 DUP1 REVERT JUMPDEST POP PUSH2 0x91B PUSH1 0x4 DUP1 CALLDATASIZE SUB PUSH2 0x916 SWAP2 SWAP1 DUP2 ADD SWAP1 PUSH2 0x36C0 JUMP JUMPDEST PUSH2 0x2CDD JUMP JUMPDEST PUSH1 0x40 MLOAD PUSH2 0x928 SWAP2 SWAP1 PUSH2 0x42E8 JUMP JUMPDEST PUSH1 0x40 MLOAD DUP1 SWAP2 SUB SWAP1 RETURN JUMPDEST CALLVALUE DUP1 ISZERO PUSH2 0x93D JUMPI PUSH1 0x0 DUP1 REVERT JUMPDEST POP PUSH2 0x946 PUSH2 0x3047 JUMP JUMPDEST PUSH1 0x40 MLOAD PUSH2 0x953 SWAP2 SWAP1 PUSH2 0x428D JUMP JUMPDEST PUSH1 0x40 MLOAD DUP1 SWAP2 SUB SWAP1 RETURN JUMPDEST CALLVALUE DUP1 ISZERO PUSH2 0x968 JUMPI PUSH1 0x0 DUP1 REVERT JUMPDEST POP PUSH2 0x971 PUSH2 0x309F JUMP JUMPDEST PUSH1 0x40 MLOAD PUSH2 0x97E SWAP2 SWAP1 PUSH2 0x45DE JUMP JUMPDEST PUSH1 0x40 MLOAD DUP1 SWAP2 SUB SWAP1 RETURN JUMPDEST CALLVALUE DUP1 ISZERO PUSH2 0x993 JUMPI PUSH1 0x0 DUP1 REVERT JUMPDEST POP PUSH2 0x99C PUSH2 0x30A5 JUMP JUMPDEST PUSH1 0x40 MLOAD PUSH2 0x9A9 SWAP2 SWAP1 PUSH2 0x42E8 JUMP JUMPDEST PUSH1 0x40 MLOAD DUP1 SWAP2 SUB SWAP1 RETURN JUMPDEST PUSH1 0xD PUSH1 0x0 SWAP1 SLOAD SWAP1 PUSH2 0x100 EXP SWAP1 DIV PUSH1 0xFF AND PUSH2 0xA01 JUMPI PUSH1 0x40 MLOAD PUSH32 0x8C379A000000000000000000000000000000000000000000000000000000000 DUP2 MSTORE PUSH1 0x4 ADD PUSH2 0x9F8 SWAP1 PUSH2 0x449E JUMP JUMPDEST PUSH1 0x40 MLOAD DUP1 SWAP2 SUB SWAP1 REVERT JUMPDEST PUSH2 0xA09 PUSH2 0x1230 JUMP JUMPDEST PUSH2 0xA48 JUMPI PUSH1 0x40 MLOAD PUSH32 0x8C379A000000000000000000000000000000000000000000000000000000000 DUP2 MSTORE PUSH1 0x4 ADD PUSH2 0xA3F SWAP1 PUSH2 0x457E JUMP JUMPDEST PUSH1 0x40 MLOAD DUP1 SWAP2 SUB SWAP1 REVERT JUMPDEST PUSH1 0x0 DUP1 SWAP1 SLOAD SWAP1 PUSH2 0x100 EXP SWAP1 DIV PUSH20 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF AND PUSH20 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF AND CALLER PUSH20 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF AND EQ DUP1 PUSH2 0xAF0 JUMPI POP PUSH1 0x1 PUSH1 0x0 SWAP1 SLOAD SWAP1 PUSH2 0x100 EXP SWAP1 DIV PUSH20 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF AND PUSH20 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF AND CALLER PUSH20 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF AND EQ JUMPDEST PUSH2 0xB2F JUMPI PUSH1 0x40 MLOAD PUSH32 0x8C379A000000000000000000000000000000000000000000000000000000000 DUP2 MSTORE PUSH1 0x4 ADD PUSH2 0xB26 SWAP1 PUSH2 0x44FE JUMP JUMPDEST PUSH1 0x40 MLOAD DUP1 SWAP2 SUB SWAP1 REVERT JUMPDEST PUSH1 0x2 PUSH1 0x0 SWAP1 SLOAD SWAP1 PUSH2 0x100 EXP SWAP1 DIV PUSH20 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF AND PUSH20 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF AND PUSH4 0x51428BC0 PUSH1 0xE DUP5 DUP5 PUSH1 0x40 MLOAD DUP5 PUSH4 0xFFFFFFFF AND PUSH1 0xE0 SHL DUP2 MSTORE PUSH1 0x4 ADD PUSH2 0xB8F SWAP4 SWAP3 SWAP2 SWAP1 PUSH2 0x42AF JUMP JUMPDEST PUSH1 0x20 PUSH1 0x40 MLOAD DUP1 DUP4 SUB DUP2 DUP7 DUP1 EXTCODESIZE ISZERO DUP1 ISZERO PUSH2 0xBA7 JUMPI PUSH1 0x0 DUP1 REVERT JUMPDEST POP GAS STATICCALL ISZERO DUP1 ISZERO PUSH2 0xBBB JUMPI RETURNDATASIZE PUSH1 0x0 DUP1 RETURNDATACOPY RETURNDATASIZE PUSH1 0x0 REVERT JUMPDEST POP POP POP POP PUSH1 0x40 MLOAD RETURNDATASIZE PUSH1 0x1F NOT PUSH1 0x1F DUP3 ADD AND DUP3 ADD DUP1 PUSH1 0x40 MSTORE POP PUSH2 0xBDF SWAP2 SWAP1 DUP2 ADD SWAP1 PUSH2 0x381A JUMP JUMPDEST PUSH2 0xC1E JUMPI PUSH1 0x40 MLOAD PUSH32 0x8C379A000000000000000000000000000000000000000000000000000000000 DUP2 MSTORE PUSH1 0x4 ADD PUSH2 0xC15 SWAP1 PUSH2 0x443E JUMP JUMPDEST PUSH1 0x40 MLOAD DUP1 SWAP2 SUB SWAP1 REVERT JUMPDEST PUSH1 0xA SLOAD PUSH1 0xC DUP2 SWAP1 SSTORE POP PUSH1 0x4 SLOAD PUSH1 0x7 PUSH1 0x0 DUP3 DUP3 SLOAD ADD SWAP3 POP POP DUP2 SWAP1 SSTORE POP PUSH1 0x4 SLOAD PUSH1 0x8 PUSH1 0x0 DUP3 DUP3 SLOAD SUB SWAP3 POP POP DUP2 SWAP1 SSTORE POP PUSH1 0x0 PUSH1 0xD PUSH1 0x0 PUSH2 0x100 EXP DUP2 SLOAD DUP2 PUSH1 0xFF MUL NOT AND SWAP1 DUP4 ISZERO ISZERO MUL OR SWAP1 SSTORE POP DUP2 DUP2 PUSH1 0x11 SWAP2 SWAP1 PUSH2 0xC77 SWAP3 SWAP2 SWAP1 PUSH2 0x31EB JUMP JUMPDEST POP POP POP JUMP JUMPDEST PUSH1 0x0 DUP1 SWAP1 SLOAD SWAP1 PUSH2 0x100 EXP SWAP1 DIV PUSH20 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF AND DUP2 JUMP JUMPDEST PUSH1 0x0 PUSH1 0x14 SLOAD SWAP1 POP SWAP1 JUMP JUMPDEST PUSH2 0xCB3 PUSH2 0x1230 JUMP JUMPDEST ISZERO PUSH2 0xCF3 JUMPI PUSH1 0x40 MLOAD PUSH32 0x8C379A000000000000000000000000000000000000000000000000000000000 DUP2 MSTORE PUSH1 0x4 ADD PUSH2 0xCEA SWAP1 PUSH2 0x44DE JUMP JUMPDEST PUSH1 0x40 MLOAD DUP1 SWAP2 SUB SWAP1 REVERT JUMPDEST PUSH1 0x1 PUSH1 0x0 SWAP1 SLOAD SWAP1 PUSH2 0x100 EXP SWAP1 DIV PUSH20 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF AND PUSH20 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF AND CALLER PUSH20 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF AND EQ PUSH2 0xD83 JUMPI PUSH1 0x40 MLOAD PUSH32 0x8C379A000000000000000000000000000000000000000000000000000000000 DUP2 MSTORE PUSH1 0x4 ADD PUSH2 0xD7A SWAP1 PUSH2 0x451E JUMP JUMPDEST PUSH1 0x40 MLOAD DUP1 SWAP2 SUB SWAP1 REVERT JUMPDEST CALLVALUE PUSH1 0x8 PUSH1 0x0 DUP3 DUP3 SLOAD ADD SWAP3 POP POP DUP2 SWAP1 SSTORE POP PUSH1 0x4 SLOAD PUSH1 0x8 SLOAD LT PUSH2 0xE02 JUMPI PUSH1 0x4 SLOAD PUSH1 0x8 PUSH1 0x0 DUP3 DUP3 SLOAD SUB SWAP3 POP POP DUP2 SWAP1 SSTORE POP PUSH1 0x4 SLOAD PUSH1 0x7 PUSH1 0x0 DUP3 DUP3 SLOAD ADD SWAP3 POP POP DUP2 SWAP1 SSTORE POP PUSH1 0x5 SLOAD NUMBER ADD PUSH1 0xC DUP2 SWAP1 SSTORE POP NUMBER PUSH1 0x9 DUP2 SWAP1 SSTORE POP PUSH1 0xC SLOAD PUSH1 0xA DUP2 SWAP1 SSTORE POP PUSH1 0xC SLOAD PUSH1 0x15 DUP2 SWAP1 SSTORE POP PUSH1 0x0 PUSH1 0xD PUSH1 0x0 PUSH2 0x100 EXP DUP2 SLOAD DUP2 PUSH1 0xFF MUL NOT AND SWAP1 DUP4 ISZERO ISZERO MUL OR SWAP1 SSTORE POP JUMPDEST JUMP JUMPDEST PUSH1 0x0 PUSH1 0x1C SLOAD SWAP1 POP SWAP1 JUMP JUMPDEST PUSH1 0xD PUSH1 0x0 SWAP1 SLOAD SWAP1 PUSH2 0x100 EXP SWAP1 DIV PUSH1 0xFF AND ISZERO PUSH2 0xE5E JUMPI PUSH1 0x40 MLOAD PUSH32 0x8C379A000000000000000000000000000000000000000000000000000000000 DUP2 MSTORE PUSH1 0x4 ADD PUSH2 0xE55 SWAP1 PUSH2 0x44BE JUMP JUMPDEST PUSH1 0x40 MLOAD DUP1 SWAP2 SUB SWAP1 REVERT JUMPDEST PUSH2 0xE66 PUSH2 0x1230 JUMP JUMPDEST PUSH2 0xEA5 JUMPI PUSH1 0x40 MLOAD PUSH32 0x8C379A000000000000000000000000000000000000000000000000000000000 DUP2 MSTORE PUSH1 0x4 ADD PUSH2 0xE9C SWAP1 PUSH2 0x457E JUMP JUMPDEST PUSH1 0x40 MLOAD DUP1 SWAP2 SUB SWAP1 REVERT JUMPDEST PUSH1 0x1 PUSH1 0x0 SWAP1 SLOAD SWAP1 PUSH2 0x100 EXP SWAP1 DIV PUSH20 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF AND PUSH20 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF AND CALLER PUSH20 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF AND EQ PUSH2 0xF35 JUMPI PUSH1 0x40 MLOAD PUSH32 0x8C379A000000000000000000000000000000000000000000000000000000000 DUP2 MSTORE PUSH1 0x4 ADD PUSH2 0xF2C SWAP1 PUSH2 0x451E JUMP JUMPDEST PUSH1 0x40 MLOAD DUP1 SWAP2 SUB SWAP1 REVERT JUMPDEST PUSH2 0xFC5 DUP9 DUP9 DUP1 DUP1 PUSH1 0x20 MUL PUSH1 0x20 ADD PUSH1 0x40 MLOAD SWAP1 DUP2 ADD PUSH1 0x40 MSTORE DUP1 SWAP4 SWAP3 SWAP2 SWAP1 DUP2 DUP2 MSTORE PUSH1 0x20 ADD DUP4 DUP4 PUSH1 0x20 MUL DUP1 DUP3 DUP5 CALLDATACOPY PUSH1 0x0 DUP2 DUP5 ADD MSTORE PUSH1 0x1F NOT PUSH1 0x1F DUP3 ADD AND SWAP1 POP DUP1 DUP4 ADD SWAP3 POP POP POP POP POP POP POP DUP8 DUP8 DUP1 DUP1 PUSH1 0x20 MUL PUSH1 0x20 ADD PUSH1 0x40 MLOAD SWAP1 DUP2 ADD PUSH1 0x40 MSTORE DUP1 SWAP4 SWAP3 SWAP2 SWAP1 DUP2 DUP2 MSTORE PUSH1 0x20 ADD DUP4 DUP4 PUSH1 0x20 MUL DUP1 DUP3 DUP5 CALLDATACOPY PUSH1 0x0 DUP2 DUP5 ADD MSTORE PUSH1 0x1F NOT PUSH1 0x1F DUP3 ADD AND SWAP1 POP DUP1 DUP4 ADD SWAP3 POP POP POP POP POP POP POP DUP7 DUP7 DUP7 DUP7 PUSH2 0x2CDD JUMP JUMPDEST PUSH2 0x1004 JUMPI PUSH1 0x40 MLOAD PUSH32 0x8C379A000000000000000000000000000000000000000000000000000000000 DUP2 MSTORE PUSH1 0x4 ADD PUSH2 0xFFB SWAP1 PUSH2 0x43BE JUMP JUMPDEST PUSH1 0x40 MLOAD DUP1 SWAP2 SUB SWAP1 REVERT JUMPDEST PUSH1 0x0 DUP1 SWAP1 POP PUSH1 0x0 PUSH2 0x1055 DUP11 DUP11 DUP1 DUP1 PUSH1 0x20 MUL PUSH1 0x20 ADD PUSH1 0x40 MLOAD SWAP1 DUP2 ADD PUSH1 0x40 MSTORE DUP1 SWAP4 SWAP3 SWAP2 SWAP1 DUP2 DUP2 MSTORE PUSH1 0x20 ADD DUP4 DUP4 PUSH1 0x20 MUL DUP1 DUP3 DUP5 CALLDATACOPY PUSH1 0x0 DUP2 DUP5 ADD MSTORE PUSH1 0x1F NOT PUSH1 0x1F DUP3 ADD AND SWAP1 POP DUP1 DUP4 ADD SWAP3 POP POP POP POP POP POP POP PUSH2 0x11FB JUMP JUMPDEST SWAP1 POP PUSH1 0x0 DUP7 DUP10 DUP10 SWAP1 POP SUB SWAP1 POP JUMPDEST DUP9 DUP9 SWAP1 POP DUP2 LT ISZERO PUSH2 0x1097 JUMPI DUP9 DUP9 DUP3 DUP2 DUP2 LT PUSH2 0x1079 JUMPI INVALID JUMPDEST SWAP1 POP PUSH1 0x20 MUL ADD CALLDATALOAD DUP3 EQ ISZERO PUSH2 0x108C JUMPI PUSH1 0x1 SWAP3 POP JUMPDEST PUSH1 0x1 DUP2 ADD SWAP1 POP PUSH2 0x1062 JUMP JUMPDEST POP DUP2 PUSH2 0x10D8 JUMPI PUSH1 0x40 MLOAD PUSH32 0x8C379A000000000000000000000000000000000000000000000000000000000 DUP2 MSTORE PUSH1 0x4 ADD PUSH2 0x10CF SWAP1 PUSH2 0x445E JUMP JUMPDEST PUSH1 0x40 MLOAD DUP1 SWAP2 SUB SWAP1 REVERT JUMPDEST PUSH1 0x1 PUSH1 0xD PUSH1 0x0 PUSH2 0x100 EXP DUP2 SLOAD DUP2 PUSH1 0xFF MUL NOT AND SWAP1 DUP4 ISZERO ISZERO MUL OR SWAP1 SSTORE POP DUP8 DUP8 PUSH1 0xF SWAP2 SWAP1 PUSH2 0x1104 SWAP3 SWAP2 SWAP1 PUSH2 0x31EB JUMP JUMPDEST POP DUP6 PUSH1 0x10 DUP2 SWAP1 SSTORE POP DUP5 PUSH1 0x12 PUSH1 0x0 PUSH2 0x100 EXP DUP2 SLOAD DUP2 PUSH1 0xFF MUL NOT AND SWAP1 DUP4 PUSH1 0xFF AND MUL OR SWAP1 SSTORE POP DUP4 PUSH1 0x13 DUP2 SWAP1 SSTORE POP DUP3 PUSH1 0x14 DUP2 SWAP1 SSTORE POP PUSH1 0x3 SLOAD NUMBER ADD PUSH1 0xC SLOAD GT ISZERO PUSH2 0x114F JUMPI PUSH1 0x3 SLOAD NUMBER ADD PUSH1 0xC DUP2 SWAP1 SSTORE POP JUMPDEST PUSH1 0x4 SLOAD PUSH1 0x7 PUSH1 0x0 DUP3 DUP3 SLOAD SUB SWAP3 POP POP DUP2 SWAP1 SSTORE POP PUSH1 0x4 SLOAD PUSH1 0x8 PUSH1 0x0 DUP3 DUP3 SLOAD ADD SWAP3 POP POP DUP2 SWAP1 SSTORE POP DUP10 DUP10 PUSH1 0xE SWAP2 SWAP1 PUSH2 0x1184 SWAP3 SWAP2 SWAP1 PUSH2 0x31EB JUMP JUMPDEST POP DUP6 DUP9 DUP9 SWAP1 POP SUB PUSH1 0xB DUP2 SWAP1 SSTORE POP POP POP POP POP POP POP POP POP POP POP JUMP JUMPDEST PUSH1 0x4 SLOAD DUP2 JUMP JUMPDEST PUSH1 0x60 PUSH1 0x1A DUP1 SLOAD DUP1 PUSH1 0x20 MUL PUSH1 0x20 ADD PUSH1 0x40 MLOAD SWAP1 DUP2 ADD PUSH1 0x40 MSTORE DUP1 SWAP3 SWAP2 SWAP1 DUP2 DUP2 MSTORE PUSH1 0x20 ADD DUP3 DUP1 SLOAD DUP1 ISZERO PUSH2 0x11F1 JUMPI PUSH1 0x20 MUL DUP3 ADD SWAP2 SWAP1 PUSH1 0x0 MSTORE PUSH1 0x20 PUSH1 0x0 KECCAK256 SWAP1 JUMPDEST DUP2 SLOAD DUP2 MSTORE PUSH1 0x20 ADD SWAP1 PUSH1 0x1 ADD SWAP1 DUP1 DUP4 GT PUSH2 0x11DD JUMPI JUMPDEST POP POP POP POP POP SWAP1 POP SWAP1 JUMP JUMPDEST PUSH1 0x0 DUP1 DUP3 PUSH1 0x40 MLOAD PUSH1 0x20 ADD PUSH2 0x120F SWAP2 SWAP1 PUSH2 0x41A6 JUMP JUMPDEST PUSH1 0x40 MLOAD PUSH1 0x20 DUP2 DUP4 SUB SUB DUP2 MSTORE SWAP1 PUSH1 0x40 MSTORE DUP1 MLOAD SWAP1 PUSH1 0x20 ADD KECCAK256 SWAP1 POP DUP1 SWAP2 POP POP SWAP2 SWAP1 POP JUMP JUMPDEST PUSH1 0x0 NUMBER PUSH1 0xC SLOAD GT SWAP1 POP SWAP1 JUMP JUMPDEST PUSH1 0x0 DUP1 DUP8 DUP8 ADDRESS PUSH1 0x40 MLOAD PUSH1 0x20 ADD PUSH2 0x1254 SWAP4 SWAP3 SWAP2 SWAP1 PUSH2 0x41BD JUMP JUMPDEST PUSH1 0x40 MLOAD PUSH1 0x20 DUP2 DUP4 SUB SUB DUP2 MSTORE SWAP1 PUSH1 0x40 MSTORE DUP1 MLOAD SWAP1 PUSH1 0x20 ADD KECCAK256 SWAP1 POP PUSH1 0x0 DUP2 PUSH1 0x40 MLOAD PUSH1 0x20 ADD PUSH2 0x127F SWAP2 SWAP1 PUSH2 0x41F6 JUMP JUMPDEST PUSH1 0x40 MLOAD PUSH1 0x20 DUP2 DUP4 SUB SUB DUP2 MSTORE SWAP1 PUSH1 0x40 MSTORE DUP1 MLOAD SWAP1 PUSH1 0x20 ADD KECCAK256 SWAP1 POP DUP4 PUSH20 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF AND PUSH1 0x1 DUP3 DUP10 DUP10 DUP10 PUSH1 0x40 MLOAD PUSH1 0x0 DUP2 MSTORE PUSH1 0x20 ADD PUSH1 0x40 MSTORE PUSH1 0x40 MLOAD PUSH2 0x12D1 SWAP5 SWAP4 SWAP3 SWAP2 SWAP1 PUSH2 0x431E JUMP JUMPDEST PUSH1 0x20 PUSH1 0x40 MLOAD PUSH1 0x20 DUP2 SUB SWAP1 DUP1 DUP5 SUB SWAP1 DUP6 GAS STATICCALL ISZERO DUP1 ISZERO PUSH2 0x12F3 JUMPI RETURNDATASIZE PUSH1 0x0 DUP1 RETURNDATACOPY RETURNDATASIZE PUSH1 0x0 REVERT JUMPDEST POP POP POP PUSH1 0x20 PUSH1 0x40 MLOAD SUB MLOAD PUSH20 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF AND EQ SWAP3 POP POP POP SWAP7 SWAP6 POP POP POP POP POP POP JUMP JUMPDEST PUSH1 0x0 DUP1 PUSH1 0x0 SWAP1 SLOAD SWAP1 PUSH2 0x100 EXP SWAP1 DIV PUSH20 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF AND PUSH20 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF AND CALLER PUSH20 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF AND EQ DUP1 PUSH2 0x13CC JUMPI POP PUSH1 0x1 PUSH1 0x0 SWAP1 SLOAD SWAP1 PUSH2 0x100 EXP SWAP1 DIV PUSH20 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF AND PUSH20 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF AND CALLER PUSH20 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF AND EQ JUMPDEST PUSH2 0x140B JUMPI PUSH1 0x40 MLOAD PUSH32 0x8C379A000000000000000000000000000000000000000000000000000000000 DUP2 MSTORE PUSH1 0x4 ADD PUSH2 0x1402 SWAP1 PUSH2 0x44FE JUMP JUMPDEST PUSH1 0x40 MLOAD DUP1 SWAP2 SUB SWAP1 REVERT JUMPDEST PUSH1 0x1 PUSH1 0x0 SWAP1 SLOAD SWAP1 PUSH2 0x100 EXP SWAP1 DIV PUSH20 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF AND PUSH20 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF AND CALLER PUSH20 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF AND EQ ISZERO PUSH2 0x148A JUMPI PUSH1 0x0 DUP1 SWAP1 SLOAD SWAP1 PUSH2 0x100 EXP SWAP1 DIV PUSH20 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF AND SWAP1 POP PUSH2 0x150D JUMP JUMPDEST PUSH1 0x0 DUP1 SWAP1 SLOAD SWAP1 PUSH2 0x100 EXP SWAP1 DIV PUSH20 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF AND PUSH20 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF AND CALLER PUSH20 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF AND EQ ISZERO PUSH2 0x1509 JUMPI PUSH1 0x1 PUSH1 0x0 SWAP1 SLOAD SWAP1 PUSH2 0x100 EXP SWAP1 DIV PUSH20 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF AND SWAP1 POP PUSH2 0x150D JUMP JUMPDEST ADDRESS SWAP1 POP JUMPDEST SWAP1 JUMP JUMPDEST PUSH1 0x0 PUSH1 0xD PUSH1 0x0 SWAP1 SLOAD SWAP1 PUSH2 0x100 EXP SWAP1 DIV PUSH1 0xFF AND SWAP1 POP SWAP1 JUMP JUMPDEST PUSH1 0x3 SLOAD DUP2 JUMP JUMPDEST PUSH1 0x1 PUSH1 0x0 SWAP1 SLOAD SWAP1 PUSH2 0x100 EXP SWAP1 DIV PUSH20 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF AND DUP2 JUMP JUMPDEST PUSH1 0x2 PUSH1 0x0 SWAP1 SLOAD SWAP1 PUSH2 0x100 EXP SWAP1 DIV PUSH20 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF AND DUP2 JUMP JUMPDEST PUSH1 0xD PUSH1 0x0 SWAP1 SLOAD SWAP1 PUSH2 0x100 EXP SWAP1 DIV PUSH1 0xFF AND PUSH2 0x15C8 JUMPI PUSH1 0x40 MLOAD PUSH32 0x8C379A000000000000000000000000000000000000000000000000000000000 DUP2 MSTORE PUSH1 0x4 ADD PUSH2 0x15BF SWAP1 PUSH2 0x449E JUMP JUMPDEST PUSH1 0x40 MLOAD DUP1 SWAP2 SUB SWAP1 REVERT JUMPDEST PUSH2 0x15D0 PUSH2 0x1230 JUMP JUMPDEST PUSH2 0x160F JUMPI PUSH1 0x40 MLOAD PUSH32 0x8C379A000000000000000000000000000000000000000000000000000000000 DUP2 MSTORE PUSH1 0x4 ADD PUSH2 0x1606 SWAP1 PUSH2 0x457E JUMP JUMPDEST PUSH1 0x40 MLOAD DUP1 SWAP2 SUB SWAP1 REVERT JUMPDEST PUSH1 0x0 DUP1 SWAP1 SLOAD SWAP1 PUSH2 0x100 EXP SWAP1 DIV PUSH20 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF AND PUSH20 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF AND CALLER PUSH20 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF AND EQ DUP1 PUSH2 0x16B7 JUMPI POP PUSH1 0x1 PUSH1 0x0 SWAP1 SLOAD SWAP1 PUSH2 0x100 EXP SWAP1 DIV PUSH20 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF AND PUSH20 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF AND CALLER PUSH20 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF AND EQ JUMPDEST PUSH2 0x16F6 JUMPI PUSH1 0x40 MLOAD PUSH32 0x8C379A000000000000000000000000000000000000000000000000000000000 DUP2 MSTORE PUSH1 0x4 ADD PUSH2 0x16ED SWAP1 PUSH2 0x44FE JUMP JUMPDEST PUSH1 0x40 MLOAD DUP1 SWAP2 SUB SWAP1 REVERT JUMPDEST PUSH2 0x1767 DUP7 DUP7 DUP1 DUP1 PUSH1 0x20 MUL PUSH1 0x20 ADD PUSH1 0x40 MLOAD SWAP1 DUP2 ADD PUSH1 0x40 MSTORE DUP1 SWAP4 SWAP3 SWAP2 SWAP1 DUP2 DUP2 MSTORE PUSH1 0x20 ADD DUP4 DUP4 PUSH1 0x20 MUL DUP1 DUP3 DUP5 CALLDATACOPY PUSH1 0x0 DUP2 DUP5 ADD MSTORE PUSH1 0x1F NOT PUSH1 0x1F DUP3 ADD AND SWAP1 POP DUP1 DUP4 ADD SWAP3 POP POP POP POP POP POP POP DUP6 DUP6 DUP6 DUP6 PUSH1 0x1 PUSH1 0x0 SWAP1 SLOAD SWAP1 PUSH2 0x100 EXP SWAP1 DIV PUSH20 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF AND PUSH2 0x123C JUMP JUMPDEST PUSH2 0x17A6 JUMPI PUSH1 0x40 MLOAD PUSH32 0x8C379A000000000000000000000000000000000000000000000000000000000 DUP2 MSTORE PUSH1 0x4 ADD PUSH2 0x179D SWAP1 PUSH2 0x43FE JUMP JUMPDEST PUSH1 0x40 MLOAD DUP1 SWAP2 SUB SWAP1 REVERT JUMPDEST DUP4 DUP7 DUP7 SWAP1 POP SUB PUSH1 0xB SLOAD GT PUSH2 0x17C1 JUMPI DUP4 DUP7 DUP7 SWAP1 POP SUB PUSH1 0xB DUP2 SWAP1 SSTORE POP JUMPDEST PUSH2 0x1860 PUSH1 0xF DUP1 SLOAD DUP1 PUSH1 0x20 MUL PUSH1 0x20 ADD PUSH1 0x40 MLOAD SWAP1 DUP2 ADD PUSH1 0x40 MSTORE DUP1 SWAP3 SWAP2 SWAP1 DUP2 DUP2 MSTORE PUSH1 0x20 ADD DUP3 DUP1 SLOAD DUP1 ISZERO PUSH2 0x1810 JUMPI PUSH1 0x20 MUL DUP3 ADD SWAP2 SWAP1 PUSH1 0x0 MSTORE PUSH1 0x20 PUSH1 0x0 KECCAK256 SWAP1 JUMPDEST DUP2 SLOAD DUP2 MSTORE PUSH1 0x20 ADD SWAP1 PUSH1 0x1 ADD SWAP1 DUP1 DUP4 GT PUSH2 0x17FC JUMPI JUMPDEST POP POP POP POP POP PUSH1 0x10 SLOAD DUP9 DUP9 DUP1 DUP1 PUSH1 0x20 MUL PUSH1 0x20 ADD PUSH1 0x40 MLOAD SWAP1 DUP2 ADD PUSH1 0x40 MSTORE DUP1 SWAP4 SWAP3 SWAP2 SWAP1 DUP2 DUP2 MSTORE PUSH1 0x20 ADD DUP4 DUP4 PUSH1 0x20 MUL DUP1 DUP3 DUP5 CALLDATACOPY PUSH1 0x0 DUP2 DUP5 ADD MSTORE PUSH1 0x1F NOT PUSH1 0x1F DUP3 ADD AND SWAP1 POP DUP1 DUP4 ADD SWAP3 POP POP POP POP POP POP POP DUP8 PUSH2 0x30BC JUMP JUMPDEST DUP1 PUSH2 0x1907 JUMPI POP PUSH2 0x1905 DUP7 DUP7 DUP1 DUP1 PUSH1 0x20 MUL PUSH1 0x20 ADD PUSH1 0x40 MLOAD SWAP1 DUP2 ADD PUSH1 0x40 MSTORE DUP1 SWAP4 SWAP3 SWAP2 SWAP1 DUP2 DUP2 MSTORE PUSH1 0x20 ADD DUP4 DUP4 PUSH1 0x20 MUL DUP1 DUP3 DUP5 CALLDATACOPY PUSH1 0x0 DUP2 DUP5 ADD MSTORE PUSH1 0x1F NOT PUSH1 0x1F DUP3 ADD AND SWAP1 POP DUP1 DUP4 ADD SWAP3 POP POP POP POP POP POP POP DUP6 PUSH1 0xF DUP1 SLOAD DUP1 PUSH1 0x20 MUL PUSH1 0x20 ADD PUSH1 0x40 MLOAD SWAP1 DUP2 ADD PUSH1 0x40 MSTORE DUP1 SWAP3 SWAP2 SWAP1 DUP2 DUP2 MSTORE PUSH1 0x20 ADD DUP3 DUP1 SLOAD DUP1 ISZERO PUSH2 0x18F8 JUMPI PUSH1 0x20 MUL DUP3 ADD SWAP2 SWAP1 PUSH1 0x0 MSTORE PUSH1 0x20 PUSH1 0x0 KECCAK256 SWAP1 JUMPDEST DUP2 SLOAD DUP2 MSTORE PUSH1 0x20 ADD SWAP1 PUSH1 0x1 ADD SWAP1 DUP1 DUP4 GT PUSH2 0x18E4 JUMPI JUMPDEST POP POP POP POP POP PUSH1 0x10 SLOAD PUSH2 0x30BC JUMP JUMPDEST ISZERO JUMPDEST PUSH2 0x1946 JUMPI PUSH1 0x40 MLOAD PUSH32 0x8C379A000000000000000000000000000000000000000000000000000000000 DUP2 MSTORE PUSH1 0x4 ADD PUSH2 0x193D SWAP1 PUSH2 0x455E JUMP JUMPDEST PUSH1 0x40 MLOAD DUP1 SWAP2 SUB SWAP1 REVERT JUMPDEST PUSH1 0xA SLOAD PUSH1 0xC DUP2 SWAP1 SSTORE POP PUSH1 0x4 SLOAD PUSH1 0x7 PUSH1 0x0 DUP3 DUP3 SLOAD ADD SWAP3 POP POP DUP2 SWAP1 SSTORE POP PUSH1 0x4 SLOAD PUSH1 0x8 PUSH1 0x0 DUP3 DUP3 SLOAD SUB SWAP3 POP POP DUP2 SWAP1 SSTORE POP PUSH1 0x0 PUSH1 0xD PUSH1 0x0 PUSH2 0x100 EXP DUP2 SLOAD DUP2 PUSH1 0xFF MUL NOT AND SWAP1 DUP4 ISZERO ISZERO MUL OR SWAP1 SSTORE POP PUSH1 0x11 PUSH1 0x0 PUSH2 0x199C SWAP2 SWAP1 PUSH2 0x3238 JUMP JUMPDEST POP POP POP POP POP POP JUMP JUMPDEST PUSH1 0x5 SLOAD DUP2 JUMP JUMPDEST PUSH1 0x16 PUSH1 0x0 SWAP1 SLOAD SWAP1 PUSH2 0x100 EXP SWAP1 DIV PUSH1 0xFF AND PUSH2 0x19F9 JUMPI PUSH1 0x40 MLOAD PUSH32 0x8C379A000000000000000000000000000000000000000000000000000000000 DUP2 MSTORE PUSH1 0x4 ADD PUSH2 0x19F0 SWAP1 PUSH2 0x45BE JUMP JUMPDEST PUSH1 0x40 MLOAD DUP1 SWAP2 SUB SWAP1 REVERT JUMPDEST PUSH2 0x1A01 PUSH2 0x1230 JUMP JUMPDEST PUSH2 0x1A40 JUMPI PUSH1 0x40 MLOAD PUSH32 0x8C379A000000000000000000000000000000000000000000000000000000000 DUP2 MSTORE PUSH1 0x4 ADD PUSH2 0x1A37 SWAP1 PUSH2 0x457E JUMP JUMPDEST PUSH1 0x40 MLOAD DUP1 SWAP2 SUB SWAP1 REVERT JUMPDEST PUSH1 0x0 DUP1 SWAP1 SLOAD SWAP1 PUSH2 0x100 EXP SWAP1 DIV PUSH20 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF AND PUSH20 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF AND CALLER PUSH20 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF AND EQ DUP1 PUSH2 0x1AE8 JUMPI POP PUSH1 0x1 PUSH1 0x0 SWAP1 SLOAD SWAP1 PUSH2 0x100 EXP SWAP1 DIV PUSH20 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF AND PUSH20 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF AND CALLER PUSH20 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF AND EQ JUMPDEST PUSH2 0x1B27 JUMPI PUSH1 0x40 MLOAD PUSH32 0x8C379A000000000000000000000000000000000000000000000000000000000 DUP2 MSTORE PUSH1 0x4 ADD PUSH2 0x1B1E SWAP1 PUSH2 0x44FE JUMP JUMPDEST PUSH1 0x40 MLOAD DUP1 SWAP2 SUB SWAP1 REVERT JUMPDEST PUSH2 0x1B98 DUP7 DUP7 DUP1 DUP1 PUSH1 0x20 MUL PUSH1 0x20 ADD PUSH1 0x40 MLOAD SWAP1 DUP2 ADD PUSH1 0x40 MSTORE DUP1 SWAP4 SWAP3 SWAP2 SWAP1 DUP2 DUP2 MSTORE PUSH1 0x20 ADD DUP4 DUP4 PUSH1 0x20 MUL DUP1 DUP3 DUP5 CALLDATACOPY PUSH1 0x0 DUP2 DUP5 ADD MSTORE PUSH1 0x1F NOT PUSH1 0x1F DUP3 ADD AND SWAP1 POP DUP1 DUP4 ADD SWAP3 POP POP POP POP POP POP POP DUP6 DUP6 DUP6 DUP6 PUSH1 0x1 PUSH1 0x0 SWAP1 SLOAD SWAP1 PUSH2 0x100 EXP SWAP1 DIV PUSH20 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF AND PUSH2 0x123C JUMP JUMPDEST PUSH2 0x1BD7 JUMPI PUSH1 0x40 MLOAD PUSH32 0x8C379A000000000000000000000000000000000000000000000000000000000 DUP2 MSTORE PUSH1 0x4 ADD PUSH2 0x1BCE SWAP1 PUSH2 0x43FE JUMP JUMPDEST PUSH1 0x40 MLOAD DUP1 SWAP2 SUB SWAP1 REVERT JUMPDEST PUSH1 0x0 DUP1 SWAP1 POP PUSH1 0x0 PUSH2 0x1C37 PUSH1 0x17 DUP1 SLOAD DUP1 PUSH1 0x20 MUL PUSH1 0x20 ADD PUSH1 0x40 MLOAD SWAP1 DUP2 ADD PUSH1 0x40 MSTORE DUP1 SWAP3 SWAP2 SWAP1 DUP2 DUP2 MSTORE PUSH1 0x20 ADD DUP3 DUP1 SLOAD DUP1 ISZERO PUSH2 0x1C2D JUMPI PUSH1 0x20 MUL DUP3 ADD SWAP2 SWAP1 PUSH1 0x0 MSTORE PUSH1 0x20 PUSH1 0x0 KECCAK256 SWAP1 JUMPDEST DUP2 SLOAD DUP2 MSTORE PUSH1 0x20 ADD SWAP1 PUSH1 0x1 ADD SWAP1 DUP1 DUP4 GT PUSH2 0x1C19 JUMPI JUMPDEST POP POP POP POP POP PUSH2 0x11FB JUMP JUMPDEST SWAP1 POP PUSH1 0x0 DUP1 SWAP1 POP JUMPDEST DUP7 DUP10 DUP10 SWAP1 POP SUB DUP2 LT ISZERO PUSH2 0x1C76 JUMPI DUP9 DUP9 DUP3 DUP2 DUP2 LT PUSH2 0x1C58 JUMPI INVALID JUMPDEST SWAP1 POP PUSH1 0x20 MUL ADD CALLDATALOAD DUP3 EQ ISZERO PUSH2 0x1C6B JUMPI PUSH1 0x1 SWAP3 POP JUMPDEST PUSH1 0x1 DUP2 ADD SWAP1 POP PUSH2 0x1C3F JUMP JUMPDEST POP DUP2 PUSH2 0x1CB7 JUMPI PUSH1 0x40 MLOAD PUSH32 0x8C379A000000000000000000000000000000000000000000000000000000000 DUP2 MSTORE PUSH1 0x4 ADD PUSH2 0x1CAE SWAP1 PUSH2 0x437E JUMP JUMPDEST PUSH1 0x40 MLOAD DUP1 SWAP2 SUB SWAP1 REVERT JUMPDEST PUSH2 0x1D56 PUSH1 0x18 DUP1 SLOAD DUP1 PUSH1 0x20 MUL PUSH1 0x20 ADD PUSH1 0x40 MLOAD SWAP1 DUP2 ADD PUSH1 0x40 MSTORE DUP1 SWAP3 SWAP2 SWAP1 DUP2 DUP2 MSTORE PUSH1 0x20 ADD DUP3 DUP1 SLOAD DUP1 ISZERO PUSH2 0x1D06 JUMPI PUSH1 0x20 MUL DUP3 ADD SWAP2 SWAP1 PUSH1 0x0 MSTORE PUSH1 0x20 PUSH1 0x0 KECCAK256 SWAP1 JUMPDEST DUP2 SLOAD DUP2 MSTORE PUSH1 0x20 ADD SWAP1 PUSH1 0x1 ADD SWAP1 DUP1 DUP4 GT PUSH2 0x1CF2 JUMPI JUMPDEST POP POP POP POP POP PUSH1 0x19 SLOAD DUP11 DUP11 DUP1 DUP1 PUSH1 0x20 MUL PUSH1 0x20 ADD PUSH1 0x40 MLOAD SWAP1 DUP2 ADD PUSH1 0x40 MSTORE DUP1 SWAP4 SWAP3 SWAP2 SWAP1 DUP2 DUP2 MSTORE PUSH1 0x20 ADD DUP4 DUP4 PUSH1 0x20 MUL DUP1 DUP3 DUP5 CALLDATACOPY PUSH1 0x0 DUP2 DUP5 ADD MSTORE PUSH1 0x1F NOT PUSH1 0x1F DUP3 ADD AND SWAP1 POP DUP1 DUP4 ADD SWAP3 POP POP POP POP POP POP POP DUP10 PUSH2 0x30BC JUMP JUMPDEST PUSH2 0x1D95 JUMPI PUSH1 0x40 MLOAD PUSH32 0x8C379A000000000000000000000000000000000000000000000000000000000 DUP2 MSTORE PUSH1 0x4 ADD PUSH2 0x1D8C SWAP1 PUSH2 0x447E JUMP JUMPDEST PUSH1 0x40 MLOAD DUP1 SWAP2 SUB SWAP1 REVERT JUMPDEST PUSH1 0x0 PUSH1 0x16 PUSH1 0x0 PUSH2 0x100 EXP DUP2 SLOAD DUP2 PUSH1 0xFF MUL NOT AND SWAP1 DUP4 ISZERO ISZERO MUL OR SWAP1 SSTORE POP DUP6 DUP9 DUP9 SWAP1 POP SUB PUSH1 0xB DUP2 SWAP1 SSTORE POP DUP8 DUP8 PUSH1 0x18 SWAP2 SWAP1 PUSH2 0x1DCD SWAP3 SWAP2 SWAP1 PUSH2 0x31EB JUMP JUMPDEST POP DUP6 PUSH1 0x19 DUP2 SWAP1 SSTORE POP DUP5 PUSH1 0x1B PUSH1 0x0 PUSH2 0x100 EXP DUP2 SLOAD DUP2 PUSH1 0xFF MUL NOT AND SWAP1 DUP4 PUSH1 0xFF AND MUL OR SWAP1 SSTORE POP DUP4 PUSH1 0x1C DUP2 SWAP1 SSTORE POP DUP3 PUSH1 0x1D DUP2 SWAP1 SSTORE POP POP POP POP POP POP POP POP POP JUMP JUMPDEST PUSH1 0x0 PUSH1 0xC SLOAD SWAP1 POP SWAP1 JUMP JUMPDEST PUSH1 0x60 PUSH1 0x11 DUP1 SLOAD DUP1 PUSH1 0x20 MUL PUSH1 0x20 ADD PUSH1 0x40 MLOAD SWAP1 DUP2 ADD PUSH1 0x40 MSTORE DUP1 SWAP3 SWAP2 SWAP1 DUP2 DUP2 MSTORE PUSH1 0x20 ADD DUP3 DUP1 SLOAD DUP1 ISZERO PUSH2 0x1E60 JUMPI PUSH1 0x20 MUL DUP3 ADD SWAP2 SWAP1 PUSH1 0x0 MSTORE PUSH1 0x20 PUSH1 0x0 KECCAK256 SWAP1 JUMPDEST DUP2 SLOAD DUP2 MSTORE PUSH1 0x20 ADD SWAP1 PUSH1 0x1 ADD SWAP1 DUP1 DUP4 GT PUSH2 0x1E4C JUMPI JUMPDEST POP POP POP POP POP SWAP1 POP SWAP1 JUMP JUMPDEST PUSH1 0x0 DUP1 SWAP1 SLOAD SWAP1 PUSH2 0x100 EXP SWAP1 DIV PUSH20 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF AND PUSH20 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF AND CALLER PUSH20 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF AND EQ DUP1 PUSH2 0x1F12 JUMPI POP PUSH1 0x1 PUSH1 0x0 SWAP1 SLOAD SWAP1 PUSH2 0x100 EXP SWAP1 DIV PUSH20 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF AND PUSH20 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF AND CALLER PUSH20 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF AND EQ JUMPDEST PUSH2 0x1F51 JUMPI PUSH1 0x40 MLOAD PUSH32 0x8C379A000000000000000000000000000000000000000000000000000000000 DUP2 MSTORE PUSH1 0x4 ADD PUSH2 0x1F48 SWAP1 PUSH2 0x44FE JUMP JUMPDEST PUSH1 0x40 MLOAD DUP1 SWAP2 SUB SWAP1 REVERT JUMPDEST PUSH1 0x0 DUP1 SWAP1 SLOAD SWAP1 PUSH2 0x100 EXP SWAP1 DIV PUSH20 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF AND PUSH20 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF AND CALLER PUSH20 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF AND EQ ISZERO PUSH2 0x2037 JUMPI PUSH1 0x0 PUSH1 0x7 SLOAD SWAP1 POP NUMBER PUSH1 0xC SLOAD GT DUP1 ISZERO PUSH2 0x1FCB JUMPI POP PUSH1 0xD PUSH1 0x0 SWAP1 SLOAD SWAP1 PUSH2 0x100 EXP SWAP1 DIV PUSH1 0xFF AND ISZERO JUMPDEST ISZERO PUSH2 0x1FDA JUMPI PUSH1 0x4 SLOAD PUSH1 0x7 SLOAD SUB SWAP1 POP JUMPDEST DUP1 PUSH1 0x7 PUSH1 0x0 DUP3 DUP3 SLOAD SUB SWAP3 POP POP DUP2 SWAP1 SSTORE POP DUP2 PUSH20 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF AND PUSH2 0x8FC DUP3 SWAP1 DUP2 ISZERO MUL SWAP1 PUSH1 0x40 MLOAD PUSH1 0x0 PUSH1 0x40 MLOAD DUP1 DUP4 SUB DUP2 DUP6 DUP9 DUP9 CALL SWAP4 POP POP POP POP ISZERO DUP1 ISZERO PUSH2 0x2030 JUMPI RETURNDATASIZE PUSH1 0x0 DUP1 RETURNDATACOPY RETURNDATASIZE PUSH1 0x0 REVERT JUMPDEST POP POP PUSH2 0x211E JUMP JUMPDEST PUSH1 0x1 PUSH1 0x0 SWAP1 SLOAD SWAP1 PUSH2 0x100 EXP SWAP1 DIV PUSH20 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF AND PUSH20 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF AND CALLER PUSH20 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF AND EQ ISZERO PUSH2 0x211D JUMPI PUSH1 0x0 PUSH1 0x8 SLOAD SWAP1 POP NUMBER PUSH1 0xC SLOAD GT DUP1 ISZERO PUSH2 0x20B1 JUMPI POP PUSH1 0xD PUSH1 0x0 SWAP1 SLOAD SWAP1 PUSH2 0x100 EXP SWAP1 DIV PUSH1 0xFF AND JUMPDEST ISZERO PUSH2 0x20C0 JUMPI PUSH1 0x4 SLOAD PUSH1 0x8 SLOAD SUB SWAP1 POP JUMPDEST DUP1 PUSH1 0x8 PUSH1 0x0 DUP3 DUP3 SLOAD SUB SWAP3 POP POP DUP2 SWAP1 SSTORE POP DUP2 PUSH20 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF AND PUSH2 0x8FC DUP3 SWAP1 DUP2 ISZERO MUL SWAP1 PUSH1 0x40 MLOAD PUSH1 0x0 PUSH1 0x40 MLOAD DUP1 DUP4 SUB DUP2 DUP6 DUP9 DUP9 CALL SWAP4 POP POP POP POP ISZERO DUP1 ISZERO PUSH2 0x2116 JUMPI RETURNDATASIZE PUSH1 0x0 DUP1 RETURNDATACOPY RETURNDATASIZE PUSH1 0x0 REVERT JUMPDEST POP POP PUSH2 0x211E JUMP JUMPDEST JUMPDEST POP JUMP JUMPDEST PUSH1 0x0 PUSH1 0x13 SLOAD SWAP1 POP SWAP1 JUMP JUMPDEST PUSH1 0x16 PUSH1 0x0 SWAP1 SLOAD SWAP1 PUSH2 0x100 EXP SWAP1 DIV PUSH1 0xFF AND PUSH2 0x217A JUMPI PUSH1 0x40 MLOAD PUSH32 0x8C379A000000000000000000000000000000000000000000000000000000000 DUP2 MSTORE PUSH1 0x4 ADD PUSH2 0x2171 SWAP1 PUSH2 0x45BE JUMP JUMPDEST PUSH1 0x40 MLOAD DUP1 SWAP2 SUB SWAP1 REVERT JUMPDEST PUSH1 0x0 DUP1 SWAP1 SLOAD SWAP1 PUSH2 0x100 EXP SWAP1 DIV PUSH20 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF AND PUSH20 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF AND CALLER PUSH20 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF AND EQ DUP1 PUSH2 0x2222 JUMPI POP PUSH1 0x1 PUSH1 0x0 SWAP1 SLOAD SWAP1 PUSH2 0x100 EXP SWAP1 DIV PUSH20 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF AND PUSH20 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF AND CALLER PUSH20 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF AND EQ JUMPDEST PUSH2 0x2261 JUMPI PUSH1 0x40 MLOAD PUSH32 0x8C379A000000000000000000000000000000000000000000000000000000000 DUP2 MSTORE PUSH1 0x4 ADD PUSH2 0x2258 SWAP1 PUSH2 0x44FE JUMP JUMPDEST PUSH1 0x40 MLOAD DUP1 SWAP2 SUB SWAP1 REVERT JUMPDEST PUSH2 0x2269 PUSH2 0x22D4 JUMP JUMPDEST ISZERO PUSH2 0x22D2 JUMPI NUMBER PUSH1 0xC DUP2 SWAP1 SSTORE POP NUMBER PUSH1 0xA DUP2 SWAP1 SSTORE POP PUSH1 0xD PUSH1 0x0 SWAP1 SLOAD SWAP1 PUSH2 0x100 EXP SWAP1 DIV PUSH1 0xFF AND ISZERO PUSH2 0x22D1 JUMPI PUSH1 0x4 SLOAD PUSH1 0x7 PUSH1 0x0 DUP3 DUP3 SLOAD ADD SWAP3 POP POP DUP2 SWAP1 SSTORE POP PUSH1 0x4 SLOAD PUSH1 0x8 PUSH1 0x0 DUP3 DUP3 SLOAD SUB SWAP3 POP POP DUP2 SWAP1 SSTORE POP PUSH1 0x0 PUSH1 0xD PUSH1 0x0 PUSH2 0x100 EXP DUP2 SLOAD DUP2 PUSH1 0xFF MUL NOT AND SWAP1 DUP4 ISZERO ISZERO MUL OR SWAP1 SSTORE POP JUMPDEST JUMPDEST JUMP JUMPDEST PUSH1 0x0 NUMBER PUSH1 0x15 SLOAD GT ISZERO DUP1 ISZERO PUSH2 0x22F4 JUMPI POP PUSH1 0x16 PUSH1 0x0 SWAP1 SLOAD SWAP1 PUSH2 0x100 EXP SWAP1 DIV PUSH1 0xFF AND JUMPDEST SWAP1 POP SWAP1 JUMP JUMPDEST PUSH1 0x16 PUSH1 0x0 SWAP1 SLOAD SWAP1 PUSH2 0x100 EXP SWAP1 DIV PUSH1 0xFF AND ISZERO PUSH2 0x2349 JUMPI PUSH1 0x40 MLOAD PUSH32 0x8C379A000000000000000000000000000000000000000000000000000000000 DUP2 MSTORE PUSH1 0x4 ADD PUSH2 0x2340 SWAP1 PUSH2 0x459E JUMP JUMPDEST PUSH1 0x40 MLOAD DUP1 SWAP2 SUB SWAP1 REVERT JUMPDEST PUSH2 0x2351 PUSH2 0x1230 JUMP JUMPDEST PUSH2 0x2390 JUMPI PUSH1 0x40 MLOAD PUSH32 0x8C379A000000000000000000000000000000000000000000000000000000000 DUP2 MSTORE PUSH1 0x4 ADD PUSH2 0x2387 SWAP1 PUSH2 0x457E JUMP JUMPDEST PUSH1 0x40 MLOAD DUP1 SWAP2 SUB SWAP1 REVERT JUMPDEST PUSH1 0x0 DUP1 SWAP1 SLOAD SWAP1 PUSH2 0x100 EXP SWAP1 DIV PUSH20 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF AND PUSH20 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF AND CALLER PUSH20 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF AND EQ PUSH2 0x241F JUMPI PUSH1 0x40 MLOAD PUSH32 0x8C379A000000000000000000000000000000000000000000000000000000000 DUP2 MSTORE PUSH1 0x4 ADD PUSH2 0x2416 SWAP1 PUSH2 0x451E JUMP JUMPDEST PUSH1 0x40 MLOAD DUP1 SWAP2 SUB SWAP1 REVERT JUMPDEST PUSH1 0x2 PUSH1 0x0 SWAP1 SLOAD SWAP1 PUSH2 0x100 EXP SWAP1 DIV PUSH20 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF AND PUSH20 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF AND PUSH4 0x51428BC0 DUP12 DUP12 DUP6 DUP6 PUSH1 0x40 MLOAD DUP6 PUSH4 0xFFFFFFFF AND PUSH1 0xE0 SHL DUP2 MSTORE PUSH1 0x4 ADD PUSH2 0x2480 SWAP5 SWAP4 SWAP3 SWAP2 SWAP1 PUSH2 0x4252 JUMP JUMPDEST PUSH1 0x20 PUSH1 0x40 MLOAD DUP1 DUP4 SUB DUP2 DUP7 DUP1 EXTCODESIZE ISZERO DUP1 ISZERO PUSH2 0x2498 JUMPI PUSH1 0x0 DUP1 REVERT JUMPDEST POP GAS STATICCALL ISZERO DUP1 ISZERO PUSH2 0x24AC JUMPI RETURNDATASIZE PUSH1 0x0 DUP1 RETURNDATACOPY RETURNDATASIZE PUSH1 0x0 REVERT JUMPDEST POP POP POP POP PUSH1 0x40 MLOAD RETURNDATASIZE PUSH1 0x1F NOT PUSH1 0x1F DUP3 ADD AND DUP3 ADD DUP1 PUSH1 0x40 MSTORE POP PUSH2 0x24D0 SWAP2 SWAP1 DUP2 ADD SWAP1 PUSH2 0x381A JUMP JUMPDEST PUSH2 0x250F JUMPI PUSH1 0x40 MLOAD PUSH32 0x8C379A000000000000000000000000000000000000000000000000000000000 DUP2 MSTORE PUSH1 0x4 ADD PUSH2 0x2506 SWAP1 PUSH2 0x443E JUMP JUMPDEST PUSH1 0x40 MLOAD DUP1 SWAP2 SUB SWAP1 REVERT JUMPDEST PUSH2 0x2580 DUP9 DUP9 DUP1 DUP1 PUSH1 0x20 MUL PUSH1 0x20 ADD PUSH1 0x40 MLOAD SWAP1 DUP2 ADD PUSH1 0x40 MSTORE DUP1 SWAP4 SWAP3 SWAP2 SWAP1 DUP2 DUP2 MSTORE PUSH1 0x20 ADD DUP4 DUP4 PUSH1 0x20 MUL DUP1 DUP3 DUP5 CALLDATACOPY PUSH1 0x0 DUP2 DUP5 ADD MSTORE PUSH1 0x1F NOT PUSH1 0x1F DUP3 ADD AND SWAP1 POP DUP1 DUP4 ADD SWAP3 POP POP POP POP POP POP POP DUP8 DUP8 DUP8 DUP8 PUSH1 0x1 PUSH1 0x0 SWAP1 SLOAD SWAP1 PUSH2 0x100 EXP SWAP1 DIV PUSH20 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF AND PUSH2 0x123C JUMP JUMPDEST PUSH2 0x25BF JUMPI PUSH1 0x40 MLOAD PUSH32 0x8C379A000000000000000000000000000000000000000000000000000000000 DUP2 MSTORE PUSH1 0x4 ADD PUSH2 0x25B6 SWAP1 PUSH2 0x43FE JUMP JUMPDEST PUSH1 0x40 MLOAD DUP1 SWAP2 SUB SWAP1 REVERT JUMPDEST PUSH1 0x0 DUP1 SWAP1 POP PUSH1 0x0 PUSH2 0x2610 DUP13 DUP13 DUP1 DUP1 PUSH1 0x20 MUL PUSH1 0x20 ADD PUSH1 0x40 MLOAD SWAP1 DUP2 ADD PUSH1 0x40 MSTORE DUP1 SWAP4 SWAP3 SWAP2 SWAP1 DUP2 DUP2 MSTORE PUSH1 0x20 ADD DUP4 DUP4 PUSH1 0x20 MUL DUP1 DUP3 DUP5 CALLDATACOPY PUSH1 0x0 DUP2 DUP5 ADD MSTORE PUSH1 0x1F NOT PUSH1 0x1F DUP3 ADD AND SWAP1 POP DUP1 DUP4 ADD SWAP3 POP POP POP POP POP POP POP PUSH2 0x11FB JUMP JUMPDEST SWAP1 POP PUSH1 0x0 DUP9 DUP12 DUP12 SWAP1 POP SUB SWAP1 POP JUMPDEST DUP11 DUP11 SWAP1 POP DUP2 LT ISZERO PUSH2 0x2652 JUMPI DUP11 DUP11 DUP3 DUP2 DUP2 LT PUSH2 0x2634 JUMPI INVALID JUMPDEST SWAP1 POP PUSH1 0x20 MUL ADD CALLDATALOAD DUP3 EQ ISZERO PUSH2 0x2647 JUMPI PUSH1 0x1 SWAP3 POP JUMPDEST PUSH1 0x1 DUP2 ADD SWAP1 POP PUSH2 0x261D JUMP JUMPDEST POP DUP2 PUSH2 0x2693 JUMPI PUSH1 0x40 MLOAD PUSH32 0x8C379A000000000000000000000000000000000000000000000000000000000 DUP2 MSTORE PUSH1 0x4 ADD PUSH2 0x268A SWAP1 PUSH2 0x441E JUMP JUMPDEST PUSH1 0x40 MLOAD DUP1 SWAP2 SUB SWAP1 REVERT JUMPDEST PUSH1 0x1 PUSH1 0x16 PUSH1 0x0 PUSH2 0x100 EXP DUP2 SLOAD DUP2 PUSH1 0xFF MUL NOT AND SWAP1 DUP4 ISZERO ISZERO MUL OR SWAP1 SSTORE POP DUP10 DUP10 PUSH1 0x18 SWAP2 SWAP1 PUSH2 0x26BF SWAP3 SWAP2 SWAP1 PUSH2 0x31EB JUMP JUMPDEST POP DUP8 PUSH1 0x19 DUP2 SWAP1 SSTORE POP DUP12 DUP12 PUSH1 0x17 SWAP2 SWAP1 PUSH2 0x26D8 SWAP3 SWAP2 SWAP1 PUSH2 0x31EB JUMP JUMPDEST POP DUP4 DUP4 PUSH1 0x1A SWAP2 SWAP1 PUSH2 0x26EA SWAP3 SWAP2 SWAP1 PUSH2 0x31EB JUMP JUMPDEST POP PUSH1 0x3 SLOAD NUMBER ADD PUSH1 0x15 DUP2 SWAP1 SSTORE POP DUP8 DUP11 DUP11 SWAP1 POP SUB PUSH1 0xB DUP2 SWAP1 SSTORE POP POP POP POP POP POP POP POP POP POP POP POP POP JUMP JUMPDEST PUSH1 0x0 PUSH1 0x1B PUSH1 0x0 SWAP1 SLOAD SWAP1 PUSH2 0x100 EXP SWAP1 DIV PUSH1 0xFF AND SWAP1 POP SWAP1 JUMP JUMPDEST PUSH1 0x60 PUSH1 0x18 DUP1 SLOAD DUP1 PUSH1 0x20 MUL PUSH1 0x20 ADD PUSH1 0x40 MLOAD SWAP1 DUP2 ADD PUSH1 0x40 MSTORE DUP1 SWAP3 SWAP2 SWAP1 DUP2 DUP2 MSTORE PUSH1 0x20 ADD DUP3 DUP1 SLOAD DUP1 ISZERO PUSH2 0x2775 JUMPI PUSH1 0x20 MUL DUP3 ADD SWAP2 SWAP1 PUSH1 0x0 MSTORE PUSH1 0x20 PUSH1 0x0 KECCAK256 SWAP1 JUMPDEST DUP2 SLOAD DUP2 MSTORE PUSH1 0x20 ADD SWAP1 PUSH1 0x1 ADD SWAP1 DUP1 DUP4 GT PUSH2 0x2761 JUMPI JUMPDEST POP POP POP POP POP SWAP1 POP SWAP1 JUMP JUMPDEST PUSH1 0x0 PUSH1 0x19 SLOAD SWAP1 POP SWAP1 JUMP JUMPDEST PUSH1 0x0 PUSH1 0x12 PUSH1 0x0 SWAP1 SLOAD SWAP1 PUSH2 0x100 EXP SWAP1 DIV PUSH1 0xFF AND SWAP1 POP SWAP1 JUMP JUMPDEST PUSH1 0x0 PUSH1 0x2 PUSH1 0x0 SWAP1 SLOAD SWAP1 PUSH2 0x100 EXP SWAP1 DIV PUSH20 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF AND SWAP1 POP SWAP1 JUMP JUMPDEST PUSH1 0x0 PUSH1 0x1D SLOAD SWAP1 POP SWAP1 JUMP JUMPDEST PUSH1 0x0 PUSH1 0x9 SLOAD SWAP1 POP SWAP1 JUMP JUMPDEST PUSH2 0x27E6 PUSH2 0x1230 JUMP JUMPDEST PUSH2 0x2825 JUMPI PUSH1 0x40 MLOAD PUSH32 0x8C379A000000000000000000000000000000000000000000000000000000000 DUP2 MSTORE PUSH1 0x4 ADD PUSH2 0x281C SWAP1 PUSH2 0x457E JUMP JUMPDEST PUSH1 0x40 MLOAD DUP1 SWAP2 SUB SWAP1 REVERT JUMPDEST PUSH1 0x0 DUP1 SWAP1 SLOAD SWAP1 PUSH2 0x100 EXP SWAP1 DIV PUSH20 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF AND PUSH20 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF AND CALLER PUSH20 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF AND EQ DUP1 PUSH2 0x28CD JUMPI POP PUSH1 0x1 PUSH1 0x0 SWAP1 SLOAD SWAP1 PUSH2 0x100 EXP SWAP1 DIV PUSH20 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF AND PUSH20 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF AND CALLER PUSH20 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF AND EQ JUMPDEST PUSH2 0x290C JUMPI PUSH1 0x40 MLOAD PUSH32 0x8C379A000000000000000000000000000000000000000000000000000000000 DUP2 MSTORE PUSH1 0x4 ADD PUSH2 0x2903 SWAP1 PUSH2 0x44FE JUMP JUMPDEST PUSH1 0x40 MLOAD DUP1 SWAP2 SUB SWAP1 REVERT JUMPDEST PUSH2 0x297D DUP7 DUP7 DUP1 DUP1 PUSH1 0x20 MUL PUSH1 0x20 ADD PUSH1 0x40 MLOAD SWAP1 DUP2 ADD PUSH1 0x40 MSTORE DUP1 SWAP4 SWAP3 SWAP2 SWAP1 DUP2 DUP2 MSTORE PUSH1 0x20 ADD DUP4 DUP4 PUSH1 0x20 MUL DUP1 DUP3 DUP5 CALLDATACOPY PUSH1 0x0 DUP2 DUP5 ADD MSTORE PUSH1 0x1F NOT PUSH1 0x1F DUP3 ADD AND SWAP1 POP DUP1 DUP4 ADD SWAP3 POP POP POP POP POP POP POP DUP6 DUP6 DUP6 DUP6 PUSH1 0x1 PUSH1 0x0 SWAP1 SLOAD SWAP1 PUSH2 0x100 EXP SWAP1 DIV PUSH20 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF AND PUSH2 0x123C JUMP JUMPDEST PUSH2 0x29BC JUMPI PUSH1 0x40 MLOAD PUSH32 0x8C379A000000000000000000000000000000000000000000000000000000000 DUP2 MSTORE PUSH1 0x4 ADD PUSH2 0x29B3 SWAP1 PUSH2 0x43FE JUMP JUMPDEST PUSH1 0x40 MLOAD DUP1 SWAP2 SUB SWAP1 REVERT JUMPDEST PUSH1 0x6 SLOAD DUP5 DUP8 DUP8 SWAP1 POP SUB GT PUSH2 0x2A05 JUMPI PUSH1 0x40 MLOAD PUSH32 0x8C379A000000000000000000000000000000000000000000000000000000000 DUP2 MSTORE PUSH1 0x4 ADD PUSH2 0x29FC SWAP1 PUSH2 0x453E JUMP JUMPDEST PUSH1 0x40 MLOAD DUP1 SWAP2 SUB SWAP1 REVERT JUMPDEST PUSH1 0xD PUSH1 0x0 SWAP1 SLOAD SWAP1 PUSH2 0x100 EXP SWAP1 DIV PUSH1 0xFF AND ISZERO PUSH2 0x2A5A JUMPI PUSH1 0x4 SLOAD PUSH1 0x7 PUSH1 0x0 DUP3 DUP3 SLOAD ADD SWAP3 POP POP DUP2 SWAP1 SSTORE POP PUSH1 0x4 SLOAD PUSH1 0x8 PUSH1 0x0 DUP3 DUP3 SLOAD SUB SWAP3 POP POP DUP2 SWAP1 SSTORE POP PUSH1 0x0 PUSH1 0xD PUSH1 0x0 PUSH2 0x100 EXP DUP2 SLOAD DUP2 PUSH1 0xFF MUL NOT AND SWAP1 DUP4 ISZERO ISZERO MUL OR SWAP1 SSTORE POP JUMPDEST NUMBER PUSH1 0xC DUP2 SWAP1 SSTORE POP NUMBER PUSH1 0xA DUP2 SWAP1 SSTORE POP POP POP POP POP POP POP JUMP JUMPDEST PUSH1 0x60 PUSH1 0xE DUP1 SLOAD DUP1 PUSH1 0x20 MUL PUSH1 0x20 ADD PUSH1 0x40 MLOAD SWAP1 DUP2 ADD PUSH1 0x40 MSTORE DUP1 SWAP3 SWAP2 SWAP1 DUP2 DUP2 MSTORE PUSH1 0x20 ADD DUP3 DUP1 SLOAD DUP1 ISZERO PUSH2 0x2ABE JUMPI PUSH1 0x20 MUL DUP3 ADD SWAP2 SWAP1 PUSH1 0x0 MSTORE PUSH1 0x20 PUSH1 0x0 KECCAK256 SWAP1 JUMPDEST DUP2 SLOAD DUP2 MSTORE PUSH1 0x20 ADD SWAP1 PUSH1 0x1 ADD SWAP1 DUP1 DUP4 GT PUSH2 0x2AAA JUMPI JUMPDEST POP POP POP POP POP SWAP1 POP SWAP1 JUMP JUMPDEST PUSH1 0x0 DUP1 PUSH1 0x0 SWAP1 SLOAD SWAP1 PUSH2 0x100 EXP SWAP1 DIV PUSH20 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF AND PUSH20 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF AND CALLER PUSH20 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF AND EQ DUP1 PUSH2 0x2B72 JUMPI POP PUSH1 0x1 PUSH1 0x0 SWAP1 SLOAD SWAP1 PUSH2 0x100 EXP SWAP1 DIV PUSH20 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF AND PUSH20 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF AND CALLER PUSH20 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF AND EQ JUMPDEST PUSH2 0x2BB1 JUMPI PUSH1 0x40 MLOAD PUSH32 0x8C379A000000000000000000000000000000000000000000000000000000000 DUP2 MSTORE PUSH1 0x4 ADD PUSH2 0x2BA8 SWAP1 PUSH2 0x44FE JUMP JUMPDEST PUSH1 0x40 MLOAD DUP1 SWAP2 SUB SWAP1 REVERT JUMPDEST PUSH1 0x0 DUP1 SWAP1 SLOAD SWAP1 PUSH2 0x100 EXP SWAP1 DIV PUSH20 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF AND PUSH20 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF AND CALLER PUSH20 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF AND EQ ISZERO PUSH2 0x2C43 JUMPI PUSH1 0x0 PUSH1 0x7 SLOAD SWAP1 POP NUMBER PUSH1 0xC SLOAD GT DUP1 ISZERO PUSH2 0x2C2B JUMPI POP PUSH1 0xD PUSH1 0x0 SWAP1 SLOAD SWAP1 PUSH2 0x100 EXP SWAP1 DIV PUSH1 0xFF AND ISZERO JUMPDEST ISZERO PUSH2 0x2C3A JUMPI PUSH1 0x4 SLOAD PUSH1 0x7 SLOAD SUB SWAP1 POP JUMPDEST DUP1 SWAP2 POP POP PUSH2 0x2CDA JUMP JUMPDEST PUSH1 0x1 PUSH1 0x0 SWAP1 SLOAD SWAP1 PUSH2 0x100 EXP SWAP1 DIV PUSH20 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF AND PUSH20 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF AND CALLER PUSH20 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF AND EQ ISZERO PUSH2 0x2CD5 JUMPI PUSH1 0x0 PUSH1 0x8 SLOAD SWAP1 POP NUMBER PUSH1 0xC SLOAD GT DUP1 ISZERO PUSH2 0x2CBD JUMPI POP PUSH1 0xD PUSH1 0x0 SWAP1 SLOAD SWAP1 PUSH2 0x100 EXP SWAP1 DIV PUSH1 0xFF AND JUMPDEST ISZERO PUSH2 0x2CCC JUMPI PUSH1 0x4 SLOAD PUSH1 0x8 SLOAD SUB SWAP1 POP JUMPDEST DUP1 SWAP2 POP POP PUSH2 0x2CDA JUMP JUMPDEST PUSH1 0x0 SWAP1 POP JUMPDEST SWAP1 JUMP JUMPDEST PUSH1 0x0 PUSH1 0xD PUSH1 0x0 SWAP1 SLOAD SWAP1 PUSH2 0x100 EXP SWAP1 DIV PUSH1 0xFF AND ISZERO PUSH2 0x2D2F JUMPI PUSH1 0x40 MLOAD PUSH32 0x8C379A000000000000000000000000000000000000000000000000000000000 DUP2 MSTORE PUSH1 0x4 ADD PUSH2 0x2D26 SWAP1 PUSH2 0x44BE JUMP JUMPDEST PUSH1 0x40 MLOAD DUP1 SWAP2 SUB SWAP1 REVERT JUMPDEST PUSH2 0x2D37 PUSH2 0x1230 JUMP JUMPDEST PUSH2 0x2D76 JUMPI PUSH1 0x40 MLOAD PUSH32 0x8C379A000000000000000000000000000000000000000000000000000000000 DUP2 MSTORE PUSH1 0x4 ADD PUSH2 0x2D6D SWAP1 PUSH2 0x457E JUMP JUMPDEST PUSH1 0x40 MLOAD DUP1 SWAP2 SUB SWAP1 REVERT JUMPDEST PUSH1 0x1 PUSH1 0x0 SWAP1 SLOAD SWAP1 PUSH2 0x100 EXP SWAP1 DIV PUSH20 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF AND PUSH20 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF AND CALLER PUSH20 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF AND EQ PUSH2 0x2E06 JUMPI PUSH1 0x40 MLOAD PUSH32 0x8C379A000000000000000000000000000000000000000000000000000000000 DUP2 MSTORE PUSH1 0x4 ADD PUSH2 0x2DFD SWAP1 PUSH2 0x451E JUMP JUMPDEST PUSH1 0x40 MLOAD DUP1 SWAP2 SUB SWAP1 REVERT JUMPDEST DUP5 DUP7 MLOAD SUB PUSH1 0xB SLOAD GT ISZERO PUSH2 0x2E4E JUMPI PUSH1 0x40 MLOAD PUSH32 0x8C379A000000000000000000000000000000000000000000000000000000000 DUP2 MSTORE PUSH1 0x4 ADD PUSH2 0x2E45 SWAP1 PUSH2 0x439E JUMP JUMPDEST PUSH1 0x40 MLOAD DUP1 SWAP2 SUB SWAP1 REVERT JUMPDEST PUSH1 0x2 PUSH1 0x0 SWAP1 SLOAD SWAP1 PUSH2 0x100 EXP SWAP1 DIV PUSH20 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF AND PUSH20 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF AND PUSH4 0x1BF28F83 DUP9 PUSH1 0x40 MLOAD DUP3 PUSH4 0xFFFFFFFF AND PUSH1 0xE0 SHL DUP2 MSTORE PUSH1 0x4 ADD PUSH2 0x2EA9 SWAP2 SWAP1 PUSH2 0x428D JUMP JUMPDEST PUSH1 0x20 PUSH1 0x40 MLOAD DUP1 DUP4 SUB DUP2 DUP7 DUP1 EXTCODESIZE ISZERO DUP1 ISZERO PUSH2 0x2EC1 JUMPI PUSH1 0x0 DUP1 REVERT JUMPDEST POP GAS STATICCALL ISZERO DUP1 ISZERO PUSH2 0x2ED5 JUMPI RETURNDATASIZE PUSH1 0x0 DUP1 RETURNDATACOPY RETURNDATASIZE PUSH1 0x0 REVERT JUMPDEST POP POP POP POP PUSH1 0x40 MLOAD RETURNDATASIZE PUSH1 0x1F NOT PUSH1 0x1F DUP3 ADD AND DUP3 ADD DUP1 PUSH1 0x40 MSTORE POP PUSH2 0x2EF9 SWAP2 SWAP1 DUP2 ADD SWAP1 PUSH2 0x381A JUMP JUMPDEST PUSH2 0x2F38 JUMPI PUSH1 0x40 MLOAD PUSH32 0x8C379A000000000000000000000000000000000000000000000000000000000 DUP2 MSTORE PUSH1 0x4 ADD PUSH2 0x2F2F SWAP1 PUSH2 0x43DE JUMP JUMPDEST PUSH1 0x40 MLOAD DUP1 SWAP2 SUB SWAP1 REVERT JUMPDEST PUSH2 0x2F68 DUP7 DUP7 DUP7 DUP7 DUP7 PUSH1 0x1 PUSH1 0x0 SWAP1 SLOAD SWAP1 PUSH2 0x100 EXP SWAP1 DIV PUSH20 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF AND PUSH2 0x123C JUMP JUMPDEST PUSH2 0x2FA7 JUMPI PUSH1 0x40 MLOAD PUSH32 0x8C379A000000000000000000000000000000000000000000000000000000000 DUP2 MSTORE PUSH1 0x4 ADD PUSH2 0x2F9E SWAP1 PUSH2 0x43FE JUMP JUMPDEST PUSH1 0x40 MLOAD DUP1 SWAP2 SUB SWAP1 REVERT JUMPDEST PUSH1 0x0 DUP1 SWAP1 POP PUSH1 0x0 PUSH2 0x2FB7 DUP10 PUSH2 0x11FB JUMP JUMPDEST SWAP1 POP PUSH1 0x0 DUP8 DUP10 MLOAD SUB SWAP1 POP JUMPDEST DUP9 MLOAD DUP2 LT ISZERO PUSH2 0x2FF6 JUMPI DUP9 DUP2 DUP2 MLOAD DUP2 LT PUSH2 0x2FD7 JUMPI INVALID JUMPDEST PUSH1 0x20 MUL PUSH1 0x20 ADD ADD MLOAD DUP3 EQ ISZERO PUSH2 0x2FEB JUMPI PUSH1 0x1 SWAP3 POP JUMPDEST PUSH1 0x1 DUP2 ADD SWAP1 POP PUSH2 0x2FC2 JUMP JUMPDEST POP DUP2 PUSH2 0x3037 JUMPI PUSH1 0x40 MLOAD PUSH32 0x8C379A000000000000000000000000000000000000000000000000000000000 DUP2 MSTORE PUSH1 0x4 ADD PUSH2 0x302E SWAP1 PUSH2 0x441E JUMP JUMPDEST PUSH1 0x40 MLOAD DUP1 SWAP2 SUB SWAP1 REVERT JUMPDEST PUSH1 0x1 SWAP3 POP POP POP SWAP7 SWAP6 POP POP POP POP POP POP JUMP JUMPDEST PUSH1 0x60 PUSH1 0x17 DUP1 SLOAD DUP1 PUSH1 0x20 MUL PUSH1 0x20 ADD PUSH1 0x40 MLOAD SWAP1 DUP2 ADD PUSH1 0x40 MSTORE DUP1 SWAP3 SWAP2 SWAP1 DUP2 DUP2 MSTORE PUSH1 0x20 ADD DUP3 DUP1 SLOAD DUP1 ISZERO PUSH2 0x3095 JUMPI PUSH1 0x20 MUL DUP3 ADD SWAP2 SWAP1 PUSH1 0x0 MSTORE PUSH1 0x20 PUSH1 0x0 KECCAK256 SWAP1 JUMPDEST DUP2 SLOAD DUP2 MSTORE PUSH1 0x20 ADD SWAP1 PUSH1 0x1 ADD SWAP1 DUP1 DUP4 GT PUSH2 0x3081 JUMPI JUMPDEST POP POP POP POP POP SWAP1 POP SWAP1 JUMP JUMPDEST PUSH1 0x6 SLOAD DUP2 JUMP JUMPDEST PUSH1 0x0 PUSH1 0x16 PUSH1 0x0 SWAP1 SLOAD SWAP1 PUSH2 0x100 EXP SWAP1 DIV PUSH1 0xFF AND SWAP1 POP SWAP1 JUMP JUMPDEST PUSH1 0x0 DUP1 PUSH1 0x0 DUP1 PUSH1 0x0 DUP1 SWAP1 POP JUMPDEST DUP8 DUP10 MLOAD SUB DUP2 LT ISZERO PUSH2 0x314E JUMPI DUP9 DUP2 DUP2 MLOAD DUP2 LT PUSH2 0x30DF JUMPI INVALID JUMPDEST PUSH1 0x20 MUL PUSH1 0x20 ADD ADD MLOAD SWAP3 POP PUSH1 0x0 SWAP4 POP PUSH1 0x0 DUP1 SWAP1 POP JUMPDEST DUP7 DUP9 MLOAD SUB DUP2 LT ISZERO PUSH2 0x3130 JUMPI DUP8 DUP2 DUP2 MLOAD DUP2 LT PUSH2 0x310A JUMPI INVALID JUMPDEST PUSH1 0x20 MUL PUSH1 0x20 ADD ADD MLOAD SWAP3 POP DUP3 DUP5 EQ ISZERO PUSH2 0x3125 JUMPI PUSH1 0x1 SWAP5 POP PUSH2 0x3130 JUMP JUMPDEST PUSH1 0x1 DUP2 ADD SWAP1 POP PUSH2 0x30F3 JUMP JUMPDEST POP DUP4 PUSH2 0x3143 JUMPI PUSH1 0x0 SWAP5 POP POP POP POP POP PUSH2 0x31E3 JUMP JUMPDEST PUSH1 0x1 DUP2 ADD SWAP1 POP PUSH2 0x30C8 JUMP JUMPDEST POP PUSH1 0x0 DUP8 DUP10 MLOAD SUB SWAP1 POP JUMPDEST DUP9 MLOAD DUP2 LT ISZERO PUSH2 0x31DA JUMPI DUP9 DUP2 DUP2 MLOAD DUP2 LT PUSH2 0x316D JUMPI INVALID JUMPDEST PUSH1 0x20 MUL PUSH1 0x20 ADD ADD MLOAD SWAP3 POP PUSH1 0x0 SWAP4 POP PUSH1 0x0 DUP1 SWAP1 POP JUMPDEST DUP8 MLOAD DUP2 LT ISZERO PUSH2 0x31BC JUMPI DUP8 DUP2 DUP2 MLOAD DUP2 LT PUSH2 0x3196 JUMPI INVALID JUMPDEST PUSH1 0x20 MUL PUSH1 0x20 ADD ADD MLOAD SWAP3 POP DUP3 DUP5 EQ ISZERO PUSH2 0x31B1 JUMPI PUSH1 0x1 SWAP5 POP PUSH2 0x31BC JUMP JUMPDEST PUSH1 0x1 DUP2 ADD SWAP1 POP PUSH2 0x3181 JUMP JUMPDEST POP DUP4 PUSH2 0x31CF JUMPI PUSH1 0x0 SWAP5 POP POP POP POP POP PUSH2 0x31E3 JUMP JUMPDEST PUSH1 0x1 DUP2 ADD SWAP1 POP PUSH2 0x3158 JUMP JUMPDEST POP PUSH1 0x1 SWAP4 POP POP POP POP JUMPDEST SWAP5 SWAP4 POP POP POP POP JUMP JUMPDEST DUP3 DUP1 SLOAD DUP3 DUP3 SSTORE SWAP1 PUSH1 0x0 MSTORE PUSH1 0x20 PUSH1 0x0 KECCAK256 SWAP1 DUP2 ADD SWAP3 DUP3 ISZERO PUSH2 0x3227 JUMPI SWAP2 PUSH1 0x20 MUL DUP3 ADD JUMPDEST DUP3 DUP2 GT ISZERO PUSH2 0x3226 JUMPI DUP3 CALLDATALOAD DUP3 SSTORE SWAP2 PUSH1 0x20 ADD SWAP2 SWAP1 PUSH1 0x1 ADD SWAP1 PUSH2 0x320B JUMP JUMPDEST JUMPDEST POP SWAP1 POP PUSH2 0x3234 SWAP2 SWAP1 PUSH2 0x3259 JUMP JUMPDEST POP SWAP1 JUMP JUMPDEST POP DUP1 SLOAD PUSH1 0x0 DUP3 SSTORE SWAP1 PUSH1 0x0 MSTORE PUSH1 0x20 PUSH1 0x0 KECCAK256 SWAP1 DUP2 ADD SWAP1 PUSH2 0x3256 SWAP2 SWAP1 PUSH2 0x3259 JUMP JUMPDEST POP JUMP JUMPDEST PUSH2 0x327B SWAP2 SWAP1 JUMPDEST DUP1 DUP3 GT ISZERO PUSH2 0x3277 JUMPI PUSH1 0x0 DUP2 PUSH1 0x0 SWAP1 SSTORE POP PUSH1 0x1 ADD PUSH2 0x325F JUMP JUMPDEST POP SWAP1 JUMP JUMPDEST SWAP1 JUMP JUMPDEST PUSH1 0x0 DUP2 CALLDATALOAD SWAP1 POP PUSH2 0x328D DUP2 PUSH2 0x4823 JUMP JUMPDEST SWAP3 SWAP2 POP POP JUMP JUMPDEST PUSH1 0x0 DUP2 CALLDATALOAD SWAP1 POP PUSH2 0x32A2 DUP2 PUSH2 0x483A JUMP JUMPDEST SWAP3 SWAP2 POP POP JUMP JUMPDEST PUSH1 0x0 DUP1 DUP4 PUSH1 0x1F DUP5 ADD SLT PUSH2 0x32BA JUMPI PUSH1 0x0 DUP1 REVERT JUMPDEST DUP3 CALLDATALOAD SWAP1 POP PUSH8 0xFFFFFFFFFFFFFFFF DUP2 GT ISZERO PUSH2 0x32D3 JUMPI PUSH1 0x0 DUP1 REVERT JUMPDEST PUSH1 0x20 DUP4 ADD SWAP2 POP DUP4 PUSH1 0x20 DUP3 MUL DUP4 ADD GT ISZERO PUSH2 0x32EB JUMPI PUSH1 0x0 DUP1 REVERT JUMPDEST SWAP3 POP SWAP3 SWAP1 POP JUMP JUMPDEST PUSH1 0x0 DUP3 PUSH1 0x1F DUP4 ADD SLT PUSH2 0x3303 JUMPI PUSH1 0x0 DUP1 REVERT JUMPDEST DUP2 CALLDATALOAD PUSH2 0x3316 PUSH2 0x3311 DUP3 PUSH2 0x4641 JUMP JUMPDEST PUSH2 0x4614 JUMP JUMPDEST SWAP2 POP DUP2 DUP2 DUP4 MSTORE PUSH1 0x20 DUP5 ADD SWAP4 POP PUSH1 0x20 DUP2 ADD SWAP1 POP DUP4 DUP6 PUSH1 0x20 DUP5 MUL DUP3 ADD GT ISZERO PUSH2 0x333B JUMPI PUSH1 0x0 DUP1 REVERT JUMPDEST PUSH1 0x0 JUMPDEST DUP4 DUP2 LT ISZERO PUSH2 0x336B JUMPI DUP2 PUSH2 0x3351 DUP9 DUP3 PUSH2 0x338A JUMP JUMPDEST DUP5 MSTORE PUSH1 0x20 DUP5 ADD SWAP4 POP PUSH1 0x20 DUP4 ADD SWAP3 POP POP PUSH1 0x1 DUP2 ADD SWAP1 POP PUSH2 0x333E JUMP JUMPDEST POP POP POP POP SWAP3 SWAP2 POP POP JUMP JUMPDEST PUSH1 0x0 DUP2 MLOAD SWAP1 POP PUSH2 0x3384 DUP2 PUSH2 0x4851 JUMP JUMPDEST SWAP3 SWAP2 POP POP JUMP JUMPDEST PUSH1 0x0 DUP2 CALLDATALOAD SWAP1 POP PUSH2 0x3399 DUP2 PUSH2 0x4868 JUMP JUMPDEST SWAP3 SWAP2 POP POP JUMP JUMPDEST PUSH1 0x0 DUP2 CALLDATALOAD SWAP1 POP PUSH2 0x33AE DUP2 PUSH2 0x487F JUMP JUMPDEST SWAP3 SWAP2 POP POP JUMP JUMPDEST PUSH1 0x0 DUP2 CALLDATALOAD SWAP1 POP PUSH2 0x33C3 DUP2 PUSH2 0x4896 JUMP JUMPDEST SWAP3 SWAP2 POP POP JUMP JUMPDEST PUSH1 0x0 PUSH1 0x20 DUP3 DUP5 SUB SLT ISZERO PUSH2 0x33DB JUMPI PUSH1 0x0 DUP1 REVERT JUMPDEST PUSH1 0x0 PUSH2 0x33E9 DUP5 DUP3 DUP6 ADD PUSH2 0x3293 JUMP JUMPDEST SWAP2 POP POP SWAP3 SWAP2 POP POP JUMP JUMPDEST PUSH1 0x0 DUP1 PUSH1 0x20 DUP4 DUP6 SUB SLT ISZERO PUSH2 0x3405 JUMPI PUSH1 0x0 DUP1 REVERT JUMPDEST PUSH1 0x0 DUP4 ADD CALLDATALOAD PUSH8 0xFFFFFFFFFFFFFFFF DUP2 GT ISZERO PUSH2 0x341F JUMPI PUSH1 0x0 DUP1 REVERT JUMPDEST PUSH2 0x342B DUP6 DUP3 DUP7 ADD PUSH2 0x32A8 JUMP JUMPDEST SWAP3 POP SWAP3 POP POP SWAP3 POP SWAP3 SWAP1 POP JUMP JUMPDEST PUSH1 0x0 DUP1 PUSH1 0x0 DUP1 PUSH1 0x0 DUP1 PUSH1 0x0 DUP1 PUSH1 0xC0 DUP10 DUP12 SUB SLT ISZERO PUSH2 0x3453 JUMPI PUSH1 0x0 DUP1 REVERT JUMPDEST PUSH1 0x0 DUP10 ADD CALLDATALOAD PUSH8 0xFFFFFFFFFFFFFFFF DUP2 GT ISZERO PUSH2 0x346D JUMPI PUSH1 0x0 DUP1 REVERT JUMPDEST PUSH2 0x3479 DUP12 DUP3 DUP13 ADD PUSH2 0x32A8 JUMP JUMPDEST SWAP9 POP SWAP9 POP POP PUSH1 0x20 DUP10 ADD CALLDATALOAD PUSH8 0xFFFFFFFFFFFFFFFF DUP2 GT ISZERO PUSH2 0x3498 JUMPI PUSH1 0x0 DUP1 REVERT JUMPDEST PUSH2 0x34A4 DUP12 DUP3 DUP13 ADD PUSH2 0x32A8 JUMP JUMPDEST SWAP7 POP SWAP7 POP POP PUSH1 0x40 PUSH2 0x34B7 DUP12 DUP3 DUP13 ADD PUSH2 0x339F JUMP JUMPDEST SWAP5 POP POP PUSH1 0x60 PUSH2 0x34C8 DUP12 DUP3 DUP13 ADD PUSH2 0x33B4 JUMP JUMPDEST SWAP4 POP POP PUSH1 0x80 PUSH2 0x34D9 DUP12 DUP3 DUP13 ADD PUSH2 0x338A JUMP JUMPDEST SWAP3 POP POP PUSH1 0xA0 PUSH2 0x34EA DUP12 DUP3 DUP13 ADD PUSH2 0x338A JUMP JUMPDEST SWAP2 POP POP SWAP3 SWAP6 SWAP9 POP SWAP3 SWAP6 SWAP9 SWAP1 SWAP4 SWAP7 POP JUMP JUMPDEST PUSH1 0x0 DUP1 PUSH1 0x0 DUP1 PUSH1 0x0 DUP1 PUSH1 0x0 DUP1 PUSH1 0x0 DUP1 PUSH1 0xE0 DUP12 DUP14 SUB SLT ISZERO PUSH2 0x3519 JUMPI PUSH1 0x0 DUP1 REVERT JUMPDEST PUSH1 0x0 DUP12 ADD CALLDATALOAD PUSH8 0xFFFFFFFFFFFFFFFF DUP2 GT ISZERO PUSH2 0x3533 JUMPI PUSH1 0x0 DUP1 REVERT JUMPDEST PUSH2 0x353F DUP14 DUP3 DUP15 ADD PUSH2 0x32A8 JUMP JUMPDEST SWAP11 POP SWAP11 POP POP PUSH1 0x20 DUP12 ADD CALLDATALOAD PUSH8 0xFFFFFFFFFFFFFFFF DUP2 GT ISZERO PUSH2 0x355E JUMPI PUSH1 0x0 DUP1 REVERT JUMPDEST PUSH2 0x356A DUP14 DUP3 DUP15 ADD PUSH2 0x32A8 JUMP JUMPDEST SWAP9 POP SWAP9 POP POP PUSH1 0x40 PUSH2 0x357D DUP14 DUP3 DUP15 ADD PUSH2 0x339F JUMP JUMPDEST SWAP7 POP POP PUSH1 0x60 PUSH2 0x358E DUP14 DUP3 DUP15 ADD PUSH2 0x33B4 JUMP JUMPDEST SWAP6 POP POP PUSH1 0x80 PUSH2 0x359F DUP14 DUP3 DUP15 ADD PUSH2 0x338A JUMP JUMPDEST SWAP5 POP POP PUSH1 0xA0 PUSH2 0x35B0 DUP14 DUP3 DUP15 ADD PUSH2 0x338A JUMP JUMPDEST SWAP4 POP POP PUSH1 0xC0 DUP12 ADD CALLDATALOAD PUSH8 0xFFFFFFFFFFFFFFFF DUP2 GT ISZERO PUSH2 0x35CD JUMPI PUSH1 0x0 DUP1 REVERT JUMPDEST PUSH2 0x35D9 DUP14 DUP3 DUP15 ADD PUSH2 0x32A8 JUMP JUMPDEST SWAP3 POP SWAP3 POP POP SWAP3 SWAP6 SWAP9 SWAP12 SWAP2 SWAP5 SWAP8 SWAP11 POP SWAP3 SWAP6 SWAP9 POP JUMP JUMPDEST PUSH1 0x0 DUP1 PUSH1 0x0 DUP1 PUSH1 0x0 DUP1 PUSH1 0xA0 DUP8 DUP10 SUB SLT ISZERO PUSH2 0x3606 JUMPI PUSH1 0x0 DUP1 REVERT JUMPDEST PUSH1 0x0 DUP8 ADD CALLDATALOAD PUSH8 0xFFFFFFFFFFFFFFFF DUP2 GT ISZERO PUSH2 0x3620 JUMPI PUSH1 0x0 DUP1 REVERT JUMPDEST PUSH2 0x362C DUP10 DUP3 DUP11 ADD PUSH2 0x32A8 JUMP JUMPDEST SWAP7 POP SWAP7 POP POP PUSH1 0x20 PUSH2 0x363F DUP10 DUP3 DUP11 ADD PUSH2 0x339F JUMP JUMPDEST SWAP5 POP POP PUSH1 0x40 PUSH2 0x3650 DUP10 DUP3 DUP11 ADD PUSH2 0x33B4 JUMP JUMPDEST SWAP4 POP POP PUSH1 0x60 PUSH2 0x3661 DUP10 DUP3 DUP11 ADD PUSH2 0x338A JUMP JUMPDEST SWAP3 POP POP PUSH1 0x80 PUSH2 0x3672 DUP10 DUP3 DUP11 ADD PUSH2 0x338A JUMP JUMPDEST SWAP2 POP POP SWAP3 SWAP6 POP SWAP3 SWAP6 POP SWAP3 SWAP6 JUMP JUMPDEST PUSH1 0x0 PUSH1 0x20 DUP3 DUP5 SUB SLT ISZERO PUSH2 0x3691 JUMPI PUSH1 0x0 DUP1 REVERT JUMPDEST PUSH1 0x0 DUP3 ADD CALLDATALOAD PUSH8 0xFFFFFFFFFFFFFFFF DUP2 GT ISZERO PUSH2 0x36AB JUMPI PUSH1 0x0 DUP1 REVERT JUMPDEST PUSH2 0x36B7 DUP5 DUP3 DUP6 ADD PUSH2 0x32F2 JUMP JUMPDEST SWAP2 POP POP SWAP3 SWAP2 POP POP JUMP JUMPDEST PUSH1 0x0 DUP1 PUSH1 0x0 DUP1 PUSH1 0x0 DUP1 PUSH1 0xC0 DUP8 DUP10 SUB SLT ISZERO PUSH2 0x36D9 JUMPI PUSH1 0x0 DUP1 REVERT JUMPDEST PUSH1 0x0 DUP8 ADD CALLDATALOAD PUSH8 0xFFFFFFFFFFFFFFFF DUP2 GT ISZERO PUSH2 0x36F3 JUMPI PUSH1 0x0 DUP1 REVERT JUMPDEST PUSH2 0x36FF DUP10 DUP3 DUP11 ADD PUSH2 0x32F2 JUMP JUMPDEST SWAP7 POP POP PUSH1 0x20 DUP8 ADD CALLDATALOAD PUSH8 0xFFFFFFFFFFFFFFFF DUP2 GT ISZERO PUSH2 0x371C JUMPI PUSH1 0x0 DUP1 REVERT JUMPDEST PUSH2 0x3728 DUP10 DUP3 DUP11 ADD PUSH2 0x32F2 JUMP JUMPDEST SWAP6 POP POP PUSH1 0x40 PUSH2 0x3739 DUP10 DUP3 DUP11 ADD PUSH2 0x339F JUMP JUMPDEST SWAP5 POP POP PUSH1 0x60 PUSH2 0x374A DUP10 DUP3 DUP11 ADD PUSH2 0x33B4 JUMP JUMPDEST SWAP4 POP POP PUSH1 0x80 PUSH2 0x375B DUP10 DUP3 DUP11 ADD PUSH2 0x338A JUMP JUMPDEST SWAP3 POP POP PUSH1 0xA0 PUSH2 0x376C DUP10 DUP3 DUP11 ADD PUSH2 0x338A JUMP JUMPDEST SWAP2 POP POP SWAP3 SWAP6 POP SWAP3 SWAP6 POP SWAP3 SWAP6 JUMP JUMPDEST PUSH1 0x0 DUP1 PUSH1 0x0 DUP1 PUSH1 0x0 DUP1 PUSH1 0xC0 DUP8 DUP10 SUB SLT ISZERO PUSH2 0x3792 JUMPI PUSH1 0x0 DUP1 REVERT JUMPDEST PUSH1 0x0 DUP8 ADD CALLDATALOAD PUSH8 0xFFFFFFFFFFFFFFFF DUP2 GT ISZERO PUSH2 0x37AC JUMPI PUSH1 0x0 DUP1 REVERT JUMPDEST PUSH2 0x37B8 DUP10 DUP3 DUP11 ADD PUSH2 0x32F2 JUMP JUMPDEST SWAP7 POP POP PUSH1 0x20 PUSH2 0x37C9 DUP10 DUP3 DUP11 ADD PUSH2 0x339F JUMP JUMPDEST SWAP6 POP POP PUSH1 0x40 PUSH2 0x37DA DUP10 DUP3 DUP11 ADD PUSH2 0x33B4 JUMP JUMPDEST SWAP5 POP POP PUSH1 0x60 PUSH2 0x37EB DUP10 DUP3 DUP11 ADD PUSH2 0x338A JUMP JUMPDEST SWAP4 POP POP PUSH1 0x80 PUSH2 0x37FC DUP10 DUP3 DUP11 ADD PUSH2 0x338A JUMP JUMPDEST SWAP3 POP POP PUSH1 0xA0 PUSH2 0x380D DUP10 DUP3 DUP11 ADD PUSH2 0x327E JUMP JUMPDEST SWAP2 POP POP SWAP3 SWAP6 POP SWAP3 SWAP6 POP SWAP3 SWAP6 JUMP JUMPDEST PUSH1 0x0 PUSH1 0x20 DUP3 DUP5 SUB SLT ISZERO PUSH2 0x382C JUMPI PUSH1 0x0 DUP1 REVERT JUMPDEST PUSH1 0x0 PUSH2 0x383A DUP5 DUP3 DUP6 ADD PUSH2 0x3375 JUMP JUMPDEST SWAP2 POP POP SWAP3 SWAP2 POP POP JUMP JUMPDEST PUSH1 0x0 PUSH2 0x384F DUP4 DUP4 PUSH2 0x3A30 JUMP JUMPDEST PUSH1 0x20 DUP4 ADD SWAP1 POP SWAP3 SWAP2 POP POP JUMP JUMPDEST PUSH1 0x0 PUSH2 0x3867 DUP4 DUP4 PUSH2 0x3A4E JUMP JUMPDEST PUSH1 0x20 DUP4 ADD SWAP1 POP SWAP3 SWAP2 POP POP JUMP JUMPDEST PUSH2 0x387C DUP2 PUSH2 0x4712 JUMP JUMPDEST DUP3 MSTORE POP POP JUMP JUMPDEST PUSH2 0x3893 PUSH2 0x388E DUP3 PUSH2 0x4712 JUMP JUMPDEST PUSH2 0x47BE JUMP JUMPDEST DUP3 MSTORE POP POP JUMP JUMPDEST PUSH2 0x38A2 DUP2 PUSH2 0x4700 JUMP JUMPDEST DUP3 MSTORE POP POP JUMP JUMPDEST PUSH1 0x0 PUSH2 0x38B4 DUP4 DUP6 PUSH2 0x46BE JUMP JUMPDEST SWAP4 POP PUSH32 0x7FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF DUP4 GT ISZERO PUSH2 0x38E3 JUMPI PUSH1 0x0 DUP1 REVERT JUMPDEST PUSH1 0x20 DUP4 MUL SWAP3 POP PUSH2 0x38F4 DUP4 DUP6 DUP5 PUSH2 0x4795 JUMP JUMPDEST DUP3 DUP5 ADD SWAP1 POP SWAP4 SWAP3 POP POP POP JUMP JUMPDEST PUSH1 0x0 PUSH2 0x390B DUP3 PUSH2 0x468E JUMP JUMPDEST PUSH2 0x3915 DUP2 DUP6 PUSH2 0x46BE JUMP JUMPDEST SWAP4 POP PUSH2 0x3920 DUP4 PUSH2 0x4669 JUMP JUMPDEST DUP1 PUSH1 0x0 JUMPDEST DUP4 DUP2 LT ISZERO PUSH2 0x3951 JUMPI DUP2 MLOAD PUSH2 0x3938 DUP9 DUP3 PUSH2 0x3843 JUMP JUMPDEST SWAP8 POP PUSH2 0x3943 DUP4 PUSH2 0x46A4 JUMP JUMPDEST SWAP3 POP POP PUSH1 0x1 DUP2 ADD SWAP1 POP PUSH2 0x3924 JUMP JUMPDEST POP DUP6 SWAP4 POP POP POP POP SWAP3 SWAP2 POP POP JUMP JUMPDEST PUSH1 0x0 PUSH2 0x3969 DUP3 PUSH2 0x468E JUMP JUMPDEST PUSH2 0x3973 DUP2 DUP6 PUSH2 0x46CF JUMP JUMPDEST SWAP4 POP PUSH2 0x397E DUP4 PUSH2 0x4669 JUMP JUMPDEST DUP1 PUSH1 0x0 JUMPDEST DUP4 DUP2 LT ISZERO PUSH2 0x39AF JUMPI DUP2 MLOAD PUSH2 0x3996 DUP9 DUP3 PUSH2 0x385B JUMP JUMPDEST SWAP8 POP PUSH2 0x39A1 DUP4 PUSH2 0x46A4 JUMP JUMPDEST SWAP3 POP POP PUSH1 0x1 DUP2 ADD SWAP1 POP PUSH2 0x3982 JUMP JUMPDEST POP DUP6 SWAP4 POP POP POP POP SWAP3 SWAP2 POP POP JUMP JUMPDEST PUSH1 0x0 PUSH2 0x39C7 DUP3 PUSH2 0x4699 JUMP JUMPDEST PUSH2 0x39D1 DUP2 DUP6 PUSH2 0x46BE JUMP JUMPDEST SWAP4 POP PUSH2 0x39DC DUP4 PUSH2 0x4679 JUMP JUMPDEST DUP1 PUSH1 0x0 JUMPDEST DUP4 DUP2 LT ISZERO PUSH2 0x3A14 JUMPI PUSH2 0x39F1 DUP3 PUSH2 0x47F6 JUMP JUMPDEST PUSH2 0x39FB DUP9 DUP3 PUSH2 0x3843 JUMP JUMPDEST SWAP8 POP PUSH2 0x3A06 DUP4 PUSH2 0x46B1 JUMP JUMPDEST SWAP3 POP POP PUSH1 0x1 DUP2 ADD SWAP1 POP PUSH2 0x39E0 JUMP JUMPDEST POP DUP6 SWAP4 POP POP POP POP SWAP3 SWAP2 POP POP JUMP JUMPDEST PUSH2 0x3A2A DUP2 PUSH2 0x4724 JUMP JUMPDEST DUP3 MSTORE POP POP JUMP JUMPDEST PUSH2 0x3A39 DUP2 PUSH2 0x4730 JUMP JUMPDEST DUP3 MSTORE POP POP JUMP JUMPDEST PUSH2 0x3A48 DUP2 PUSH2 0x4730 JUMP JUMPDEST DUP3 MSTORE POP POP JUMP JUMPDEST PUSH2 0x3A57 DUP2 PUSH2 0x4730 JUMP JUMPDEST DUP3 MSTORE POP POP JUMP JUMPDEST PUSH2 0x3A6E PUSH2 0x3A69 DUP3 PUSH2 0x4730 JUMP JUMPDEST PUSH2 0x47D0 JUMP JUMPDEST DUP3 MSTORE POP POP JUMP JUMPDEST PUSH2 0x3A7D DUP2 PUSH2 0x4771 JUMP JUMPDEST DUP3 MSTORE POP POP JUMP JUMPDEST PUSH1 0x0 PUSH2 0x3A90 PUSH1 0x1C DUP4 PUSH2 0x46EB JUMP JUMPDEST SWAP2 POP PUSH32 0x19457468657265756D205369676E6564204D6573736167653A0A333200000000 PUSH1 0x0 DUP4 ADD MSTORE PUSH1 0x1C DUP3 ADD SWAP1 POP SWAP2 SWAP1 POP JUMP JUMPDEST PUSH1 0x0 PUSH2 0x3AD0 PUSH1 0x2F DUP4 PUSH2 0x46DA JUMP JUMPDEST SWAP2 POP PUSH32 0x5175657374696F6E206973206E6F7420696E2074686520616E73776572656420 PUSH1 0x0 DUP4 ADD MSTORE PUSH32 0x6861736865732070726F76696465640000000000000000000000000000000000 PUSH1 0x20 DUP4 ADD MSTORE PUSH1 0x40 DUP3 ADD SWAP1 POP SWAP2 SWAP1 POP JUMP JUMPDEST PUSH1 0x0 PUSH2 0x3B36 PUSH1 0x39 DUP4 PUSH2 0x46DA JUMP JUMPDEST SWAP2 POP PUSH32 0x43616E27742061707065616C206F6E206C65737320616E737765726564207175 PUSH1 0x0 DUP4 ADD MSTORE PUSH32 0x657374696F6E73207468616E2073686F776E206265666F726500000000000000 PUSH1 0x20 DUP4 ADD MSTORE PUSH1 0x40 DUP3 ADD SWAP1 POP SWAP2 SWAP1 POP JUMP JUMPDEST PUSH1 0x0 PUSH2 0x3B9C PUSH1 0xF DUP4 PUSH2 0x46DA JUMP JUMPDEST SWAP2 POP PUSH32 0x436F756C646E27742061707065616C0000000000000000000000000000000000 PUSH1 0x0 DUP4 ADD MSTORE PUSH1 0x20 DUP3 ADD SWAP1 POP SWAP2 SWAP1 POP JUMP JUMPDEST PUSH1 0x0 PUSH2 0x3BDC PUSH1 0x19 DUP4 PUSH2 0x46DA JUMP JUMPDEST SWAP2 POP PUSH32 0x5175657374696F6E2073686F756C642062652076616C69642E00000000000000 PUSH1 0x0 DUP4 ADD MSTORE PUSH1 0x20 DUP3 ADD SWAP1 POP SWAP2 SWAP1 POP JUMP JUMPDEST PUSH1 0x0 PUSH2 0x3C1C PUSH1 0x1F DUP4 PUSH2 0x46DA JUMP JUMPDEST SWAP2 POP PUSH32 0x48617368657320617265206E6F74207369676E656420636F72726563746C7900 PUSH1 0x0 DUP4 ADD MSTORE PUSH1 0x20 DUP3 ADD SWAP1 POP SWAP2 SWAP1 POP JUMP JUMPDEST PUSH1 0x0 PUSH2 0x3C5C PUSH1 0x31 DUP4 PUSH2 0x46DA JUMP JUMPDEST SWAP2 POP PUSH32 0x5175657374696F6E206973206E6F7420696E2074686520756E616E7377657265 PUSH1 0x0 DUP4 ADD MSTORE PUSH32 0x64206861736865732070726F7669646564000000000000000000000000000000 PUSH1 0x20 DUP4 ADD MSTORE PUSH1 0x40 DUP3 ADD SWAP1 POP SWAP2 SWAP1 POP JUMP JUMPDEST PUSH1 0x0 PUSH2 0x3CC2 PUSH1 0x1D DUP4 PUSH2 0x46DA JUMP JUMPDEST SWAP2 POP PUSH32 0x416E737765722073686F756C64206D61746368207175657374696F6E2E000000 PUSH1 0x0 DUP4 ADD MSTORE PUSH1 0x20 DUP3 ADD SWAP1 POP SWAP2 SWAP1 POP JUMP JUMPDEST PUSH1 0x0 PUSH2 0x3D02 PUSH1 0x2F DUP4 PUSH2 0x46DA JUMP JUMPDEST SWAP2 POP PUSH32 0x7175657374696F6E2061707065616C6564206D75737420626520696E20756E61 PUSH1 0x0 DUP4 ADD MSTORE PUSH32 0x6E73776572656420686173686573730000000000000000000000000000000000 PUSH1 0x20 DUP4 ADD MSTORE PUSH1 0x40 DUP3 ADD SWAP1 POP SWAP2 SWAP1 POP JUMP JUMPDEST PUSH1 0x0 PUSH2 0x3D68 PUSH1 0x2A DUP4 PUSH2 0x46DA JUMP JUMPDEST SWAP2 POP PUSH32 0x43616E27742070726F76696465206F6C646572206F7220646966666572656E74 PUSH1 0x0 DUP4 ADD MSTORE PUSH32 0x207369676E617475726500000000000000000000000000000000000000000000 PUSH1 0x20 DUP4 ADD MSTORE PUSH1 0x40 DUP3 ADD SWAP1 POP SWAP2 SWAP1 POP JUMP JUMPDEST PUSH1 0x0 PUSH2 0x3DCE PUSH1 0x2C DUP4 PUSH2 0x46DA JUMP JUMPDEST SWAP2 POP PUSH32 0x43616E27742075736520746869732066756E6374696F6E207768696C65206E6F PUSH1 0x0 DUP4 ADD MSTORE PUSH32 0x742061707065616C696E672E0000000000000000000000000000000000000000 PUSH1 0x20 DUP4 ADD MSTORE PUSH1 0x40 DUP3 ADD SWAP1 POP SWAP2 SWAP1 POP JUMP JUMPDEST PUSH1 0x0 PUSH2 0x3E34 PUSH1 0x28 DUP4 PUSH2 0x46DA JUMP JUMPDEST SWAP2 POP PUSH32 0x43616E27742075736520746869732066756E6374696F6E207768696C65206170 PUSH1 0x0 DUP4 ADD MSTORE PUSH32 0x7065616C696E672E000000000000000000000000000000000000000000000000 PUSH1 0x20 DUP4 ADD MSTORE PUSH1 0x40 DUP3 ADD SWAP1 POP SWAP2 SWAP1 POP JUMP JUMPDEST PUSH1 0x0 PUSH2 0x3E9A PUSH1 0x24 DUP4 PUSH2 0x46DA JUMP JUMPDEST SWAP2 POP PUSH32 0x43616E27742075736520746869732066756E6374696F6E207768656E20616374 PUSH1 0x0 DUP4 ADD MSTORE PUSH32 0x6976652E00000000000000000000000000000000000000000000000000000000 PUSH1 0x20 DUP4 ADD MSTORE PUSH1 0x40 DUP3 ADD SWAP1 POP SWAP2 SWAP1 POP JUMP JUMPDEST PUSH1 0x0 PUSH2 0x3F00 PUSH1 0x25 DUP4 PUSH2 0x46DA JUMP JUMPDEST SWAP2 POP PUSH32 0x4F6E6C7920616E206F776E65722063616E2063616C6C20746869732066756E63 PUSH1 0x0 DUP4 ADD MSTORE PUSH32 0x74696F6E2E000000000000000000000000000000000000000000000000000000 PUSH1 0x20 DUP4 ADD MSTORE PUSH1 0x40 DUP3 ADD SWAP1 POP SWAP2 SWAP1 POP JUMP JUMPDEST PUSH1 0x0 PUSH2 0x3F66 PUSH1 0x29 DUP4 PUSH2 0x46DA JUMP JUMPDEST SWAP2 POP PUSH32 0x4F6E6C792074686520636F7374756D65722063616E2063616C6C207468697320 PUSH1 0x0 DUP4 ADD MSTORE PUSH32 0x66756E6374696F6E2E0000000000000000000000000000000000000000000000 PUSH1 0x20 DUP4 ADD MSTORE PUSH1 0x40 DUP3 ADD SWAP1 POP SWAP2 SWAP1 POP JUMP JUMPDEST PUSH1 0x0 PUSH2 0x3FCC PUSH1 0x17 DUP4 PUSH2 0x46DA JUMP JUMPDEST SWAP2 POP PUSH32 0x6469646E74207265616368206D61782071756572696573000000000000000000 PUSH1 0x0 DUP4 ADD MSTORE PUSH1 0x20 DUP3 ADD SWAP1 POP SWAP2 SWAP1 POP JUMP JUMPDEST PUSH1 0x0 PUSH2 0x400C PUSH1 0x1C DUP4 PUSH2 0x46DA JUMP JUMPDEST SWAP2 POP PUSH32 0x6469736D6973732077697468206F6C646572207369676E617475726500000000 PUSH1 0x0 DUP4 ADD MSTORE PUSH1 0x20 DUP3 ADD SWAP1 POP SWAP2 SWAP1 POP JUMP JUMPDEST PUSH1 0x0 PUSH2 0x404C PUSH1 0x28 DUP4 PUSH2 0x46DA JUMP JUMPDEST SWAP2 POP PUSH32 0x43616E27742075736520746869732066756E6374696F6E207768656E206E6F74 PUSH1 0x0 DUP4 ADD MSTORE PUSH32 0x206163746976652E000000000000000000000000000000000000000000000000 PUSH1 0x20 DUP4 ADD MSTORE PUSH1 0x40 DUP3 ADD SWAP1 POP SWAP2 SWAP1 POP JUMP JUMPDEST PUSH1 0x0 PUSH2 0x40B2 PUSH1 0x28 DUP4 PUSH2 0x46DA JUMP JUMPDEST SWAP2 POP PUSH32 0x43616E27742075736520746869732066756E6374696F6E207768696C65206465 PUSH1 0x0 DUP4 ADD MSTORE PUSH32 0x6D616E64696E672E000000000000000000000000000000000000000000000000 PUSH1 0x20 DUP4 ADD MSTORE PUSH1 0x40 DUP3 ADD SWAP1 POP SWAP2 SWAP1 POP JUMP JUMPDEST PUSH1 0x0 PUSH2 0x4118 PUSH1 0x2C DUP4 PUSH2 0x46DA JUMP JUMPDEST SWAP2 POP PUSH32 0x43616E27742075736520746869732066756E6374696F6E207768696C65206E6F PUSH1 0x0 DUP4 ADD MSTORE PUSH32 0x742064656D616E64696E672E0000000000000000000000000000000000000000 PUSH1 0x20 DUP4 ADD MSTORE PUSH1 0x40 DUP3 ADD SWAP1 POP SWAP2 SWAP1 POP JUMP JUMPDEST PUSH2 0x417A DUP2 PUSH2 0x475A JUMP JUMPDEST DUP3 MSTORE POP POP JUMP JUMPDEST PUSH2 0x4191 PUSH2 0x418C DUP3 PUSH2 0x475A JUMP JUMPDEST PUSH2 0x47EC JUMP JUMPDEST DUP3 MSTORE POP POP JUMP JUMPDEST PUSH2 0x41A0 DUP2 PUSH2 0x4764 JUMP JUMPDEST DUP3 MSTORE POP POP JUMP JUMPDEST PUSH1 0x0 PUSH2 0x41B2 DUP3 DUP5 PUSH2 0x395E JUMP JUMPDEST SWAP2 POP DUP2 SWAP1 POP SWAP3 SWAP2 POP POP JUMP JUMPDEST PUSH1 0x0 PUSH2 0x41C9 DUP3 DUP7 PUSH2 0x395E JUMP JUMPDEST SWAP2 POP PUSH2 0x41D5 DUP3 DUP6 PUSH2 0x4180 JUMP JUMPDEST PUSH1 0x20 DUP3 ADD SWAP2 POP PUSH2 0x41E5 DUP3 DUP5 PUSH2 0x3882 JUMP JUMPDEST PUSH1 0x14 DUP3 ADD SWAP2 POP DUP2 SWAP1 POP SWAP5 SWAP4 POP POP POP POP JUMP JUMPDEST PUSH1 0x0 PUSH2 0x4201 DUP3 PUSH2 0x3A83 JUMP JUMPDEST SWAP2 POP PUSH2 0x420D DUP3 DUP5 PUSH2 0x3A5D JUMP JUMPDEST PUSH1 0x20 DUP3 ADD SWAP2 POP DUP2 SWAP1 POP SWAP3 SWAP2 POP POP JUMP JUMPDEST PUSH1 0x0 PUSH1 0x20 DUP3 ADD SWAP1 POP PUSH2 0x4231 PUSH1 0x0 DUP4 ADD DUP5 PUSH2 0x3899 JUMP JUMPDEST SWAP3 SWAP2 POP POP JUMP JUMPDEST PUSH1 0x0 PUSH1 0x20 DUP3 ADD SWAP1 POP PUSH2 0x424C PUSH1 0x0 DUP4 ADD DUP5 PUSH2 0x3873 JUMP JUMPDEST SWAP3 SWAP2 POP POP JUMP JUMPDEST PUSH1 0x0 PUSH1 0x40 DUP3 ADD SWAP1 POP DUP2 DUP2 SUB PUSH1 0x0 DUP4 ADD MSTORE PUSH2 0x426D DUP2 DUP7 DUP9 PUSH2 0x38A8 JUMP JUMPDEST SWAP1 POP DUP2 DUP2 SUB PUSH1 0x20 DUP4 ADD MSTORE PUSH2 0x4282 DUP2 DUP5 DUP7 PUSH2 0x38A8 JUMP JUMPDEST SWAP1 POP SWAP6 SWAP5 POP POP POP POP POP JUMP JUMPDEST PUSH1 0x0 PUSH1 0x20 DUP3 ADD SWAP1 POP DUP2 DUP2 SUB PUSH1 0x0 DUP4 ADD MSTORE PUSH2 0x42A7 DUP2 DUP5 PUSH2 0x3900 JUMP JUMPDEST SWAP1 POP SWAP3 SWAP2 POP POP JUMP JUMPDEST PUSH1 0x0 PUSH1 0x40 DUP3 ADD SWAP1 POP DUP2 DUP2 SUB PUSH1 0x0 DUP4 ADD MSTORE PUSH2 0x42C9 DUP2 DUP7 PUSH2 0x39BC JUMP JUMPDEST SWAP1 POP DUP2 DUP2 SUB PUSH1 0x20 DUP4 ADD MSTORE PUSH2 0x42DE DUP2 DUP5 DUP7 PUSH2 0x38A8 JUMP JUMPDEST SWAP1 POP SWAP5 SWAP4 POP POP POP POP JUMP JUMPDEST PUSH1 0x0 PUSH1 0x20 DUP3 ADD SWAP1 POP PUSH2 0x42FD PUSH1 0x0 DUP4 ADD DUP5 PUSH2 0x3A21 JUMP JUMPDEST SWAP3 SWAP2 POP POP JUMP JUMPDEST PUSH1 0x0 PUSH1 0x20 DUP3 ADD SWAP1 POP PUSH2 0x4318 PUSH1 0x0 DUP4 ADD DUP5 PUSH2 0x3A3F JUMP JUMPDEST SWAP3 SWAP2 POP POP JUMP JUMPDEST PUSH1 0x0 PUSH1 0x80 DUP3 ADD SWAP1 POP PUSH2 0x4333 PUSH1 0x0 DUP4 ADD DUP8 PUSH2 0x3A3F JUMP JUMPDEST PUSH2 0x4340 PUSH1 0x20 DUP4 ADD DUP7 PUSH2 0x4197 JUMP JUMPDEST PUSH2 0x434D PUSH1 0x40 DUP4 ADD DUP6 PUSH2 0x3A3F JUMP JUMPDEST PUSH2 0x435A PUSH1 0x60 DUP4 ADD DUP5 PUSH2 0x3A3F JUMP JUMPDEST SWAP6 SWAP5 POP POP POP POP POP JUMP JUMPDEST PUSH1 0x0 PUSH1 0x20 DUP3 ADD SWAP1 POP PUSH2 0x4378 PUSH1 0x0 DUP4 ADD DUP5 PUSH2 0x3A74 JUMP JUMPDEST SWAP3 SWAP2 POP POP JUMP JUMPDEST PUSH1 0x0 PUSH1 0x20 DUP3 ADD SWAP1 POP DUP2 DUP2 SUB PUSH1 0x0 DUP4 ADD MSTORE PUSH2 0x4397 DUP2 PUSH2 0x3AC3 JUMP JUMPDEST SWAP1 POP SWAP2 SWAP1 POP JUMP JUMPDEST PUSH1 0x0 PUSH1 0x20 DUP3 ADD SWAP1 POP DUP2 DUP2 SUB PUSH1 0x0 DUP4 ADD MSTORE PUSH2 0x43B7 DUP2 PUSH2 0x3B29 JUMP JUMPDEST SWAP1 POP SWAP2 SWAP1 POP JUMP JUMPDEST PUSH1 0x0 PUSH1 0x20 DUP3 ADD SWAP1 POP DUP2 DUP2 SUB PUSH1 0x0 DUP4 ADD MSTORE PUSH2 0x43D7 DUP2 PUSH2 0x3B8F JUMP JUMPDEST SWAP1 POP SWAP2 SWAP1 POP JUMP JUMPDEST PUSH1 0x0 PUSH1 0x20 DUP3 ADD SWAP1 POP DUP2 DUP2 SUB PUSH1 0x0 DUP4 ADD MSTORE PUSH2 0x43F7 DUP2 PUSH2 0x3BCF JUMP JUMPDEST SWAP1 POP SWAP2 SWAP1 POP JUMP JUMPDEST PUSH1 0x0 PUSH1 0x20 DUP3 ADD SWAP1 POP DUP2 DUP2 SUB PUSH1 0x0 DUP4 ADD MSTORE PUSH2 0x4417 DUP2 PUSH2 0x3C0F JUMP JUMPDEST SWAP1 POP SWAP2 SWAP1 POP JUMP JUMPDEST PUSH1 0x0 PUSH1 0x20 DUP3 ADD SWAP1 POP DUP2 DUP2 SUB PUSH1 0x0 DUP4 ADD MSTORE PUSH2 0x4437 DUP2 PUSH2 0x3C4F JUMP JUMPDEST SWAP1 POP SWAP2 SWAP1 POP JUMP JUMPDEST PUSH1 0x0 PUSH1 0x20 DUP3 ADD SWAP1 POP DUP2 DUP2 SUB PUSH1 0x0 DUP4 ADD MSTORE PUSH2 0x4457 DUP2 PUSH2 0x3CB5 JUMP JUMPDEST SWAP1 POP SWAP2 SWAP1 POP JUMP JUMPDEST PUSH1 0x0 PUSH1 0x20 DUP3 ADD SWAP1 POP DUP2 DUP2 SUB PUSH1 0x0 DUP4 ADD MSTORE PUSH2 0x4477 DUP2 PUSH2 0x3CF5 JUMP JUMPDEST SWAP1 POP SWAP2 SWAP1 POP JUMP JUMPDEST PUSH1 0x0 PUSH1 0x20 DUP3 ADD SWAP1 POP DUP2 DUP2 SUB PUSH1 0x0 DUP4 ADD MSTORE PUSH2 0x4497 DUP2 PUSH2 0x3D5B JUMP JUMPDEST SWAP1 POP SWAP2 SWAP1 POP JUMP JUMPDEST PUSH1 0x0 PUSH1 0x20 DUP3 ADD SWAP1 POP DUP2 DUP2 SUB PUSH1 0x0 DUP4 ADD MSTORE PUSH2 0x44B7 DUP2 PUSH2 0x3DC1 JUMP JUMPDEST SWAP1 POP SWAP2 SWAP1 POP JUMP JUMPDEST PUSH1 0x0 PUSH1 0x20 DUP3 ADD SWAP1 POP DUP2 DUP2 SUB PUSH1 0x0 DUP4 ADD MSTORE PUSH2 0x44D7 DUP2 PUSH2 0x3E27 JUMP JUMPDEST SWAP1 POP SWAP2 SWAP1 POP JUMP JUMPDEST PUSH1 0x0 PUSH1 0x20 DUP3 ADD SWAP1 POP DUP2 DUP2 SUB PUSH1 0x0 DUP4 ADD MSTORE PUSH2 0x44F7 DUP2 PUSH2 0x3E8D JUMP JUMPDEST SWAP1 POP SWAP2 SWAP1 POP JUMP JUMPDEST PUSH1 0x0 PUSH1 0x20 DUP3 ADD SWAP1 POP DUP2 DUP2 SUB PUSH1 0x0 DUP4 ADD MSTORE PUSH2 0x4517 DUP2 PUSH2 0x3EF3 JUMP JUMPDEST SWAP1 POP SWAP2 SWAP1 POP JUMP JUMPDEST PUSH1 0x0 PUSH1 0x20 DUP3 ADD SWAP1 POP DUP2 DUP2 SUB PUSH1 0x0 DUP4 ADD MSTORE PUSH2 0x4537 DUP2 PUSH2 0x3F59 JUMP JUMPDEST SWAP1 POP SWAP2 SWAP1 POP JUMP JUMPDEST PUSH1 0x0 PUSH1 0x20 DUP3 ADD SWAP1 POP DUP2 DUP2 SUB PUSH1 0x0 DUP4 ADD MSTORE PUSH2 0x4557 DUP2 PUSH2 0x3FBF JUMP JUMPDEST SWAP1 POP SWAP2 SWAP1 POP JUMP JUMPDEST PUSH1 0x0 PUSH1 0x20 DUP3 ADD SWAP1 POP DUP2 DUP2 SUB PUSH1 0x0 DUP4 ADD MSTORE PUSH2 0x4577 DUP2 PUSH2 0x3FFF JUMP JUMPDEST SWAP1 POP SWAP2 SWAP1 POP JUMP JUMPDEST PUSH1 0x0 PUSH1 0x20 DUP3 ADD SWAP1 POP DUP2 DUP2 SUB PUSH1 0x0 DUP4 ADD MSTORE PUSH2 0x4597 DUP2 PUSH2 0x403F JUMP JUMPDEST SWAP1 POP SWAP2 SWAP1 POP JUMP JUMPDEST PUSH1 0x0 PUSH1 0x20 DUP3 ADD SWAP1 POP DUP2 DUP2 SUB PUSH1 0x0 DUP4 ADD MSTORE PUSH2 0x45B7 DUP2 PUSH2 0x40A5 JUMP JUMPDEST SWAP1 POP SWAP2 SWAP1 POP JUMP JUMPDEST PUSH1 0x0 PUSH1 0x20 DUP3 ADD SWAP1 POP DUP2 DUP2 SUB PUSH1 0x0 DUP4 ADD MSTORE PUSH2 0x45D7 DUP2 PUSH2 0x410B JUMP JUMPDEST SWAP1 POP SWAP2 SWAP1 POP JUMP JUMPDEST PUSH1 0x0 PUSH1 0x20 DUP3 ADD SWAP1 POP PUSH2 0x45F3 PUSH1 0x0 DUP4 ADD DUP5 PUSH2 0x4171 JUMP JUMPDEST SWAP3 SWAP2 POP POP JUMP JUMPDEST PUSH1 0x0 PUSH1 0x20 DUP3 ADD SWAP1 POP PUSH2 0x460E PUSH1 0x0 DUP4 ADD DUP5 PUSH2 0x4197 JUMP JUMPDEST SWAP3 SWAP2 POP POP JUMP JUMPDEST PUSH1 0x0 PUSH1 0x40 MLOAD SWAP1 POP DUP2 DUP2 ADD DUP2 DUP2 LT PUSH8 0xFFFFFFFFFFFFFFFF DUP3 GT OR ISZERO PUSH2 0x4637 JUMPI PUSH1 0x0 DUP1 REVERT JUMPDEST DUP1 PUSH1 0x40 MSTORE POP SWAP2 SWAP1 POP JUMP JUMPDEST PUSH1 0x0 PUSH8 0xFFFFFFFFFFFFFFFF DUP3 GT ISZERO PUSH2 0x4658 JUMPI PUSH1 0x0 DUP1 REVERT JUMPDEST PUSH1 0x20 DUP3 MUL SWAP1 POP PUSH1 0x20 DUP2 ADD SWAP1 POP SWAP2 SWAP1 POP JUMP JUMPDEST PUSH1 0x0 DUP2 SWAP1 POP PUSH1 0x20 DUP3 ADD SWAP1 POP SWAP2 SWAP1 POP JUMP JUMPDEST PUSH1 0x0 DUP2 SWAP1 POP DUP2 PUSH1 0x0 MSTORE PUSH1 0x20 PUSH1 0x0 KECCAK256 SWAP1 POP SWAP2 SWAP1 POP JUMP JUMPDEST PUSH1 0x0 DUP2 MLOAD SWAP1 POP SWAP2 SWAP1 POP JUMP JUMPDEST PUSH1 0x0 DUP2 SLOAD SWAP1 POP SWAP2 SWAP1 POP JUMP JUMPDEST PUSH1 0x0 PUSH1 0x20 DUP3 ADD SWAP1 POP SWAP2 SWAP1 POP JUMP JUMPDEST PUSH1 0x0 PUSH1 0x1 DUP3 ADD SWAP1 POP SWAP2 SWAP1 POP JUMP JUMPDEST PUSH1 0x0 DUP3 DUP3 MSTORE PUSH1 0x20 DUP3 ADD SWAP1 POP SWAP3 SWAP2 POP POP JUMP JUMPDEST PUSH1 0x0 DUP2 SWAP1 POP SWAP3 SWAP2 POP POP JUMP JUMPDEST PUSH1 0x0 DUP3 DUP3 MSTORE PUSH1 0x20 DUP3 ADD SWAP1 POP SWAP3 SWAP2 POP POP JUMP JUMPDEST PUSH1 0x0 DUP2 SWAP1 POP SWAP3 SWAP2 POP POP JUMP JUMPDEST PUSH1 0x0 DUP2 SWAP1 POP SWAP2 SWAP1 POP JUMP JUMPDEST PUSH1 0x0 PUSH2 0x470B DUP3 PUSH2 0x473A JUMP JUMPDEST SWAP1 POP SWAP2 SWAP1 POP JUMP JUMPDEST PUSH1 0x0 PUSH2 0x471D DUP3 PUSH2 0x473A JUMP JUMPDEST SWAP1 POP SWAP2 SWAP1 POP JUMP JUMPDEST PUSH1 0x0 DUP2 ISZERO ISZERO SWAP1 POP SWAP2 SWAP1 POP JUMP JUMPDEST PUSH1 0x0 DUP2 SWAP1 POP SWAP2 SWAP1 POP JUMP JUMPDEST PUSH1 0x0 PUSH20 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF DUP3 AND SWAP1 POP SWAP2 SWAP1 POP JUMP JUMPDEST PUSH1 0x0 DUP2 SWAP1 POP SWAP2 SWAP1 POP JUMP JUMPDEST PUSH1 0x0 PUSH1 0xFF DUP3 AND SWAP1 POP SWAP2 SWAP1 POP JUMP JUMPDEST PUSH1 0x0 PUSH2 0x477C DUP3 PUSH2 0x4783 JUMP JUMPDEST SWAP1 POP SWAP2 SWAP1 POP JUMP JUMPDEST PUSH1 0x0 PUSH2 0x478E DUP3 PUSH2 0x473A JUMP JUMPDEST SWAP1 POP SWAP2 SWAP1 POP JUMP JUMPDEST DUP3 DUP2 DUP4 CALLDATACOPY PUSH1 0x0 DUP4 DUP4 ADD MSTORE POP POP POP JUMP JUMPDEST PUSH1 0x0 PUSH2 0x47B7 PUSH2 0x47B2 DUP4 PUSH2 0x4816 JUMP JUMPDEST PUSH2 0x46F6 JUMP JUMPDEST SWAP1 POP SWAP2 SWAP1 POP JUMP JUMPDEST PUSH1 0x0 PUSH2 0x47C9 DUP3 PUSH2 0x47DA JUMP JUMPDEST SWAP1 POP SWAP2 SWAP1 POP JUMP JUMPDEST PUSH1 0x0 DUP2 SWAP1 POP SWAP2 SWAP1 POP JUMP JUMPDEST PUSH1 0x0 PUSH2 0x47E5 DUP3 PUSH2 0x4809 JUMP JUMPDEST SWAP1 POP SWAP2 SWAP1 POP JUMP JUMPDEST PUSH1 0x0 DUP2 SWAP1 POP SWAP2 SWAP1 POP JUMP JUMPDEST PUSH1 0x0 PUSH2 0x4802 DUP3 SLOAD PUSH2 0x47A4 JUMP JUMPDEST SWAP1 POP SWAP2 SWAP1 POP JUMP JUMPDEST PUSH1 0x0 DUP2 PUSH1 0x60 SHL SWAP1 POP SWAP2 SWAP1 POP JUMP JUMPDEST PUSH1 0x0 DUP2 PUSH1 0x0 SHR SWAP1 POP SWAP2 SWAP1 POP JUMP JUMPDEST PUSH2 0x482C DUP2 PUSH2 0x4700 JUMP JUMPDEST DUP2 EQ PUSH2 0x4837 JUMPI PUSH1 0x0 DUP1 REVERT JUMPDEST POP JUMP JUMPDEST PUSH2 0x4843 DUP2 PUSH2 0x4712 JUMP JUMPDEST DUP2 EQ PUSH2 0x484E JUMPI PUSH1 0x0 DUP1 REVERT JUMPDEST POP JUMP JUMPDEST PUSH2 0x485A DUP2 PUSH2 0x4724 JUMP JUMPDEST DUP2 EQ PUSH2 0x4865 JUMPI PUSH1 0x0 DUP1 REVERT JUMPDEST POP JUMP JUMPDEST PUSH2 0x4871 DUP2 PUSH2 0x4730 JUMP JUMPDEST DUP2 EQ PUSH2 0x487C JUMPI PUSH1 0x0 DUP1 REVERT JUMPDEST POP JUMP JUMPDEST PUSH2 0x4888 DUP2 PUSH2 0x475A JUMP JUMPDEST DUP2 EQ PUSH2 0x4893 JUMPI PUSH1 0x0 DUP1 REVERT JUMPDEST POP JUMP JUMPDEST PUSH2 0x489F DUP2 PUSH2 0x4764 JUMP JUMPDEST DUP2 EQ PUSH2 0x48AA JUMPI PUSH1 0x0 DUP1 REVERT JUMPDEST POP JUMP INVALID LOG3 PUSH6 0x627A7A723158 KECCAK256 0xDC SDIV 0xE4 0xE1 PC 0xA5 CODESIZE 0xE1 0xB5 PUSH21 0x1A373D911FE531827E01D1A10CB626A9ADEE6B6D17 0xC8 PUSH13 0x6578706572696D656E74616CF5 PUSH5 0x736F6C6343 STOP SDIV GT STOP BLOCKHASH ",
    "sourceMap": "146:15668:0:-;;;4605:590;8:9:-1;5:2;;;30:1;27;20:12;5:2;4605:590:0;;;;;;;;;;;;;;;;;;;;;;;;4799:10;4788:8;;:21;;;;;;;;;;;;;;;;;;4824:9;4813:8;;:20;;;;;;;;;;;;;;;;;;4857:18;4837:17;:38;;;;4886:5;4879:4;:12;;;;4916:19;4895:18;:40;;;;4961:10;4939:9;;:33;;;;;;;;;;;;;;;;;;4993:12;4979:11;:26;;;;5035:1;5012:20;:24;;;;5068:1;5040:25;:29;;;;5095:1;5073:19;:23;;;;5119:1;5100:16;:20;;;;5143:1;5124:16;:20;;;;5163:1;5148:12;:16;;;;5186:5;5168:15;;:23;;;;;;;;;;;;;;;;;;4605:590;;;;;;146:15668;;5:134:-1;;89:6;83:13;74:22;;101:33;128:5;101:33;;;68:71;;;;;146:150;;238:6;232:13;223:22;;250:41;285:5;250:41;;;217:79;;;;;303:134;;387:6;381:13;372:22;;399:33;426:5;399:33;;;366:71;;;;;444:962;;;;;;;652:3;640:9;631:7;627:23;623:33;620:2;;;669:1;666;659:12;620:2;704:1;721:72;785:7;776:6;765:9;761:22;721:72;;;711:82;;683:116;830:2;848:64;904:7;895:6;884:9;880:22;848:64;;;838:74;;809:109;949:2;967:64;1023:7;1014:6;1003:9;999:22;967:64;;;957:74;;928:109;1068:2;1086:64;1142:7;1133:6;1122:9;1118:22;1086:64;;;1076:74;;1047:109;1187:3;1206:64;1262:7;1253:6;1242:9;1238:22;1206:64;;;1196:74;;1166:110;1307:3;1326:64;1382:7;1373:6;1362:9;1358:22;1326:64;;;1316:74;;1286:110;614:792;;;;;;;;;1413:91;;1475:24;1493:5;1475:24;;;1464:35;;1458:46;;;;1511:99;;1581:24;1599:5;1581:24;;;1570:35;;1564:46;;;;1617:121;;1690:42;1683:5;1679:54;1668:65;;1662:76;;;;1745:72;;1807:5;1796:16;;1790:27;;;;1824:117;1893:24;1911:5;1893:24;;;1886:5;1883:35;1873:2;;1932:1;1929;1922:12;1873:2;1867:74;;1948:133;2025:32;2051:5;2025:32;;;2018:5;2015:43;2005:2;;2072:1;2069;2062:12;2005:2;1999:82;;2088:117;2157:24;2175:5;2157:24;;;2150:5;2147:35;2137:2;;2196:1;2193;2186:12;2137:2;2131:74;;146:15668:0;;;;;;;"
}
class Signer:
    @staticmethod
    def hash(s):
        return w3.soliditySha3(['bytes32[]'], [s])
    @staticmethod
    def get_v_r_s(sig):
        if type(sig) == tuple:
            return sig
        v,r,s = w3.toInt(sig[-1]+27), w3.toHex(sig[:32]), w3.toHex(sig[32:64])
        return v,r,s

    @staticmethod
    def check_sig(questions_hashes, unanswered, contract_address, sig, signerPubKey):
        h1 = w3.soliditySha3(['bytes32[]', 'uint256', 'address'], 
                            [questions_hashes, unanswered, contract_address])
        msg_hash = eth_account.messages.defunct_hash_message(h1)
        if type(sig) is tuple:
            v,r,s = sig
            contract = w3.eth.contract(
                address=contract_address,
                abi=SUBSCRIPTION_ABI,
            )
            return contract.functions.verifySig(questions_hashes, unanswered, v, r, s, signerPubKey)
        else:
            return w3.eth.account.recoverHash(msg_hash, signature=sig) == signerPubKey

    @staticmethod
    def sign(questions_hashes, unanswered, contract_address, signer_account):
        #print("Signing: ", questions_hashes, unanswered, contract_address)
        msg_hash = w3.soliditySha3(['bytes32[]', 'uint256', 'address'], 
                                    [questions_hashes, unanswered, contract_address])
        return w3.eth.sign(signer_account, msg_hash)

def bytes_to_str(chunk):
    if type(chunk) is not list:
        return chunk.hex()
    ret = []
    for c in chunk:
        ret.append(c.hex())
    return ret

def str_to_bytes(chunk):
    if type(chunk) is not list:
        ret = None
        try:
            ret = bytes.fromhex(chunk)
        except:
            ret = bytes.fromhex(chunk[2:])
        return ret
    ret = []
    for c in chunk:
        try:
            ret.append(bytes.fromhex(c))
        except:
            ret.append(bytes.fromhex(c[2:]))
    return ret

def dict_to_bytes(d):
    s = json.dumps(d)
    s += " "*(BLOCKLEN - (len(s) % BLOCKLEN))
    return s.encode('utf-8')

def bytes_to_dict(b):
    d = json.loads(b.decode('utf-8'))
    return d

def int_to_bytes(x: int) -> bytes:
    return x.to_bytes(BLOCKLEN, 'big')

def bytes_to_int(xbytes: bytes) -> int:
    return int.from_bytes(xbytes, 'big')

def receive_dict(conn):
    data = conn.recv(BLOCKLEN)
    #print("LenData: " + str(data))
    if (not data) or data == b'':
        #print("ERROR: not data")
        return None
    length = bytes_to_int(data)  
    total_len = 0
    bdict = bytes()
    while total_len < length:
        data = conn.recv(BLOCKLEN)
        if (not data) or data == b'':
            #print("ERROR: not data")
            return None
        #print("Data: " + str(data))
        total_len += len(data)
        bdict += data
    return bytes_to_dict(bdict)

def send_dict(conn, d):
    bdict = dict_to_bytes(d)
    conn.sendall(int_to_bytes(len(bdict)))
    conn.sendall(bdict)


class QA:
    # receives encoded
    def __init__(self, question, answer=None, asker=None):
        self.question = question
        self.answer = answer
        self.hash = Signer.hash(question)
        self.asker = asker

    def is_answered(self):
        return self.answer is not None

    def get_asker(self):
        return self.asker

    def get_hash(self):
        return self.hash

    def get_question(self):
        return self.question

    def get_answer(self):
        return self.answer

    def set_answer(self, answer):
        self.answer = answer


class Appeal:
    def __init__(self, eos_block, question, ack, address = None):
        self.eos_block = eos_block
        self.question = question
        self.ack = ack
        self.address = address
    def get_question(self):
        return self.question
    def get_end_of_service_block(self):
        return self.eos_block
    def get_ack(self):
        return self.ack
    def get_customer_address(self):
        return self.address

class Ack:
    def __init__(self, _hashes, _unanswered, _signature):
        self.hashes = _hashes
        self.unanswered = _unanswered
        self.signature = _signature

    def get_all(self):
        return self.hashes, self.unanswered, self.signature

    def get_hashes(self):
        return self.hashes

    def get_unanswered_hashes(self):
        if self.unanswered == 0:
            return []
        return self.hashes[-self.unanswered:]

    def get_answered_hashes(self):
        if self.unanswered == 0:
            return self.hashes
        return self.hashes[:-self.unanswered]

    def is_newer_than(self, other):
        if other is None:
            return True
        other_answered = other.get_answered_hashes()
        for h in other_answered:
            if h not in self.get_answered_hashes():
                return False
        other_unanswered = other.get_unanswered_hashes()
        for h in other_unanswered:
            if h not in self.get_hashes():
                return False
        return True

    def is_different(self, other):
        return not (self.is_newer_than(other) or other.is_newer_than(self))

class Validator:  # This class validates answers and questions of all problem types.
                  # Questions and answers should be encoded.

    def __init__(self, validator_address):
        self.contract = w3.eth.contract(
            address = validator_address,
            abi     = VALIDATOR_ABI)

    def is_valid_question(self, question):
        return self.contract.functions.is_valid_question(question).call()

    def is_answer_correct(self, question, answer):
        return self.contract.functions.is_answer_correct(question, answer).call()


class Provider: # This class is intended for the provider to interact with the blockchain. 
                # It doesn't do any computing itself, and doesn't interact with the customers.
    def __init__(self, address, validator_address):
        # creates the validator contract
        self.address = address
        self.validator_address = validator_address
        self.validator = Validator(validator_address)
        self.channels = {}

    def get_contract_address(self, customer_address):
        contract = self.channels[customer_address]
        return contract.address

    def get_validator(self):
        return self.validator

    def get_customers(self):
        return self.channels.keys()

    def create_subscription(self, customer_address):
        # creates a single subscription contract, returns contract address
        # uses the constants in the beginning of this file
        # Should hold a list/dict of all subscriptions by customer address
        service_contract = w3.eth.contract(
            abi     = SUBSCRIPTION_ABI,
            bytecode= SUBSCRIPTION_SOL["object"])
        txn_dict = {
            'from': self.address,
        }
        tx_hash = service_contract.constructor(customer_address, APPEAL_PERIOD, SUBSCRIPTION_COST, SUBSCRIPTION_PERIOD, self.validator_address, MAX_QUERIES).transact(txn_dict)
        tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
        contract = w3.eth.contract(
            address=tx_receipt.contractAddress,
            abi     = SUBSCRIPTION_ABI
        )
        self.channels[customer_address] = contract
        return contract.address

    def is_subscription_active(self, customer_address):
        contract = self.channels[customer_address]
        txn_dict = {
            'from': self.address,
        }
        status = contract.functions.is_active().call(txn_dict)
        return status

    def check_for_appeal(self, customer_address):
        # returns None or a question appealed by the specified customer
        contract = self.channels[customer_address]
        txn_dict = {
            'from': self.address,
        }
        appeal_status = contract.functions.is_customer_appealing().call(txn_dict)

        if not appeal_status:
            return None

        eos_block = contract.functions.get_end_of_service_block().call(txn_dict)
        question = contract.functions.get_question_appealed().call(txn_dict)
        hashes = contract.functions.get_question_hashes_demanded().call(txn_dict)
        unanswered = contract.functions.get_unanswered_demanded().call(txn_dict)
        v = contract.functions.get_v_provided().call(txn_dict)
        r = contract.functions.get_r_provided().call(txn_dict)
        s = contract.functions.get_s_provided().call(txn_dict)
        ack = Ack(hashes, unanswered, (v,r,s))
        appeal = Appeal(eos_block, question, ack, address=customer_address)
        return appeal

    def resolve_appeal(self, customer_address, answer):
        # submit answer to resolve appeal by the specified customer
        #print("Resolving: ", answer)
        contract = self.channels[customer_address]
        txn_dict = {
            'from': self.address,
        }
        #print("Resolving with:",answer)
        tx_hash = contract.functions.resolve(answer).transact(txn_dict)
        tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)

    def dismiss_appeal(self, customer_address, questions_hashes, unanswered, signature):
        contract = self.channels[customer_address]
        txn_dict = {
            'from': self.address,
        }
        v, r, s = Signer.get_v_r_s(signature)
        tx_hash = contract.functions.dismiss(questions_hashes, unanswered, v, r, s).transact(txn_dict)
        tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)

    def demand_signature(self, customer_address, question, questions_hashes, unanswered, signature, answer):
        contract = self.channels[customer_address]
        txn_dict = {
            'from': self.address,
        }
        is_provider_demanding = contract.functions.is_provider_demanding().call(txn_dict)

        if is_provider_demanding:
            return False

        v, r, s = Signer.get_v_r_s(signature)
        tx_hash = contract.functions.demand_signature(question, questions_hashes, unanswered, v, r, s, answer).transact(txn_dict)
        tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
        return True

    def exec_demand(self, customer_address):
        contract = self.channels[customer_address]
        txn_dict = {
            'from': self.address,
        }
        if(contract.functions.can_exec_demand().call(txn_dict)):
            tx_hash = contract.functions.exec_demand().transact(txn_dict)
            tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
            ret = contract.functions.is_active().call(txn_dict)
            return not ret
        return False

    def overflow(self, customer_address, questions_hashes, unanswered, signature):
        contract = self.channels[customer_address]
        txn_dict = {
            'from': self.address,
        }
        v, r, s = Signer.get_v_r_s(signature)
        tx_hash = contract.functions.overflow(questions_hashes, unanswered, v, r, s).transact(txn_dict)
        tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)

    def check_demand(self, customer_address):
        contract = self.channels[customer_address]
        txn_dict = {
            'from': self.address,
        }
        is_provider_demanding = contract.functions.is_provider_demanding().call(txn_dict)

        if is_provider_demanding:
            return None
        hashes = contract.functions.get_question_hashes_demanded().call(txn_dict)
        unanswered = contract.functions.get_unanswered_demanded().call(txn_dict)
        v = contract.functions.get_v_provided().call(txn_dict)
        r = contract.functions.get_r_provided().call(txn_dict)
        s = contract.functions.get_s_provided().call(txn_dict)
        return hashes, unanswered, (v,r,s)

    def withdraw(self, customer_address):
        # withdraws money from the subscription of the specified customer
        contract = self.channels[customer_address]
        txn_dict = {
            'from': self.address,
        }
        amount = contract.functions.withdraw_funds_amount().call(txn_dict);
        if amount > 0:
            tx_hash = contract.functions.withdraw_funds(self.address).transact(txn_dict)
            tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
        return amount

class Customer: # This class is intended for the customer to interact with the blockchain. 
                # It doesn't generate any questions, and doesn't interact with the provider.
    def __init__(self, address):
        self.address = address
        self.contract = None
        self.validator = None

    def is_subscription_active(self):
        txn_dict = {
            'from': self.address,
        }
        status = self.contract.functions.is_active().call(txn_dict)
        return status

    def get_validator(self):
        return self.validator

    def join_subscription(self, subscription_address):
        self.contract = w3.eth.contract(
            address=subscription_address,
            abi=SUBSCRIPTION_ABI,
        )
        txn_dict = {
            'from': self.address,
            'value': SUBSCRIPTION_COST,
        }
        tx_hash = self.contract.functions.activate().transact(txn_dict)
        tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
        self.validator = Validator(self.get_validator_address())

    def get_validator_address(self):
        txn_dict = {
            'from': self.address,
        }
        address = self.contract.functions.get_validator_address().call(txn_dict)
        return address

    def check_demand(self):
        txn_dict = {
            'from': self.address,
        }
        if not self.is_subscription_active():
            return None
        is_provider_demanding = self.contract.functions.is_provider_demanding().call(txn_dict)

        if not is_provider_demanding:
            return None
        question = self.contract.functions.get_question_demanded().call(txn_dict)
        answer = self.contract.functions.get_answer_demanded().call(txn_dict)
        return question, answer

    def provide_signature(self, questions_hashes, unanswered, signature):
        txn_dict = {
            'from': self.address,
        }
        if not self.is_subscription_active():
            return False
        v, r, s = Signer.get_v_r_s(signature)
        tx_hash = self.contract.functions.provide_signature(questions_hashes, unanswered, v, r, s).transact(txn_dict)
        tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
        return True

    def appeal(self, question, questions_hashes, unanswered, signature):
        txn_dict = {
            'from': self.address,
        }
        if not self.is_subscription_active():
            print("Couldn't appeal: subscription not active")
            return False
        v, r, s = Signer.get_v_r_s(signature)
        #print("Appealing with:",question, questions_hashes, unanswered, v, r, s)
        #print(type(question), type(questions_hashes), type(unanswered), type(v), type(r), type(s))
        try:
            x = self.contract.functions.try_appeal(question, questions_hashes, unanswered, v, r, s).call(txn_dict)
            if not x:
                raise Exception("Appeal failed.")
        except Exception as e:
            print("Coundnt appeal:",e)
            return False
        tx_hash = self.contract.functions.appeal(question, questions_hashes, unanswered, v, r, s).transact(txn_dict)
        tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
        return True

    def check_appeal(self):
        txn_dict = {
            'from': self.address,
        }
        if not self.is_subscription_active():
            return None
        appeal_status = self.contract.functions.is_customer_appealing().call(txn_dict)
        if appeal_status:
            return None
        answer = self.contract.functions.get_answer_resolved().call(txn_dict)
        return answer

    def get_question_appealed(self):
        if not self.is_subscription_active():
            return None
        txn_dict = {
            'from': self.address,
        }
        return self.contract.functions.get_question_appealed().call(txn_dict)

    def withdraw(self):
        txn_dict = {
            'from': self.address,
        }
        amount = self.contract.functions.withdraw_funds_amount().call(txn_dict);
        if amount > 0:
            tx_hash = self.contract.functions.withdraw_funds(self.address).transact(txn_dict)
            tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
        return amount


def wait_k_blocks(k: int, sleep_interval: int = 2):
    start = w3.eth.blockNumber
    time.sleep(sleep_interval)
    while w3.eth.blockNumber < start + k:
        time.sleep(sleep_interval)

def Scene_1(address1, address2):
    print("Creating Validator contract...")
    ValidatorContract = w3.eth.contract(
        abi     = VALIDATOR_ABI,
        bytecode=VALIDATOR_SOL["object"])
    txn_dict = {'from': address1}
    tx_hash = ValidatorContract.constructor().transact(txn_dict)
    tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    validator_address = tx_receipt.contractAddress


    customer = Customer(address1)
    provider = Provider(address2, validator_address)
    print("Creating Subscription contract...")
    sub_address = provider.create_subscription(address1)
    customer.join_subscription(sub_address)

    for i in range(3):
        # Customer running
        question = Solver.generate()
        print("Customer: Appealing for question:", question)
        customer.appeal(question)
        print("Customer: Checking for appeal...")
        question = customer.check_appeal()
        print("Got: ", question)
        wait_k_blocks(1)

        # Provider running
        print("Provider: Checking for appeal...")
        appeal = provider.check_for_appeal(address1)
        if appeal is None:
            print("ERROR: coudn't find an appeal")
            return -1
        question = appeal[1]
        print("Provider: Found appeal for question:", question)
        answer = Solver.solve(question)
        print("Provider: Resolving appeal with answer:", answer)
        provider.resolve_appeal(address1, answer)
        question = provider.check_for_appeal(address1)
        if question is not None:
            print("ERROR: appeal still active")
            return -1

        # Customer running
        print("Customer: Checking appeal...")
        answer = customer.check_appeal()
        if answer is None:
            print("ERROR: appeal didn't resolve")
            return -1
        c = Coder.decode_answer(answer)
        print("Customer: found answer: " + str(c))
        print("~~~\n")

if __name__ == "__main__":
    address1 = "0x2577d3ceb68148E2e22A314ad99A26B67A7F26EC"
    address2 = "0x8408861D0C5cf6b52Eb7c799D1C0B05365FF65cd"
    Scene_1(address1, address2)
