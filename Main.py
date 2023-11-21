import requests
from colorama import Fore, Style, init
import re
import time
from win10toast import ToastNotifier
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter
from bs4 import BeautifulSoup

init(autoreset=True)

def print_colored(line, color=Fore.WHITE):
    print(f"{color}{line}{Style.RESET_ALL}")

def get_logs_from_website_by_date(name_query, date):
    url = f'https://logs21.mcskill.net/HardEvolution3_isis_public_logs/{date}.txt'
    response = requests.get(url)

    if response.status_code == 200:
        log_text = response.text.strip()
        filtered_logs = [line for line in log_text.split('\n') if name_query in line]
        return filtered_logs
    else:
        return [f"Ошибка при запросе к сайту. Код статуса: {response.status_code}"]

# Функция для получения логов по имени
def get_logs_from_website_by_name(name_query):
    url = f'https://logs21.mcskill.net/HardEvolution3_isis_public_logs/latest.txt'
    response = requests.get(url)

    if response.status_code == 200:
        log_text = response.text.strip()
        filtered_logs = [line for line in log_text.split('\n') if name_query in line]
        return filtered_logs
    else:
        return [f"Ошибка при запросе к сайту. Код статуса: {response.status_code}"]

def get_player_names_from_server(ip):
    try:
        url = f'https://api.mcsrvstat.us/2/{ip}'
        response = requests.get(url)
        data = response.json()

        if response.status_code == 200 and data.get("players"):
            player_names = data["players"]["list"]
            return player_names
        else:
            print("Не удалось получить список игроков с сервера.")
            return []
    except Exception as e:
        print(f"Ошибка при получении списка игроков с сервера: {e}")
        return []

def get_full_logs_by_date(date):
    url = f'https://logs21.mcskill.net/HardEvolution3_isis_public_logs/{date}.txt'
    response = requests.get(url)

    if response.status_code == 200:
        log_text = response.text.strip()
        return log_text.split('\n')
    else:
        return [f"Ошибка при запросе к сайту. Код статуса: {response.status_code}"]

def get_new_logs(full_log, last_index):
    if last_index >= len(full_log) - 1:
        return []
    return full_log[last_index + 1:]

def process_log_line(log_line):
    # Проверяем строки на определенные шаблоны и применяем цвета соответственно
    if re.search(r"\[\d{2}:\d{2}:\d{2}\] .* issued server command: /*", log_line):
        print_colored(log_line, Fore.YELLOW)
    elif re.search(r"\[\d{2}:\d{2}:\d{2}\] .* (вышел|зашёл)", log_line):
        print_colored(log_line, Fore.RED)
    elif re.search(r"\[\d{2}:\d{2}:\d{2}\] \[(G|L)\] .*: .*", log_line):
        print_colored(log_line, Fore.LIGHTMAGENTA_EX)
    elif re.search(r"\[\d{2}:\d{2}:\d{2}\] \[ClearLag\] Удалено \d+ предметов в мире .*", log_line):
        print_colored(log_line, Fore.CYAN)
    elif re.search(r"\[\d{2}:\d{2}:\d{2}\] .* умер .*", log_line):
        print_colored(log_line, Fore.LIGHTCYAN_EX)
    else:
        # Проверка на маты и капс
        check_profanity(log_line)

def check_profanity(log_line):
    # Проводим проверку на маты и капс в сообщении
    words = re.findall(r'\b\w+\b', log_line)
    profanity_count = sum(1 for word in words if is_profanity(word) or is_all_caps(word))

    # Если маты или капс обнаружены, выводим уведомление
    if profanity_count > 3:
        print_colored(f"Обнаружено {profanity_count} матерных слов в сообщении: {log_line}", Fore.RED)
        notify_windows(f"Обнаружено {profanity_count} матерных слов в сообщении:\n{log_line}")

def notify_windows(message):
    toaster = ToastNotifier()
    toaster.show_toast("Обнаружено", message, duration=10)

def is_profanity(word):
    # Пример: простейшая проверка на маты
    profanity_list = ['СУКА', 'сука', 'Блять','нахуя', 'гандон']  # Замените это на ваш список матерных слов
    return word.lower() in profanity_list

def is_all_caps(word):
    # Проверка, является ли слово написанным заглавными буквами
    return word.isupper()

def main():
    last_index = 0

    while True:
        ip_address = "s21.mcskill.net:24566"  # Замените на адрес вашего сервера

        player_names = get_player_names_from_server(ip_address)
        name_query_completer = WordCompleter(player_names)
        name_query = prompt("Введите имя для поиска: ", completer=name_query_completer)

        print("\nВыберите функцию:")
        print_colored("[1] Полный лог по дате и имени", Fore.GREEN)
        print_colored("[2] Все логи по имени", Fore.YELLOW)
        print_colored("[3] Полный лог по дате", Fore.CYAN)
        print_colored("[4] Проверка на маты и капс в новых логах", Fore.MAGENTA)
        print_colored("[5] Получение ников с сервера по IP", Fore.BLUE)
        print_colored("[q] Выход", Fore.RED)

        choice = input("Введите номер функции: ")

        if choice == '1':
            date_query = input("Введите дату (в формате dd-mm-yyyy): ")
            logs_by_date = get_logs_from_website_by_date(name_query, date_query)
            for log_line in logs_by_date:
                process_log_line(log_line)
            logs_by_name = get_logs_from_website_by_name(name_query)
            for log_line in logs_by_name:
                process_log_line(log_line)
            last_index = len(logs_by_name) - 1
        elif choice == '3':
            date_query = input("Введите дату (в формате dd-mm-yyyy): ")
            full_logs_by_date = get_full_logs_by_date(date_query)
            for log_line in full_logs_by_date:
                process_log_line(log_line)
            last_index = len(full_logs_by_date) - 1
        elif choice == '4':
            # Проверка на маты и капс в новых логах раз в секунду
            while True:
                new_logs = get_new_logs(get_full_logs_by_date(time.strftime("%d-%m-%Y")), last_index)
                for log_line in new_logs:
                    process_log_line(log_line)
                last_index += len(new_logs)
                time.sleep(1)
        elif choice == '5':
            # Получаем список игроков с сервера и выводим на экран
            player_names = get_player_names_from_server(ip_address)
            if player_names:
                print("Список игроков на сервере:")
                for name in player_names:
                    print(name)
            else:
                print("Не удалось получить список игроков с сервера.")
        elif choice.lower() == 'q':
            break
        else:
            print_colored("Некорректный выбор. Пожалуйста, введите 1, 2, 3, 4, 5 или 'q'.", Fore.RED)

if __name__ == "__main__":
    main()
