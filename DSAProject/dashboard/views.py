""" Связывание всех компонентов: запросов от пользователя, БД и алгоритмов"""
from django.shortcuts import render
from .models import Flight
from .structures import MyHashMap


def index(request):
    # Пока тестовые, тк выгрузки из файла в бд нет (request содержит всю инфу про запрос)
    if Flight.objects.count() == 0:
        Flight.objects.create(flight_id="FLT001", airline="Lufthansa", origin_airport="FRA",
                              destination_airport="DEL", departure_delay_min=45)

    # Инициализация Hash Map
    hash_map = MyHashMap()
    # достаем все рейсы из бд как SELECT *
    flights = Flight.objects.all()
    for flight in flights:
        # Ключ = Flight_ID, Значение = Сам объект рейса
        hash_map.put(flight.flight_id, flight)

    # всё, что кладется в словарь, Django передаст в HTML-шаблон, чтобы показать пользователю на экране
    context = {}

    # Обработка поиска (если пользователь нажал кнопку "Найти", форма отправляет запрос POST)
    if request.method == "POST":
        # Что ввел юзер?
        search_id = request.POST.get("flight_id")
        # ИСПОЛЬЗУЕМ ХЕШ-ТАБЛИЦУ ЗА O(1)
        found_flight = hash_map.get(search_id)

        if found_flight:
            context['flight'] = found_flight
        else:
            context['error'] = f"Рейс {search_id} не найден"

    # В страницу юзера передаем сообщение через index.html
    return render(request, 'dashboard/index.html', context)
