from cipher import cipher_in, cipher_out

def check(st, key):
    if st == cipher_out(key, cipher_in(key, st)):
        return 0
    else:
        return 1

def lower_case(key):
    st = "privet"
    return check(st, key)

def with_numbers_case(key):
    st = "123chess321"
    return check(st, key)

def upper_case(key):
    st = "AleXandR13"
    return check(st, key)

def special_symb_case(key):
    st = "-_1fs*/fafFAWF?21"
    return check(st, key)
    
def testing():
    key = "keyword"

    errors = 0
    errors += lower_case(key)
    errors += with_numbers_case(key)
    errors += upper_case(key)
    errors += special_symb_case(key)

    return errors


if __name__ == "__main__":
    errors = testing()
    print("Testing has ended with", errors, "failed tests")