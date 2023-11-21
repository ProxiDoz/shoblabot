import re


def word_in_message(message, trigger_words_list):
    pattern = r'\W+'
    message_as_list = re.split(pattern, message.lower())
    for word in trigger_words_list:
        if word.lower() in message_as_list:
            return True
    return False
