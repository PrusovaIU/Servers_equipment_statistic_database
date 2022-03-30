from .dal_meta import DAL
from abc import ABCMeta
from datetime import datetime
from typing import Optional


class StatisticDAL(DAL, metaclass=ABCMeta):
    async def _add_statistic(self, time: Optional[datetime] = None, **kwargs):
        if time is not None:
            kwargs["time"] = time
        new_row = self._table(**kwargs)
        await self._add(new_row)
