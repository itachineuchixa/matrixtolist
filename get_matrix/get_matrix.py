from typing import List, Tuple, Any
import httpx
import math


def filters(char: str) -> bool:
    if char.isdigit() or char == ' ':
        return True
    return False


def snail(m: List[Tuple[Any, ...]]) -> List[int]:
    return list(m[0]) + snail(list(zip(*m[1:]))[::-1]) if m else []


"""
На входе функция принимиает url с матрицей.
Полученные данные фильтруются, оставляя только числовую матрицу размером n.
Далее матрица развертывается и возвращается пользователю в виде List[int]
"""


async def get_matrix(url: str) -> List[int]:
    try:
        async with httpx.AsyncClient(http2=True) as client:
            response = await client.get(url=url, timeout=1)
            digits: List[str] = ''.join(filter(filters, response.text)).split()
            n: int = int(math.sqrt(len(digits)))
            matrix: List[List[int]] = [list(map(int, digits[i * n:(i + 1) * n])) for i in range(n)]
            transpose_matrix: List[Tuple[Any, ...]] = list(list(zip(*matrix)))
    except Exception as e:
        print("Exception: {}".format(e))
        exit()
    return snail(transpose_matrix)
