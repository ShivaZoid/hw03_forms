"""
При запросе клиента возвращается специальный объект response.
В нём содержится ответ сервера и дополнительная информация:

status_code — содержит код ответа запрошенного адреса;

client — объект клиента, который использовался для обращения;

content — данные ответа в виде строки байтов;

context — словарь переменных, переданный для отрисовки шаблона при вызове
функции render();

request — объект request, первый параметр view-функции, обработавшей запрос;

templates — перечень шаблонов, вызванных для отрисовки запрошенной страницы;

resolver_match — специальный объект, соответствующий path() из списка
urlpatterns.
"""


from django.test import TestCase, Client


class StaticURLTests(TestCase):
    def setUp(self):
        # Устанавливаем данные для тестирования
        # Создаём экземпляр клиента. Он неавторизован.
        self.guest_client = Client()

    def test_homepage(self):
        # Отправляем запрос через client,
        # созданный в setUp()
        response = self.guest_client.get('/')
        self.assertEqual(response.status_code, 200)
