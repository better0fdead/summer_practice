def cipher_in(key_word, word):
    start = 33
    end = 122
    length = end - start + 1
    n_key_words = len(word) // len(key_word)
    helping_word = key_word * n_key_words + key_word[:len(word) % len(key_word)]

    chiffre = ""
    for i in range(len(word)):
        line = ord(helping_word[i]) - start
        column = ord(word[i]) - start

        if start + line + column <= end:
            symbol = chr(start + line + column)
        else:
            symbol = chr(start + line + column - length)
        chiffre = chiffre + symbol

    return chiffre

def cipher_out(key_word, word):
    start = 33
    end = 122
    length = end - start + 1

    n_key_words = len(word) // len(key_word)
    helping_word = key_word * n_key_words + key_word[:len(word) % len(key_word)]

    message = ""
    for i in range(len(word)):
        line = ord(helping_word[i]) - start
        letter = ord(word[i]) - start
        column = letter - line
        if column < 0:
            column = column + length
        symbol = chr(start + column)
        message = message + symbol

    return message