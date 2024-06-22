import pytest

from src.sha3_256 import fiat_shamir_heuristic, generate


def test_empty_string_hash():
    h = generate("")
    assert h == "a7ffc6f8bf1ed76651c14756a061d662f580ff4de43b49fa82d80a4b80f8434a"


def test_hello_world_hash():
    input_string = "Hello, world!"
    h = generate(input_string)
    assert h == "f345a219da005ebe9c1a1eaad97bbf38a10c8473e41d0af7fb617caa0c6aa722"


def test_empty_fiat_shamir_heuristic():
    fsh = fiat_shamir_heuristic("", "", "")
    assert fsh == "a7ffc6f8bf1ed76651c14756a061d662f580ff4de43b49fa82d80a4b80f8434a"


def test_real_fiat_shamir_heuristic():
    fsh = fiat_shamir_heuristic(
        "86f0c64bd433568dd92751f0bee97feaaeee6f3c2144b210be68d2bc85253b1994703caf7f8361ccf246fef52c0ad859",
        "97f1d3a73197d7942695638c4fa9ac0fc3688c4f9774b905a14e3a3f171bac586c55e83ff97a1aeffb3af00adb22c6bb",
        "a2cbc5c3c72a7bc9047971345df392a67279d2f32082891976d913c699885c3ff9a90a8ea942bef4729cf93f526521e4")
    assert fsh == "524fb8209e14641b3202adcab15bddae592b83fafc34d74abb79b572bd883930"


if __name__ == "__main__":
    pytest.main()
