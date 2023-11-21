from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout

class MinecraftLogsApp(App):
    def build(self):
        self.ip_address = "s21.mcskill.net:24566"
        self.last_index = 0

        layout = BoxLayout(orientation='vertical')

        self.name_query_input = TextInput(text='', multiline=False)
        layout.add_widget(self.name_query_input)

        self.function_spinner = Spinner(
            text='Выберите функцию',
            values=["Полный лог по дате и имени", "Все логи по имени", "Полный лог по дате",
                    "Проверка на маты и капс в новых логах", "Получение ников с сервера по IP", "Выход"]
        )
        self.function_spinner.bind(on_text=self.on_spinner_select)
        layout.add_widget(self.function_spinner)

        self.output_label = Label(text='', halign='left', valign='top', size_hint_y=None, height=500)
        layout.add_widget(self.output_label)

        return layout

    def on_spinner_select(self, spinner, text):
        if text == "Выход":
            self.stop()
        elif text == "Получение ников с сервера по IP":
            self.get_player_names()
        elif text == "Полный лог по дате и имени":
            self.get_full_logs_by_date_and_name()
        # Добавьте другие функции по мере необходимости

    def get_player_names(self):
        player_names = self.get_player_names_from_server(self.ip_address)
        if player_names:
            self.output_label.text = "Список игроков на сервере:\n" + "\n".join(player_names)
        else:
            self.output_label.text = "Не удалось получить список игроков с сервера."

    def get_full_logs_by_date_and_name(self):
        date_query = input("Введите дату (в формате dd-mm-yyyy): ")
        logs_by_date = self.get_logs_from_website_by_date(self.name_query_input.text, date_query)
        for log_line in logs_by_date:
            self.process_log_line(log_line)
        logs_by_name = self.get_logs_from_website_by_name(self.name_query_input.text)
        for log_line in logs_by_name:
            self.process_log_line(log_line)
        self.last_index = len(logs_by_name) - 1

    # Добавьте другие методы по мере необходимости

    # Остальной код остается примерно таким же

if __name__ == '__main__':
    MinecraftLogsApp().run()
