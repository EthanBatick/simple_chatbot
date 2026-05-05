from word_pool_10000 import words as word_pool

def score_first_letter(pool_map={}, word="") -> dict:
    #   points for match or no match
    p_match = 5
    p_no_match = -2

    first_letter = word[0]

    for w in pool_map:
        if w[0] == first_letter:
            pool_map[w] += p_match
        else:
            pool_map[w] += p_no_match

    return pool_map

def score_match_letters_over_tape(pool_map={}, word="") -> dict:
    #   points for match or no match
    p_match = 1
    p_no_match = 0

    for w in pool_map:
        tape_word = word
        for letter in w:
            try:
                tape_word = tape_word[tape_word.index(letter)+1:]
                pool_map[w] += p_match
            except:
                pool_map[w] += p_no_match

    return pool_map

def score_length_match(pool_map={}, word="") -> dict:
    p_every_extra_letter = -1

    len_word = len(word)

    for w in pool_map:
        pool_map[w] += max(abs(len(w)-len_word)-1,0)*p_every_extra_letter

    return pool_map

def score_more_commonly_used(pool_map={}, word="") -> dict:
    p_match = 1
    p_no_match = 0

    for w in word_pool[:len(word_pool)//5]:
        pool_map[w] += p_match
    
    return pool_map


def match_word(pool=word_pool, word="") -> str:

    pool_map = {}

    #   initialize points
    for w in pool:
        pool_map[w] = 0
    
    # check for perfect matc and only vote if needed
    if word in pool_map:
        return word
    #   score first letter
    pool_map = score_first_letter(pool_map=pool_map, word=word)
    #   score matching letters tapewise
    pool_map = score_match_letters_over_tape(pool_map=pool_map, word=word)
    #   score based on length of word
    pool_map = score_length_match(pool_map=pool_map, word=word)
    # score based on height in list aka how common its used
    pool_map = score_more_commonly_used(pool_map=pool_map, word=word)
    #   find the max score and return the word
    best_word = "test"
    for w in pool_map:
        if pool_map[w] > pool_map[best_word]:
            best_word = w
    return best_word