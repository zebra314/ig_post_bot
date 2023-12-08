import os
import asyncio
from concurrent.futures import ThreadPoolExecutor
from ig import IG

# Get the token from github action secret
try:
  token_ur_always_my = os.environ['TOKEN_UR_ALWAYS_MY']
  token_optimum_pride = os.environ['TOKEN_OPTIMUM_PRIDE']
  print("Token available.")
except:
  print("Token not available, maybe it is expired.")
  raise

version = 'v18.0'
ig_ur = IG('ur_always_my', token_ur_always_my, version)
ig_op = IG('optimum_pride', token_optimum_pride, version)

async def run():
  with ThreadPoolExecutor() as executor:
    loop = asyncio.get_event_loop()
    tasks = [loop.run_in_executor(executor, ig.run) for ig in [ig_ur, ig_op]]
    await asyncio.gather(*tasks)

if __name__ == '__main__':
  asyncio.run(run())
  logger.info("Finish running.")