from os import path
import re
from datetime import datetime, timedelta
from typing import Dict, List, Tuple
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
                messages.append(line)

    return messages


def get_name_from_message(message_text: str):

    message_without_count = re.sub(r'\+(\d+)', '', message_text)  # removes +4
    cleaned_message = re.sub(
        r'#(\w{3,4})', '', message_without_count).strip()  # removes #noe

    # Se só tiver uma palavra, essa palavra é o nome
    message_words = cleaned_message.split(' ')
    if len(message_words) == 1:
        name = message_words[0]
    else:
        # Se tiver mais de uma palavra, pega as palavras que começam com letra maiúscula e junta
        capitalized_words = re.findall(
            r'\b[A-Z][^A-Z ]+\b', cleaned_message)  # ex: Chico Buarque
        name = ' '.join(capitalized_words)

        # Se tiver mais de uma palavra mas nenhuma começar com letra maiúscula, pega a primeira palavra
        if not name:
            name = message_words[0]

    return name.title()


def create_dict_sector2count(messages: List) -> Tuple[Dict, Dict]:
    sector_and_count = {}
    name_and_count = {}

    for message in messages:

        # Pega o corpo da mensagem (que inicia depois dos dois pontos)
        # message_text = '10/05/2023 17:02 - Chico: Chico +2 #NOE'
        message_text = "".join(message.split(':')[2:]).strip()

        sector_match = re.search(
            r'#(\w{3,4})', message_text)  # ex: #nip, #bope
        count_match = re.search(r'\+(\d+)', message_text)  # ex: +2, +10

        if sector_match and count_match:
            sector = sector_match.group(1).lower()
            count = count_match.group(1)

            if sector in sector_and_count:
                sector_and_count[sector] += int(count)

            else:
                sector_and_count[sector] = int(count)

            # caso message_text possua sector e count mas não tenha nome, sector pontua mas a pessoa não.
            # pontuação para o núcleo será considerada mas não será atribuída a nenhum jogador
            name = get_name_from_message(message_text)
            if name:
                if name in name_and_count:
                    name_and_count[name] += int(count)
                else:
                    name_and_count[name] = int(count)
            else:
                print(f'Mensagem sem nome: {message}')
        else:
            continue

    return sector_and_count, name_and_count


def save_results_file(sector_and_count: Dict, name_and_count, output_directory_path: str, start_date: datetime,
                      end_date: datetime):
    sector_and_count_sorted_by_count = dict(sorted(sector_and_count.items(),
                                                   key=lambda item: item[1],
                                                   reverse=True))

    name_and_count_sorted_by_count = dict(sorted(name_and_count.items(),
                                                 key=lambda item: item[1],
                                                 reverse=True))

    output_file_path = path.join(output_directory_path, 'results.txt')

    with open(output_file_path, 'w', encoding='utf-8') as file:

        start_date_formatted = start_date.strftime('%d/%m')
        end_date_formatted = end_date.strftime('%d/%m')

        file.write(
            f'🦾 FOCA FIT SEMANAL - {start_date_formatted} A {end_date_formatted} 🦾 \n')
        file.write('Gerado por: Focafit_counter 😎 \n\n')

        file.write('💜💙🖤 RANKING POR NÚCLEO 💚🧡💛 \n\n')

        for rank, sector_count in enumerate(sector_and_count_sorted_by_count.items()):
            sector = sector_count[0]
            count = sector_count[1]
            file.write(f'{rank + 1}º {sector.upper()}: {count}\n')

        file.write('\n\n')

        file.write('🏆 RANKING POR PESSOA 🏆\n\n')
        for rank, name_count in enumerate(name_and_count_sorted_by_count.items()):
            name = name_count[0]
            count = name_count[1]
            file.write(f'{rank + 1}º {name}: {count}\n')


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('-i', '--input_file_path', type=str,
                        default='./assets/input/chat.txt')
    parser.add_argument('-o', '--output_directory_path',
                        type=str, default='./assets/output')
    parser.add_argument('-d', '--dia_da_contagem', type=str,
                        default=datetime.now().strftime('%d/%m/%Y'))
    args = parser.parse_args()

    input_file_path = args.input_file_path
    output_directory_path = args.output_directory_path
    dia_da_contagem = args.dia_da_contagem
    today = datetime.strptime(dia_da_contagem, '%d/%m/%Y')

    # considerando que a contagem se inicia na segunda-feira
    start_date = today - timedelta(days=7)

    # considerando que o relatório de contagem é realizado na próxima segunda (um dia depois do último dia válido para a contagem da semana em questão)
    end_date = today - timedelta(days=1)

    messages_of_week = extract_messages_of_week(
        input_file_path, start_date, end_date)

    sector_and_count, name_and_count = create_dict_sector2count(
        messages_of_week)

    save_results_file(sector_and_count, name_and_count,
                      output_directory_path, start_date, end_date)

    print(f"Relatório gerado com sucesso e salvo em {output_directory_path}")
