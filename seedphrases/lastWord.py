from constants import word_list, mnemonic_length
from hashlib import sha256

def lastWord(mnemonic):
    words = mnemonic.split()

    size_checksum = (len(words) + 1 ) // 3
    if size_checksum > 8 or size_checksum < 4:
        raise ValueError("Incorrect seedphrase size.")
    size_entropy_bit = mnemonic_length[len(words) + 1]
    size_entropy_byte = int(size_entropy_bit/8)

    entropy_bit_list = []
    for word in words:
        if word not in words:
            raise ValueError("Words not valid.")
        index = word_list.index(word)
        word_bin = bin(index)[2:].zfill(11)
        entropy_bit_list.append(word_bin)

    entropy_bit_known = "".join(entropy_bit_list)
    possible_solutions = []
    for word in range(2048):
        word_bit = bin(word)[2:].zfill(11) # Testing word in position 'value'
        word_checksum = word_bit[11-size_checksum:] # Getting the checksum bits
        word_entropy = word_bit[:11-size_checksum] # Getting remaining bits
        word_string = entropy_bit_known + word_entropy # Adding static entropy with bits of candidate as string
        word_int = int(word_string,2) # Integer of candidate entropy
        word_byte = word_int.to_bytes(size_entropy_byte,"big") # bytes of entropy
        entropy_hash = sha256(word_byte).digest() # Digest of Hash
        entropy_hash_int = int.from_bytes(entropy_hash,"big") # Number of hashing
        entropy_hash_bin = bin(entropy_hash_int)[2:].zfill(256) # Binary of hashing the candidate entropy
        candidate_checksum = entropy_hash_bin[:size_checksum] # Getting Checksum
        if candidate_checksum == word_checksum:
            possible_solutions.append(word_list[word]) 

    return possible_solutions

print(lastWord(" ".join(["sea"]*11)))
