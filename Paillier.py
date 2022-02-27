# -*- coding: utf-8 -*-
"""
Created on Fri Nov 20 09:15:49 2020

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
 
def phi(n):  # Leonard Euler's Totient Function
    y = 0
    for k in range(1, n + 1): 
        if gcd(n, k) == 1:  
            y += 1
    return y

def carmichael(n):  # Robert Daniel Carmichael's Function
    y = (phi(n) * 1/2) if (n > 4 and ((n & (n - 1)) == 0)) else phi(n)  
    return y
        
class Paillier:
    def __init__(self,p,q):
        self.p = p
        self.q = q
        self.n = p*q
        self.lam = carmichael(self.n)
        self.u = self.get_u()
        
    def get_g(self, i=0):
        random_state = gmpy2.random_state(i)
        g = gmpy2.mpz_random(random_state, self.n**2)
        return g
            
    def L(self,x):
        L_x = (x-1)/self.n
        return mpz(L_x)
    
    def get_u(self):
        i = 0
        while i >= 0:
            self.g = self.get_g(i)
            g_pow = gmpy2.powmod(self.g, self.lam, self.n**2)    
            L_g_pow = self.L(g_pow)
            i = i+1
            try:
                u = gmpy2.powmod(L_g_pow, -1, self.n)
                break
            except:
                pass
        self.u = u
        return u
    
    def get_r(self,i=0):
        random_state = gmpy2.random_state(i)
        r = gmpy2.mpz_random(random_state, self.n)
        return r
    
    def encrypt(self,m):
        i = 0
        while i >=0:    
            r = self.get_r(i)
            if gcd(r,self.n) == 1:
                break
            i = i+1
        c = gmpy2.f_mod(gmpy2.mul(mpz((self.g)**(m)),mpz(r**self.n)), self.n**2)
        return c
    
    def decrypt(self,c):
        c_pow = gmpy2.powmod(c, self.lam, self.n**2)
        L_c_pow = self.L(c_pow)
        prod = gmpy2.mul(L_c_pow, self.u)
        out = gmpy2.f_mod(prod, self.n)
        return out


p = 11
q = 13
my_paillier = Paillier(p,q)

m1 = 6
c1 = my_paillier.encrypt(m1)
d1 = my_paillier.decrypt(c1)

m2 = 3
c2 = my_paillier.encrypt(m2)
d2 = my_paillier.decrypt(c2)

c = gmpy2.f_mod(gmpy2.mul(c1,c2), my_paillier.n**2)
d = my_paillier.decrypt(c)

c_ = gmpy2.f_mod((c1**4), my_paillier.n**2)
d_ = my_paillier.decrypt(c_)