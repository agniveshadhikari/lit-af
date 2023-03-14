def split(a: list, n: int):

    if len(a) % n != 0:
        raise ValueError(f"{a} can not be split into {n} equal parts")

    chunk_size = len(a) // n
    start = 0
    while start < len(a):
        yield a[start:start+chunk_size]
        start += chunk_size
