from typing import List


def query_all(query: str, con) -> List[dict]:
    result = con.execute(query)
    return [row._asdict() for row in result]

def query_first(query: str, con) -> dict:
    result = con.execute(query)
    return [row._asdict() for row in result][0]