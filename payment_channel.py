import pprint

from src.payment import Payment
from src.Registry.registry import Registry


def two_party_exchange_with_fee():

    X = Registry()
    xh = X.hash()
    print(f"User X: {xh}")

    Y = Registry()
    yh = Y.hash()
    print(f"User Y: {yh}")

    # F always exists as the fee owner
    F = Registry()
    fh = F.hash()
    print(f"Fee: {fh}")

    # this is going to act like our onchain merkle tree
    print("\nInitial State:")
    values = {
        xh: 100,
        yh: 25,
        fh: 0,
    }
    pprint.pp(values)

    # x wants to send b to y and pay f' to f
    b = 15
    fee = 1

    # calculate the final states
    x = values[xh] - fee - b
    y = values[yh] + b
    f = values[fh] + fee

    # the payment proof
    payment = Payment(
        X.boneh_lynn_shacham_signature(xh),
        (values[xh], values[yh], values[fh]),
        (x, y, f),
        Y,
        fee,
        b,
    )

    print("\nIs the payment valid?")
    print(payment)
    is_valid = payment.prove()
    print(is_valid)
    if is_valid is True:
        del values[xh]
        X.rerandomize()
        xh = X.hash()
        print(f"\nUser X Re-Randomized: {xh}")
        values[xh] = x
        values[yh] = y
        values[fh] = f

        print("\nFinal State:")
        pprint.pp(values)


if __name__ == "__main__":
    two_party_exchange_with_fee()
