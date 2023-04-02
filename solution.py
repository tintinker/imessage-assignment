import assignment_dependency_wrappers as assignment
import sys

USERNAME = 'justint'

def response_time(message_list):
    """
    prints average response time in minutes using the is_sent info from given thread
    """
    for (_, _, is_sent, date, _) in message_list:
        me_time = num_me = 0
        other_time = num_other = 0

        for i in range(1, len(message_list)):
            (_, _, curr_is_sent, curr_date, _) = message_list[i]
            (_, _, prev_is_sent, prev_date, _) = message_list[i - 1]

            if curr_is_sent != prev_is_sent:
                if curr_is_sent:
                    me_time += (curr_date - prev_date).total_seconds() // 60
                    num_me += 1
                else:
                    other_time += (curr_date - prev_date).total_seconds() // 60
                    num_other += 1

    print(f"Me average: {me_time/num_me}")
    print(f"Their average: {other_time/num_other}")

def format_message(message, highlight=None):
    """
    jibberish to pretty
    optional param highlight adds ***arterisks*** around given word
    """
    (number, _, _, date, text) = message
    if highlight and text:
        text = text.replace(highlight, "***"+highlight+"***")
    return f"{assignment.to_contact_name(number, number_name)} on {assignment.pretty_date(date)}: {text}"

def print_all_chats(all_chats):
    for chat in all_chats:
        print("\n\n")
        for message in all_chats[chat]:
            print(format_message(message))

def search(keyword, all_chats):
    """
    prints all messages with given keyword with 6 messages of surrounding context
    """
    for chat in all_chats:
        for i in range(len(all_chats[chat])):
            (_, _, _, _, text) = all_chats[chat][i]
            if text and keyword in text:
                print("\n\n")
                for j in range(max(0, i - 3), min(i + 3, len(all_chats[chat]) - 1)):
                    print(format_message(all_chats[chat][j], highlight=keyword))


def main():
    """
    examples of program calls:
    python3 solution.py -since 01-01-2019
    python3 solution.py -range 01-01-2019 01-02-2019
    python3 solution.py -responsetime +12162884710
    python3 solution.py -search love
    """

    """
    From assignment_dependency_wrappers.py:
    
    Function info for getsmessages()

    @param since_date (optional):
    string in the form mm-dd-YYYY representing date at which to start retrieving messages
    @param before (optional):
    string in the form mm-dd-YYYY representing date at which to stop retrieving messages
    @param limit (optional):
    max amount of messages (if 0 or not provided, returns all messages that match query)

    @returns
    dictionary where each key is a chat, and each value is a tuple representing a message in the form
    (number, chat_id, is_sent, date, text)
    """
    if len(sys.argv) > 1 and "-since" in sys.argv[1]:
        all_chats = (assignment.getmessages(conn, sincedate=sys.argv[2]))
        print_all_chats(all_chats)

    elif len(sys.argv) > 2 and "-range" in sys.argv[1]:
        all_chats = (assignment.getmessages(conn, sincedate=sys.argv[2], beforedate=sys.argv[3]))
        print_all_chats(all_chats)

    elif len(sys.argv) > 1 and "-responsetime" in sys.argv[1]:
        all_chats = assignment.getmessages(conn)
        response_time(all_chats[sys.argv[2]])

    elif len(sys.argv) > 1 and "-search" in sys.argv[1]:
        all_chats = assignment.getmessages(conn)
        search(sys.argv[2], all_chats)

    else:
        print("Please specify an option (-since -responsetime or -search)")
        print("see examples at top of main function")

if __name__ == '__main__':
    if(USERNAME == 'justint'):
        print("replace USERNAME constant at top of this file with your username")
    else:
        conn = assignment.init(f'/Users/{USERNAME}/Library/Messages/chat.db')
        name_number,number_name = assignment.get_contacts("example_contacts.txt")
        main()
