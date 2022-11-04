from find import next_instance


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

    def __iter__(self) -> str:
        """
        Возвращает текущий объект итератора.

        :return: Текущий объект итератора.
        """
        return self._instance

    def __next__(self) -> str:
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
