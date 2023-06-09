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

def get_capitalized_name(message_text: str):
    capitalized_words = re.findall(
            r'\b[A-Z][^A-Z ]+\b', message_text)  # ex: Chico Buarque
    name = ' '.join(capitalized_words)

    return name

def get_name_from_message(message_text: str):
    # Se só tiver uma palavra, essa palavra é o nome
    message_words = message_text.split(' ')
    if len(message_words) == 1:
        name = message_words[0]
    else:
        # Se tiver mais de uma palavra, pega as palavras que começam com letra maiúscula e junta
        name = get_capitalized_name(message_text)
        # Se tiver mais de uma palavra mas nenhuma começar com letra maiúscula, pega a primeira palavra
        if not name:
            name = message_words[0]

    return name.title()

def get_names_from_message(message_text: str):
    names = []
    splitted_message = message_text.split(',')

    for text in splitted_message:
        name = get_capitalized_name(text)
        if name:
            names.append(name.title())

    return names


def assign_points(sector_and_points: Dict, name_and_points: Dict, message: str, message_text: str, sector: str, points: str):
    names = []

    # caso message_text possua sector e points mas não tenha nome, sector pontua mas a pessoa não.
    # pontuação para o núcleo será considerada mas não será atribuída a nenhum jogador
    if sector in sector_and_points:
        sector_and_points[sector] += int(points)
    else:
        sector_and_points[sector] = int(points)

    if ',' in message_text:
        names = get_names_from_message(message_text)
        points = int(points) // len(names)
    else:
        name = get_name_from_message(message_text)
        if name:
            names.append(name)

    if not names:
        print(f'Mensagem sem nome: {message}')

    for name in names:
        if name in name_and_points:
            name_and_points[name] += int(points)
        else:
            name_and_points[name] = int(points)


def create_dict_sector2points(messages: List) -> Tuple[Dict, Dict]:
    sector_and_points = {}
    name_and_points = {}

    sector_pattern = re.compile(r'#(noe|nip|nut|bope|ndp|pres|trainees)', re.IGNORECASE)
    points_pattern = re.compile(r'([\+|\-]\d+)') # ex: +2, -10

    for message in messages:

        # Pega o corpo da mensagem (que inicia depois dos dois pontos)
        # message = '10/05/2023 17:02 - Chico: Chico +2 #NOE'
        message_text = "".join(message.split(':')[2:]).strip()

        sector_match = sector_pattern.search(message_text)  # ex: #noe
        points_match = points_pattern.search(message_text)  # ex: +2, -10

        if sector_match and points_match:
            message_without_sector = sector_pattern.sub('', message_text)  # removes #noe
            cleaned_message = points_pattern.sub('', message_without_sector).strip()  # removes +2

            sector = sector_match.group(1).lower()
            points = points_match.group(1)

            assign_points(sector_and_points, name_and_points, message, cleaned_message, sector, points)
        else:
            continue

    return sector_and_points, name_and_points


def save_results_file(sector_and_points: Dict, name_and_points, output_directory_path: str, start_date: datetime,
                      end_date: datetime):
    sector_and_points_sorted_by_points = dict(sorted(sector_and_points.items(),
                                                     key=lambda item: item[1],
                                                     reverse=True))

    name_and_points_sorted_by_points = dict(sorted(name_and_points.items(),
                                                   key=lambda item: item[1],
                                                   reverse=True))

    output_file_path = path.join(output_directory_path, 'results.txt')

    with open(output_file_path, 'w', encoding='utf-8') as file:

        start_date_formatted = start_date.strftime('%d/%m')
        end_date_formatted = end_date.strftime('%d/%m')

        file.write(
            f'🦾 FOCA FIT SEMANAL - {start_date_formatted} A {end_date_formatted} 🦾 \n')
        file.write('Gerado por: Focafit_pointser 😎 \n\n')

        file.write('💜💙🖤 RANKING POR NÚCLEO 💚🧡💛 \n\n')

        for rank, sector_points in enumerate(sector_and_points_sorted_by_points.items()):
            sector = sector_points[0]
            points = sector_points[1]
            file.write(f'{rank + 1}º {sector.upper()}: {points}\n')

        file.write('\n\n')

        file.write('🏆 RANKING POR PESSOA 🏆\n\n')
        for rank, name_points in enumerate(name_and_points_sorted_by_points.items()):
            name = name_points[0]
            points = name_points[1]
            file.write(f'{rank + 1}º {name}: {points}\n')


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

    sector_and_points, name_and_points = create_dict_sector2points(
        messages_of_week)

    save_results_file(sector_and_points, name_and_points,
                      output_directory_path, start_date, end_date)

    print(f"Relatório gerado com sucesso e salvo em {output_directory_path}")
