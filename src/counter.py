from os import path
import re
from datetime import datetime, timedelta
from typing import Dict, List
from argparse import ArgumentParser

def extract_messages_of_week(input_file_path: str, start_date: datetime, end_date: datetime):
    """

    :type end_date: datetime
    """
    with open(input_file_path, 'r', encoding='utf-8') as file:
        text = file.readlines()

    messages = []
    for line in text:

        # padrão para identificar o dia da mensagem
        match = re.search(r'\d{2}/\d{2}/\d{4}', line)
        if match:
            message_date = datetime.strptime(match.group(0), '%d/%m/%Y')
            if start_date <= message_date <= end_date:
                messages.append(line.lower())

    return messages


def create_dict_sector2count(messages: List) -> Dict:
    sector_and_count = {}
    for message in messages:

        # Pega o corpo da mensagem depois dos dois pontos
        message_text = "".join(message.split(':')[2:]).strip()

        sector_match = re.search(r'#(\w{3}\w?)', message_text) # ex: #nip, #bope
        count_match = re.search(r'\+(\d*)', message_text) # ex: +2, +10

        if sector_match and count_match:
            sector = sector_match.group(1).lower()
            count = count_match.group(1)
        else:
            continue
        if sector in sector_and_count:
            sector_and_count[sector] += int(count)
        else:
            sector_and_count[sector] = int(count)
    return sector_and_count


def show_results_in_txt(sector_and_count: Dict, output_directory_path: str):
    sector_and_count_sorted_by_count = dict(sorted(sector_and_count.items(),
                                                   key=lambda item: item[1],
                                                   reverse=True))

    output_file_path = path.join(output_directory_path, 'results.txt')

    with open(output_file_path, 'w', encoding='utf-8') as file:
        file.write('FOCA FIT SEMANAL\n')
        for rank, sector_count in enumerate(sector_and_count_sorted_by_count.items()):
            sector = sector_count[0]
            count = sector_count[1]
            file.write(f'{rank + 1}ª {sector.upper()}: {count}\n')


if __name__ == '__main__':

    parser = ArgumentParser()
    parser.add_argument('-i', '--input_file_path', type=str, default='./assets/input/chat.txt', dest='input_file_path')
    parser.add_argument('-o', '--output_directory_path', type=str, default='./assets/output', dest='output_directory_path')
    parser.add_argument('-d', '--dia_da_contagem', type=str, default=datetime.now().strftime('%d/%m/%Y'), dest='dia_da_contagem')
    args = parser.parse_args()

    input_file_path = args.input_file_path
    output_directory_path = args.output_directory_path
    dia_da_contagem = args.dia_da_contagem
    today = datetime.strptime(dia_da_contagem, '%d/%m/%Y')

    start_date = today - timedelta(days=7)
    end_date = today - timedelta(days=1)

    messages_of_week = extract_messages_of_week(input_file_path, start_date, end_date)

    sector_and_count = create_dict_sector2count(messages_of_week)

    show_results_in_txt(sector_and_count, output_directory_path)

    print(f"Relatório gerado com sucesso e salvo em {output_directory_path}")

