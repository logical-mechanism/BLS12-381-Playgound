# import time

from py_ecc.fields import optimized_bls12_381_FQ12 as FQ12

from src.bls12_381 import (combine, g1_identity, g1_point, g2_point, invert,
                           pair, scale)


def two_party_exchange_with_fee():
    # The initial amounts
    x0 = 100
    y0 = 25
    f0 = 0

    # x wants to send b to y and pay f' to f
    b = 15
    fee = 1

    x = x0 - fee - b
    y = y0 + b
    f = f0 + fee

    P = g1_point(1)
    Q = g2_point(1)
    QI = invert(Q)

    positive = [
        scale(P, x0),
        scale(P, y0),
        scale(P, f0),
        # These should be able to be removed due to non-degeneracy
        # scale(P, fee),
        # scale(P, b),
    ]
    negative = [
        scale(P, x),
        scale(P, y),
        scale(P, f),
        # These should be able to be removed due to non-degeneracy
        # scale(P, fee),
        # scale(P, b),
    ]

    # start_time = time.time()
    A = g1_identity
    for p in positive:
        A = combine(A, p)

    B = g1_identity
    for n in negative:
        B = combine(B, n)

    print(pair(Q, A) * pair(QI, B) == FQ12.one())
    # end_time = time.time()
    # elapsed_time = end_time - start_time
    # print(f"Elapsed time: {elapsed_time} seconds")


if __name__ == "__main__":
    two_party_exchange_with_fee()
