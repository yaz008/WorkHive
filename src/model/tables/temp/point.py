from project.configs import TableConfig
from project.libs.orm import TempValue, CachedSingleTable


temp_points: CachedSingleTable[int, TempValue] = CachedSingleTable(
    database=TableConfig.TempPoints.database,
    table=TableConfig.TempPoints.table,
    key_cls=int,
    value_cls=TempValue,
    cache_size=TableConfig.TempPoints.cache_size,
)
