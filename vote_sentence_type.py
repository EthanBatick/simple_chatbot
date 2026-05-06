from sentence_type_pool import statement_start_words, command_start_words, question_start_words

def vote_sentence_type(normalized_sentence=[]):
    if normalized_sentence[0] in statement_start_words:
        return "statement"
    elif normalized_sentence[0] in question_start_words:
        return "question"
    elif normalized_sentence[0] in command_start_words:
        return "command"
    else:
        return None