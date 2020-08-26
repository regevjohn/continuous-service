import web3
import time
import eth_account.messages
import web3.contract
import sys
import socket
from threading import Thread, Lock
from lib import *
from Files import *
from FilesValidator import *
import json
from lib import w3
import traceback

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 29290        # Port to listen on (non-privileged ports are > 1023)

class CustomerInterface: # This class is intended for the customer to interact with the blockchain. It doesn't generate any questions, and doesn't interact with the provider.
    def __init__(self, address):
        self.customer = Customer(address)
        self.qas = {}
        self.subscription_address = None

    def is_subscription_active(self):
        return self.customer.is_subscription_active()


    def join_subscription(self, subscription_address):
        self.customer.join_subscription(subscription_address)
        self.subscription_address = subscription_address

    def register_question(self, question):
        if not self.customer.get_validator().is_valid_question(question):
            print("Question invalid!!!")
            return False
        q_hash = Signer.hash(question)
        if q_hash not in self.qas:
            self.qas[q_hash] = QA(question)
        #print("registerd:",q_hash)
        return True

    def register_answer(self, question, answer):
        if not self.customer.validator.is_answer_correct(question, answer):
            print("Tried to register incorrect answer!")
            return
        q_hash = Signer.hash(question)
        done = False
        if q_hash not in self.qas:
            self.qas[q_hash] = QA(question, answer=answer)
        else:
            self.qas[q_hash].set_answer(answer)

    def get_all_hashes(self):
        answered = []
        unanswered = []
        for qa in self.qas.values():
            if qa.is_answered():
                answered.append(qa.get_hash())
            else:
                unanswered.append(qa.get_hash())
        return answered + unanswered, len(unanswered)

    def get_signed_hashes(self):
        hashes, unanswered = self.get_all_hashes()
        return hashes, unanswered, self.sign_hashes(hashes, unanswered)

    def sign_hashes(self, hashes, unanswered):
        return Signer.sign(hashes, unanswered, self.subscription_address, self.customer.address)

    def get_answer(self, question):
        q_hash = Signer.hash(question)
        if q_hash in self.qas:
            return self.qas[q_hash].get_answer()
        return None

    def check_demand(self):
        ret = self.customer.check_demand()
        if ret is not None:
            question, answer = ret
            self.register_answer(question, answer)
        return ret

    def resolve_demand(self):
        demand = self.check_demand()
        if demand is not None:
            hashes, unanswered, signature = self.get_signed_hashes()
            print("Providing: ", hashes, unanswered)
            self.provide_signature(hashes, unanswered, signature)
        return demand

    def provide_signature(self, hashes, unanswered, signature=None):
        if signature is None:
            signature = self.sign_hashes(hashes, unanswered)
        try:
            self.customer.provide_signature(hashes, unanswered, signature)
        except Exception as e:
            print("Coudn't provide signature:", e)
            traceback.print_tb(e.__traceback__)

    def get_all_answers(self):
        questions = []
        answers = []
        for qa in self.qas.values():
            if qa.is_answered():
                questions.append(qa.get_question())
                answers.append(qa.get_answer())
        return questions, answers

    def appeal(self, question, hashes=None, unanswered=None):
        if not self.register_question(question):
            print("Couldn't appeal: question not registered")
            return False
        signature = None
        if hashes is None:
            hashes, unanswered, signature = self.get_signed_hashes()
        else:
            signature = self.sign_hashes(hashes, unanswered)
        try:
            #print("Appealing with:", Coder.str_question(question), hashes, unanswered, signature)
            #print(QA(question).get_hash())
            if not self.customer.appeal(question, hashes, unanswered, signature):
                raise ""
        except Exception as e:
            print("Couldn't appeal:", e)
            traceback.print_tb(e.__traceback__)
            return False
        return True

    def check_appeal(self):
        answer = self.customer.check_appeal()
        if answer is not None:
            answer = answer
            self.register_answer(self.customer.get_question_appealed(), answer)
        return answer

    def withdraw(self):
        return self.customer.withdraw()

# Class for interaction between threads and socket thread
class CommandsList():
    def __init__(self):
        self.commands = []
        self.inputs = []
    
    def insert_command(self, msg):
        self.commands.append(msg)

    def get_last_input(self):
        if len(self.inputs) < 1:
            return None
        ret, self.inputs = self.inputs[-1], self.inputs[:-1]
        return ret

    def insert_input(self, inp):
        self.inputs.append(inp)

    def next(self):
        if len(self.commands) < 1:
            return None
        ret, self.commands = self.commands[0], self.commands[1:]
        return ret

def handle_socket_customer(host, port, cmd_list, lock, QUIT_MSG):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        s.settimeout(0.2)
        while True:
            time.sleep(0.1)
            inp = None
            try:
                inp = receive_dict(s)
                if inp == None:
                    #print("CLOSING...")
                    print("\nSocket connection was closed by provider.")
                    s.close()
                    break
            except socket.timeout:
                pass
            except Exception as e:
                print(e)
                #print("CLOSING...")
                s.close()
                break
            lock.acquire()
            try:
                if inp is not None:
                    cmd_list.insert_input(inp)
                    #print("GOT MSG: ", inp)
                msg = cmd_list.next()
            finally:
                lock.release()
            if msg is None:
                time.sleep(0.5)
            else:
                if msg == QUIT_MSG:
                    print("\nSocket connection was closed by you.")
                    s.close()
                    break
                #print("SENDING MSG: ", msg)
                send_dict(s, msg)
    

def init_customer(address, host, port):
    #provider_int = ProviderInterface(address)
    #provider_lock = Lock()
    #x = Thread(target=handle_provider, args=(provider_lock, provider_int))
    #x.start()
    to_join = []
    customer_int = CustomerInterface(address)
    cmd_list = CommandsList()
    lock = Lock()
    customer_lock = Lock()
    QUIT_MSG = {"close":True}
    x = Thread(target=handle_socket_customer, args=(host, port, cmd_list, lock, QUIT_MSG))
    x.start()
    to_join.append(x)
    print("Sending address...")
    msg = {"type": "address", "address": str(address)}
    lock.acquire()
    try:
        cmd_list.insert_command(msg)
    finally:
        lock.release()
    print("Waiting for subscription address...")
    while True:
        lock.acquire()
        try:
            msg = cmd_list.get_last_input()
        finally:
            lock.release()
        if msg is not None and "type" in msg and msg["type"] == "subscription" and "address" in msg:
            customer_int.join_subscription(msg["address"])
            break
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #------------------------------------------------
    x = Thread(target=auto_customer_background, args=(customer_int, customer_lock))
    x.start()
    to_join.append(x)
    auto_customer(customer_int, customer_lock, cmd_list, lock, user_input=True, only_appeals=False, sending_ack=True, auto_file=False, num_of_questions=4)
    #------------------------------------------------
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'''
    lock.acquire()
    try:
        cmd_list.insert_command(QUIT_MSG)
    finally:
        lock.release()
    for x in to_join:
        x.join()


def user_customer(customer_int, cmd_list, lock):
    print("Joined Subscription!\n")
    print("Commands:")
    print("q - exit")
    print("new - register new question and send to provider")
    print("check - check for new answers from provider")
    print("get - get specific answer if submitted by provider")
    print("ackall - sign all answers submitted by provider")
    print("appeal - appeal a question")
    print("status - check appeal and active")
    print("demand - check if provider demanded signature")
    print("resolve - resolve provider's signature demand")
    print("withdraw - withdraw funds from contract")
    while(True):
        value = input("$>> ")
        if value ==  "q":
            break
        elif value == "new":
            # register new question and send to provider
            print("Input new question:")
            try:
                question = Solver.input()
            except Exception as e:
                traceback.print_tb(e.__traceback__)
                continue
            #print("Got new question:",question)
            if not customer_int.register_question(question):
                print("Warning: invalid question")
            hashes, unanswered, signature = customer_int.get_signed_hashes()
            #print("providing: ", hashes, unanswered)
            msg = {
                "type": "new_question", 
                "question": Coder.encoded_to_stream(question),
                "hashes": bytes_to_str(hashes),
                "unanswered": unanswered,
                "signature": bytes_to_str(signature)}
            lock.acquire()
            try:
                cmd_list.insert_command(msg)
            finally:
                lock.release()
            print("Sent question:", Coder.str_question(question))
        elif value == "check":
            msg = {"type": "send_answer"}
            lock.acquire()
            try:
                cmd_list.insert_command(msg)
            finally:
                lock.release()
            while True:
                time.sleep(0.2)
                lock.acquire()
                try:
                    msg = cmd_list.get_last_input()
                finally:
                    lock.release()
                if msg is not None:
                    break
            answers = []
            questions = []
            answers_stream = []
            questions_stream = []
            if "type" in msg and msg["type"] == "answer" and "answers" in msg and "questions" in msg:
                answers_stream = msg["answers"]
                questions_stream = msg["questions"]

            for i in range(min(len(questions_stream), len(answers_stream))):
                answers.append(Coder.stream_to_encoded(answers_stream[i]))
                questions.append(Coder.stream_to_encoded(questions_stream[i]))
            print("Got answers and questions:")
            for i in range(min(len(answers), len(questions))):
                answer = answers[i]
                question = questions[i]
                customer_int.register_answer(question, answer)
                print(Coder.str_question(question), "->", Coder.str_answer(answer))
            # get next answer from provider
            pass
        elif value == "get":
            # get specific answer
            try:
                question = Solver.input()
            except Exception as e:
                traceback.print_tb(e.__traceback__)
                continue
            answer = customer_int.get_answer(question)
            if answer is None:
                print("Got no answer yet.")
            else:
                print("Answer: ", answer)
        elif value == "ackall":
            # sign all answers submitted by provider
            #questions, answers = customer_int.get_all_answers()
            hashes, unanswered, signature = customer_int.get_signed_hashes()
            msg = {
            "type": "ack",
            "hashes": bytes_to_str(hashes),
            "unanswered": unanswered,
            "signature": bytes_to_str(signature)
            }
            lock.acquire()
            try:
                cmd_list.insert_command(msg)
            finally:
                lock.release()
            print("Sent ack for all answers")
        elif value == "appeal":
            try:
                question = Solver.input()
            except Exception as e:
                traceback.print_tb(e.__traceback__)
                continue
            if not customer_int.appeal(question):
                #print("Couldn't appeal - invalid question.")
                pass
        elif value == "status":
            print("Check appeal status: ", customer_int.check_appeal())
        elif value == "demand":
            ret = customer_int.check_demand()
            if ret is None:
                print("No demand from provider.")
            else:
                print("Provider demanded signature for: ")
                question, answer = ret
                print(Coder.str_question(question), "->", Coder.str_answer(answer))
        elif value == "resolve":
            ret = customer_int.resolve_demand()
            if ret is None:
                print("No demand from provider.")
            else:
                print("Resolved demand for: ")
                question, answer = ret
                print(Coder.str_question(question), "->", Coder.str_answer(answer))
        elif value == "withdraw":
            amount = customer_int.withdraw()
            if amount > 0:
                print("Withdrew:", amount)
                break
            else:
                print("No funds to withdraw")
        else:
            print("[x] Unknown command:", value)


def auto_customer(customer_int, customer_lock, cmd_list, lock, user_input=False, only_appeals=False, sending_ack=False, auto_file=False, num_of_questions=3):
    # Generate all Questions
    questions = []
    answers = []
    if auto_file:
        filename, questions = generate_file_questions(customer_int, customer_lock)
    else:
        for x in range(num_of_questions):
            question = None
            if user_input:
                print("Input next question:")
                try:
                    question = Solver.input()
                except Exception as e:
                    traceback.print_tb(e.__traceback__)
                    continue
            else:
                question = Solver.generate()
            questions.append(question)

    # Send Questions
    for question in questions:
        # Register Question
        customer_lock.acquire()
        try:
            customer_int.register_question(question)
            #print("registed question")
        except Exception as e:
            traceback.print_tb(e.__traceback__)
            print(e)
        finally:
            customer_lock.release() 

        # Announce Question to Provider(?)
        if only_appeals:
            print("Generated question secretly:", Coder.str_question(question))
        else:
            customer_lock.acquire()
            try:
                hashes, unanswered, signature = customer_int.get_signed_hashes()
            finally:
                customer_lock.release() 
            msg = {
                "type": "new_question", 
                "question": Coder.encoded_to_stream(question),
                "hashes": bytes_to_str(hashes),
                "unanswered": unanswered,
                "signature": bytes_to_str(signature)}
            lock.acquire()
            try:
                cmd_list.insert_command(msg)
            finally:
                lock.release()
            print("Generated and sent question:", Coder.str_question(question))

        # Wait for Answer from Provider
        t = 0
        T = 50
        if only_appeals:
            T = 1
        appealed_block = 0
        answer = None
        ask_again = True
        printed_waiting = False
        while True:
            #print(".")
            # Break if inactive
            customer_lock.acquire()
            try:
                active = customer_int.is_subscription_active()
            finally:
                customer_lock.release() 
            if not active:
                print("Subscription ended, closing main thread.")
                break

            t += 1
            time.sleep(0.1)

            answer = None
            customer_lock.acquire()
            try:
                answer = customer_int.get_answer(question)
            finally:
                customer_lock.release() 
            if answer is not None:
                print("Got answer from demand!")
                break

            # Appeal Question
            if t == T:
                print("Appealing question - took too long for provider to respond.")
                customer_lock.acquire()
                try:
                    customer_int.appeal(question)
                finally:
                    customer_lock.release() 
                appealed_block = w3.eth.blockNumber
                printed_waiting = False

            # Check if Appeal Resolved
            if t > T:
                customer_lock.acquire()
                try:
                    answer = customer_int.check_appeal()
                finally:
                    customer_lock.release() 
                
                if answer is not None:
                    customer_lock.acquire()
                    try:
                        customer_int.register_answer(question, answer)
                    finally:
                        customer_lock.release()
                    print("Appeal resolved by provider!")
                    break            
            
            if only_appeals:
                print("Only appeals")
                continue
            
            # Ask for Answers from Provider
            if ask_again:
                #print("asking again")
                msg = {"type": "send_answer"}
                lock.acquire()
                try:
                    cmd_list.insert_command(msg)
                finally:
                    lock.release()
                ask_again = False

            # Receive Answers

            msg = None
            lock.acquire()
            try:
                msg = cmd_list.get_last_input()
            finally:
                lock.release()
            if msg is not None:
                ask_again = True
            else:
                continue
            answers_ = []
            questions_ = []
            answers_stream = []
            questions_stream = []
            if "type" in msg and msg["type"] == "answer" and "answers" in msg and "questions" in msg:
                answers_stream = msg["answers"]
                questions_stream = msg["questions"]

            for i in range(min(len(answers_stream), len(questions_stream))):
                answer_ = Coder.stream_to_encoded(answers_stream[i])
                question_ = Coder.stream_to_encoded(questions_stream[i])
                answers_.append(answer_)
                questions_.append(question_)
                customer_lock.acquire()
                try:
                    customer_int.register_answer(question_, answer_)
                finally:
                    customer_lock.release()

            # Send Ack for Answers
            if sending_ack:
                # sign all answers submitted by provider
                #questions, answers = customer_int.get_all_answers()
                customer_lock.acquire()
                try:
                    hashes, unanswered, signature = customer_int.get_signed_hashes()
                finally:
                    customer_lock.release()
                
                msg = {
                "type": "ack",
                "hashes": bytes_to_str(hashes),
                "unanswered": unanswered,
                "signature": bytes_to_str(signature)
                }
                lock.acquire()
                try:
                    cmd_list.insert_command(msg)
                finally:
                    lock.release()
                print("Sent ack for all answers")

            if question not in questions_:
                if not printed_waiting:
                    print("question not answered - waiting...")
                    printed_waiting = True
                time.sleep(0.1)
                continue

            print("Received answer from provider.")

            got_correct = False
            for i in range(len(questions_)):
                if questions_[i] == question:
                    answer = answers_[i]
                    ret = False
                    customer_lock.acquire()
                    try:
                        ret = customer_int.customer.validator.is_answer_correct(question, answer)
                    finally:
                        customer_lock.release()
                    if not ret:
                        if t < T:
                            print("Answer incorrect!")
                            t = T-1
                    else:
                        got_correct = True
            if got_correct:
                break
        if answer is not None:
            print("Got answer: ", Coder.str_answer(answer))
            answers.append(answer)
        else:
            print("Got no answer.")
        customer_lock.acquire()
        try:
            active = customer_int.is_subscription_active()
        finally:
            customer_lock.release() 
        if not active:
            break
    if auto_file:
        file = open('./FilesReceived/' + filename, 'wb')
        for answer in answers:
            answer = Coder.decode_answer(answer)
            print(answer[0])
            file.write(answer[0])
        file.close()
        print("Saved file to ./FilesReceived/" + filename)
        if len(answers) < len(questions):
            print("File saved is partial - not all answers recevied.")

# Resolve Demands
def auto_customer_background(customer_int, customer_lock):
    while True:
        active = False
        customer_lock.acquire()
        try:
            active = customer_int.is_subscription_active()
        finally:
            customer_lock.release() 
        if not active:
            print("Subscription ended, closing background thread.")
            break
        time.sleep(0.05)
        customer_lock.acquire()
        try:
            ret = customer_int.resolve_demand()
        finally:
            customer_lock.release() 
        if not (ret is None):
            print("Resolved demand for: ")
            question, answer = ret
            print(Coder.str_question(question), "->", Coder.str_answer(answer))
    customer_lock.acquire()
    try:
        amount = customer_int.withdraw()
    finally:
        customer_lock.release()
    print("Withdrew funds:", amount)
    return

# Generate Queries for all chunks of a File
def generate_file_questions(customer_int, customer_lock):
    filename = input("File name:")
    customer_lock.acquire()
    try:
        print("Aquiring chunk num")
        chunks = customer_int.customer.validator.contract.functions.get_chunks_num(filename).call()
    finally:
        customer_lock.release()
    questions = []
    for x in range(chunks):
        question = Coder.encode_question([filename, x])
        questions.append(question)
        print("Genrating Questions...")
    return filename, questions


if __name__ == '__main__':
    #print(sys.argv)
    #print(len(sys.argv))
    if(len(sys.argv) < 2):
        print("USAGE: <filename> address [port]")
        sys.exit()
    address = sys.argv[1]
    port = PORT
    if(len(sys.argv) > 2):
        port = int(sys.argv[2])
    from main import HOST
    init_customer(address, HOST, port)


    

    



