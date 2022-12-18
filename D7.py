#Сделать программу расписание - делаем расписание занятий/тренировок или что-то своё.
#Для хранения информации используем текстовые файлы (сохраняем, перезаписываем в них и т.д.) ,
#бесконечный цикл, функции и прочий функционал.
#Программа будет, как консольный бот, который будет нас спрашивать что и как нужно сделать -
#вывести, показать, перезаписать, добавить событие в определенный день недели

import time
import os


# Функция для создания файла со словарем расшифровки дней недели
# Существует для удобства пользователя, чтобы вводить номера, как у нас принято
def weekdays_file_creator(file='weekdays.txt'):
    week_days = {1: 'Понедельник', 2: 'Вторник', 3: 'Среда',
                 4: 'Четверг', 5: 'Пятница', 6: 'Суббота', 0: 'Воскресенье'}
    with open(file, mode='w', encoding='utf-8') as weekdays:
        for key, val in week_days.items():
            weekdays.write('{}:{}\n'.format(key, val))

    return file


# Функция для создания файла со словарем расшифровки дней недели в обратном направлении
def reverse_weekdays_file_creator(file='reverse_weekdays.txt'):
    week_days = {'Понедельник': 0, 'Вторник': 1, 'Среда': 2,
                 'Четверг': 3, 'Пятница': 4, 'Суббота': 5, 'Воскресенье': 6}
    with open(file, mode='w', encoding='utf-8') as reverse_weekdays:
        for key, val in week_days.items():
            reverse_weekdays.write('{}:{}\n'.format(key, val))

    return file


# Функция для чтения созданного выше файла
def weekdays_file_reader(file='weekdays.txt'):
    week_days = {}
    with open(file, mode='r', encoding='utf-8') as weekdays:
        for i in weekdays.readlines():
            key, val = i.strip().split(':')
            week_days[key] = val

    return week_days


# Функция для получения дня недели с пользовательского ввода
# Переформатирует полученное число в формат, пригодный для структуры time
def day_getter(inp_day):
    while True:
        try:
            inp_day = int(inp_day)
            if inp_day in range(1, 6):
                time.strptime(f'{inp_day + 1}', '%w')
                inp_day = str(inp_day + 1)
                return inp_day
            elif inp_day == 6:
                time.strptime(f'{0}', '%w')
                inp_day = '0'
                return inp_day
            elif inp_day == 7:
                time.strptime(f'{1}', '%w')
                inp_day = '1'
                return inp_day
            else:
                raise ValueError
        except ValueError:
            print('Нет такого дня недели, попробуйте еще раз!')
            inp_day = input(f'Введите номер дня недели:\n"1" - Понедельник\n"2" - Вторник\n"3" - Среда'
                            f'\n"4" - Четверг\n"5" - Пятница\n"6" - Суббота\n"7" - Воскресенье\n')


# Аналогично для времени в часах и минутах
def time_getter(inp_time):
    try:
        time.strptime(inp_time, '%H:%M')
    except ValueError:
        print('Ввод неверен, попробуйте еще раз!')
        return time_getter(input(f'Введите время в формате ЧЧ:ММ\n'))

    return inp_time


# Функция собирает время и день недели, делает из них строку
# Возвращает эту строку (будет использоваться дальше как ключ другого словаря)
# Вторым элементом кортежа возвращает заполненную этим днем недели и временем структуру time
def day_and_time_getter():
    inp_day = day_getter(input(f'Введите номер дня недели:\n"1" - Понедельник\n"2" - Вторник\n"3" - Среда'
                               f'\n"4" - Четверг\n"5" - Пятница\n"6" - Суббота\n"7" - Воскресенье\n'))
    week_days_dict = weekdays_file_reader(weekdays_file_creator())
    inp_time = time_getter(input(f'Введите время в формате ЧЧ:ММ\n'))

    day_and_time_struct = time.strptime(f'{inp_time} {int(inp_day)}', '%H:%M %w')
    week_day_str = week_days_dict[str(day_and_time_struct.tm_wday)]
    time_str = time.strftime("%H:%M", day_and_time_struct)

    return f'{week_day_str}, {time_str}', day_and_time_struct


# Функция для создания пустой сетки расписания
def empty_schedule_generator():
    week_days = list(weekdays_file_reader().values())
    hours = []
    for i in range(0, 24):
        for j in range(0, 60):
            if i < 10:
                if j < 10:
                    hours.append(f'0{i}:0{j}')
                else:
                    hours.append(f'0{i}:{j}')
            else:
                if j < 10:
                    hours.append(f'{i}:0{j}')
                else:
                    hours.append(f'{i}:{j}')
    schedule = {}
    for weekday in week_days:
        for hour in hours:
            schedule[f'{weekday}, {hour}'] = 'пусто'

    return schedule


# Функция для сохранения расписания в файл
# Для простоты каждый раз будем перезаписывать заново
def save_schedule(schedule):
    with open("schedule.txt", mode='w', encoding='utf-8') as schedule_file:
        for day_and_time, activity in schedule.items():
            schedule_file.write('{} - {}\n'.format(day_and_time, activity))

    return schedule_file.name


# Функция для получения общего расписания из файла
def get_schedule(file='schedule.txt'):
    schedule = {}
    with open(file, mode='r', encoding='utf-8') as schedule_file:
        for i in schedule_file.readlines():
            day_and_time, activity = i.strip().split(' - ')
            schedule[day_and_time] = activity

    return schedule


# Функция для получения текущего расписания из общего
def get_active_schedule_first(schedule):
    active_schedule_lst = []
    [active_schedule_lst.append(f'{key} - {value}') for key, value in schedule.items() if
        key.split(", ")[0] not in active_schedule_lst and value != 'пусто']

    active_schedule = {}
    for event in active_schedule_lst:
        day_and_time, activity = event.strip().split(' - ')
        active_schedule[day_and_time] = activity

    return active_schedule


# Функция для получения текущего расписания из файла
def get_active_schedule():
    active_schedule = {}
    with open('active_schedule.txt', mode='r', encoding='utf-8') as active_schedule_file:
        for i in active_schedule_file.readlines():
            day_and_time, activity = i.strip().split(' - ')
            active_schedule[day_and_time] = activity

    return active_schedule


# Функция для сохранения текущего расписания в файл
def save_active_schedule(active_schedule):
    with open("active_schedule.txt", mode='w', encoding='utf-8') as active_schedule_file:
        for day_and_time, activity in active_schedule.items():
            active_schedule_file.write('{} - {}\n'.format(day_and_time, activity))

    return active_schedule_file.name


# Функция для вывода текущего расписания в консоль
def print_active_schedule():
    active_schedule = get_active_schedule_first(get_schedule())
    act_schedule_dict = {}
    time_finish, start_out, day, starttime, whats_left, out_activity = '', '', '', '', '', ''
    for day_and_time, activity in active_schedule.items():
        for key, value in active_schedule.items():
            start = day_and_time
            start_out = f'{day_and_time}  -  '
            if active_schedule[start] == value:
                time_finish = key.split(', ')[1]
            else:
                break
        start_out += time_finish
        _, checktime = start_out.split('  -  ')[0].split(', ')
        day_and_starttime, whats_left = start_out.split('  -  ')
        day, starttime = day_and_starttime.split(', ')
        check_activity = active_schedule[f'{day}, {checktime}']
        if act_schedule_dict == {}:
            act_schedule_dict[start_out] = activity
            out_activity = act_schedule_dict[f'{day}, {starttime}  -  {whats_left}']
        elif out_activity != check_activity and start_out not in act_schedule_dict.keys():
            act_schedule_dict[start_out] = activity
            out_activity = act_schedule_dict[f'{day}, {starttime}  -  {whats_left}']

    active_schedule_file = save_active_schedule(act_schedule_dict)

    print(f'Ваше расписание записано в файл {active_schedule_file}')
    print('-' * 75)
    print('Вот ваше расписание:')
    for day_and_time, activity in act_schedule_dict.items():
        print(f'{day_and_time} - {activity}')


# Функция для удаления существующего события
def clear_time_period(schedule, start_struct, new_activity='пусто'):
    for day_and_time, activity in schedule.items():
        day_str, time_str = day_and_time.split(', ')

        week_days_dict = weekdays_file_reader()
        week_day_str = week_days_dict[str(start_struct.tm_wday)]
        schedule[f'{week_day_str}, {time_str}'] = new_activity
    return schedule


# Функция для чтения, проверки и записи события в указанный пользователем диапазон
def activity_period_changer(inp_day_and_time, start_struct, finish_struct, new_activity='пусто'):
    schedule = get_schedule()
    reverse_weekdays = weekdays_file_reader('reverse_weekdays.txt')

    new_schedule = {}
    if new_activity != 'пусто':
        for day_and_time, activity in schedule.items():
            day_str, time_str = day_and_time.split(', ')
            day_num = reverse_weekdays[day_str]
            day_and_time_struct = time.strptime(f'{time_str} {int(day_num)}', '%H:%M %w')

            if start_struct < day_and_time_struct <= finish_struct and activity == 'пусто' \
                    and day_and_time != inp_day_and_time:
                week_days_dict = weekdays_file_reader()
                week_day_str = week_days_dict[str(start_struct.tm_wday)]
                new_schedule[f'{week_day_str}, {time_str}'] = new_activity

        for day_and_time, activity in new_schedule.items():
            schedule[day_and_time] = activity
    else:
        schedule = clear_time_period(schedule, start_struct)

    return schedule


# Функция для проверки ввода диапазона пользователя
def time_period_check(start_struct, finish_struct):
    if start_struct < finish_struct:
        return True
    return False


# Функция для добавления события в расписание
def add():
    print('-' * 75)
    print('Меню добавления')
    print('-' * 75)

    print('-' * 75)
    print('ВНИМАНИЕ')
    print('-' * 75)
    print('Если существующее событие полностью войдет в диапазон нового события, оно будет стерто!')
    print('-' * 75)
    print('ВНИМАНИЕ')
    print('-' * 75)

    print('Введите дату начала нового события')
    inp_day_and_time, start_struct = day_and_time_getter()
    active_schedule = get_active_schedule_first(get_schedule())
    if inp_day_and_time in active_schedule.keys():
        print('Это время уже занято!')
        return
    else:
        print('Введите дату окончания нового события')
        inp_day_and_time_finish, finish_struct = day_and_time_getter()
        if inp_day_and_time_finish in active_schedule.keys():
            print('Это время уже занято!')
            return
        if not time_period_check(start_struct, finish_struct):
            print('Время начала не может быть позже времени окончания!')
            print('Возврат в главное меню')
            return
        if inp_day_and_time_finish.split(', ')[0] != inp_day_and_time.split(', ')[0]:
            print('Нельзя установить одно событие на несколько дней!')
            print('Возврат в главное меню')
            return

        activity = input(f'Событие (00 - для возврата в главное меню): ')
        if activity == '00':
            print('Возврат в главное меню')
            return

        schedule = activity_period_changer(inp_day_and_time, start_struct, finish_struct, activity)
        save_schedule(schedule)

        active_schedule = get_active_schedule_first(get_schedule())
        save_active_schedule(active_schedule)
    return


# Функция для изменения события в расписании
# Начальное время будет являться началом нового события, конечное - его окончанием
# Любые события, попавшие в этот диапазон будут стираться, даже если их временной диапазон выходил за указанный выше
def rewrite():
    print('-' * 75)
    print('Меню редактирования')
    print('-' * 75)

    print('-' * 75)
    print('ВНИМАНИЕ')
    print('-' * 75)
    print('Любые события, попавшие в этот диапазон будут стираться,'
          '\nдаже если их временной диапазон выходил за указанный выше')
    print('-' * 75)
    print('ВНИМАНИЕ')
    print('-' * 75)

    print('Введите день и время для редактирования события')

    inp_day_and_time, start_struct = day_and_time_getter()
    active_schedule = get_active_schedule_first(get_schedule())
    if inp_day_and_time in active_schedule.keys():
        print('Введите дату окончания нового события')
        inp_day_and_time_finish, finish_struct = day_and_time_getter()

        if not time_period_check(start_struct, finish_struct):
            print('Время начала не может быть позже времени окончания!')
            print('Возврат в главное меню')
            return
        if inp_day_and_time_finish.split(', ')[0] != inp_day_and_time.split(', ')[0]:
            print('Нельзя установить одно событие на несколько дней!')
            print('Возврат в главное меню')
            return

        activity = input(f'Событие (00 - для возврата в главное меню): ')
        if activity == '00':
            print('Возврат в главное меню')
            return

        schedule = activity_period_changer(inp_day_and_time, start_struct, finish_struct)
        save_schedule(schedule)

        schedule = activity_period_changer(inp_day_and_time, start_struct, finish_struct, activity)
        save_schedule(schedule)

        active_schedule = get_active_schedule_first(get_schedule())
        save_active_schedule(active_schedule)

        print('Успешно!')
        return

    print('Такого события нет!')
    return


# Функция для удаления события из расписания
def delete():
    print('-' * 75)
    print('ВНИМАНИЕ')
    print('-' * 75)
    print('Вы будете указывать только одно время события!\n'
          'Событие, которое проходит в это время, будет удалено полностью!')
    print('-' * 75)
    print('ВНИМАНИЕ')
    print('-' * 75)
    confirm = input('Вы уверены?\nДля продолжения нажмите Enter\nДля отмены введите "00" и нажмите Enter: ')
    if confirm == '00':
        print('Возврат в главное меню')
        return

    print('-' * 75)
    print('Меню удаления')
    print('-' * 75)

    print('Введите день и время для удаления события')
    inp_day_and_time, start_struct = day_and_time_getter()
    active_schedule = get_active_schedule_first(get_schedule())

    if inp_day_and_time in active_schedule.keys():
        schedule = get_schedule()
        clear_time_period(schedule, start_struct)
        save_schedule(schedule)

        active_schedule = get_active_schedule_first(get_schedule())
        save_active_schedule(active_schedule)

        print('Успешно!')
        return

    print('Такого события нет!')
    return


# Функция для очистки расписания
def clear():
    print('-' * 75)
    print('ВНИМАНИЕ')
    print('-' * 75)
    print('Все события будут удалены!')
    print('-' * 75)
    print('ВНИМАНИЕ')
    print('-' * 75)
    confirm = input('Вы уверены?\nДля продолжения нажмите Enter\nДля отмены введите "00" и нажмите Enter: ')
    if confirm == '00':
        return

    save_active_schedule(get_active_schedule_first(get_schedule(save_schedule(empty_schedule_generator()))))
    print('Успешно!')
    return


# Функция для выбора действия, которое хочет совершить пользователь
# Является основной функцией - зациклена и имеет возможность выхода
def calendar():
    if not os.path.exists('weekdays.txt.txt'):
        weekdays_file_creator()
    if not os.path.exists('reverse_weekdays.txt.txt'):
        reverse_weekdays_file_creator()
    if not os.path.exists('active_schedule.txt'):
        save_active_schedule(get_active_schedule_first(get_schedule(save_schedule(empty_schedule_generator()))))

    while True:
        print('-' * 75)
        print('Главное меню')
        print('-' * 75)
        inp_com = input(f'Введите номер действия:\n"1" - Показать расписание\n'
                        f'"2" - Добавить событие\n"3" - Редактировать событие\n'
                        f'"4" - Удалить событие\n"5" - Очистить расписание\n'
                        f'"0" - Выход из программы\n')
        print('-' * 75)
        try:
            inp_com = int(inp_com)
            if inp_com == 1:
                save_active_schedule(get_active_schedule_first(get_schedule()))
                print_active_schedule()
            elif inp_com == 2:
                add()
            elif inp_com == 3:
                rewrite()
            elif inp_com == 4:
                delete()
            elif inp_com == 5:
                clear()
            elif inp_com == 0:
                quit()
            else:
                raise ValueError
        except ValueError:
            print('Нет такой команды, попробуйте еще раз!')
            return calendar()


calendar()