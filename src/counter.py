from os import path
import re
from datetime import datetime, timedelta
from typing import Dict, List, Tuple
from argparse import ArgumentParser
from tests.functions import print_messages_from_interval
import json


def main():
    parser = ArgumentParser()
    parser.add_argument('-i', '--input_file_path', type=str,
                        default='./assets/input/chat.txt')
    parser.add_argument('-o', '--output_directory_path',
                        type=str, default='./assets/output')
    parser.add_argument('-d', '--primeiro_dia_contagem', type=str,
                        default=datetime.now().strftime('%d/%m/%Y'))
    parser.add_argument('-l', '--language', type=str,
                        default='pt')

    parser.add_argument('-t', '--test', action='store_true')

    parser.add_argument('-e', '--example', action='store_true')

    args = parser.parse_args()

    test = args.test
    input_file_path = args.input_file_path
    output_directory_path = args.output_directory_path
    primeiro_dia_contagem = args.primeiro_dia_contagem
    language = args.language
    example = args.example

    start_date = datetime.strptime(primeiro_dia_contagem, '%d/%m/%Y')
    end_date = start_date + timedelta(days=6)

    messages_from_date_interval = extract_messages_from_date_interval(language,
                                                                      input_file_path, start_date, end_date)

    if test:
        print_messages_from_interval(messages_from_date_interval)

    nucleos_and_points, name_and_points = create_rankings(
        messages_from_date_interval)

    save_results_file(nucleos_and_points, name_and_points,
                      output_directory_path, start_date, end_date, example)

    print(f"Relatório gerado com sucesso e salvo em {output_directory_path}")


def extract_messages_from_date_interval(language: str, input_file_path: str, start_date: datetime,
                                        end_date: datetime) -> List[str]:
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
        date_match = re.search(r'\d{1,2}/\d{1,2}/\d{2,4}', message)
        if date_match:

            if language == 'pt':
                message_date = datetime.strptime(date_match.group(0), '%d/%m/%Y')  # 22/04/23
            elif language == 'en':
                message_date = datetime.strptime(date_match.group(0), '%m/%d/%y')  # 04/22/23
            else:
                print("Linguagem incorreta")
                exit()
            if start_date <= message_date <= end_date:
                messages_from_date_interval.append(message)

    return messages_from_date_interval


def create_rankings(messages_from_date_interval: List) -> Tuple[Dict, Dict]:
    """
    :param messages_from_date_interval: lista de mensagens do grupo focafit entre start_date e end_date
    :return nucleos_and_points: dicionário que mapeia cada nucleo para a sua pontuação
    :return name_and_points: dicionário que mapeia cada nome para a sua pontuação
    """

    nucleos_and_points = {}

    name_and_points = {}
    nucleo_pattern = re.compile(r'#(noe|nip|nut|bope|ndp|pres|trainees)', re.IGNORECASE)  # ex: #noe, #NUT
    points_pattern = re.compile(r'([\+|\-]\d+)')  # ex: +2, -10
    name_pattern = re.compile(r'([A-ZÁÉÍÓÚ][a-záéíóú ]+)+')

    # message = '10/05/2023 17:02 - Chico: Chico +2 #NOE'
    for message in messages_from_date_interval:
        # Pega o corpo da mensagem (que inicia depois dos dois pontos)
        # message without date and time        
        message_body = "".join(message.split(':')[-1]).strip()  # NOTE: pq não por [-1]?
        nucleo_match = nucleo_pattern.search(message_body)  # ex: #noe
        points_match = points_pattern.search(message_body)  # ex: +2, -10
        name_match = name_pattern.search(message_body)
        if points_match:
            if nucleo_match:
                nucleo  = nucleo_match.group(1).lower()
                points = points_match.group(1)
                assign_points_ranking_nucleo(nucleos_and_points, nucleo, points)
            if name_match:
                points = points_match.group(1)
                message_without_nucleo = nucleo_pattern.sub('', message_body)  # removes #noe
                cleaned_message = points_pattern.sub('', message_without_nucleo).strip()  # removes +2
                assign_points_ranking_individual(name_and_points, cleaned_message, points)
        else:
            continue
    return nucleos_and_points, name_and_points


def assign_points_ranking_nucleo(nucleos_and_points: dict, nucleo: str, points: int):
    if nucleo in nucleos_and_points:
        nucleos_and_points[nucleo] += int(points)
    else:
        nucleos_and_points[nucleo] = int(points)


# sub function
def assign_points_ranking_individual(name_and_points: Dict, cleaned_message: str, points: str):
    names = []
    if ',' in cleaned_message:
        names = get_names_from_message(cleaned_message)
        points = int(points) // len(names)
    else:
        name = get_name_from_message(cleaned_message)
        if name:
            names.append(name)

    for name in names:
        if name in name_and_points:
            name_and_points[name] += int(points)
        else:
            name_and_points[name] = int(points)


# sub function
def get_name_from_message(cleaned_message: str):
    message_words = cleaned_message.split(' ')
    # Se só tiver uma palavra, essa palavra é o nome
    if len(message_words) == 1:
        name = message_words[0]
    else:
        # Se tiver mais de uma palavra, pega as palavras que começam com letra maiúscula e junta
        name = get_capitalized_name(cleaned_message)
        # Se tiver mais de uma palavra mas nenhuma começar com letra maiúscula, pega a primeira palavra
        if not name:
            name = message_words[0]

    # return name.title()
    return name


# sub function
def get_names_from_message(cleaned_message: str):
    names = []
    splitted_message = cleaned_message.split(',')

    for text in splitted_message:
        name = get_capitalized_name(text)
        
        #TEST: Testando nomes que não necessariamente seguem formato "Rafael Costa". Pode ser "RAFAEL costa, Rafael COSTA, etc"
        if name:
            # names.append(name.title())
            names.append(name)

    return names


# sub function
def get_capitalized_name(cleaned_message: str):

    #TEST: Testando nomes que não necessariamente seguem formato "Rafael Costa". Pode ser "RAFAEL costa, Rafael COSTA, etc"
    # capitalized_words = re.findall(
    #     r'\b[A-Z][^A-Z ]+\b', cleaned_message)  # ex: Chico Buarque
    capitalized_words = re.findall(
        r'\b[A-Z][a-zA-Z]+\b', cleaned_message)  # ex: Chico Buarque
    name = ' '.join(capitalized_words)
    # brbrbrb #NUT Gui +2
    return name


def save_results_file(nucleos_and_points: Dict, name_and_points: Dict, output_directory_path: str, start_date: datetime,
                      end_date: datetime, example: bool):
    """
    :param nucleos_and_points: dicionário que mapeia cada nucleo para a sua pontuação
    :param name_and_points: dicionário que mapeia cada nome para a sua pontuação
    :param output_directory_path: caminho do diretório de saída onde arquivo 'results.txt' será salvo; ex: './assets/output'
    :param start_date: data de início da contagem; ex: datetime(2023, 7, 10) # 2023-07-10 00:00:00
    :param end_date:  data de fim da contagem; ex: datetime(2023, 7, 16) # 2023-07-16 00:00:00
    """
    nucleos_and_points_sorted_by_points = dict(sorted(nucleos_and_points.items(),
                                                      key=lambda item: item[1],
                                                      reverse=True))

    name_and_points_sorted_by_points = dict(sorted(name_and_points.items(),
                                                   key=lambda item: item[1],
                                                   reverse=True))
    if example:
        with open('./assets/input/minimo_pontos_nucleo_example.json', 'r', encoding='utf-8') as file:
            name_and_points_minimo = json.load(file)
        
    else:
        with open('./assets/input/minimo_pontos_nucleo.json', 'r', encoding='utf-8') as file:
            name_and_points_minimo = json.load(file)

    output_file_path = path.join(output_directory_path, 'results.txt')

    with open(output_file_path, 'w', encoding='utf-8') as file:

        start_date_formatted = start_date.strftime('%d/%m/%y')
        end_date_formatted = end_date.strftime('%d/%m/%y')

        file.write(
            f'🦾 FOCA FIT SEMANAL - {start_date_formatted} A {end_date_formatted} 🦾 \n')
        file.write('Gerado por: Focafit_counter 😎 \n\n')

        file.write('💜💙🖤✅ RANKING POR NÚCLEO ✅💚🧡💛 \n\n')

        for rank, nucleo_and_points in enumerate(nucleos_and_points_sorted_by_points.items()):
            nucleo = nucleo_and_points[0]
            points = nucleo_and_points[1]

            if points >= name_and_points_minimo[nucleo]:
                file.write(f'{rank + 1}º {nucleo.upper()}: {points} ✅\n')
            else:
                file.write(f'{rank + 1}º {nucleo.upper()}: {points}\n')

        file.write('\n\n')

        file.write('🏆 RANKING POR PESSOA 🏆\n\n')
        for rank, name_points in enumerate(name_and_points_sorted_by_points.items()):
            name = name_points[0]
            points = name_points[1]
            file.write(f'{rank + 1}º {name}: {points}\n')


if __name__ == '__main__':
    main()
