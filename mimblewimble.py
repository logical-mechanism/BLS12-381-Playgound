from src.commitment import Commitment
from src.range import Range


def no_fee_no_leak():
    # the input_commitments
    input_commitments = [Commitment(123), Commitment(321)]
    input_range_proofs = [Range(secret_value=i.v, lower_bound=0, upper_bound=1234).generate_proof() for i in input_commitments]
    # the output_commitments
    output_commitments = [Commitment(222), Commitment(222)]
    output_range_proofs = [Range(secret_value=i.v, lower_bound=0, upper_bound=1234).generate_proof() for i in output_commitments]
    # the left r sum of the ouputs
    input_total = sum([i.r for i in input_commitments])
    output_total = sum([o.r for o in output_commitments])
    # compute the totals
    left = Commitment(0, output_total)
    right = Commitment(0, input_total)
    for i in input_commitments:
        left += i
    for o in output_commitments:
        right += o
    is_equal = (left == right)
    input_valid = all(Range.verify_proof(i, 0, 1234) for i in input_range_proofs)
    output_valid = all(Range.verify_proof(o, 0, 1234) for o in output_range_proofs)

    assert is_equal and input_valid and output_valid


def no_leak():
    fee = 1
    # the input_commitments
    input_commitments = [Commitment(123), Commitment(321)]
    input_range_proofs = [Range(secret_value=i.v, lower_bound=0, upper_bound=1234).generate_proof() for i in input_commitments]
    # the output_commitments
    output_commitments = [Commitment(222), Commitment(222 - fee)]
    output_range_proofs = [Range(secret_value=i.v, lower_bound=0, upper_bound=1234).generate_proof() for i in output_commitments]
    # the left r sum of the ouputs
    input_total = sum([i.r for i in input_commitments])
    output_total = sum([o.r for o in output_commitments])
    # compute the totals
    left = Commitment(0, output_total)
    right = Commitment(fee, input_total)
    for i in input_commitments:
        left += i
    for o in output_commitments:
        right += o
    is_equal = (left == right)
    input_valid = all(Range.verify_proof(i, 0, 1234) for i in input_range_proofs)
    output_valid = all(Range.verify_proof(o, 0, 1234) for o in output_range_proofs)

    assert is_equal and input_valid and output_valid


def fee_and_leak():
    fee = 1
    leak = 1
    # the input_commitments
    input_commitments = [Commitment(123), Commitment(321)]
    input_range_proofs = [Range(secret_value=i.v, lower_bound=0, upper_bound=1234).generate_proof() for i in input_commitments]
    # the output_commitments
    output_commitments = [Commitment(222 - leak), Commitment(222 - fee)]
    output_range_proofs = [Range(secret_value=i.v, lower_bound=0, upper_bound=1234).generate_proof() for i in output_commitments]
    # the left r sum of the ouputs
    input_total = sum([i.r for i in input_commitments])
    output_total = sum([o.r for o in output_commitments])
    # compute the totals
    left = Commitment(0, output_total)
    right = Commitment(fee + leak, input_total)
    for i in input_commitments:
        left += i
    for o in output_commitments:
        right += o
    is_equal = (left == right)
    input_valid = all(Range.verify_proof(i, 0, 1234) for i in input_range_proofs)
    output_valid = all(Range.verify_proof(o, 0, 1234) for o in output_range_proofs)

    assert is_equal and input_valid and output_valid


def bad_proof():
    fee = 1
    leak = 1
    # the input_commitments
    input_commitments = [Commitment(1233), Commitment(321)]
    input_range_proofs = [Range(secret_value=i.v, lower_bound=0, upper_bound=1234).generate_proof() for i in input_commitments]
    # the output_commitments
    output_commitments = [Commitment(222 - leak), Commitment(222 - fee)]
    output_range_proofs = [Range(secret_value=i.v, lower_bound=0, upper_bound=1234).generate_proof() for i in output_commitments]
    # the left r sum of the ouputs
    input_total = sum([i.r for i in input_commitments])
    output_total = sum([o.r for o in output_commitments])
    # compute the totals
    left = Commitment(0, output_total)
    right = Commitment(fee + leak, input_total)
    for i in input_commitments:
        left += i
    for o in output_commitments:
        right += o
    is_equal = (left == right)
    input_valid = all(Range.verify_proof(i, 0, 1234) for i in input_range_proofs)
    output_valid = all(Range.verify_proof(o, 0, 1234) for o in output_range_proofs)

    assert not (is_equal and input_valid and output_valid)


if __name__ == "__main__":
    no_fee_no_leak()
    no_leak()
    fee_and_leak()
    bad_proof()
