import hashlib
from constants import word_list, mnemonic_length
from hashlib import sha256
import secrets

# Edit the variable below this line
size = 18

def seedphrase_generator(size = 12):
    if size not in mnemonic_length:
        raise ValueError("Invalid size")
    
    # Get number of bits
    bit_size = mnemonic_length[size]


    # Generate bits randomly and secretly
    ENT_int = secrets.randbits(bit_size)

    # Calculate the number of bits of the entropy to split it properly
    ENT_bytes = int(bit_size/8)

    # Entropy is made bytes to make it manageble for sha256 later
    ENT = ENT_int.to_bytes(ENT_bytes,"big")

    # Number of bits of the checksum
    CHECKSUM_size = bit_size // 32

    # Digest is a way to call the result in bytes. It's the hash itself
    # If you try to output without digest it won't work
    # SHA256 throws a bytes object, so you need a number 
    HASH = hashlib.sha256(ENT).digest()

    # We get the bites to get the checksum bytes we need to finish our seedphrase
    HASH_int = int.from_bytes(HASH, "big")
    CHECKSUM_binary = bin(HASH_int)[2:].zfill(256)

    CHECKSUM = CHECKSUM_binary[:CHECKSUM_size]

    ENT_bin = bin(ENT_int)[2:]
    binary = (ENT_bin + CHECKSUM).zfill(bit_size + CHECKSUM_size)

    wordsIndices = []
    for index in range(0, len(binary), 11):
        wordsIndices.append(binary[index : index + 11])
    
    seedphrase = []
    for index in wordsIndices:
        position = int(index, 2)
        word = word_list[position]
        seedphrase.append(word)

    return(' '.join(seedphrase))


print(seedphrase_generator(size))
