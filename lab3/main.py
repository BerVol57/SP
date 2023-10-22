"""
Лабораторна робота №3
Код нижче майже нічим не відрізняється від початку другої лабораторної
"""

# Новеньке
from spyre import server

from datetime import datetime
import pandas as pd
import urllib
# Новеньке
import os

print("Setup complete")

# Функція що повертає час в момент виклику
date_and_time_time = ''
data_time_file = "data_time.txt"


def time_now():
    now = datetime.now()
    global date_and_time_time
    date_and_time_time = now.strftime("%d%m%Y%H%M%S")
    print("Time now:", date_and_time_time)


def _save(file_name, file_data):
    if os.path.isfile(file_name):
        _delete(file_name)
    f = open(file_name, "w")
    f.write(file_data)
    f.close()


def _load(file_name):
    f = open(file_name, "r")
    return f.read()


def _delete(file_name):
    if os.path.isfile(file_name):
        os.remove(file_name)


# Функція оновлдення та заванатаження нових даних
def _download_data():
    # Оновл.ємо час
    time_now()

    # Масив з навзами областей України розташовані в алфавітному порядку відносно кирилиці
    index_ua = ['plashka', 22, 24, 23, 25, 3, 4, 8, 19, 20, 21, 9, 90, 10, 11, 12, 13, 14, 15, 16, 250, 17, 18, 6, 1, 2,
                7, 5]

    # Перевіряємо чи папка з даними пуста та чи ця папка існує,
    # якщо ні, то відопвідно очищуємо, або створюємо нову папку
    if os.path.isdir("data"):
        print("Clean directory <data>...")
        for f in os.listdir('data'):
            os.remove("data/" + f)
        print("Complete")
    else:
        print("Create new directory <data>...")
        os.mkdir('data')
        print("Complete")

    # Початок завантаження даних
    print("Download...")

    for i in range(1, 28):
        url = 'https://www.star.nesdis.noaa.gov/smcd/emb/vci/VH/get_TS_admin.php?provinceID={}&country=UKR&yearlyTag=Weekly&type=Mean&TagCropland=crop&year1=1982&year2=2023'.format(
            i)
        wp = urllib.request.urlopen(url)

        text = wp.read()
        out = open(f'data/NOAA_ID_{str(index_ua[i])}_{date_and_time_time}.csv', 'wb')

        # Очищення даних від різного сміття
        text = '\n'.join(text.decode().split("\n")[1:]).replace("<tt><pre>", '').replace("<br>", '').replace(
            "</pre></tt>", '').replace(",", ';').encode()
        out.write(text)
        out.close()
    print("Complete")


#
def get_dataframes(region_index):
    df = pd.read_csv(f'data/NOAA_ID_{region_index}_{date_and_time_time}.csv',
                     sep=';', index_col=False)
    df.columns = df.columns.str.replace(' ', '')
    df = df.drop(df.loc[df['VHI'] == -1].index)
    return df


def take_data_year_week(df, year, week):
    return df[(df['year'] == year) & (df['week'] == week)]


def select_date(df, selected_date):
    try:
        year1 = int(selected_date[:selected_date.find('w')])
        week1 = int(selected_date[selected_date.find('w') + 1:selected_date.find('-')])
        selected_date = selected_date[selected_date.find('-') + 1:]
        year2 = int(selected_date[:selected_date.find('w')])
        week2 = int(selected_date[selected_date.find('w') + 1:])
        print([year1, week1, year2, week2])
        index_first_date = take_data_year_week(df, year1, week1).index[0]
        print(index_first_date)
        index_second_date = take_data_year_week(df, year2, week2).index[0]
        return df.iloc[index_first_date:index_second_date + 1]
    except:
        print("error")
        return df


if input("Update/Download data? [y/n]:") == 'y':
    _download_data()
    _save(data_time_file, date_and_time_time)
else:
    date_and_time_time = _load(data_time_file)


class StockExample(server.App):
    title = "NOAA data visualisation"

    inputs = [{"type": "dropdown",
               "label": "Select value",
               "options": [{"label": "VCI", "value": "VCI"},
                           {"label": "TCI", "value": "TCI"},
                           {"label": "VHI", "value": "VHI"}],
               "key": "selected_value",
               "action_id": "update_data"},
              {"type": 'dropdown',
               "label": 'Province',
               "options": [{"label": "Vinnytsya", "value": 1},
                           {"label": "Volyn", "value": 2},
                           {"label": "Dnipropetrovs'k", "value": 3},
                           {"label": "Donets'k", "value": 4},
                           {"label": "Zhytomyr", "value": 5},
                           {"label": "Transcarpathia", "value": 6},
                           {"label": "Zaporizhzhya", "value": 7},
                           {"label": "Ivano-Frankivs'k", "value": 8},
                           {"label": "Kiev", "value": 9},
                           {"label": "Kirovohrad", "value": 10},
                           {"label": "Luhans'k", "value": 11},
                           {"label": "L'viv", "value": 12},
                           {"label": "Mykolayiv", "value": 13},
                           {"label": "Odessa", "value": 14},
                           {"label": "Poltava", "value": 15},
                           {"label": "Rivne", "value": 16},
                           {"label": "Sumy", "value": 17},
                           {"label": "Ternopil'", "value": 18},
                           {"label": "Kharkiv", "value": 19},
                           {"label": "Kherson", "value": 20},
                           {"label": "Khmel'nyts'kyy", "value": 21},
                           {"label": "Cherkasy", "value": 22},
                           {"label": "Chernivtsi", "value": 23},
                           {"label": "Chernihiv", "value": 24},
                           {"label": "Crimea", "value": 25},
                           {"label": "Kiev City", "value": 90},
                           {"label": "Sevastopol'", "value": 250}],
               "key": "region",
               "action_id": "update_data"},
              {"type": "text",
               "label": "Select date",
               "value": "1982w1-2023w40",
               "key": "selected_date",
               "id": "update_data"}
              ]

    controls = [{"type": "hidden",
                 "id": "update_data"}]

    tabs = ["Plot", "Table"]

    outputs = [{"type": "plot",
                "id": "plot",
                "control_id": "update_data",
                "tab": "Plot"},
               {"type": "table",
                "id": "table_id",
                "control_id": "update_data",
                "tab": "Table",
                "on_page_load": True}]

    def getData(self, params):
        df = get_dataframes(int(params['region']))
        df = select_date(df, params['selected_date'])
        return df

    def getPlot(self, params):
        df = self.getData(params)
        plt_obj = df.plot(y=params['selected_value'], marker="*", color="r")
        plt_obj.set_title(params['selected_value'])
        plt_obj.set_ylabel(params['selected_value'])
        plt_obj.set_xlabel("weeks")
        plt_obj.grid()
        fig = plt_obj.get_figure()
        return fig


app = StockExample()
app.launch()
