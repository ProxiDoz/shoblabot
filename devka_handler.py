# Function return true if all letters in message is 'a'
def is_message_has_only_a_char(message_text):
    # print("check '" + message_text + "' for all A symbols") # debug log
    if (len(message_text) == 0):
        return False

    for char in message_text.lower():
        # latin and cyrillic chars
        if char == 'a' or char == 'а':
            continue
        else:
            return False
    print("devka detected")
    return True

## Cases for test

## Must return False
#print(is_message_has_only_a_char("aaaatest"))
#print(is_message_has_only_a_char(""))

## Must return True
#print(is_message_has_only_a_char("aaa")) # latin
#print(is_message_has_only_a_char("aAa")) # latin
#print(is_message_has_only_a_char("ааа")) # cyrillic
#print(is_message_has_only_a_char("аАа")) # cyrillic