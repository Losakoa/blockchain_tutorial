#!/usr/bin/env python

import hashlib
import json
from time import time
from uuid import uuid4

# https://hackernoon.com/learn-blockchains-by-building-one-117428612f46
# create class contructor for blockchain (an empty list to store transactions)
# each block is an index, a timestamp, a list of transactions, proof, and
# previous block

class blockchain(object):


    def __init__(self):
        self.chain = []
        self.current_transactions = []

        #Create new genesis block
        self.new_block(previous_hash=1, proof=100)



    def new_block(self,proof,previous_hash=None):
        """
        Create a new Block in the Blockchain
        :param proof: <int> The proof given by the Proof of Work algorithm
        :param previous_hash: (Optional) <str> Hash of previous Block
        :return: <dict> New Block
        """
        #creates a new block and adds it to the blockchain
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.current_transactions,
            'previous_hash': previous_hash or self.hash(self.chain)
        }

        # reset the current list of transactions
        self.current_transactions = []

        self.append(block)
        return block



    def new_transaction(self, sender, recipient, amount):
        # Adds a new transaction to the list of transactions
        """
        Creates a new transaction to go into the next mined Block
        :param sender: <str> Address of the Sender
        :param recipient: <str> Address of the Recipient
        :param amount: <int> Amount
        :return: <int> The index of the Block that will hold this transaction
        AKA it adds a transaction to the list and returns an index +1 which is
        the next block it goes on
        """

        self.current_transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount,
        })

        return self.last_block['index'] + 1


    def proof_of_work(self, last_proof):
        """
        Simple Proof of Work Algorithm:
         - Find a number p' such that hash(pp') contains leading 4 zeroes, where p is the previous p'
         - p is the previous proof, and p' is the new proof
        :param last_proof: <int>
        :return: <int>
        """
        proof = 0
        while self.valid_proof(last_proof, proof) is False:
            proof +=1
        return proof


    def valid_proof(last_proof, Proof):
        """
        Validates the Proof: Does hash(last_proof, proof) contain 4 leading zeroes?
        :param last_proof: <int> Previous Proof
        :param proof: <int> Current Proof
        :return: <bool> True if correct, False if not.
        """
        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"

    @staticmethod
    def hash(block):
        """
        Creates a SHA-256 hash of a Block
        :param block: <dict> Block
        :return: <str>
        """

        # we must make sure that the dictionary is Ordered, or we'll have inconsistant hashes
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()



    @property
    def last_block(self):
        # Returns the last block in the blockchain
        return self.chain[-1]
