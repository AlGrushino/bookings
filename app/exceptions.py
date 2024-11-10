from fastapi import HTTPException, status


class BookingException(HTTPException):
    status_code = 500
    detail = ""

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class UserAlreadyExistsException(BookingException):
    status_code = (status.HTTP_409_CONFLICT,)
    detail = "Пользователь уже существует"


class IncorrectEmailOrPasswordException(BookingException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Неверная почта или пароль"


class TokenExpiredException(BookingException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Токен истёк"


class TokenAbsentException(BookingException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Токен отсутствует"


class IncorrectTokenFormatException(BookingException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Неверный формат токена"


class UserIsNotPresentException(BookingException):
    status_code = status.HTTP_401_UNAUTHORIZED


class RoomCannotBeBooked(BookingException):
    status_code = status.HTTP_409_CONFLICT
    detail = "Не осталось свободных номеров"


class HotelCannotBeAdded(BookingException):
    status_code = status.HTTP_409_CONFLICT
    detail = "Отель не может быть добавлен"


class HotelDoesNotExist(BookingException):
    status_code = status.HTTP_409_CONFLICT
    detail = "Отель не сущесвует в базе данных"


class RoomCannotBeAdded(BookingException):
    status_code = status.HTTP_409_CONFLICT
    detail = "Комната не может быть добавлена"


class RoomDoesNotExist(BookingException):
    status_code = status.HTTP_409_CONFLICT
    detail = "Комната не существует"
