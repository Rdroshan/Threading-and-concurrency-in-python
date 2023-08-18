# adding to a dict is thread-safe
# updating a dict is also thread-safe
# removing from dict is also thread-safe
# All are thread-safe because they're atomic operation in python
# Only removing operation can be made thread-unsafe,
# If we don't check for the existance of key.
# But adding that means we have more than 2 operations.
# and more than two operations are thread-unsafe.
# Solution: We need mutex lock.
# This similar concept can be applied to other built-in types.
# like list, set.
# Also in other languages like Go, Java these operations are
# not atomic and hence lock is required.

from threading import Thread, Lock

# Example adding to dict
shared_dict = {}


def add_items(shared_dict, start, num_of_vals):
  for i in range(start, start + num_of_vals):
    shared_dict[i] = i


threads = []
for i in range(0, 1000000, 1000):
  threads.append(Thread(target=add_items, args=(shared_dict, i, 1000)))

for t in threads:
  t.start()

for t in threads:
  t.join()

print(f"len of shared_dict: {len(shared_dict)} expected: 1000000")

# Example update a dict
shared_dict = {}


def update_items(shared_dict, start, num_of_vals):
  d = {i: i for i in range(start, start + num_of_vals)}
  shared_dict.update(d)


threads = []
for i in range(0, 1000000, 1000):
  threads.append(Thread(target=update_items, args=(shared_dict, i, 1000)))

for t in threads:
  t.start()

for t in threads:
  t.join()

print(f"len of shared_dict: {len(shared_dict)} expected: 1000000")

## Example remove from dict
lock = Lock()
# NOTE: The remove operation is itself atomic.
# But here we're just showing how it can become thread unsafe.

# Value should be large enough to see the thread-unsafety
# of dicts in case of 
TOTAL_VALS = 10**6 
# first populate dict with 1000,000 items
shared_dict = {i: i for i in range(TOTAL_VALS)}


def delete_items(shared_dict):

  with lock:  # without lock there will be KeyError
    for i in range(TOTAL_VALS):
      # two operations will almost always result in race conditions.
      # with lock: putting lock here is SLOW.
      if shared_dict.get(i) is not None:
        shared_dict.pop(i)
    
threads = []
for i in range(10):
  threads.append(Thread(target=delete_items, args=(shared_dict,)))

for t in threads:
  t.start()

for t in threads:
  t.join()

print(f"len of shared_dict: {len(shared_dict)} expected: 0")


