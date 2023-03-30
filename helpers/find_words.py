import re

def wordInMessage(message = '', trigger_words_list = []):
  pattern = r'\W+'
  message_as_list = re.split(pattern, message)
  # print(trigger_words_list)
  for word in trigger_words_list:
    # print(word)
    if word.lower() in message_as_list:
      return True
  return False
