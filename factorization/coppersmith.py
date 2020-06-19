import logging

from sage.all import PolynomialRing
from sage.all import ZZ
from sage.all import Zmod

from small_roots.coron import integer_bivariate
from small_roots.howgrave_graham import modular_univariate


def factorize_univariate(n, bits, msb_known, msb, lsb_known, lsb):
    """
    Recovers the prime factors from a modulus using Coppersmith's method.
    :param n: the modulus
    :param bits: the amount of bits of the target prime factor
    :param msb_known: the amount of known most significant bits of the target prime factor
    :param msb: the known most significant bits of the target prime factor
    :param lsb_known: the amount of known least significant bits of the target prime factor
    :param lsb: the known least significant bits of the target prime factor
    :return: a tuple containing the prime factors
    """
    pr = PolynomialRing(Zmod(n), "x")
    x = pr.gen()
    f = msb * 2 ** (bits - msb_known) + x * 2 ** lsb_known + lsb
    bound = 2 ** (bits - msb_known - lsb_known)
    m = 1
    while True:
        t = m
        logging.debug(f"Trying m = {m}, t = {t}...")
        for root in modular_univariate(f, n, m, t, bound):
            p = msb * 2 ** (bits - msb_known) + root * 2 ** lsb_known + lsb
            if p != 0 and n % p == 0:
                return p, n // p

        m += 1


def factorize_bivariate(n, p_bits, p_msb_known, p_msb, p_lsb_known, p_lsb, q_bits, q_msb_known, q_msb, q_lsb_known, q_lsb):
    """
    Recovers the prime factors from a modulus using Coppersmith's method.
    For more complex combinations of known bits, the coron module in the small_roots package should be used directly.
    :param n: the modulus
    :param p_bits: the amount of bits of the first prime factor
    :param p_msb_known: the amount of known most significant bits of the first prime factor
    :param p_msb: the known most significant bits of the first prime factor
    :param p_lsb_known: the amount of known least significant bits of the first prime factor
    :param p_lsb: the known least significant bits of the first prime factor
    :param q_bits: the amount of bits of the second prime factor
    :param q_msb_known: the amount of known most significant bits of the second prime factor
    :param q_msb: the known most significant bits of the second prime factor
    :param q_lsb_known: the amount of known least significant bits of the second prime factor
    :param q_lsb: the known least significant bits of the second prime factor
    :return: a tuple containing the prime factors
    """
    pr = PolynomialRing(ZZ, "x, y")
    x, y = pr.gens()
    f = (p_msb * 2 ** (p_bits - p_msb_known) + x * 2 ** p_lsb_known + p_lsb) * (q_msb * 2 ** (q_bits - q_msb_known) + y * 2 ** q_lsb_known + q_lsb) - n
    xbound = 2 ** (p_bits - p_msb_known - p_lsb_known)
    ybound = 2 ** (q_bits - q_msb_known - q_lsb_known)
    k = 1
    while True:
        logging.debug(f"Trying k = {k}...")
        for xroot, yroot in integer_bivariate(f, k, xbound, ybound):
            p = p_msb * 2 ** (p_bits - p_msb_known) + xroot * 2 ** p_lsb_known + p_lsb
            q = q_msb * 2 ** (q_bits - q_msb_known) + yroot * 2 ** q_lsb_known + q_lsb
            if p * q == n:
                return p, q

        k += 1
