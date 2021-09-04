from typing import List


async def query_all(query: str, con) -> List[dict]:
    result = con.execute(query)


async def query_first():
    ...
