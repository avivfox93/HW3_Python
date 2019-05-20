import time


def _word_file():
    return open('word.txt', mode='r')


def word_generator(char, include):
    file = _word_file()
    for line in file:
        for word in line.split(','):
            if include and (char.lower() in word.lower()):
                yield word
                time.sleep(1)
            elif (not include) and (not (char.lower() in word.lower())):
                yield word
                time.sleep(1)
    file.close()


def word_count():
    result = {}
    for i in range(ord('a'), ord('j')+1):
        result[chr(i)] = 0
    file = _word_file()
    for line in file:
        for word in line.split(','):
            for ch in word.lower():
                if ch < 'a' or ch > 'j':
                    continue
                result[ch] += 1
    file.close()
    return result
