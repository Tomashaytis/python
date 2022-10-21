import os
import logging
from find import next_exemplar

logger = logging.getLogger()
logger.setLevel('INFO')


class ExemplarIterator:
    """
    Класс-итератор для работы с экземплярами классов.
    """
    _exemplar: str

    def __init__(self, exemplar: str):
        """
        Инициализирует итератор экземпляром exemplar, который содержит путь до него.

        :param exemplar: Путь до экземпляра.
        """
        self._exemplar = exemplar

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
            self._exemplar = next_exemplar(self._exemplar)
        except OSError as error:
            raise error
        if self._exemplar is not None:
            return self._exemplar
        else:
            raise StopIteration


if __name__ == "__main__":
    dataset = 'dataset1'
    ei = ExemplarIterator(os.path.join(dataset, 'leopard_0000.jpg'))
    try:
        while True:
            ei.__next__()
    except StopIteration:
        logging.info('Все данные датасета перебраны')
    except OSError as err:
        logging.warning(f'При переборе датасета {dataset} возникла ошибка:\n{err}')
