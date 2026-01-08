from typing import List
import random
import string

def fake_vins(num: int) -> List[str]:
    chars = string.ascii_uppercase + string.digits
    return [
        ''.join(random.choice(chars) for _ in range(17))
        for _ in range(num)
    ]




if __name__ == "__main__":
    print("Generated Fake VINs:")
    num = 5
    for vin in fake_vins(num):
        print(vin)
