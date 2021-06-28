import random


dir = "BUY" if random.random() < 0.5 else "SELL"
print(dir)