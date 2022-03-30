from db.dals.modules_info_dal import ModulesInfoDAL, ModulesInfo
from db.dals.modules_statistic_dal import ModulesStatisticDAL
from db.dals.servers_info_dal import ServersInfoDAL
from db.dals.servers_statistic_dal import ServersStatisticDAL
from db.dals.sockets_info_dal import SocketsInfoDAL
from db.dals.sockets_statistic_dal import SocketsStatisticDAL
from fastapi import APIRouter
from http import HTTPStatus
from initers import get_session
from logging import getLogger
from random import randint, choice, uniform
from typing import Dict, List


api_router = APIRouter()


class RandomDataGenerator:
    def __init__(self, db_session):
        self.__db_session = db_session
        self.__logger = getLogger("Random data generator logger")
        self.__modules_amount = list()
        self.__sockets = list()
        self.__task_types: Dict[str, List[str]] = {
            type_name: self.__generate_config_params(f"{type_name}", params_amount)
            for type_name, params_amount in zip(['ta', 'tb', 'tc'], [10, 7, 3])
        }
        self.__module_types: Dict[str, List[str]] = {
            type_name: self.__generate_config_params(f"{type_name}_module", params_amount)
            for type_name, params_amount in zip(['A', 'B', 'C', 'D', 'E', 'F'], [9, 17, 7, 4, 15, 4])
        }

    @staticmethod
    def __generate_config_params(param_type: str, param_amount: int) -> List[str]:
        return [f"{param_type}_param_{i}" for i in range(param_amount)]

    async def create_info(self):
        servers_info_dal = ServersInfoDAL(self.__db_session)
        modules_info_dal = ModulesInfoDAL(self.__db_session)
        socket_info_dal = SocketsInfoDAL(self.__db_session)
        for server_id in range(randint(5, 15)):
            task = choice(list(self.__task_types.keys()))
            await servers_info_dal.add_server(
                server_id,
                task,
                str('.').join([f"{randint(100, 255)}" for _ in range(4)]),
                {param_name: randint(-100, 100) for param_name in self.__task_types[task]}
            )
            modules_amount = randint(10, 30)
            self.__modules_amount.append(modules_amount)
            for module_position in range(modules_amount):
                await modules_info_dal.add_module(server_id, module_position, choice(list(self.__module_types.keys())))
            sockets = list()
            for socket in range(randint(5, 10)):
                port = randint(1, 99999)
                sockets.append(port)
                await socket_info_dal.add_socket(
                    server_id,
                    f"socket_server:{server_id}_{socket}",
                    port,
                    choice(["net1", "net2", "net3", "net4"])
                )
            self.__sockets.append(sockets)

    async def add_statistic(self):
        servers_statistic_dal = ServersStatisticDAL(self.__db_session)
        servers_temperatures = [uniform(0, 100) for _ in range(len(self.__modules_amount))]
        servers_disc = [randint(1048576, 13421772800) for _ in range(len(self.__modules_amount))]
        for i in range(10):
            for server_id in range(len(self.__modules_amount)):
                await servers_statistic_dal.add(
                    server_id,
                    servers_temperatures[server_id],
                    choice([None, uniform(-10, 50)]),
                    randint(1048576, 1048576000),
                    servers_disc[server_id]
                )
                servers_temperatures[server_id] += uniform(-5, 5)
                servers_disc[server_id] += randint(-134217728, 134217728)
                await self.__add_modules_statistic(server_id)
                await self.__add_sockets_statistic(server_id)

    async def __add_modules_statistic(self, server_id: int):
        modules_statistic_dal = ModulesStatisticDAL(self.__db_session)
        modules_info_dal = ModulesInfoDAL(self.__db_session)
        for module_position in range(self.__modules_amount[server_id]):
            if randint(1, 100) % 13.5 == 0:
                status, message = choice([
                    [-2, "Warning text"],
                    [-1, "Error text"],
                    [0, None]
                ])
            else:
                status = 1
                message = None
            data = {}
            if status == 1:
                module_info_rows = await modules_info_dal.get_module(server_id, module_position)
                for module_info in module_info_rows:
                    module_type = module_info.module_type
                    data = {param_name: randint(-1000, 5000) for param_name in self.__module_types[module_type]}
            await modules_statistic_dal.add(server_id, module_position, status, message, data)

    async def __add_sockets_statistic(self, server_id: int):
        socket_statistic_dal = SocketsStatisticDAL(self.__db_session)
        sockets = self.__sockets[server_id]
        statuses = ["run", "stop"]
        for port in sockets:
            status = choice(statuses)
            params_amount = 6
            if status == statuses[0]:
                args = [randint(0, 1000000) for _ in range(params_amount)]
            else:
                args = [None] * params_amount
            for direction in [False, True]:
                await socket_statistic_dal.add(server_id, port, status, direction, *args)


@api_router.post("/generate_random_data", status_code=HTTPStatus.CREATED)
async def generate_random_data():
    async with get_session() as session:
        generator = RandomDataGenerator(session)
        await generator.create_info()
        await generator.add_statistic()
