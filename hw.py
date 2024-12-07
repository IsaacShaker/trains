result = 0

for i in range(512):
    result += i

result = result/(2**9)
print('The average number of backoff slots that a device will wait before attempting to retransmit after 9 collisions will be ', result, 'slots.')