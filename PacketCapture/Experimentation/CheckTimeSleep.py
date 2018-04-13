import time


wait = 0.005

sum = 0
for x in range(0, 100):
    start = time.time()
    time.sleep(wait)
    final = time.time()
    elapsed = final - start

    sum += (elapsed - wait)

print("Error: ", sum)