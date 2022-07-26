from typing import Type
from dataclasses import dataclass


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    def __init__(self, training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float,
                 ) -> None:
        self.training_type = training_type
        self.distance = distance
        self.speed = speed
        self.calories = calories
        self.duration = duration

    def get_message(self) -> str:
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')


class Training:
    """Базовый класс тренировки."""
    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000
    M_IN_H: int = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action: int = action
        self.duration: float = duration
        self.weight: float = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        distance = self.action * self.LEN_STEP / self.M_IN_KM
        return distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        speed = self.get_distance() / self.duration
        return speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError('Метод не унаследован')

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.__class__.__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""
    CALORIES_MEAN_SPEED_MULTIPLIER: int = 18
    CALORIES_MEAN_SPEED_MULTIPLIER_2: int = 20

    def get_spent_calories(self) -> float:
        calories_run = ((self.CALORIES_MEAN_SPEED_MULTIPLIER
                        * self.get_mean_speed()
                        - self.CALORIES_MEAN_SPEED_MULTIPLIER_2)
                        * self.weight
                        / self.M_IN_KM * self.duration * 60)
        return calories_run


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    A1: float = 0.035
    A3: float = 0.029

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self):
        return (
            (self.A1 * self.weight
             + (self.get_mean_speed()**2 // self.height)
             * self.A3 * self.weight) * self.M_IN_H * self.duration)


class Swimming(Training):
    """Тренировка: плавание."""
    B1: float = 1.1
    B2: int = 2
    LEN_STEP: float = 1.38

    def __init__(self,
                 action: float,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: float) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_distance(self) -> float:
        return self.LEN_STEP * self.action / self.M_IN_KM

    def get_mean_speed(self):
        return (self.length_pool * self.count_pool / self.M_IN_KM
                / self.duration)

    def get_spent_calories(self) -> float:
        return (self.get_mean_speed() + self.B1) * self.B2 * self.weight


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    read: dict[str, Type[Training]] = {
        'RUN': Running,
        'SWM': Swimming,
        'WLK': SportsWalking,
    }
    try:
        return read[workout_type](*data)
    except KeyError:
        raise KeyError(f'Неизвестный код тренировки - {workout_type}')


def main(training: Training) -> None:
    """Главная функция."""
    info: InfoMessage = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)