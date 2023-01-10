import multiprocessing
import time

session = None


def set_global_session():
  global session
  if not session:
    session = requests.Session()


def start_listeners():
  with multiprocessing.Pool(initializer=set_global_session) as pool:
    pool.map(download_site, sites)


if __name__ == "__main__":
  start_listeners()