# -*- coding: utf-8 -*-
"""
Created on Fri Dec 25 12:59:57 2020

@author: Ajay Sailopal
"""

import numpy as np
import math
import os
import gmpy2
from gmpy2 import mpz
import argparse

def sieve(n,limit):
    sieve_lim = gmpy2.isqrt(n) + 1
    lim += 1
    bitmap = gmpy2.xmpz(3)
    bitmap[4:lim:2] = -1
    for p in bitmap.iter_clear(3, sieve_lim):
        bitmap[p*p : lim : p+p] = -1
    return bitmap
    
def generate_primes(n=1000000): #Generates primes, checks from hash table if it is with n otherwise generates probably primes
    table = sieve(n,)
    for m in table.iter_clear(2, n):
        yield m
        
def gcd(a, b):  
    return gmpy2.gcd(a,b)

def gcd_list(num_list):
    l = len(num_list)
    if l == 2:
        return gcd(num_list[0], num_list[1])
    else:
        return gcd(gcd_list(num_list[0:l-1]), num_list[l-1])
 
def phi(n):  # Leonard Euler's Totient Function
    y = 0
    for k in range(1, n + 1): 
        if gcd(n, k) == 1:  
            y += 1
    return y

def carmichael(n):  # Robert Daniel Carmichael's Function
    y = (phi(n) * 1/2) if (n > 4 and ((n & (n - 1)) == 0)) else phi(n)  
    return y

def mul_lists(list1, list2):
    if len(list1) != len(list2):
        print("Not compatible")
        return 0
    else:
        out = 0
        for i in range(len(list1)):
            out = out + gmpy2.mul(list1[i],list2[i])
        return out
    
def get_coprime(list_int, num):
    if len(list_int) == 0:
        return True
    for elt in list_int:
        if gcd(num, elt) != 1:
            return False
    return True

def euclidean_extended(a, b):  
    # Base Case  
    if a == 0 :   
        return b,0,1
             
    gcd,x1,y1 = euclidean_extended(b%a, a)  
     
    # Update x and y using results of recursive  
    # call  
    x = y1 - (b//a) * x1  
    y = x1  
     
    return gcd,x,y 

    
class Simple_HE:
    def __init__(self,M,k,l):
        self.M = M
        self.k = k
        self.l = l
        self.m = self.get_m()
        self.s = self.get_s()
        
    def get_m(self):
        i = 0
        j = 0
        m = []
        while i >= 0:    
            random_state = gmpy2.random_state(i)
            random_i = gmpy2.mpz_random(random_state, self.M)
            if get_coprime(m, random_i) == True:
                m.append(random_i)
                j = j+1
            if j == self.k:
                return s
            j = j+1
        return s
            
    def get_s(self):
        i = 0
        s = []
        for p in range(self.k):
            s.append([])
            while i >= 0:
                random_state = gmpy2.random_state(i)
                random_i = gmpy2.mpz_random(random_state, self.m[p])
                s[p].append(random_i)
                if len(s[p] == self.l):
                    if gcd(gcd_list(s[p]), self.m[p]) == 1:
                        break
                    else:
                        s[p] = []
        self.s = s
                    
            
    def invert_s(self):
        s = self.s
        s_inv = []
        for i in range(self.k):
            s_inv.append([0]*self.l)
            for j in reversed(range(self.l)):
                if j > 2:
                    temp_gcd = gcd_list(s[i][0:j-1])
                    g, tmp, s_inv[i][j] = euclidean_extended(temp_gcd, s[i][j])
                if j == 2:
                    g, s_inv[i][0], s_inv[i][1] = euclidean_extended(s[i][0], s[i][1])
        self.s_inv = s_inv
        return

    def encrypt(self,X):
        c = []
        for idx in len(X):
            c.append(mul_lists(X, self.s[idx]))
        return c
    
    def decrypt(self):
        

