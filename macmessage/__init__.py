import sqlite3
import pandas as pd
from datetime import datetime
import math

#seconds between January 1, 1970 and January 1, 2001
ELAPSE = 978336000
EPOCH = datetime.fromtimestamp(0)
JAN2001 = datetime.fromtimestamp(ELAPSE)
#pacific time offset in seconds
PACIFIC_TIME_OFFSET = 8 * 60 * 60

def seconds_to_date(seconds):
    return (datetime.fromtimestamp(int(seconds/1000000000) + ELAPSE - PACIFIC_TIME_OFFSET))

def date_to_seconds(date):
    return ((date - EPOCH).total_seconds() - ELAPSE + PACIFIC_TIME_OFFSET) * 1000000000

def day_date_format(date):
    return datetime.strptime(date, "%m-%d-%Y")

def minute_date_format(date):
    #24 hour time
    return datetime.strptime(date, "%m-%d-%Y %H:%M")


def to_organized_messages(message_data):
    all_chats = {}

    for i in range(len(message_data)):
        if(message_data['chat_identifier'][i] in all_chats.keys()):
            all_chats[message_data['chat_identifier'][i]][2].append((message_data['phone_number'][i], message_data['chat_id'][i], message_data['is_sent'][i], seconds_to_date(message_data['date'][i]), message_data['text'][i]))
        else:
            all_chats[message_data['chat_identifier'][i]] = (message_data['chat_display_name'][i], message_data['chat_identifier'][i], [(message_data['phone_number'][i], message_data['chat_id'][i], message_data['is_sent'][i], seconds_to_date(message_data['date'][i]), message_data['text'][i])])
    return all_chats

def number_to_handle(phone_number, conn):
    # get the handles to apple-id mapping table
    handles = pd.read_sql_query(f"select ROWID from handle WHERE id = '{phone_number}'", conn)
    return list(map(str, handles['ROWID'].tolist()))


def get_messages(conn, handle_id="", before_date=None, since_date=None, limit=0):

    #get messages
    temp = constraints = ""
    if handle_id:
        temp += f"AND handle_id = '{handle_id}' "
    if since_date:
        temp += f"AND date >= {date_to_seconds(since_date)} "
    if before_date:
        temp += f"AND date <= {date_to_seconds(before_date)} "
    if temp:
        constraints = "WHERE" + temp[3:]

    if limit:
        constraints += f"limit {limit}"

    messages = pd.read_sql_query("select * from message "+constraints, conn)

    # get the handles to apple-id mapping table
    if not handle_id:
        handles = pd.read_sql_query(f"select * from handle", conn)
    else:
        handles = pd.read_sql_query(f"select * from handle where ROWID = '{handle_id}'", conn)



    #rename to match
    messages.rename(columns={'ROWID' : 'message_id'}, inplace = True)
    handles.rename(columns={'id' : 'phone_number', 'ROWID': 'handle_id'}, inplace = True)

    # and join to the messages, on handle_id
    merge_level_1 = pd.merge(messages[['text', 'handle_id', 'date','is_sent', 'message_id']],  handles[['handle_id', 'phone_number']], on ='handle_id', how='left')

    # get the chat to message mapping
    chat_message_joins = pd.read_sql_query("select * from chat_message_join", conn)

    #get chat info
    chats = pd.read_sql_query("select * from chat", conn)
    chats.rename(columns={'ROWID': 'chat_id', 'display_name': 'chat_display_name'}, inplace = True)

    # and join back to the merge_level_1 table
    merge_level_2 = pd.merge(merge_level_1, chat_message_joins[['chat_id', 'message_id']], on = 'message_id', how='left')
    merge_level_3 = pd.merge(merge_level_2, chats[['chat_identifier', 'chat_display_name', 'chat_id']], on = 'chat_id', how='left')
    return merge_level_3

def init_connection(database='/Users/justin/Library/Messages/chat.db'):
    # substitute username with your username
    conn = sqlite3.connect(database)
    # connect to the database
    cur = conn.cursor()
    #update recent messages
    cur.execute("pragma main.wal_checkpoint")

    return conn

def get_convos_with_person(conn, number, since_date=None, imessageonly=False):
    #ex. '+12162884711'
    handles = number_to_handle(number, conn)

    if imessageonly:
        return get_messages(conn, handle_id=handles[len(handles) - 1], since_date=since_date)

    message_list = []
    for handle in handles:
        message_list.append(get_messages(conn, handle_id=handle, since_date=since_date))
    messages = pd.concat(message_list, ignore_index = True)
    return messages

def get_messages_in_chat(chat_identifier, conn=None, messages = None, since_date=None):
    if conn is None and messages is None:
        raise ValueError('Need to specify either conn or messages')

    _messages = messages if messages is not None else get_messages(conn, since_date)
    chats = to_organized_messages(messages)
    return chats[chat_identifier][2]

def pretty_print_all(message_data, number_name_map):
    chats = to_organized_messages(message_data)
    for chat in chats:
        print("-"*20+str(chats[chat][0])+"-"*20)
        pretty_print_messages_in_chat(chats[chat][2], number_name_map)

def pretty_print_messages_in_chat(messages, number_name_map):
    for (number, _, is_sent, date, text) in messages:
        #sender is a special field for the person who's computer is being controlled
        #if a message is from the sender, the number will be nan (float), else it will be a string
        sender = number_name_map['sender'] if isinstance(number, float) or is_sent else number_name_map[number] if number in number_name_map.keys() else number
        print(f"{sender} on {date.strftime('%b %d at %I:%M %p')}: {text}")

def pretty_return_messages_in_chat(messages, number_name_map):
    lst = []
    for (number, _, is_sent, date, text) in messages:
        #sender is a special field for the person who's computer is being controlled
        #if a message is from the sender, the number will be nan (float), else it will be a string
        sender = number_name_map['sender'] if isinstance(number, float) or is_sent else number_name_map[number] if number in number_name_map.keys() else number
        lst.append(f"{sender} on {date.strftime('%b %d at %I:%M %p')}: {text}\n")
    return lst


"""
Example:
conn = init_connection()
messages = get_messages(conn)
chat_messages = get_messages_in_chat(conn, 'chat953999257728652495', messages = messages)
pretty_print_messages_in_chat(chat_messages, contacts.number_name)
#messages = get_convos_with_person(contacts.contacts["Sammy"])
"""
