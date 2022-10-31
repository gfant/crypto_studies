import hashlib
from constants import word_list, mnemonic_length

# Edit the variable below this line
size = 12

def monotone_seedphrase(words = 12):
    candidates = []
    checksum_size = words // 3
    bit_size = mnemonic_length[words]
    bytes_size = int(bit_size/8)

    for value in range(2048):
        binary = bin(value)[2:].zfill(11)
        entropy_checksum = binary*words
        separator = len(entropy_checksum) - checksum_size
        checksum = entropy_checksum[separator:]
        entropy = entropy_checksum[:separator]
        candidates.append([entropy,checksum, value])

    possible_solutions = []
    for candidate in candidates:
        entropy,checksum,value = candidate
        entropy_int = int(entropy,2) # Integer of candidate entropy
        entropy_bytes = entropy_int.to_bytes(bytes_size,"big") # bytes of entropy
        HASH = hashlib.sha256(entropy_bytes).digest() # Digest of Hash
        HASH_int = int.from_bytes(HASH,"big") # Number of hashing
        HASH_binary = bin(HASH_int)[2:].zfill(256) # Binary of hashing the candidate entropy
        CHECKSUM = HASH_binary[:checksum_size] # Getting Checksum
        if CHECKSUM == checksum:
            valid_word = word_list[value]
            possible_solutions.append(valid_word) 

    return possible_solutions

solutions = monotone_seedphrase(size)

print(f"The current words are useful to generate valid seedphrases of size {size} with only one word:")
for index in range(len(solutions)):
    word = solutions[index]
    print(f"{index+1}:\t{word}")