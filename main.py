import match_parse_sentence
import vote_sentence_type
from linking_verb_pool import linking_verbs
from name_pool_1000 import names
import random
import Context

def send_response(message="", bot_name="placeholder"):
    print(bot_name + ": " + message)
    pass

chat_context = Context.Context()

user_input = None
while user_input != 'q':
    user_input = str(input("You: "))
    normalized_sentence = match_parse_sentence.patch_parse_sentence(user_input)

    #   first we handle the simplest cases, example: if
    #   the sentence contains a goodbye or hello we instantly snap to greeting
    #   or goodbye



    #   empty message
    empty_input_responses = [
    "say something",
    "you didn't type anything",
    "i need some words to respond to",
    "try typing a message",
    "i'm listening"
]
    if len(normalized_sentence) == 0:
        send_response(random.choice(empty_input_responses))



    #   handle hello's
    hello_responses = [
    "hello",
    "hey",
    "hi, how can I help?",
    "what's up?",
    "hey, good to see you"
]
    if bool(set(normalized_sentence) & set(["hello", "hi", "hey"])):
        send_response(random.choice(hello_responses))
        continue



    #   handle goodbyes
    goodbye_responses = [
    "goodbye",
    "bye",
    "see you later",
    "talk to you later",
    "catch you later"
]
    if bool(set(normalized_sentence) & set(["goodbye", "bye", "ciao"])):
        send_response(random.choice(goodbye_responses))
        continue


    #   now we split the sentence into 3 main types of sentences:
    #   statement, command, and question, voting on what type we think it is
    #   and handling it as that type of sentence
    sentence_type = vote_sentence_type.vote_sentence_type(normalized_sentence=normalized_sentence)

    #   handle statements
    if sentence_type == "statement":
        #   split into subject and predicate
        subject = []
        predicate = []
        i = 0
        hit = False
        while i < len(normalized_sentence):
            if not hit and normalized_sentence[i] in linking_verbs:
                hit = True
            if not hit:
                subject.append(normalized_sentence[i])
            else:
                predicate.append(normalized_sentence[i])
            i += 1
        #   statements about user
        if subject[0] in ["my", "i", "im"]:
            chat_context.user.info[" ".join(subject[1:])] = predicate
            if len(list(set(["name", "named"]) & set(subject + predicate))):
                send_response("Hello " + predicate[-1] + "!")
        
        #   general context statements
        else:
            chat_context.world_info[" ".join(subject[1:])] = predicate