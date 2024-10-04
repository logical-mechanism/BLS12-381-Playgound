from py_ecc.bls.g2_primitives import G1_to_pubkey
from py_ecc.fields import optimized_bls12_381_FQ as FQ
from py_ecc.optimized_bls12_381 import b
from py_ecc.optimized_bls12_381 import field_modulus as p


def string_to_int(s):
    data_int = int(s.encode('utf-8').hex(), 16)
    if data_int >= p:
        raise ValueError("Data too large to fit in field")
    return data_int


def legendre_symbol(a, p):
    """Check if a is a quadratic residue modulo p."""
    if a % p == 0:
        return True  # 0 is always a quadratic residue
    exponent = (p - 1) // 2
    legendre_symbol = pow(a, exponent, p)
    return legendre_symbol == 1


def modular_sqrt(a, p):
    """ Find a quadratic residue (mod p) of 'a'. p
        must be an odd prime.

        Solve the congruence of the form:
            x^2 = a (mod p)
        And returns x. Note that p - x is also a root.

        0 is returned is no square root exists for
        these a and p.

        The Tonelli-Shanks algorithm is used (except
        for some simple cases in which the solution
        is known from an identity). This algorithm
        runs in polynomial time (unless the
        generalized Riemann hypothesis is false).
    """
    # Simple cases
    #
    if legendre_symbol(a, p) != 1:
        return 0
    elif a == 0:
        return 0
    elif p == 2:
        return 0
    elif p % 4 == 3:
        return pow(a, (p + 1) // 4, p)

    # Partition p-1 to s * 2^e for an odd s (i.e.
    # reduce all the powers of 2 from p-1)
    #
    s = p - 1
    e = 0
    while s % 2 == 0:
        s /= 2
        e += 1

    # Find some 'n' with a legendre symbol n|p = -1.
    # Shouldn't take long.
    #
    n = 2
    while legendre_symbol(n, p) != -1:
        n += 1

    # Here be dragons!
    # Read the paper "Square roots from 1; 24, 51,
    # 10 to Dan Shanks" by Ezra Brown for more
    # information
    #

    # x is a guess of the square root that gets better
    # with each iteration.
    # b is the "fudge factor" - by how much we're off
    # with the guess. The invariant x^2 = ab (mod p)
    # is maintained throughout the loop.
    # g is used for successive powers of n to update
    # both a and b
    # r is the exponent - decreases with each update
    #
    x = pow(a, (s + 1) / 2, p)
    b = pow(a, s, p)
    g = pow(n, s, p)
    r = e

    while True:
        t = b
        m = 0
        for m in range(r):
            if t == 1:
                break
            t = pow(t, 2, p)

        if m == 0:
            return x

        gs = pow(g, 2 ** (r - m - 1), p)
        g = (gs * gs) % p
        x = (x * gs) % p
        b = (b * g) % p
        r = m


def short_weierstrass_form(x: int) -> int:
    return (pow(x, 3, p) + 4) % p


def find_valid_point(x: int) -> tuple[int, int, int]:
    for o in range(p):
        d = (x + o) % p
        y_squared = short_weierstrass_form(d)
        y = modular_sqrt(y_squared, p)
        if y != 0:
            return x, y, o
    raise ValueError("No valid point found")


def verify_point_on_curve(point):
    x, y = point
    return pow(y, 2, p) - pow(x, 3, p) == b


def compress_point(point):
    x, y = point
    G = (
        FQ(x),
        FQ(y),
        FQ(1),
    )
    compressed = G1_to_pubkey(G)
    return compressed


def map_to_point(s: str) -> tuple[str, int]:
    d = string_to_int(s)
    x, y, o = find_valid_point(d)
    point = (x + o, y)
    return compress_point(point).hex(), o


def point_to_map(p: str, o: int) -> str:
    compressed_point = bytes.fromhex(p)
    x_bytes = compressed_point[1:]
    x = int.from_bytes(x_bytes, byteorder='big')
    return bytes.fromhex(hex(x - o)[2:]).decode('ascii')
