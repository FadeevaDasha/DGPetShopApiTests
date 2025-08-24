import allure
import requests
import jsonschema


from .schemas.store_schema import STORE_SCHEMA
from .schemas.store_inventory_schema import INVENTORY_SCHEMA
from .conftest import create_store

BASE_URL = 'http://5.181.109.28:9090/api/v3'

@allure.feature('Store')
class TestStore:

    @allure.title('Размещение заказа ')
    def test_placing_order(self):

        with allure.step('Отправка POST-запрос с телом'):
            payload = {
                "id": 1,
                "petId": 1,
                "quantity": 1,
                "status": "placed",
                "complete": True
            }

            response = requests.post(url=f'{BASE_URL}/store/order', json=payload)
            response_json = response.json()

        with allure.step('Проверка статуса ответа'):
            assert response.status_code == 200, 'Код ответа не совпал с ожидаемым'
            jsonschema.validate(response_json, STORE_SCHEMA)

        with allure.step('Проверка полей в ответе'):
            assert response_json['id'] == payload['id'], 'id заказа не совпадает с ожидаемым'
            assert response_json['petId'] == payload['petId'], 'petId заказа не совпадает с ожидаемым'
            assert response_json['quantity'] == payload['quantity'], 'quantity заказа не совпадает с ожидаемым'
            assert response_json['status'] == payload['status'], 'status заказа не совпадает с ожидаемым'
            assert response_json['complete'] == payload['complete'], 'complete заказа не совпадает с ожидаемым'


    @allure.title('Получение информации о заказе по ID')
    def test_get_store_by_id(self, create_store):
        with allure.step('Получение ID созданного заказа'):
            order_id = create_store['id']

        with allure.step('Отправка запроса на получение информации о заказе по ID'):
            response = requests.get(url=f'{BASE_URL}/store/order/{order_id}')

        with allure.step('Проверка статуса ответа и данных заказа'):
            assert response.status_code == 200, 'Код ответа не совпал с ожидаемым'
            assert response.json()['id'] == order_id, 'id заказа не совпадает с ожидаемым'


    @allure.title('Удаление заказа по ID')
    def test_delete_store_by_id(self, create_store):
        with allure.step('Получение ID созданного заказа'):
            order_id = create_store['id']

        with allure.step('Отправка запроса на удаление заказа'):
            response = requests.delete(url=f'{BASE_URL}/store/order/{order_id}')

        with allure.step('Проверка статуса ответа'):
            assert response.status_code == 200, 'Код ответа не совпал с ожидаемым'

        with allure.step('Отправка запроса на получение информации о заказе по ID'):
            response = requests.get(url=f'{BASE_URL}/store/order/{order_id}')

        with allure.step('Проверка статуса ответа и данных заказа'):
            assert response.status_code == 404, 'Код ответа не совпал с ожидаемым'


    @allure.title('Попытка получить информацию о несуществующем заказе')
    def test_get_nonexistent_order(self):
        with allure.step('Отправка запроса на получение информации о несуществующем заказе'):
            response = requests.get(url=f'{BASE_URL}/store/order/9999')

        with allure.step('Проверка статуса ответа'):
            assert response.status_code == 404, 'Код ответа не совпал с ожидаемым'


    @allure.title('Получение инвентаря магазина')
    def test_get_stores_by_inventory(self):
        with allure.step('Отправка запроса на получение инвентаря магазина'):
            response = requests.get(url=f'{BASE_URL}/store/inventory')

        with allure.step('Проверка статуса ответа и формат'):
            assert response.status_code == 200
            jsonschema.validate(response.json(), INVENTORY_SCHEMA)