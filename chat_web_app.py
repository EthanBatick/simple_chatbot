import match_parse_sentence
import vote_sentence_type
from linking_verb_pool import linking_verbs
from name_pool_1000 import names
import random
import Context

from flask import Flask, request, jsonify, send_from_directory


app = Flask(__name__, static_folder="static")

chat_context = Context.Context()


def send_response(message="", bot_name="placeholder"):
    return bot_name + ": " + message


def get_response(user_input):
    normalized_sentence = match_parse_sentence.patch_parse_sentence(user_input)

    # debug info
    if normalized_sentence == ["debug"]:
        return (
            "User info: " + str(chat_context.user.info) +
            " General info: " + str(chat_context.world_info)
        )

    # empty message
    empty_input_responses = [
        "say something",
        "you didn't type anything",
        "i need some words to respond to",
        "try typing a message",
        "i'm listening"
    ]

    if len(normalized_sentence) == 0:
        return send_response(random.choice(empty_input_responses))

    # handle hello's
    hello_responses = [
        "hello",
        "hey",
        "hi, how can I help?",
        "what's up?",
        "hey, good to see you"
    ]

    if bool(set(normalized_sentence) & set(["hello", "hi", "hey"])):
        return send_response(random.choice(hello_responses))

    # handle goodbyes
    goodbye_responses = [
        "goodbye",
        "bye",
        "see you later",
        "talk to you later",
        "catch you later"
    ]

    if bool(set(normalized_sentence) & set(["goodbye", "bye", "ciao"])):
        return send_response(random.choice(goodbye_responses))

    # now we split the sentence into 3 main types of sentences:
    # statement, command, and question, voting on what type we think it is
    sentence_type = vote_sentence_type.vote_sentence_type(
        normalized_sentence=normalized_sentence
    )

    # handle statements
    if sentence_type == "statement":
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

        if len(subject) == 0:
            return send_response("I'm not sure!")

        # statements about user
        if (
            subject[0] == "my"
            and len(list(set(["name", "named", "names", "name's"]) & set(subject + predicate)))
            and len(subject) == 2
        ):
            chat_context.user.info[" ".join(subject[1:])] = predicate
            chat_context.user.info["name"] = predicate
            chat_context.user.info["my name"] = predicate
            chat_context.user.info[""] = predicate

            return send_response("Hello " + predicate[-1] + "!")

        elif (
            subject[0] in ["i", "im"]
            and len(list(set(predicate) & set(names))) > 0
        ):
            chat_context.user.info[" ".join(subject[1:])] = predicate
            chat_context.user.info["name"] = ["is"] + predicate[1:]
            chat_context.user.info["my name"] = ["is"] + predicate[1:]
            chat_context.user.info[""] = predicate

            return send_response("Hello " + predicate[-1] + "!")

        # general context statements
        else:
            chat_context.world_info[" ".join(subject)] = predicate
            return send_response("Got it.")

    elif sentence_type == "question":
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

        if len(normalized_sentence) == 0:
            return send_response("I'm not sure!")

        # questions about stuff
        if normalized_sentence[0] in ["who", "what"]:
            if len(predicate) >= 3:
                user_key = " ".join(predicate[2:])
                world_key = " ".join(predicate[1:])

                if user_key in chat_context.user.info and predicate[1] in ["my"]:
                    if predicate[1] == "your":
                        return send_response(
                            "my "
                            + " ".join(predicate[2:])
                            + " "
                            + " ".join(chat_context.user.info[user_key])
                        )

                    elif predicate[1] == "my":
                        return send_response(
                            "your "
                            + " ".join(predicate[2:])
                            + " "
                            + " ".join(chat_context.user.info[user_key])
                        )

                    else:
                        return send_response(
                            " ".join(predicate[1:])
                            + " "
                            + " ".join(chat_context.user.info[user_key])
                        )

                elif world_key in chat_context.world_info:
                    if predicate[1] == "your":
                        return send_response(
                            "my "
                            + " ".join(predicate[2:])
                            + " "
                            + " ".join(chat_context.world_info[world_key])
                        )

                    elif predicate[1] == "my":
                        return send_response(
                            "your "
                            + " ".join(predicate[2:])
                            + " "
                            + " ".join(chat_context.world_info[world_key])
                        )

                    else:
                        return send_response(
                            " ".join(predicate[1:])
                            + " "
                            + " ".join(chat_context.world_info[world_key])
                        )

                else:
                    return send_response("I'm not sure!")

            else:
                return send_response("I'm not sure!")

        else:
            return send_response("I'm not sure!")

    else:
        return send_response("I'm not sure!")


@app.route("/")
def home():
    return send_from_directory("static", "index.html")


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()

    if not data or "message" not in data:
        return jsonify({"error": "No message provided"}), 400

    user_message = data["message"]
    bot_response = get_response(user_message)

    return jsonify({
        "response": bot_response
    })


def terminal_loop():
    user_input = None

    while user_input != "q":
        user_input = str(input("You: "))

        if user_input == "q":
            break

        response = get_response(user_input)
        print(response)


if __name__ == "__main__":
    mode = input("Run as website or terminal? ").lower().strip()

    if mode in ["website", "web", "server"]:
        app.run(host="0.0.0.0", port=5000)
    else:
        terminal_loop()