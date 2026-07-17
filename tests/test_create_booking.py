import allure
import jsonschema
import pytest
import requests
from tests.schemas.booking_schema import BOOKING_SCHEMA
from pydantic import ValidationError
from core.models.booking import BookingResponse


@allure.feature('Test сreating booking')
@allure.story('Test successful сreating booking with faker data and json-schema')
def test_create_booking_with_faker(api_client, booking_dates, generate_random_booking_data):
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


@allure.feature('Test сreating booking')
@allure.story('Test successful сreating booking without faker data')
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


@allure.feature('Test сreating booking')
@allure.story('Test successful сreating booking with pydantic validate')
def test_create_booking_with_pydantic(api_client, generate_random_booking_data):
    with allure.step("Генерация данных для создания бронирования"):
        data = generate_random_booking_data

    with allure.step("Создание бронирования"):
        booking_data = api_client.create_booking(data)

    with allure.step("Валидация Pydantic созданного бронирования"):
        try:
            BookingResponse(**booking_data)
        except ValidationError as e:
            raise ValidationError(f"Response validation failed: {e}")#gpt говорит, что такая конструкция
            # с raise ValidationError(f"Response validation failed: {e}") уже не используется в версии Pydantic 2. Верить ему)?

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


@allure.feature('Test сreating booking')
@allure.story('Test successful сreating booking without optional field additionalneeds')
def test_create_booking_without_optional_field(api_client, generate_random_booking_data):
    with allure.step("Генерация данных для создания бронирования без опционального поля additionalneeds"):
        full_data = generate_random_booking_data
        data_without_needs = {k: v for k, v in full_data.items() if
                              k != "additionalneeds"}  # Подсмотрел в gpt пересобрать словарь без одного поля

    with allure.step("Создание бронирования без опционального поля additionalneeds"):
        booking_data = api_client.create_booking(data_without_needs)

    with allure.step("Валидация Pydantic созданного бронирования"):
        try:
            BookingResponse(**booking_data)
        except ValidationError as e:
            raise ValidationError(f"Response validation failed: {e}")

    with allure.step("Проверка данных бронирования в ответе"):
        assert booking_data["booking"]["firstname"] == data_without_needs[
            "firstname"], "firstname бронирования не совпадает с ожидаемым"

        assert booking_data["booking"]["lastname"] == data_without_needs[
            "lastname"], "lastname бронирования не совпадает с ожидаемым"

        assert booking_data["booking"]["totalprice"] == data_without_needs[
            "totalprice"], "totalprice бронирования не совпадает с ожидаемым"

        assert booking_data["booking"]["depositpaid"] == data_without_needs[
            "depositpaid"], "depositpaid бронирования не совпадает с ожидаемым"

        assert booking_data["booking"]["bookingdates"]["checkin"] == data_without_needs["bookingdates"][
            "checkin"], "checkin бронирования не совпадает с ожидаемым"

        assert booking_data["booking"]["bookingdates"]["checkout"] == data_without_needs["bookingdates"][
            "checkout"], "checkout бронирования не совпадает с ожидаемым"

        assert "additionalneeds" not in data_without_needs #Здесь правильно проверку написал?


@allure.feature('Test сreating booking')
@allure.story('Test 500 error if create a booking without a required field bookingdates')
def test_server_error_if_creating_without_required_field(api_client, generate_random_booking_data):
    with allure.step("Генерация данных для создания бронирования без обязательного поля bookingdates"):
        full_data = generate_random_booking_data
        data_without_bookingdates = {k: v for k, v in full_data.items() if k != "bookingdates"}

    # не уверен в логичности и правильности проверки этого теста, но по-другому не придумал, как проверить 500 ошибку,
    # которая отдается постманом, если дернуть пост запрос создания брони без обязательного поля
    with allure.step("Проверка исключения HTTPError из метода raise_for_status функции create_booking api-клиента"):
        with pytest.raises(requests.exceptions.HTTPError) as exc_info:
            api_client.create_booking(data_without_bookingdates)
        assert "500 Server Error: Internal Server Error for url: https://restful-booker.herokuapp.com/booking" in str(
            exc_info.value)


@allure.feature('Test сreating booking')
@allure.story('Test wrong HTTP method')
def test_creating_booking_with_wrong_method(api_client, generate_random_booking_data, mocker):
    with allure.step("Генерация данных для создания бронирования"):
        data = generate_random_booking_data

    with allure.step("Мокирование запроса, чтоб отдал код ошибки 405"):
        mock_response = mocker.Mock()
        mock_response.status_code = 405
        mocker.patch.object(api_client.session, 'post', return_value=mock_response)

    with allure.step("Проверка исключения AssertionError и текста ошибки"):
        with pytest.raises(AssertionError, match="Expected status 200 but got 405"):
            api_client.create_booking(data)


@allure.feature('Test сreating booking')
@allure.story('Test сreating booking with wrong data type')
def test_create_booking_with_wrong_data_type(api_client):
    with allure.step("Подготовка данных c неверным типом у ключа totalprice"):
        wrong_data = {
            "firstname": "Jim",
            "lastname": "Brown",
            "totalprice": "one hundred thousand", # намеренно поменял тип на string
            "depositpaid": 100500,
            "bookingdates": {
                "checkin": "2018-01-01",
                "checkout": "2019-01-01"
            },
            "additionalneeds": "Breakfast"
        }

    with allure.step("Создание бронирования"):
        booking_data = api_client.create_booking(wrong_data)

    with allure.step("Валидация Pydantic созданного бронирования"):
        BookingResponse(**booking_data) # Здесь переписал валидацию, как gpt мне посоветовал, это верно или нет?


@allure.feature('Test сreating booking')
@allure.story('Test сreating booking with wrong URL')
def test_create_booking_with_wrong_url(api_client, generate_random_booking_data, mocker):
    with allure.step("Генерация данных для создания бронирования"):
        data = generate_random_booking_data

    with allure.step("Мокирование запроса, чтоб отдал код ошибки 404"):
        mock_response = mocker.Mock()
        mock_response.status_code = 404
        mocker.patch.object(api_client.session, 'post', return_value=mock_response)

    with allure.step("Проверка исключения AssertionError и текста ошибки"):
        with pytest.raises(AssertionError, match="Expected status 200 but got 404"):
            api_client.create_booking(data)


@allure.feature('Test сreating booking')
@allure.story('Test сreating booking with server timeout')
def test_create_booking_with_server_timeout(api_client, generate_random_booking_data, mocker):
    with allure.step("Генерация данных для создания бронирования"):
        data = generate_random_booking_data

    with allure.step("Мокирование запроса, для возникновения таймаута"):
        mocker.patch.object(api_client.session, 'post', side_effect=requests.Timeout)

    with allure.step("Проверка таймаута"):
        with pytest.raises(requests.Timeout):
            api_client.create_booking(data)


@allure.feature('Test сreating booking')
@allure.story('Test сreating booking with server unavailability')
def test_create_booking_with_server_unavailability(api_client, generate_random_booking_data, mocker):
    with allure.step("Генерация данных для создания бронирования"):
        data = generate_random_booking_data

    with allure.step("Мокирование запроса, для возникновения недоступности сервера"):
        mocker.patch.object(api_client.session, 'post', side_effect=Exception("Server unavailable"))

    with allure.step("Проверка исключения, если сервер недоступен"):
        with pytest.raises(Exception, match="Server unavailable"):
            api_client.create_booking(data)
