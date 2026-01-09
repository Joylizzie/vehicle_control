from typing import List
import random
import string

import random, string

def generate_vin():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=17))

if __name__ == "__main__":
    print("Generated Fake VINs:")
    num = 5
    for vin in [generate_vin() for _ in range(num)]:
        print(vin)
