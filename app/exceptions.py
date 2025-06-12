from fastapi import HTTPException,status



UserAlreadyExistsExceptions = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="Пользователь уже существует",
)


IncorrectEmailOrPasswordException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail= 'Неверная почта или пароль',
)

TokenExpiredException = HTTPException(
    status_code = status.HTTP_401_UNAUTHORIZED,
    detail='Токен истек',
)

TokeAbsentException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Токен отсутствует",
)


IncorrectTokenFormaException  = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Неверный формат токена",
)

UserIsNotPresentHTTPException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
)

NoHotelHTTPException = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail= "Нету Отеля "

)


RoomCannotBeBooked = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail= "Не осталось свободных номеров "

)


AbsentBooking = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail= "Нету такой брони "

)


LargeDateFromHttpException = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail = 'Дата заезда больше или равна даты выезда'
)

UnableToBookDate = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail = 'Количество забронированных дней больше 30'
)