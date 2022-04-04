from abc import ABCMeta, abstractmethod


class MetaTable:
    @property
    @abstractmethod
    def _schema(self) -> str:
        pass

    @classmethod
    def get_full_name(cls) -> str:
        a = f"{cls._schema}.{cls.__tablename__}"
        return f"{cls._schema}.{cls.__tablename__}"
