import hashlib
from constants import word_list, mnemonic_length
from hashlib import sha256

def lastWord(mnemonic):
    words = mnemonic.split()

    checksum_size = (len(words) + 1 ) // 3
    if checksum_size > 8 or checksum_size < 4:
        raise ValueError("Incorrect seedphrase size.")
    bit_size = mnemonic_length[len(words) + 1]
    entropy_bytes = int(bit_size/8)

    entropy_list = []
    for word in words:
        if word not in words:
            raise ValueError("Words not valid.")
        index = word_list.index(word)
        bits = bin(index)[2:].zfill(11)
        entropy_list.append(bits)

    entropy_known = "".join(entropy_list)
    possible_solutions = []
    for value in range(2048):
        value_bits = bin(value)[2:].zfill(11) # Testing word in position 'value'
        checksum = value_bits[11-checksum_size:] # Getting the checksum bits
        current_remaining_entropy = value_bits[:11-checksum_size] # Getting remaining bits
        current_entropy_string = entropy_known + current_remaining_entropy # Adding static entropy with bits of candidate as string
        current_entropy_int = int(current_entropy_string,2) # Integer of candidate entropy
        current_entropy_bytes = current_entropy_int.to_bytes(entropy_bytes,"big") # bytes of entropy
        HASH = hashlib.sha256(current_entropy_bytes).digest() # Digest of Hash
        HASH_int = int.from_bytes(HASH,"big") # Number of hashing
        HASH_binary = bin(HASH_int)[2:].zfill(256) # Binary of hashing the candidate entropy
        CHECKSUM = HASH_binary[:checksum_size] # Getting Checksum
        if CHECKSUM == checksum:
            possible_solutions.append(word_list[value]) 

    return possible_solutions

print(lastWord(" ".join(["sea"]*11)))