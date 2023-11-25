import itertools
import os
import math 

# https://headfullofciphers.com/2020/08/27/cryptopy-caesar-cipher-aka-shift-cipher-in-python/
# https://www.khanacademy.org/computing/computer-science/cryptography/ciphers/a/shift-cipher
# https://github.com/HolzerSoahita/Cracking_code_python/tree/main/Simple_substitution
# 

current_directory = os.getcwd()
print("Current working directory:", current_directory)
os.chdir("C:\\Users\\ACER\\Desktop\\COMP 424 - Assignment 1")

ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

def decrypt_column_transpose(cipher, key): 
    new_string = "" 
  
    k_indx = 0
   
    new_string_indx = 0
    new_string_len = float(len(cipher)) 
    new_string_lst = list(cipher) 
    col = len(key) 
    row = int(math.ceil(new_string_len / col)) 
    key_lst = sorted(list(key)) 
    dec_cipher = [] 
    for _ in range(row): 
        dec_cipher += [[None] * col] 
  
    for _ in range(col): 
        curr_idx = key.index(key_lst[k_indx]) 
  
        for j in range(row): 
            dec_cipher[j][curr_idx] = new_string_lst[new_string_indx] 
            new_string_indx += 1
        k_indx += 1
  
    try: 
        new_string = ''.join(sum(dec_cipher, [])) 
    except TypeError: 
        raise TypeError("This program cannot", 
                        "handle repeating words.") 
  
    null_count = new_string.count('_') 
  
    if null_count > 0: 
        return new_string[: -null_count] 
  
    return new_string 


def suffix_text(new_string, dictionary):
    for i in range(1, len(new_string)+1):
        prefix = new_string[:i]
        if dictionary.word_exists(prefix):
            suffix = new_string[i:] 
            seg_suffix = suffix_text(suffix, dictionary)
            if seg_suffix is not None:
                return prefix + " " + seg_suffix
            else:
                return suffix
    return None

def decrypt_simple_substitution(shift, cipher_text):
    plain_text = ""
    for ch in cipher_text:
        alpha_in = ALPHABET.index(ch)
        if (alpha_in - shift) < 0:
            remainder = abs(alpha_in - shift) % 25
            plain_text += ALPHABET[26 - remainder]
        else:
            plain_text += ALPHABET[alpha_in - shift]
    return plain_text

def frequent_chars(cipher_text):
    frequency_map = {}
    
    for alphabet in range(ord('A'), ord('Z')+1):
        count = 0
        alphabet = chr(alphabet)
        
        for char in cipher_text:
            if alphabet == char:
                count += 1
                
        if count > 3:
            frequency_map[alphabet] = count
    
    return frequency_map

def sort_map(frequency_map):
    key_list = []
    max_val = max(frequency_map.values())
    for max_value in range(max_val, -1, -1):
        for aplha_char in frequency_map.keys():
            if frequency_map[aplha_char] == max_value:
                key_list.append(aplha_char)
    return key_list


def calculate_shifts(sorted_characters):
    shifts = set()
    most_common_arr = ['E', 'T', 'A', 'O', 'I', 'N', 'S', 'R', 'H', 'L']
    
    for sorted_char in sorted_characters:
        alpha_index = ALPHABET.index(sorted_char)
        done = False
        shift = 1
        
        while not done:
            if alpha_index - shift < 0:
                remainder = abs(alpha_index - shift) % 25
                shifted_char = ALPHABET[26 - remainder]
            else:
                shifted_char = ALPHABET[alpha_index - shift]
            
            if shifted_char in most_common_arr:
                shifts.add(shift)
                done = True
            shift += 1
    
    return shifts

class Dictionary:
    def __init__(self):
        self.dictionary = []
        self.read_in_dictionary() 

    def read_in_dictionary(self):
        dictionary_file_path = "dictionary.txt"
        with open(dictionary_file_path, "r") as dictionary_file:
            self.dictionary = [line.strip().upper() for line in dictionary_file]
            print(self.dictionary)

    def word_exists(self, word_to_lookup):
        return word_to_lookup in self.dictionary

def main():
    cipher_text = "KUHPVIBQKVOSHWHXBPOFUXHRPVLLDDWVOSKWPREDDVVIDWQRBHBGLLBBPKQUNRVOHQEIRLWOKKRDD"

    dictionary=Dictionary()
    frequency_map = frequent_chars(cipher_text)
    print(frequency_map)
    sorted_characters = sort_map(frequency_map)
    print(sorted_characters)
    shifts = calculate_shifts(sorted_characters)
    ciphers_set = set()

    for shift in shifts:
        ciphers_set.add(decrypt_simple_substitution(shift, cipher_text))

    key_list = []

    for i in range(7, 8):
        key = ALPHABET[:i]
        for p in itertools.permutations(key):
            key_list.append(''.join(p))

    count = 1

    for cipher in ciphers_set:
        for k in key_list:
            deciphered = decrypt_column_transpose(cipher, k)
            print(f"Candidate: [{cipher}] key = {k}")
            print(f"Deciphered: #{count} [{suffix_text(deciphered, dictionary)}]\n")
            count += 1
                
    candidate = "HREMSFYNHSLPETEUYMLCRUEOMSIIAATSLPHTMOBAASSFATNOYEYDIIYYMHNRKOSLENBFOITLHHOAA"
    test=decrypt_column_transpose(candidate, "GCAEDBF")
    print(test)
    print(suffix_text(test,dictionary))

if __name__ == "__main__":
    main()