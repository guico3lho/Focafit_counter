from os import path
import re
from datetime import datetime, timedelta
from typing import Dict, List, Tuple
from argparse import ArgumentParser


def main():
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
    end_date = datetime.strptime(dia_da_contagem, '%d/%m/%Y')
    start_date = end_date - timedelta(days=6)

    messages_from_date_interval = extract_messages_from_date_interval(
        input_file_path, start_date, end_date)

    nucleo_and_points, name_and_points = create_dict_nucleo2points(
        messages_from_date_interval)

    save_results_file(nucleo_and_points, name_and_points,
                      output_directory_path, start_date, end_date)

    print(f"Relatório gerado com sucesso e salvo em {output_directory_path}")


def extract_messages_from_date_interval(input_file_path: str, start_date: datetime, end_date: datetime) -> List[str]:
    """
    :param input_file_path: caminho do arquivo de entrada; ex: './assets/input/chat.txt'
    :param start_date: data de início da contagem; ex: datetime(2023, 7, 10) # 2023-07-10 00:00:00
    :param end_date: data de fim da contagem; ex: datetime(2023, 7, 16) # 2023-07-16 00:00:00
    :return messages_from_date_interval: lista de mensagens do grupo focafit entre start_date e end_date
    """
    with open(input_file_path, 'r', encoding='utf-8') as file:
        messages = file.readlines()

    messages_from_date_interval = []

    # para cada linha das mensagens do grupo focafit, fazer:
    for message in messages:
        # REFAC: Em vez de usar for para cada mensagem, usar regex para filtrar todas as mensagens de uma só vez
        # identificar a data contida na linha
        date_match = re.search(r'\d{2}/\d{2}/\d{4}', message)
        if date_match:
            message_date = datetime.strptime(date_match.group(0), '%d/%m/%Y')  # 2023-04-04 00:00:00
            if start_date <= message_date <= end_date:
                messages_from_date_interval.append(message)

    return messages_from_date_interval


def create_dict_nucleo2points(messages_from_date_interval: List) -> Tuple[Dict, Dict]:
    """
    :param messages_from_date_interval: lista de mensagens do grupo focafit entre start_date e end_date
    :return nucleo_and_points: dicionário que mapeia cada nucleo para a sua pontuação
    :return name_and_points: dicionário que mapeia cada nome para a sua pontuação
    """

    nucleo_and_points = {}
    name_and_points = {}

    nucleo_pattern = re.compile(r'#(noe|nip|nut|bope|ndp|pres|trainees)', re.IGNORECASE)  # ex: #noe, #NUT
    points_pattern = re.compile(r'([\+|\-]\d+)')  # ex: +2, -10

    for message in messages_from_date_interval:

        # Pega o corpo da mensagem (que inicia depois dos dois pontos)
        # message = '10/05/2023 17:02 - Chico: Chico +2 #NOE'
        message_body = "".join(message.split(':')[2:]).strip()  # NOTE: pq não por [-1]?

        nucleo_match = nucleo_pattern.search(message_body)  # ex: #noe
        points_match = points_pattern.search(message_body)  # ex: +2, -10

        if nucleo_match and points_match:
            message_without_nucleo = nucleo_pattern.sub('', message_body)  # removes #noe
            cleaned_message = points_pattern.sub('', message_without_nucleo).strip()  # removes +2

            nucleo = nucleo_match.group(1).lower()
            points = points_match.group(1)

            assign_points(nucleo_and_points, name_and_points, message, cleaned_message, nucleo, points)
        else:
            continue

    return nucleo_and_points, name_and_points


# sub function
def assign_points(nucleo_and_points: Dict, name_and_points: Dict, message: str, message_text: str, nucleo: str,
                  points: str):
    names = []

    # caso message_text possua nucleo e points mas não tenha nome, nucleo pontua mas a pessoa não.
    # pontuação para o núcleo será considerada mas não será atribuída a nenhum jogador

    # pontuando o núcleo
    if nucleo in nucleo_and_points:
        nucleo_and_points[nucleo] += int(points)
    else:
        nucleo_and_points[nucleo] = int(points)
    try:
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
    except ZeroDivisionError:
        print(f'Problema ao pegar nomes e pontos na seguinte mensagem: {message}')

# sub function
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


# sub function
def get_names_from_message(message_text: str):
    names = []
    splitted_message = message_text.split(',')

    for text in splitted_message:
        name = get_capitalized_name(text)
        if name:
            names.append(name.title())

    return names


# sub function
def get_capitalized_name(message_text: str):
    capitalized_words = re.findall(
        r'\b[A-Z][^A-Z ]+\b', message_text)  # ex: Chico Buarque
    name = ' '.join(capitalized_words)

    return name


def save_results_file(nucleo_and_points: Dict, name_and_points, output_directory_path: str, start_date: datetime,
                      end_date: datetime):
    nucleo_and_points_sorted_by_points = dict(sorted(nucleo_and_points.items(),
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

        file.write('💜💙🖤✅ RANKING POR NÚCLEO ✅💚🧡💛 \n\n')

        for rank, nucleo_points in enumerate(nucleo_and_points_sorted_by_points.items()):
            nucleo = nucleo_points[0]
            points = nucleo_points[1]
            file.write(f'{rank + 1}º {nucleo.upper()}: {points}\n')

        file.write('\n\n')

        file.write('🏆 RANKING POR PESSOA 🏆\n\n')
        for rank, name_points in enumerate(name_and_points_sorted_by_points.items()):
            name = name_points[0]
            points = name_points[1]
            file.write(f'{rank + 1}º {name}: {points}\n')


if __name__ == '__main__':
    main()
