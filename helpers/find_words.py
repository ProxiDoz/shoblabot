def wordInMessage(message = '', trigger_words_list = []):
  message_as_list = message.split(' ')
  list_words = list(map(lambda w: w.replace(' ', '').lower().replace('ё', 'е'), message_as_list))
  for word in trigger_words_list:
    if word.lower() in list_words:
      return True
    else:
      return False