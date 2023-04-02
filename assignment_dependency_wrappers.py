from macmessage import (init_connection, to_organized_messages, get_messages, day_date_format)
from macmessage import contacts

def init(database):
    """
    Initializes database, returns connecdtion object needed in get_messages
    """
    return init_connection(database)

def getmessages(conn, sincedate=None, beforedate=None, limit=0):
    """
    Gets messages with given parameters

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
    #data from base library comes in the form {'chat_id': (name of chat, chat_id, message list)}
    all_data = to_organized_messages(get_messages(conn, before_date=(day_date_format(beforedate) if beforedate else None), since_date=(day_date_format(sincedate) if sincedate else None), limit=limit))
#   #convert to form {'chat_id': message_list} for simplicity
    return {key:all_data[key][2] for key in all_data}

def get_contacts(filename):
    """
    Returns two dictionaries representing contacts in number->sender form and sender->number from
    """
    return contacts.contacts(filename, "You")

def pretty_date(date):
    """
    Wrapper for strftime
    """
    return date.strftime('%b %d at %I:%M %p')

def to_contact_name(number, number_name_map):
    """
    Converts number to contact name based on given dictionary
    """
    #sender is a special field for the person who's computer is being controlled
    #if a message is from the sender, the number will be nan (float), else it will be a string
    return number_name_map['sender'] if isinstance(number, float) else number_name_map[number] if number in number_name_map.keys() else number
