import time
import hashlib

seed = time.time()

def sha512(value):
  return hashlib.sha512(value.encode('utf-8')).hexdigest()

def uid():
  time.sleep(.1)
  return sha512(str(seed + time.time()))