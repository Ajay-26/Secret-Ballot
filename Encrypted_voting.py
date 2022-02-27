# -*- coding: utf-8 -*-
"""
Created on Sat Dec 19 22:45:21 2020

@author: Ajay Sailopal
"""
import numpy as np
import math
import os
import gmpy2
from gmpy2 import mpz
import argparse
from Paillier import *

class Ballot:
    def __init__(self,C,T,p,q):
        self.num_candidates = C
        self.num_voters = T
        self.cryptosystem = Paillier(p,q)
        if(p*q < 10**(2*C)):
            print("Warning - n is too low")
    
    def convert_vote(self,vote):
        num_digits = 2
        x = 10**((num_digits)*(vote-1))
        return x
    
    def encrypt_votes(self,votes):
        enc_votes = []
        for i,vote in enumerate(votes):
            conv_vote = self.convert_vote(vote)
            enc_votes.append(self.cryptosystem.encrypt(conv_vote))
        self.enc_list = enc_votes
    
    def get_count_digit(self):
        prod = 1
        for enc_vote in self.enc_list:
            prod = gmpy2.f_mod(gmpy2.mul(prod,enc_vote), self.cryptosystem.n**2)
        count_digit = self.cryptosystem.decrypt(prod)
        self.count_digit = count_digit
        
    def compute_counts(self):
        self.get_count_digit()
        count_digits = self.count_digit
        counts = []
        while count_digits > 0:
            counts.append(count_digits%100)
            count_digits = count_digits//100
            print(count_digits)
        self.counts = counts
        
    def do_all(self, votes):
        self.encrypt_votes(votes)
        self.compute_counts()

T = 10
C = 2
p = mpz(641)
q = mpz(2**16 + 1)
my_ballot = Ballot(C,T,p,q)
vote_list= [1,1,1,1,1,2,2,2,2,2]
my_ballot.do_all(vote_list)
print(my_ballot.counts)