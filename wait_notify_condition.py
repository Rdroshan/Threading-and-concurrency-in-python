# wait, notify and condition
import threading
import time

# threads have to wait for a certain condition in critical
# section before continuing
counter = 0
max_val = 10
mutex = threading.Lock()

def some_work():
  with mutex:
    if counter >= max_val: # >= 10
      # do some work
      print("condition met doing some work!")

# THIS IS WITHOUT USING threading.Condition
# But the above doesn't wait for the condition to be met in
# future. we want thread to wait until condition meet.
# "This could be achieved using a mutual exclusion lock to protect the critical section, 
# but the threads waiting for the condition would have to spin (execute in a loop) repeatedly 
# releasing/re-acquiring the mutex lock until the condition was met."
# Making changes according to the above.
def some_work_with_wait():
  global counter, max_val
  while counter < max_val:
    print("condition didn't match!!")
    with mutex:
      if counter >= max_val: # >= 10
        # do some work
        counter += 1
        print("condition met doing some work!")
        print("counter:", counter)

def change_counter_val():
  time.sleep(1)
  global counter
  counter = 10

# thread1 = threading.Thread(target=some_work_with_wait, name="Thread-1")
# thread2 = threading.Thread(target=some_work_with_wait, name="Thread-2")

# thread1.start()
# thread2.start()
# thread3 = threading.Thread(target=change_counter_val, name="Thread-3")
# thread3.start()
# thread1.join()
# thread3.join()
# thread2.join()


# An alternative is to use a condition (also called a monitor) 
# that builds upon a mutex and allows threads to wait and be notified.
condition = threading.Condition()


def some_work_with_wait1():
  global counter, max_val, condition
  with condition:
    if counter < max_val:
      print("waiting until notified!!")
      condition.wait()
    if counter >= max_val: # >= 10
        # do some work
        counter += 1
        print("condition met doing some work!")
        print("counter:", counter)

def change_counter_val1():
  time.sleep(1)
  global counter, condition
  with condition:
    counter = 10
    # Try using only `notify` and you'll see that one thread gets unblocked
    # but the other is still waiting.
    condition.notify_all()

thread1 = threading.Thread(target=some_work_with_wait1, name="Thread-1")
thread2 = threading.Thread(target=some_work_with_wait1, name="Thread-2")

thread1.start()
thread2.start()
thread3 = threading.Thread(target=change_counter_val1, name="Thread-3")
thread3.start()
thread1.join()
thread3.join()
thread2.join()
