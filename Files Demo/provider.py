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




class ProviderInterface: # This class is intended for the provider to interact with the blockchain. 
    # It doesn't do any computing itself, and doesn't interact with the customers.
    def __init__(self, address, _max_queries=0):
        validator_address = Solver.init_validator(address)
        self.provider = Provider(address, validator_address)
        self._terminate = False
        self.customers = []
        self.unsolved_questions = {}
        self.unsolved_stack = []
        self.solved_questions = {}
        self.done_questions = {}
        self.urgent = []
        self.latest_signature = None
        self.latest_hashes = []
        self.latest_unanswered = 0
        self.customers_demanded = []
        self.latest_ack = dict()
        self.acks = dict()
        self.max_queries = _max_queries

    def get_active_customers(self):
        customers = []
        for c in self.provider.get_customers():
            if self.provider.is_subscription_active(c):
                customers.append(c)
        return customers

    def check_signature(self, customer_address, ack):
        questions_hashes, unanswered, signature = ack.get_all()
        return Signer.check_sig(questions_hashes, unanswered, self.provider.get_contract_address(customer_address), signature, customer_address)

    def demand_signature(self, customer_address, question, answer):
        #questions_hashes, unanswered, signature = [], 0, 0
        if customer_address in self.customers_demanded:
            print(shorten_addr(customer_address), "Tried demanding signature - but already demanding.")
            return False
        ack = self.latest_ack[customer_address]
        if ack is None:
            print(shorten_addr(customer_address), "Tried demanding signature - no valid ack.")
            return False
        self.customers_demanded.append(customer_address)
        questions_hashes, unanswered, signature = ack.get_all()
        demanded = self.provider.demand_signature(customer_address, question, questions_hashes, unanswered, signature, answer)
        if demanded:
            print(shorten_addr(customer_address), "Demanded signature.")
        else:
            print(shorten_addr(customer_address), "Tried demanding signature - failed.")
        return demanded

    def demand_all(self):
        demanded = []
        for address in self.get_active_customers():
            if address in self.customers_demanded:
                continue
            if self.latest_ack[address] is not None and 0 < len(self.solved_questions[address].keys()):
                qa = self.solved_questions[address][list(self.solved_questions[address].keys())[0]]
                if self.demand_signature(address, qa.get_question(), qa.get_answer()):
                    demanded.append(address)
        return demanded

    def exec_demands(self):
        to_remove = []
        for address in self.customers_demanded:
            closed = self.provider.exec_demand(address)
            if closed:
                to_remove.append(address)
        for address in to_remove:
            self.customers_demanded.remove(address)
        return to_remove

    def check_demands(self):
        to_remove = []
        for address in self.customers_demanded:
            ret = self.provider.check_demand(address)
            if ret is not None:
                hashes, unanswered, signature = ret
                closed = self.register_ack(address, Ack(hashes, unanswered, signature))
                if closed is not None:
                    for q in closed:
                        print(shorten_addr(address), "Got new answer ack:", Coder.str_question(q))
                to_remove.append(address)
        for address in to_remove:
            self.customers_demanded.remove(address)
        return to_remove


    def get_different_ack(self, customer_address, ack):
        if not self.check_signature(customer_address, ack):
            return None
        for ack2 in self.acks[customer_address]:
            if ack.is_different(ack2):
                return ack2
        self.acks[customer_address].append(ack)
        return None


    def register_ack(self, customer_address, ack):
        #print(customer_address, hashes, unanswered, signature)
        if len(ack.get_hashes()) < 0:
            return None
        if not self.check_signature(customer_address, ack):
            return None
        if ack.is_newer_than(self.latest_ack[customer_address]):
            self.latest_ack[customer_address] = ack
            to_close = []
            for h in ack.get_answered_hashes():
                if h in self.solved_questions[customer_address]:
                    to_close.append(self.solved_questions[customer_address][h].get_question())
                if h in self.unsolved_questions[customer_address]:
                    to_close.append(self.solved_questions[customer_address][h].get_question())
            for q in to_close:
                self.close_question(customer_address, q)
            return to_close
        elif ack.is_different(self.latest_ack[customer_address]):
            self.acks[customer_address].append(ack)
        return None

    def set_urgent(self, appeals):
        self.urgent = appeals

    def get_urgent(self):
        return self.urgent

    def get_next_question(self):
        if len(self.unsolved_stack) < 1:
            return None
        return self.unsolved_stack[0]

    def create_subscription(self, customer_address):
        self.customers.append(customer_address)
        self.unsolved_questions[customer_address] = dict()
        self.solved_questions[customer_address] = dict()
        self.done_questions[customer_address] = dict()
        self.acks[customer_address] = dict()
        self.latest_ack[customer_address] = None
        return self.provider.create_subscription(customer_address)

    def register_question(self, customer_address, question):
        if not self.provider.get_validator().is_valid_question(question):
            return False
        qa = QA(question, asker = customer_address)
        self.unsolved_questions[customer_address][qa.get_hash()] = qa
        self.unsolved_stack.append(qa)
        return True

    def register_answer(self, customer_address, question, answer):
        q_hash = Signer.hash(question)
        qa = None
        if q_hash in self.unsolved_questions[customer_address]:
            qa = self.unsolved_questions[customer_address][q_hash]
            self.unsolved_stack.remove(qa)
            qa.set_answer(answer)
            del self.unsolved_questions[customer_address][q_hash]
        if qa is None:
            qa = QA(question, asker=customer_address, answer=answer)
        self.solved_questions[customer_address][q_hash] = qa

    def close_question(self, customer_address, question):
        q_hash = Signer.hash(question)
        qa = None
        if q_hash in self.unsolved_questions[customer_address]:
            qa = self.unsolved_questions[customer_address][q_hash]
            self.unsolved_stack.remove(qa)
            del self.unsolved_questions[customer_address][q_hash]
        if q_hash in self.solved_questions[customer_address]:
            qa = self.solved_questions[customer_address][q_hash]
            del self.solved_questions[customer_address][q_hash]
        if qa is None:
            qa = QA(question, asker=customer_address)
        self.done_questions[customer_address][q_hash] = qa

    def get_new_answers(self, customer_address, close=True):
        return self.solved_questions[customer_address].values()

    def is_subscription_active(self, customer_address):
        return self.provider.is_subscription_active(customer_address)

    def is_appealing(self, customer_address):
        return self.provider.check_for_appeal(customer_address) is not None

    def get_answer(self, customer_address, question):
        q_hash = Signer.hash(question)
        answer = None
        if q_hash in self.solved_questions[customer_address]:
            answer = self.solved_questions[customer_address][q_hash].get_answer()
        elif q_hash in self.done_questions[customer_address]:
            answer = self.done_questions[customer_address][q_hash].get_answer()
        return answer


    def check_for_appeals(self):
        # returns None or a question appealed by the specified customer
        appeals = []
        for address in self.get_active_customers():
            appeal = self.provider.check_for_appeal(address)
            if(appeal is not None):
                appeals.append(appeal)
                closed = self.register_ack(address, appeal.get_ack())
                if not closed is None:
                    for q in closed:
                        print(shorten_addr(customer_address), "Got new answer ack:", Coder.str_question(q))
        return appeals

    def resolve_appeal(self, customer_address, appeal):
        # submit answer to resolve appeal by the specified customer
        if self.overflow(customer_address):
            print(shorten_addr(customer_address), "dismissed appeal - max queries met")
            return True
        question = appeal.get_question()
        q_hash = Signer.hash(question)
        answer = self.get_answer(customer_address, question)
        if answer is not None:
            self.provider.resolve_appeal(customer_address, answer)
            return True
        if q_hash not in self.unsolved_questions[customer_address]:
            self.register_question(customer_address, question)
        return False

    def can_overflow(self, customer_address):
        if self.latest_ack[customer_address] is None:
            return False
        if self.max_queries == 0:
            return False
        questions_hashes, unanswered, signature = self.latest_ack[customer_address].get_all()
        if len(questions_hashes) - unanswered <= MAX_QUERIES:
            return False
        return True

    def overflow(self, customer_address):
        if not self.can_overflow(customer_address):
            return False
        questions_hashes, unanswered, signature = self.latest_ack[customer_address].get_all()
        try:
            self.provider.overflow(customer_address, questions_hashes, unanswered, signature)
        except Exception as e:
            traceback.print_tb(e.__traceback__)
            print("ERROR:",e)
            return False
        print(shorten_addr(customer_address), "Overflow: closed contract")
        return True

    def withdraw(self, customer_address):
        # withdraws money from the subscription of the specified customer
        return self.provider.withdraw(customer_address)

    def withdraw_all(self):
        amount = 0
        # withdraws money from the subscription of the specified customer
        for customer_address in self.provider.get_customers():
            amount += self.withdraw(customer_address)
        return amount

    def terminate(self):
        self._terminate = True

    def terminated(self):
        return self._terminate

def shorten_addr(addr):
    s = str(addr)
    if len(s) < 8:
        s += "-"*(8-len(s))
    return "[" + s[:7] + "]"



def init_provider(address, host, port):
    provider_int = None
    
    # Get Behavior of Provider from user
    PROVIDER_APPEAL_ONLY = False
    PROVIDER_WAIT_APPEAL = False
    PROVIDER_DROP_APPEAL = False
    PROVIDER_WRONG_ANSWER = False
    PROVIDER_IMMIDIEATE_DEMAND = False
    STOP_ON_MAX = False

    '''
    value = input("Should the provider send answers? (y/n):")
    if value == "y":
        PROVIDER_APPEAL_ONLY = False
    value = input("Should the provider wait for the last minute with appeals? (y/n):")
    if value == "y":
        PROVIDER_WAIT_APPEAL = True
    value = input("Should the provider drop appeals? (y/n):")
    if value == "y":
        PROVIDER_DROP_APPEAL = True
    value = input("Should the provider provide wrong answers (in appeals also)? (y/n):")
    if value == "y":
        PROVIDER_WRONG_ANSWER = True
    value = input("Should the provider demand a signature for every answer? (y/n):")
    if value == "y":
        PROVIDER_IMMIDIEATE_DEMAND = True
    value = input("Should the provider stop answering when max queries met? (y/n):")
    if value == "y":
        STOP_ON_MAX = True'''

    global MAX_QUERIES
    if not STOP_ON_MAX:
        MAX_QUERIES = 0

    # Create all threads
    provider_int = ProviderInterface(address, MAX_QUERIES)
    provider_lock = Lock()

    to_join = []
    x = Thread(target=handle_appeals_provider, args=(provider_lock, provider_int, PROVIDER_WAIT_APPEAL, PROVIDER_DROP_APPEAL))
    x.start()
    to_join.append(x)
    x = Thread(target=solve_provider, args=(provider_lock, provider_int, Solver.solve, PROVIDER_WRONG_ANSWER, PROVIDER_IMMIDIEATE_DEMAND))
    x.start()
    to_join.append(x)
    x = Thread(target=handle_input_provider, args=(provider_lock, provider_int))
    x.start()
    to_join.append(x)
    
    # Receive connections
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen()
        print("[x] Started listening: ", (host, port))
        s.settimeout(1)
        while True:
            try:
                conn, addr = s.accept()
            except socket.timeout:
                terminated = False
                provider_lock.acquire()
                try:
                    terminated = provider_int.terminated()
                except Exception as e:
                    traceback.print_tb(e.__traceback__)
                    print("ERROR:",e)
                finally:
                    provider_lock.release()
                if(terminated):
                    break
            else:
                x = Thread(target=provider_handle_client, args=(provider_lock, provider_int, conn, addr, PROVIDER_APPEAL_ONLY, STOP_ON_MAX))
                x.start()
                to_join.append(x)
        for x in to_join:
            x.join()
        s.close()
        print("[x] Closing server")

def handle_appeals_provider(provider_lock, provider_int, PROVIDER_WAIT_APPEAL, PROVIDER_DROP_APPEAL):
    #main logic of provider
    while(True):
        #Check if provider terminated
        terminated = False
        provider_lock.acquire()
        try:
            terminated = provider_int.terminated()
        except Exception as e:
            traceback.print_tb(e.__traceback__)
            print("ERROR:",e)
        finally:
            provider_lock.release()
        if(terminated):
            print("[x] Closing appeals provider")
            return
        time.sleep(0.1)

        # Check for all appeals
        appeals = []
        provider_lock.acquire()
        try:
            appeals = provider_int.check_for_appeals()
        except Exception as e:
            traceback.print_tb(e.__traceback__)
            print("ERROR:",e)
        finally:
            provider_lock.release()
        if PROVIDER_DROP_APPEAL:
            appeals = []

        # Resolve every appeal if able
        unresolved = []
        for appeal in appeals:
            customer_address = appeal.get_customer_address()
            deadline_block, question = appeal.get_end_of_service_block(), appeal.get_question()
            if PROVIDER_WAIT_APPEAL and w3.eth.blockNumber < deadline_block - 2:
               continue
            provider_lock.acquire()
            try:
                resolved = provider_int.resolve_appeal(customer_address, appeal)
            except Exception as e:
                traceback.print_tb(e.__traceback__)
                print("ERROR:",e)
                print(shorten_addr(customer_address), "Couldn't resolve appeal! Is answer incorrect?")
            finally:
                provider_lock.release()
            if resolved:
                print(shorten_addr(customer_address), "Resolved appeal")
            else:
                print(shorten_addr(customer_address), "Appealed an unsent question")
                unresolved.append(appeal)

        # Set unresolved appeals to urgent
        provider_lock.acquire()
        try:
            resolved = provider_int.set_urgent(unresolved)
        except Exception as e:
            traceback.print_tb(e.__traceback__)
            print("ERROR:",e)
        finally:
            provider_lock.release()

        # Check for status of demands
        solved = []
        provider_lock.acquire()
        try:
            solved = provider_int.check_demands()
        except Exception as e:
            traceback.print_tb(e.__traceback__)
            print("ERROR:",e)
        finally:
            provider_lock.release()
        for address in solved:
            print(shorten_addr(address), "Has resolved the signature demand")

        # Execute unresolved timed demands
        solved = []
        provider_lock.acquire()
        try:
            solved = provider_int.exec_demands()
        except Exception as e:
            traceback.print_tb(e.__traceback__)
            print("ERROR:",e)
        finally:
            provider_lock.release()
        for address in solved:
            print(shorten_addr(address), "Channel closed - demand not resolved")

        # Try withdrawing funds
        if w3.eth.blockNumber % 10 == 0:
            amount = 0
            provider_lock.acquire()
            try:
                amount = provider_int.withdraw_all()
            except Exception as e:
                traceback.print_tb(e.__traceback__)
                print("ERROR:",e)
            finally:
                provider_lock.release()
            if amount > 0:
                print("Withdrew funds:", amount)

def solve_provider(provider_lock, provider_int, solver, PROVIDER_WRONG_ANSWER, PROVIDER_IMMIDIEATE_DEMAND):
    solved_counter = 0
    while True:
        # Check if Provider terminated
        terminated = False
        provider_lock.acquire()
        try:
            terminated = provider_int.terminated()
        except Exception as e:
            traceback.print_tb(e.__traceback__)
            print("ERROR:",e)
        finally:
            provider_lock.release()
        if(terminated):
            print("[x] Closing solve provider")
            return
        time.sleep(0.1)

        # Get Urgent to Solve
        urgent = []
        question = None
        customer_address = None
        provider_lock.acquire()
        try:
            urgent = provider_int.get_urgent()
            qa = provider_int.get_next_question()
        except Exception as e:
            traceback.print_tb(e.__traceback__)
            print("ERROR:",e)
        finally:
            provider_lock.release()
        if qa is not None:
            customer_address = qa.get_asker()
            question = qa.get_question()

        # Get most Urgent Question
        if len(urgent) > 0:
            closest = urgent[0].get_end_of_service_block()
            for appeal in urgent:
                add = appeal.get_customer_address()
                deadline_block, q = appeal.get_end_of_service_block(), appeal.get_question()
                if deadline_block < closest:
                    customer_address = add
                    question = q
                    closest = deadline_block

        # Sleep if no question to solve
        if question is None:
            time.sleep(0.5)
            continue

        # Solve most recent or urgent
        answer = solver(question, wrong=PROVIDER_WRONG_ANSWER)
        print(shorten_addr(customer_address), "Solved:", Coder.str_question(question), "->", Coder.str_answer(answer))
        provider_lock.acquire()
        try:
            provider_int.register_answer(customer_address, question, answer)
            if(PROVIDER_IMMIDIEATE_DEMAND):
                provider_int.demand_signature(customer_address, question, answer)
        except Exception as e:
            traceback.print_tb(e.__traceback__)
            print("ERROR:",e)
        finally:
            provider_lock.release()

def handle_input_provider(provider_lock, provider_int): 
    while(True):
        value = input("")
        if value ==  "q":
            provider_lock.acquire()
            try:
                provider_int.terminate()
            except Exception as e:
                traceback.print_tb(e.__traceback__)
                print("ERROR:",e)
            finally:
                provider_lock.release()
            print("[x] Closing input provider")
            return
        elif value == "demand":
            ret = None
            provider_lock.acquire()
            try:
                ret = provider_int.demand_all()
            except Exception as e:
                print("ERROR demand:",e)
            finally:
                provider_lock.release()
            print("[x] Demanded", len(ret), "signatures")
            for a in ret:
                print(shorten_addr(a), "Demanded signature")
        else:
            print("[x] Unknown command:", value)


def provider_handle_client(provider_lock, provider_int, conn, addr, PROVIDER_APPEAL_ONLY, STOP_ON_MAX):
    customer_address = 0x000000000
    state = 0
    with conn:
        conn.settimeout(1)
        print(shorten_addr(customer_address), "New Connection: ", addr)
        state = 0
        # Getting Address
        while True:
            terminated = False
            provider_lock.acquire()
            try:
                terminated = provider_int.terminated()
            except Exception as e:
                traceback.print_tb(e.__traceback__)
                print("ERROR:",e)
            finally:
                provider_lock.release()

            if(terminated):
                conn.close()
                print(shorten_addr(customer_address), "Closing connection", addr)
                return
            try:
                msg = receive_dict(conn)
                if msg is None:
                    break
            except:
                continue
            # get next message
            if state == 0:
                #print(addr, "Received: " + str(msg))
                if not msg:
                    print(addr, "ERROR: connection ended?")
                    return
                if "type" in msg and msg["type"] == "address" and "address" in msg:
                    customer_address = msg["address"]
                    print(shorten_addr(customer_address), "Got Address. (" + str(addr) + ")")
                    # Creating contract and sending it:
                    sub_add = None
                    provider_lock.acquire()
                    try:
                        sub_add = provider_int.create_subscription(customer_address)
                    except Exception as e:
                        traceback.print_tb(e.__traceback__)
                        print("ERROR:",e)
                    finally:
                        provider_lock.release()

                    if not sub_add:
                        print(shorten_addr(customer_address), "No subscription address! Returning.")
                        return
                    print(shorten_addr(customer_address), "Sending subscription...")
                    send_dict(conn,{
                        "type": "subscription",
                        "address": sub_add
                        })
                    state = 1
                    print(shorten_addr(customer_address), "Waiting for msg")
                    continue

            # Getting questions and sending answers
            if state == 1:
                active = True
                provider_lock.acquire()
                try:
                    active = provider_int.is_subscription_active(customer_address)
                except Exception as e:
                    traceback.print_tb(e.__traceback__)
                    print("ERROR:",e)
                finally:
                    provider_lock.release()

                if not active:
                    print(shorten_addr(customer_address), "Subscription no longer active.")
                    conn.close()
                    print(shorten_addr(customer_address), "Closing connection", addr)
                    return

                provider_lock.acquire()
                try:
                    demanding = customer_address in provider_int.customers_demanded
                except Exception as e:
                    traceback.print_tb(e.__traceback__)
                    print("ERROR:",e)
                finally:
                    provider_lock.release()
                if demanding:
                    continue
                # Dismiss Broken Messages
                if not msg:
                    break
                if "type" not in msg:
                    continue

                # Handle Msgs by Types
                elif msg["type"] == "new_question":

                    # Decode Message
                    question = Coder.stream_to_encoded(msg["question"])
                    hashes = str_to_bytes(msg["hashes"])
                    unanswered = msg["unanswered"]
                    signature = str_to_bytes(msg["signature"])
                    print(shorten_addr(customer_address), "Got new question:", Coder.str_question(question))

                    # Register Ack
                    closed = []
                    provider_lock.acquire()
                    try:
                        closed = provider_int.register_ack(customer_address, Ack(hashes, unanswered, signature))
                    except Exception as e:
                        traceback.print_tb(e.__traceback__)
                        print("ERROR:",e)
                    finally:
                        provider_lock.release()
                    if closed is None:
                        print(shorten_addr(customer_address), "Invalid ack! Ignoring.")
                        continue
                    for q in closed:
                        print(shorten_addr(customer_address), "Got new answer ack:", Coder.str_question(q))

                    # Check for Overflow
                    overflow = False
                    provider_lock.acquire()
                    try:
                        overflow = provider_int.can_overflow(customer_address)
                    except Exception as e:
                        traceback.print_tb(e.__traceback__)
                        print("ERROR:",e)
                    finally:
                        provider_lock.release()
                    
                    if overflow:
                        print(shorten_addr(customer_address), "Max queries met! Ignoring.")
                        continue

                    #Register Question
                    qa = QA(question)
                    h = qa.get_hash()
                    if h not in hashes:
                        print(shorten_addr(customer_address), "Question not in hashes! Ignoring.")
                    
                    ret = False
                    provider_lock.acquire()
                    try:
                        ret = provider_int.register_question(customer_address, question)
                    except Exception as e:
                        traceback.print_tb(e.__traceback__)
                        print("ERROR:",e)
                    finally:
                        provider_lock.release()
                    if not ret:
                        print(shorten_addr(customer_address), "Invalid question! Ignoring.")
                

                elif msg["type"] == "ack":
                    # Decode Msg
                    hashes = str_to_bytes(msg["hashes"])
                    unanswered = msg["unanswered"]
                    signature = str_to_bytes(msg["signature"])

                    # Register Ack
                    closed = []
                    provider_lock.acquire()
                    try:
                        closed = provider_int.register_ack(customer_address, Ack(hashes, unanswered, signature))
                    except Exception as e:
                        traceback.print_tb(e.__traceback__)
                        print("ERROR:",e)
                    finally:
                        provider_lock.release()
                    if closed is None:
                        print(shorten_addr(customer_address), "Got useless ack...")
                    elif len(closed) < 1:
                        print(shorten_addr(customer_address), "Got stale ack")
                    else:
                        for q in closed:
                            print(shorten_addr(customer_address), "Got new answer ack:", Coder.str_question(q))
                    
                elif msg["type"] == "send_answer":
                    # Check if specific question needed (currently useless)
                    question = None
                    if "question" in msg:
                        question = Coder.stream_to_encoded(msg["question"])
                    q = question
                    if q is not None:
                        q = Coder.str_question(q)
                    print(shorten_addr(customer_address), "Asking for new answers, prefered question:", q)

                    # Get all qas
                    qas = []
                    provider_lock.acquire()
                    try:
                        qas = provider_int.get_new_answers(customer_address)
                    except Exception as e:
                        traceback.print_tb(e.__traceback__)
                        print("ERROR:",e)
                    finally:
                        provider_lock.release()

                    # Send all answers
                    questions = [Coder.encoded_to_stream(qa.get_question()) for qa in qas]
                    answers = [Coder.encoded_to_stream(qa.get_answer()) for qa in qas]
                    #print(shorten_addr(customer_address), "Almost sent answers:", len(answers))
                    if PROVIDER_APPEAL_ONLY:
                        questions = answers = []
                    send_dict(conn, {
                        "type": "answer",
                        "questions": questions,
                        "answers": answers
                        })
                    print(shorten_addr(customer_address), "Sent answers:", len(answers))
                else:
                    print(shorten_addr(customer_address), "??? Received: " + str(msg))
        print(shorten_addr(customer_address), "Ended Connection.")

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
    init_provider(address, HOST, port)


    

    



