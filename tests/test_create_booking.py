import allure
import jsonschema
from tests.schemas.booking_schema import BOOKING_SCHEMA


@allure.feature('Test сreate booking')
@allure.story('Test successful сreate booking')
def test_create_booking(api_client, booking_dates, generate_random_booking_data):
    with allure.step("Генерация данных для создания бронирования"):
        data = generate_random_booking_data
    with allure.step("Создание бронирования"):
        booking_data = api_client.create_booking(data)

    with allure.step("Валидация JSON-схемы созданного бронирования"):
        jsonschema.validate(booking_data, BOOKING_SCHEMA)

    with allure.step("Проверка данных бронирования в ответе"):
        assert booking_data["booking"]["firstname"] == data[
            "firstname"], "firstname бронирования не совпадает с ожидаемым"

        assert booking_data["booking"]["lastname"] == data["lastname"], "lastname бронирования не совпадает с ожидаемым"

        assert booking_data["booking"]["totalprice"] == data[
            "totalprice"], "totalprice бронирования не совпадает с ожидаемым"

        assert booking_data["booking"]["depositpaid"] == data[
            "depositpaid"], "depositpaid бронирования не совпадает с ожидаемым"

        assert booking_data["booking"]["additionalneeds"] == data[
            "additionalneeds"], "additionalneeds бронирования не совпадает с ожидаемым"

        assert booking_data["booking"]["bookingdates"]["checkin"] == data["bookingdates"][
            "checkin"], "checkin бронирования не совпадает с ожидаемым"

        assert booking_data["booking"]["bookingdates"]["checkout"] == data["bookingdates"][
            "checkout"], "checkout бронирования не совпадает с ожидаемым"


@allure.feature('Test сreate booking')
@allure.story('Test successful сreate booking without faker data')
def test_create_booking_without_faker(api_client):
    with allure.step("Подготовка данных для создания бронирования"):
        data = {
            "firstname": "Jim",
            "lastname": "Brown",
            "totalprice": 111,
            "depositpaid": True,
            "bookingdates": {
                "checkin": "2018-01-01",
                "checkout": "2019-01-01"
            },
            "additionalneeds": "Breakfast"
        }

    with allure.step("Создание бронирования"):
        booking_data = api_client.create_booking(data)

    with allure.step("Валидация JSON-схемы созданного бронирования"):
        jsonschema.validate(booking_data, BOOKING_SCHEMA)

    with allure.step("Проверка данных бронирования в ответе"):
        assert booking_data["booking"]["firstname"] == data[
            "firstname"], "firstname бронирования не совпадает с ожидаемым"

        assert booking_data["booking"]["lastname"] == data["lastname"], "lastname бронирования не совпадает с ожидаемым"

        assert booking_data["booking"]["totalprice"] == data[
            "totalprice"], "totalprice бронирования не совпадает с ожидаемым"

        assert booking_data["booking"]["depositpaid"] == data[
            "depositpaid"], "depositpaid бронирования не совпадает с ожидаемым"

        assert booking_data["booking"]["additionalneeds"] == data[
            "additionalneeds"], "additionalneeds бронирования не совпадает с ожидаемым"

        assert booking_data["booking"]["bookingdates"]["checkin"] == data["bookingdates"][
            "checkin"], "checkin бронирования не совпадает с ожидаемым"

        assert booking_data["booking"]["bookingdates"]["checkout"] == data["bookingdates"][
            "checkout"], "checkout бронирования не совпадает с ожидаемым"
