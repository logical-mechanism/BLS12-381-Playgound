from dataclasses import dataclass, field

from src.bls12_381 import field_order, g2_point, gt_identity, invert, pair
from src.commitment import Commitment
from src.Registry.element import Element


@dataclass
class Range:
    """
    Range is a cryptographic class for generating and verifying range proofs
    using BLS12-381 elliptic curve operations. If the lower and upper bounds
    are not provided they are assume to be 1 and the field prime. The proof
    solves a + b + w = y + 2d, assuming a - d = y and d - b = w, such that the
    equality a > d > b holds.

    It is assumed that the lower and upper bound values are public.

    Attributes:
        secret_value (int): The value to be proven within the range.
        lower_bound (int | None): The lower bound of the range.
        upper_bound (int | None): The upper bound of the range.
    """
    secret_value: int
    lower_bound: int | None = None
    upper_bound: int | None = None

    A_commit: Commitment = field(init=False)
    B_commit: Commitment = field(init=False)
    D_commit: Commitment = field(init=False)
    Y_commit: Commitment = field(init=False)
    W_commit: Commitment = field(init=False)
    K_commit: Commitment = field(init=False)
    right: Commitment = field(init=False)
    left: Commitment = field(init=False)
    Q: Element = field(init=False)
    QI: Element = field(init=False)

    def __post_init__(self):
        # if upper bound is not set then it becomes field prime minus one
        if self.upper_bound is None:
            self.upper_bound = field_order - 1
        # upper bound cant be larger than the field prime
        if self.upper_bound > field_order - 1:
            raise ValueError("Invalid range proof: Upper bound must be less than field order.")

        # if the lower bound is not set it becomes one
        if self.lower_bound is None:
            self.lower_bound = 1
        # lower bound cant be smaller then the identiy
        if self.lower_bound < 1:
            raise ValueError("Invalid range proof: Lower bound must be greater than zero.")

        # Set up D commitment
        self.D_commit = Commitment(self.secret_value)

        # Set up Y commitment
        y = self.upper_bound - self.secret_value
        if y <= 0:
            raise ValueError("Invalid range proof: Y value must be greater than zero.")
        self.Y_commit = Commitment(y)

        # Set up W commitment
        w = self.secret_value - self.lower_bound
        if w <= 0:
            raise ValueError("Invalid range proof: W value must be greater than zero.")
        self.W_commit = Commitment(w)

        # Set up K commitment (Y + 2D)
        self.K_commit = self.Y_commit + self.D_commit + self.D_commit

        # Set up A and B commitments with public randomness
        self.A_commit = Commitment(self.upper_bound, 0)
        self.B_commit = Commitment(self.lower_bound, 0)

        # Set up Q and Q Inverse
        self.Q = Element(g2_point(1))
        self.QI = invert(self.Q.value)

        # need to account for the random r values
        self.right = Commitment(0, self.W_commit.r)
        self.left = Commitment(0, self.K_commit.r)

    def __str__(self):
        return f"Range(\nK={self.K_commit.c},\nR={self.right.c},\nW={self.W_commit.c},\nL={self.left.c}\n)"

    def prove(self) -> bool:
        # Verifying that the commitments are consistent with the expected range proof
        check_r = pair(self.Q.value, (self.K_commit.c + self.right.c).value) * pair(self.QI, (self.A_commit.c + self.B_commit.c + self.W_commit.c + self.left.c).value) == gt_identity
        return check_r
