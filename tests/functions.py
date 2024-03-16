def print_messages_from_interval(messages_from_date_interval):
    with open('./assets/output/messages_from_data_interval.txt', 'w', encoding='utf-8') as file:
        for message in messages_from_date_interval:
            file.write(message)
