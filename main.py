import logging
import logging.handlers
import os
import asyncio
from concurrent.futures import ThreadPoolExecutor
from ig import IG

# Set up logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger_file_handler = logging.handlers.RotatingFileHandler(
  "status.log",
  maxBytes=1024 * 1024,
  backupCount=1,
  encoding="utf8",
)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger_file_handler.setFormatter(formatter)
logger.addHandler(logger_file_handler)

# Get the token from github action secret
try:
  token_ur_always_my = os.environ['TOKEN_UR_ALWAYS_MY']
  token_optimum_pride = os.environ['TOKEN_OPTIMUM_PRIDE']
  logger.info("Token available.")
except:
  logger.info("Token not available, maybe it is expired.")
  raise

# Get the video url from github action secret
url_ur_always_my = os.environ['URL_UR_ALWAYS_MY']
url_optimum_pride = os.environ['URL_OPTIMUM_PRIDE']

version = 'v18.0'

logger.info("Start running.")
ig_ur = IG('ur_always_my', token_ur_always_my, url_ur_always_my, version)
ig_op = IG('optimum_pride', token_optimum_pride, url_optimum_pride, version)

async def run():
  with ThreadPoolExecutor() as executor:
    loop = asyncio.get_event_loop()
    tasks = [loop.run_in_executor(executor, ig.run) for ig in [ig_ur, ig_op]]
    await asyncio.gather(*tasks)

if __name__ == '__main__':
  asyncio.run(run())
  logger.info("Finish running.")