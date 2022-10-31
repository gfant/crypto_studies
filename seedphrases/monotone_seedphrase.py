import hashlib
from constants import word_list, mnemonic_length

# Edit the variable below this line
size = 12

def monotone_seedphrase(words = 12):
    candidates = []
    size_checksum = words // 3
    size_bit = mnemonic_length[words]
    size_byte = int(size_bit/8)

    for value in range(2048):
        value_bin = bin(value)[2:].zfill(11)

        entropy_checksum = value_bin*words
        checksum = entropy_checksum[ len(entropy_checksum) - size_checksum : ]
        entropy = entropy_checksum[ : len(entropy_checksum) - size_checksum ]
        
        candidates.append([ entropy, checksum, value])

    possible_solutions = []
    for candidate in candidates:
        entropy, checksum, value = candidate
        entropy_int = int(entropy,2) # Integer of candidate entropy
        entropy_byte = entropy_int.to_bytes(size_byte,"big") # bytes of entropy
        entropy_hash = hashlib.sha256(entropy_byte).digest() # Digest of Hash
        entropy_hash_int = int.from_bytes(entropy_hash,"big") # Number of hashing
        entropy_hash_bin = bin(entropy_hash_int)[2:].zfill(256) # Binary of hashing the candidate entropy
        checksum_candidate = entropy_hash_bin[:size_checksum] # Getting Checksum
        if checksum_candidate == checksum:
            valid_word = word_list[value]
            possible_solutions.append(valid_word) 

    return possible_solutions

solutions = monotone_seedphrase(size)

print(f"The current words are useful to generate valid seedphrases of size {size} with only one word:")
for index in range(len(solutions)):
    word = solutions[index]
    print(f"{index+1}:\t{word}")
