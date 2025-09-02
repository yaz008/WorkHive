from project.configs import TableConfig
from project.libs.orm import TempValue, CachedSingleTable


temp_users: CachedSingleTable[int, TempValue] = CachedSingleTable(
    database=TableConfig.TempUsers.database,
    table=TableConfig.TempUsers.table,
    key_cls=int,
    value_cls=TempValue,
    cache_size=TableConfig.TempUsers.cache_size,
)
