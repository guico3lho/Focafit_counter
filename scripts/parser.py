import re
from datetime import datetime, timedelta
from typing import Dict, List


def extract_messages_of_week(file_path: str, start_date: datetime, end_date: datetime):
    """

    :type end_date: datetime
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.readlines()

    messages = []
    for line in text:
        match = re.search(r'\d{2}/\d{2}/\d{4}', line)
        if match:
            message_date = datetime.strptime(match.group(0), '%d/%m/%Y')
            if start_date <= message_date <= end_date:
                messages.append(line.lower())

    return messages


def parse_sectors_of_messages(messages : List) -> Dict:
    sector_and_count = {}
    for index, message in enumerate(messages):
        match = re.search(r'#?(\w{3})\s*\+(\d)', message)
        match_2 = re.search(r'\+(\d)\s*#?(\w{3})', message)
        if match:
            sector = match.group(1)
            count = match.group(2)
        elif match_2:
            sector = match_2.group(2)
            count = match_2.group(1)
        else:
            continue
        if sector in sector_and_count:
            sector_and_count[sector] += int(count)
        else:
            sector_and_count[sector] = int(count)
    return sector_and_count


def show_results_in_txt(sector_and_count: Dict):
    sector_and_count_sorted_by_count = dict(sorted(sector_and_count.items(),
                                                   key=lambda item: item[1],
                                                   reverse=True))

    value_key_pairs = ((value, key) for (key, value) in sector_and_count_sorted_by_count.items())
    sorted_value_key_pairs = sorted(value_key_pairs, reverse=True)
    sector_and_count_sorted_by_count = {k: v for v, k in sorted_value_key_pairs}

    with open('../assets/results_16_05.txt', 'w', encoding='utf-8') as file:
        file.write('FOCA FIT SEMANAL\n')
        for rank, sector_count in enumerate(sector_and_count_sorted_by_count.items()):
            sector = sector_count[0]
            count = sector_count[1]
            file.write(f'{rank + 1}ª {sector.upper()}: {count}\n')


if __name__ == '__main__':
    file_path = '../assets/chat_16_05.txt'
    today = datetime.strptime('15/05/2023', '%d/%m/%Y')
    # today = datetime.now()
    start_date = today - timedelta(days=7)
    end_date = today - timedelta(days=1)

    messages_of_week = extract_messages_of_week(file_path, start_date, end_date)

    sector_and_count = parse_sectors_of_messages(messages_of_week)

    show_results_in_txt(sector_and_count)
    ...

    # Now lets count
    # if the sector is NUT, I will search for the string "#NOE +\d"
    # if the sector is BOPE, I will search for the string "#BOPE +\d"
    # if the sector is NOE, I will search for the string "#NOE +\d"
    # if the sector is NDP, I will search for the string "#NDP +\d"
    # if the sector is NIP, I will search for the string "#NIP +\d"

    # for message in messages_of_week:
    #     print(message)
    # start_date = datetime(2023, 05, 14)
    # end_date = datetime(2020, 12, 31)
    # messages = extract_messages_of_week('chat_16_05.txt', start_date, end_date)
    # print(messages)
