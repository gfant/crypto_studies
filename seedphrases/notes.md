# About Seedphrases

In order to generate a seedphrase, you require to generate a random number that will depend on the size of the seedphrase you want. This random number is usually called **entropy**. In the table below you can see the number of bits your entropy must have to generate the appropiate size of your seedphrase.


| Size | Bits | 
|------|------|
|   12 |  128 | 
|   15 |  160 | 
|   18 |  192 | 
|   21 |  224 | 
|   24 |  256 | 

After generating your random number of `ENT` bits, you need to get the **checksum** of this string. 

To get the checksum, first calculate the number of bits you'll require. For this step take the number of bits (`ENT`) and divide it by 32. This result will be the number (`CSUM`) of bits you require for your checksum.

Second you have to apply a SHA256 hashing on your entropy and make the digest a number again, so you can get the bits of this digest. 

After getting the SHA256 digest as a number, take the bits of the hashing and get the first `CSUM` ones.

Add the bits of your entropy with the bits obtained from your checksum (if we consider them as strings it would be `entropy + checksum`). Remember to fill the string if the entropy doesn't have the size you need for the seedphrase size. For example if you want a seedphrase of 128 and the size of your entropy is 120, you need to add 8 zero bits to the left to your entropy so it becomes 128. 

After this, you should have a total of `ENT`+`CSUM` bits (in the case of 12 words you would have 132 bits, 128 by the entropy and 4 by the checksum). Split these bits in blocks of 11 bits, and just locate these numbers with the word list that you can find [here](https://github.com/bitcoin/bips/blob/master/bip-0039/english.txt) so you can generate the result of your seedphrase.


##### Key concepts

* Seedphrase: Set of words that can be of different sizes that determine your wallet.
* Entropy: Random input to generate a seedphrase
* Checksum: Bits that depend on the SHA256 hashing of the entropy.
* SHA256: Process of hashing. Hashing is just a one-way function where the output can't be easily determined without the input.
* Digest: Output of the SHA256 hashing.

##### Side notes

* 1 byte = 8 bits
* [SHA256](https://en.wikipedia.org/wiki/SHA-2) algorithm returns a 256 bit digest (like all SHA2 algorithms, they return bits)
