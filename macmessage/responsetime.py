from . import (init_connection, get_convos_with_person, get_messages_in_chat)
from . import contacts

def responsetime(contacts_file, sender_name, other_name, other_number, since_date, imessageonly=False):
    name_number, number_name = contacts.contacts(contacts_file, sender_name)
    conn = init_connection()


    #example 1
    messages = get_convos_with_person(conn, other_number, since_date=since_date, imessageonly=imessageonly)
    just_us = get_messages_in_chat(other_number, messages = messages)

    """
    #example 2
    messages = mm.get_messages(conn = conn, since_date=mm.day_date_format("05-12-2019"))
    chat_messages = mm.get_messages_in_chat('chat953999257728652495', messages = messages)
    mm.pretty_print_messages_in_chat(chat_messages, number_name)
    """

    me_time = num_me = 0
    other_time = num_other = 0
    threshold = 60 * 60 * 24 * 5#threshold of 2 days in seconds

    for i in range(1, len(just_us)):
        (_, _, curr_is_sent, curr_date, curr_text) = just_us[i]
        (_, _, prev_is_sent, prev_date, prev_text) = just_us[i - 1]

        if curr_is_sent != prev_is_sent and (curr_date - prev_date).total_seconds() < threshold :
            if curr_is_sent:
                me_time += (curr_date - prev_date).total_seconds() / 60
                num_me += 1
                print("+"+f'{((curr_date - prev_date).total_seconds() / 60):5.2f}' + " (me): "+prev_text+"->"+curr_text)
            else:
                other_time += (curr_date - prev_date).total_seconds() / 60
                num_other += 1
                print("+"+f'{((curr_date - prev_date).total_seconds() / 60):5.2f}' + " (them): "+prev_text+"->"+curr_text)

    print(("-"*40)+" Report "+("-"*40))
    print(f"Total sent by {sender_name}: {num_me}")
    print(f"Total sent by {other_name}: {num_other}")

    print(f"Total response time by {sender_name}: " + f"{me_time:5.2f}")
    print(f"Total response time by {other_name}: " + f"{other_time:5.2f}")

    print(f"{sender_name} average: " + f"{me_time/num_me:5.2f}")
    print(f"{other_name} average: " + f"{other_time/num_other:5.2f}")

    print(("-"*40)+" Report "+("-"*40))
