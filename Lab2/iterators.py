import os
import logging
from find import next_instance

logger = logging.getLogger()
logger.setLevel('INFO')


class InstanceIterator:
    """
    Класс-итератор для работы с экземплярами классов.
    """

    def __init__(self, instance: str):
        """
        Инициализирует итератор экземпляром exemplar, который содержит путь до него.

        :param instance: Путь до экземпляра.
        """
        self._instance = instance

    def __iter__(self):
        """
        Возвращает текущий объект итератора.

        :return: Текущий объект итератора.
        """
        return self

    def __next__(self):
        """
        Возвращает следующий экземпляр класса на основе текущего.
        Если его нет - бросает исключение StopIteration.

        :return: Следующий экземпляр класса.
        """
        try:
            self._instance = next_instance(self._instance)
        except OSError as error:
            raise error
        if self._instance is not None:
            return self._instance
        else:
            raise StopIteration


if __name__ == "__main__":
    dataset = 'dataset1'
    ei = InstanceIterator(os.path.join(dataset, 'leopard_0000.jpg'))
    try:
        while True:
            ei.__next__()
    except StopIteration:
        logging.info('Все данные датасета перебраны')
    except OSError as err:
        logging.warning(f'При переборе датасета {dataset} возникла ошибка:\n{err}')
