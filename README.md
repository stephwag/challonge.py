# Challonge.py

Python wrapper for the Challonge API

## Example
```
async def main():
    t = Tournament({ 'id' : 'challonge url or id'})

    async with aiohttp.ClientSession() as session:
        await t.get(session)
        print("Welcome to the %s tournament!" % t.name)

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
```

## Requirements

* Python 3.5.3+
* `asyncio` and `aiohttp` libraries