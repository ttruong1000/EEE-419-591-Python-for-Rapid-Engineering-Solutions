# Import necessary packages for calculations
import numpy as np                                                                   # For real roots

# Finding the prime numbers between 1 and N, inclusive
def primes_list(N):
    primes_list = [2]                                                                # Initialize prime numbers list with even prime 2
    for num in range(3, N + 1):                                                      # Find all odd prime numbers up to N
        for factor in [prime for prime in primes_list if prime <= np.sqrt(num)]:     # Test all primes up to the square root of the number
            if num % factor == 0:
                break                                                                # No need to test more primes if one of them divides the number; it is composite (not prime)
        else:
            primes_list.append(num)
    print(primes_list)                                                               # Print primes list

primes_list(10000)                                                                   # Print primes list up to 10000