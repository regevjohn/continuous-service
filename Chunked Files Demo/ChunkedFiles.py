import web3
import web3.contract
from lib import w3
from ChunkedFilesValidator import VALIDATOR_ABI, VALIDATOR_SOL
import math
from Crypto.Hash import keccak
import os
import pickle
import random

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
            chunk = ""
            chunks = []
            merkle_level = []
            merkle_tree = []
            size = len(content)
            chunks_num = int(math.ceil(len(content) / Solver.CHUNK_SIZE))
            for i in range(chunks_num):
                chunk = content[i * Solver.CHUNK_SIZE:(i + 1) * Solver.CHUNK_SIZE]
                chunks.append(chunk)
                k = keccak.new(digest_bits=256)
                k.update(chunk)
                merkle_level.append(k.digest())
            if chunks_num % 2:
                merkle_level.append(b'\x00'*32)
            merkle_tree.append(merkle_level)
            high = 0
            if chunks_num == 1:
                high = 1
            else:
                high = int(math.ceil(math.log(chunks_num, 2)))
            for _ in range(high):
                prev_level = merkle_level
                merkle_level = []
                for i in range(int(len(prev_level) / 2)):
                    k = keccak.new(digest_bits=256)
                    k.update(prev_level[2*i])
                    k.update(prev_level[2*i+1])
                    merkle_level.append(k.digest())
                if int(len(prev_level) / 2) % 2:
                    merkle_level.append(b'\x00'*32)
                merkle_tree.append(merkle_level)
            merkle_tree[-1] = [merkle_level[0]]
            merkle_root = merkle_level[0]
            file = open('./FilesData/' + file_name + '.data', 'wb')
            pickle.dump([chunks, merkle_tree], file)
            file.close()
            tx_hash = validator_contract.functions.add_file_info(file_name, size, merkle_root).transact(txn_dict)
            tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
        return validator_address

    @staticmethod
    def solve(question, wrong=False):
        if wrong:
            return Coder.encode_answer([bytes("wrong chunk", 'utf-8')])
        question = Coder.decode_question(question)
        file_name = question[0]
        chunk_num = question[1]
        file = open('./FilesData/' + file_name + '.data', 'rb')
        [chunks, merkle_tree] = pickle.load(file)
        file.close()
        chunk = chunks[chunk_num]
        answer = [len(chunk)]
        answer.append(chunk)
        chunks_num = len(merkle_tree[0])
        high = 0
        if chunks_num == 1:
            high = 1
        else:
            high = int(math.ceil(math.log(chunks_num, 2)))
        tmp_chunk_num = int(chunk_num)
        answer.append(merkle_tree[0][tmp_chunk_num])
        for i in range(high):
            if tmp_chunk_num % 2 == 0:
                answer.append(merkle_tree[i][tmp_chunk_num + 1])
            else:
                answer.append(merkle_tree[i][tmp_chunk_num - 1])
            tmp_chunk_num = int(tmp_chunk_num / 2)
        answer.append(merkle_tree[-1][0])
        return Coder.encode_answer(answer)

    @staticmethod
    def generate():
        file_name = random.choice(os.listdir('./Files'))
        file = open('./Files/' + file_name, 'rb')
        content = file.read()
        file.close()
        chunks_num = int(math.ceil(len(content) / Solver.CHUNK_SIZE))
        chunk_num = random.choice(range(chunks_num))
        return Coder.encode_question([file_name, chunk_num])

    @staticmethod
    def input():
        file_name = input("file name: ")
        chunk_num = int(input("chunk index: "))
        return Coder.encode_question([file_name, chunk_num])


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
        file_name = question[0]
        chunk_num = question[1]
        file_name_len = len(file_name)
        encoded_question = bytes([file_name_len])
        encoded_question += bytes(file_name, 'utf-8')
        encoded_question += chunk_num.to_bytes(1 if chunk_num in [0, 1] else int(math.ceil(math.log(chunk_num, 256))),'big')
        return Coder.bytes_to_bytes32array(encoded_question)

    @staticmethod
    def str_question(question):
        file_name, chunk_num = Coder.decode_question(question)
        return "file name: " + file_name + ", chunk index: " + str(chunk_num)

    def str_answer(answer):
        answer = Coder.decode_answer(answer)
        return str(answer[1])


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
        file_name_len = int(question[0])
        file_name = (question[1:1 + file_name_len]).decode('utf-8')
        chunk_num = int.from_bytes(question[1 + file_name_len:], 'big')
        return [file_name, chunk_num]

    @staticmethod
    def compare_questions(question1, question2):
        return question1[0] == question2[0] and question1[1] == question2[1]

    @staticmethod
    def encode_answer(answer):
        chunk_size = answer[0]
        chunk_size_num_of_bytes = 1 if chunk_size == 1 else int(math.ceil(math.log(chunk_size, 256)))
        encoded_answer = chunk_size_num_of_bytes.to_bytes(1, 'big')
        encoded_answer += chunk_size.to_bytes(chunk_size_num_of_bytes, 'big')
        encoded_answer += answer[1]
        for i in range(2, len(answer)):
            encoded_answer += answer[i]
        return Coder.bytes_to_bytes32array(encoded_answer)

    @staticmethod
    def decode_answer(_answer):
        answer = Coder.bytes32array_to_bytes(_answer)
        decoded_answer = []
        chunk_size_num_of_bytes = int.from_bytes(answer[0:1], 'big')
        chunk_size = int.from_bytes(answer[1:1+chunk_size_num_of_bytes], 'big')
        decoded_answer.append(chunk_size)
        decoded_answer.append(answer[1+chunk_size_num_of_bytes:1+chunk_size_num_of_bytes+chunk_size])
        for i in range(int((len(answer)-(1+chunk_size_num_of_bytes+chunk_size))/32)):
            decoded_answer.append(answer[(1+chunk_size_num_of_bytes+chunk_size)+32*i:(1+chunk_size_num_of_bytes+chunk_size)+32*(i+1)])
        return decoded_answer