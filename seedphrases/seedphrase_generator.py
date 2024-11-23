import hashlib
from constants import word_list, mnemonic_length
from hashlib import sha256
from random import randint

# Edit the variable below this line
size = 24

def randbits(size) -> int:
    value = 0
    for _ in range(size):
        value <<= 1
        value += randint(0,1)
    return value

def seedphrase_generator(size = 12):
    verify_size(size)
    
    # Get number of bits
    size_bit = mnemonic_length[size]

    # Generate bits randomly and secretly
    entropy_int = randbits(size_bit)

    # Calculate the number of bits of the entropy to split it properly
    entropy_byte = int(size_bit/8)

    # Entropy is made bytes to make it manageble for sha256 later
    entropy = entropy_int.to_bytes(entropy_byte,"big")

    # Number of bits of the checksum
    checksum_size = size_bit // 32

    # Digest is a way to call the result in bytes. It's the hash itself
    # If you try to output without digest it won't work
    # SHA256 throws a bytes object, so you need a number 
    entropy_hash = hashlib.sha256(entropy).digest()

    # We get the bites to get the checksum bytes we need to finish our seedphrase
    entropy_hash_int = int.from_bytes(entropy_hash, "big")
    checksum_bin = bin(entropy_hash_int)[2:].zfill(256)

    checksum = checksum_bin[:checksum_size]

    entropy_bin = bin(entropy_int)[2:]
    entropy_full_bin = (entropy_bin + checksum).zfill(size_bit + checksum_size)

    wordsIndices = []
    for index in range(0, len(entropy_full_bin), 11):
        wordsIndices.append(entropy_full_bin[index : index + 11])
    
    seedphrase = []
    for index in wordsIndices:
        position = int(index, 2)
        word = word_list[position]
        seedphrase.append(word)

    return(' '.join(seedphrase))

def checkIsNumber(size):
    if not size.isdigit() or size == "" or size[0] == "0":
        raise ValueError("Invalid size")
    return int(size)

def verify_size(size):
    if int(size) not in mnemonic_length:
        raise ValueError("Invalid size")

if __name__ == "__main__":
    size = input("Seedphrase size\n")
    size = checkIsNumber(size)
    output = seedphrase_generator(size)
    print(output)