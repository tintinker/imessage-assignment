import assignment_dependency_wrappers as assignment
import sys

USERNAME = 'justin'

def response_time(message_list):
    """
    prints average response time in minutes using the is_sent info from given thread
    """
    pass

def format_message(message, highlight=None):
    """
    jibberish to pretty
    optional param highlight adds ***arterisks*** around given word
    """
    pass

def print_all_chats(all_chats):
    pass

def search(keyword, all_chats):
    """
    prints all messages with given keyword with 6 messages of surrounding context
    """
    pass


def main():
    """
    examples of program calls:
    python3 solution.py -since 01-01-2019
    python3 solution.py -range 01-01-2019 01-02-2019
    python3 solution.py -responsetime +12162884710
    python3 solution.py -search love
    """
    
    if len(sys.argv) > 1 and "-since" in sys.argv[1]:
        #implement this
        pass

    elif len(sys.argv) > 2 and "-range" in sys.argv[1]:
        #implement this
        pass

    elif len(sys.argv) > 1 and "-responsetime" in sys.argv[1]:
        all_chats = assignment.getmessages(conn)
        response_time(all_chats[sys.argv[2]])

    elif len(sys.argv) > 1 and "-search" in sys.argv[1]:
        all_chats = assignment.getmessages(conn)
        search(sys.argv[2], all_chats)

    else:
        print("Please specify an option (-since -responsetime or -search)")

if __name__ == '__main__':
    conn = assignment.init(f'/Users/{USERNAME}/Library/Messages/chat.db')
    name_number,number_name = assignment.get_contacts("example_contacts.txt")
    main()
