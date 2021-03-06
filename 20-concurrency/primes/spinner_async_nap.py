# spinner_async_experiment.py

# credits: Example by Luciano Ramalho inspired by
# Michele Simionato's multiprocessing example in the python-list:
# https://mail.python.org/pipermail/python-list/2009-February/675659.html

import asyncio
import itertools
import math

# tag::SPINNER_ASYNC_NAP[]
async def is_prime(n):
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False

    sleep = asyncio.sleep  # <1>
    root = int(math.floor(math.sqrt(n)))
    for i in range(3, root + 1, 2):
        if n % i == 0:
            return False
        if i % 100_000 == 1:  # <2>
            await sleep(0)
    return True
# end::SPINNER_ASYNC_NAP[]


async def spin(msg: str) -> None:
    for char in itertools.cycle(r'\|/-'):
        status = f'\r{char} {msg}'
        print(status, flush=True, end='')
        try:
            await asyncio.sleep(.1)
        except asyncio.CancelledError:
            break
    blanks = ' ' * len(status)
    print(f'\r{blanks}\r', end='')

async def slow() -> int:
    await is_prime(5_000_111_000_222_021)  # <4>
    return 42

async def supervisor() -> int:
    spinner = asyncio.create_task(spin('thinking!'))  # <1>
    print('spinner object:', spinner)  # <2>
    result = await slow()  # <3>
    spinner.cancel()  # <5>
    return result

def main() -> None:
    result = asyncio.run(supervisor())
    print('Answer:', result)

if __name__ == '__main__':
    main()
