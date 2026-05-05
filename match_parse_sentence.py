import fuzzy_matching
'''
in_w = str(input())
while in_w != 'q':
    filtered = match_word(word_pool, in_w)
    print(match_word(word_pool, in_w), "\n\n\n")
    in_w = str(input())
'''
in_s = str(input())
while in_s != 'q':
    s_arr = in_s.split(" ")
    for i in range(len(s_arr)-1, -1, -1):
        if s_arr[i] == '':
            s_arr.pop(i)
    build_str = ""
    for w in s_arr:
        build_str += fuzzy_matching.match_word(word=w) + " "
    build_str = build_str[:-1]

    print(build_str, '\n')

    in_s = str(input())