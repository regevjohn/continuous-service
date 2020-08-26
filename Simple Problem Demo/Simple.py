import web3
from decimal import *
import web3.contract
import random
from lib import w3
from SimpleValidator import *

class Solver:
    @staticmethod
    def init_validator(address):
        ValidatorContract = w3.eth.contract(
            abi     = VALIDATOR_ABI,
            bytecode= VALIDATOR_SOL["object"])
        txn_dict = {'from': address}
        tx_hash = ValidatorContract.constructor().transact(txn_dict)
        tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
        validator_address = tx_receipt.contractAddress
        return validator_address

    @staticmethod
    def solve(question, wrong=False):
        a,b,c = Coder.decode_question(question)
        if a == 0:
            print("WTF?")
            return None
        x = (c - b) / a
        if wrong:
            x = (c - b + 100) / a
        return Coder.encode_answer(x)

    @staticmethod
    def generate():
        a,b,c = random.randint(1,100), random.randint(0,100), random.randint(0,100)
        return Coder.encode_question(a,b,c)

    @staticmethod
    def input():
        print("a * x + b = c")
        a = abs(int(input("a = ")))
        b = abs(int(input("b = ")))
        c = abs(int(input("c = ")))
        question = Coder.encode_question(a,b,c)
        return question
    

class Coder:  # This class encodes and decodes question and answers of specific problem type.
                           # An encoded question or answer is an array of integers.
    
    @staticmethod
    def encode(array):
        ret = []
        for x in array:
            ret.append(x.to_bytes(32, byteorder='big'))
        return ret

    @staticmethod
    def decode(array):
        ret = []
        for x in array:
            ret.append(int.from_bytes(x, 'big'))
        return ret

    @staticmethod
    def encode_question(a, b, c):
        return Coder.encode([a,b,c])

    @staticmethod
    def str_question(question):
        a,b,c = Coder.decode_question(question)
        return str(a) + "*x + " + str(b) + " = " + str(c)

    @staticmethod
    def str_answer(answer):
        x = Coder.decode_answer(answer)
        return "±" + str(x)

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
    def decode_question(question):
        return Coder.decode(question)

    @staticmethod
    def compare_questions(question1, question2):
        return all([question1[i] == question2[i] for i in range(3)])

    @staticmethod
    def encode_answer(c):
        d, e = Decimal(c).as_integer_ratio()
        d = abs(d)
        e = abs(e)
        return Coder.encode([d,e])

    @staticmethod
    def decode_answer(answer):
        decoded = Coder.decode(answer)
        return decoded[0] / decoded[1]