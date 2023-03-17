import numpy as np
import xxhash

epsilon = 1

g = int(round(np.exp(epsilon))) + 1
print(g)
report_value = (xxhash.xxh32(str(1), seed=3).intdigest() % g)
print(report_value)