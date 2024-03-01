#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

"""

from myhdl import *


@block
def halfAdder(a, b, soma, carry):
    @always_comb
    def comb():
        soma.next = a ^ b
        carry.next = a and b

    return instances()


@block
def fullAdder(a, b, c, soma, carry):
    s1 = Signal(bool(0)) # (1)
    s2 = Signal(bool(0)) 
    s3 = Signal(bool(0))

    half_1 = halfAdder(a, b, s1, s2) # (2)
    half_2 = halfAdder(c, s1, soma, s3) # (3)

    @always_comb
    def comb():
        carry.next = s2 or s3 # (4)

    return instances()


@block
def adder2bits(x, y, soma, carry):
    c1 = Signal(bool(0))
    c2 = Signal(bool(0))
    c3 = Signal(bool(0))

    full_1 = fullAdder(x[0], y[0], c1, soma[0], c2)
    full_2 = fullAdder(x[1], y[1], c2, soma[1], c3)

    @always_comb
    def comb():
        carry.next = c3

    return instances()


@block
def adder(x, y, soma, carry):
    bit_width = len(x)
    carry_bits = [Signal(bool(0)) for _ in range(bit_width + 1)]

    adder_bits = [fullAdder(x[i], y[i], carry_bits[i], soma[i], carry_bits[i + 1]) for i in range(bit_width)]

    @always_comb
    def comb():
        carry.next = carry_bits[-1]

    return instances()
