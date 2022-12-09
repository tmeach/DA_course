# АНАЛИЗ ДАННЫХ О БРОНИРОВАНИИ ОТЕЛЕЙ

import pandas as pd

bookings = pd.read_csv('2_bookings.csv', sep =';')
bookings.head()
bookings.dtypes

# 1: Исправляю внешний вид колонок датасета (верхний регистр, пробелы между словами)

# Функция, которая в названиях колонках датасета заменяет пробелы на нижнее подчеркивание и приводит названия к нижнему регистру  
def rename_c(columns):
    new_columns = columns.replace(' ','_').lower()
    return (new_columns)

# Применяю метод rename, в качестве аргумента параметра columns указываю написанную выше функцию
bookings=bookings.rename(columns=rename_c)
bookings

# 2: Пользователи из каких стран совершили наибольшее число успешных бронирований?
top5_book=bookings.query("is_canceled==0").country.value_counts()
top5_book.head()

# 3: На сколько ночей (stays_total_nights) в среднем бронируют отели типа City Hotel? Resort Hotel?
bookings.hotel.unique()
bookings.groupby('hotel', as_index=False).agg({'stays_total_nights':'mean'}).round(2)

# 4: Иногда тип номера, присвоенного клиенту (assigned_room_type),отличается от изначально забронированного (reserved_room_type).Такое может произойти, например, по причине овербукинга. Сколько подобных наблюдений встретилось в датасете?
bookings.query('assigned_room_type != reserved_room_type')

# 5: На какой месяц чаще всего оформляли бронь в 2016 году? Изменился ли самый популярный месяц в 2017?
bookings.arrival_date_year.unique()
bookings.groupby('arrival_date_year').arrival_date_month.agg(pd.Series.mode)

# 6: Сгруппируйте данные по годам, а затем проверьте, на какой месяц (arrival_date_month) бронирования отеля типа City Hotel отменялись чаще всего в 2015? 2016? 2017? 
bookings.query('hotel=="City Hotel"').groupby(['arrival_date_year', 'arrival_date_month']).is_canceled.sum()

# 7: Посмотрите на числовые характеристики трёх колонок: adults, children и babies. Какая из них имеет наибольшее среднее значение?

bookings[['adults', 'children', 'babies']].mean()

# 8 Создайте колонку total_kids, объединив столбцы children и babies. Для отелей какого типа среднее значение переменной оказалось наибольшим?
bookings['total_kids'] = bookings.children + bookings.babies
bookings.groupby('hotel').total_kids.mean().round(2)

# 9 Не все бронирования завершились успешно (is_canceled), поэтому можно посчитать, сколько клиентов было потеряно в процессе(Churn Rate).Создайте переменную has_kids, которая принимает значение True, если клиент при бронировании указал хотя бы одного ребенка (total_kids), в противном случае – False. Далее проверьте, среди какой группы пользователей показатель оттока выше. 

def has_kids(x):
    if x > 0:
        return True
    else:
        return False

bookings['has_kids'] = bookings.total_kids.apply(has_kids)
bookings['has_kids'] = bookings.total_kids.astype(bool)
bookings[['has_kids', 'is_canceled']].value_counts() / bookings [['has_kids']].value_counts() *100