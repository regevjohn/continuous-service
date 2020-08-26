import web3
import web3.contract
from lib import w3
from FilesValidator import VALIDATOR_ABI, VALIDATOR_SOL
from Crypto.Hash import keccak
import os
import random
import math

class Solver:

    CHUNK_SIZE = 10

    @staticmethod
    def init_validator(address):
        ValidatorContract = w3.eth.contract(
            abi=VALIDATOR_ABI,
            bytecode=VALIDATOR_SOL["object"])
        txn_dict = {'from': address}
        tx_hash = ValidatorContract.constructor(Solver.CHUNK_SIZE).transact(txn_dict)
        tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
        validator_address = tx_receipt.contractAddress

        validator_contract = w3.eth.contract(
            address=validator_address,
            abi=VALIDATOR_ABI,
        )
        for file_name in os.listdir('./Files'):
            file = open('./Files/' + file_name, 'rb')
            content = file.read()
            file.close()
            k = keccak.new(digest_bits=256)
            k.update(content)
            file_hash = k.hexdigest()
            tx_hash = validator_contract.functions.add_file_hash(file_name, file_hash).transact(txn_dict)
            tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
        return validator_address

    @staticmethod
    def solve(question, wrong=False):
        if wrong:
            return Coder.encode_answer("wrong file content")
        question = Coder.decode_question(question)
        file = open('./Files/' + question, 'r')
        content = file.read()
        file.close()
        return Coder.encode_answer(content)

    @staticmethod
    def generate():
        file_name = random.choice(os.listdir('./Files'))
        return Coder.encode_question(file_name)

    @staticmethod
    def input():
        file_name = input("file name: ")
        return Coder.encode_question(file_name)


class Coder:  # This class encodes and decodes question and answers of specific problem type.
    # An encoded question or answer is an array of integers.
    @staticmethod
    def bytes_to_bytes32array(_bytes):
        nonzero_bytes = len(_bytes) % 32
        bytes32array = [nonzero_bytes.to_bytes(1, 'big') + b'\x00'*31]
        for i in range(int(math.floor(len(_bytes) / 32))):
            bytes32 = bytes()
            for j in range(32):
                bytes32 += _bytes[(i * 32 + j):(i * 32 + j+1)]
            bytes32array.append(bytes32)
        bytes32 = bytes()
        for j in range(nonzero_bytes):
            bytes32 += _bytes[(int(math.floor(len(_bytes) / 32)) * 32 + j):(int(math.floor(len(_bytes) / 32)) * 32 + j+1)]
        bytes32 += b'\x00'*(32-nonzero_bytes)
        bytes32array.append(bytes32)
        return bytes32array

    @staticmethod
    def bytes32array_to_bytes(bytes32array):
        nonzero_bytes = int.from_bytes(bytes32array[0][0:1], 'big')
        _bytes = bytes()
        for i in range(len(bytes32array) - 2):
            for j in range(32):
                _bytes += bytes32array[i+1][j:j+1]
        for j in range(nonzero_bytes):
            _bytes += bytes32array[len(bytes32array)-1][j:j+1]
        return _bytes

    @staticmethod
    def encode_question(question):
        return Coder.bytes_to_bytes32array(bytes(question, 'utf-8'))

    @staticmethod
    def str_question(question):
        file_name = Coder.decode_question(question)
        return "file name: " + file_name

    @staticmethod
    def str_answer(answer):
        answer = Coder.decode_answer(answer)
        return str(answer)
    
    @staticmethod
    def encoded_to_stream(chunk):
        ret = []
        for c in chunk:
            ret.append(c.hex())
        return ret

    @staticmethod
    def stream_to_encoded(chunk):
        ret = []
        for c in chunk:
            ret.append(bytes.fromhex(c))
        return ret

    @staticmethod
    def decode_question(_question):
        question = Coder.bytes32array_to_bytes(_question)
        return question.decode('utf-8')

    @staticmethod
    def compare_questions(question1, question2):
        return question1 == question2

    @staticmethod
    def encode_answer(answer):
        return Coder.bytes_to_bytes32array(bytes(answer, 'utf-8'))

    @staticmethod
    def decode_answer(_answer):
        answer = Coder.bytes32array_to_bytes(_answer)
        return answer.decode('utf-8')