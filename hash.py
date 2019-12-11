import hashlib
import requests
import re


def md5(s):
    return str(hashlib.md5(s.encode()).hexdigest())


def sha1(s):
    return str(hashlib.sha1(s.encode()).hexdigest())


def sha224(s):
    return str(hashlib.sha224(s.encode()).hexdigest())


def sha256(s):
    return str(hashlib.sha256(s.encode()).hexdigest())


def sha384(s):
    return str(hashlib.sha384(s.encode()).hexdigest())


def sha512(s):
    return str(hashlib.sha512(s.encode()).hexdigest())


def provider1(hash, type):
    response = requests.get('https://hashtoolkit.com/reverse-hash/?hash=' + hash).text
    match = re.search(r'/generate-hash/?text=.*?"', response)
    if match:
        return match.group(1)
    else:
        return False


def provider2(hash, type):
    # https://md5decrypt.net/Api/
    response = requests.get(
        'https://md5decrypt.net/Api/api.php?hash=%s&hash_type=%s&email=wea.kit@outlook.com&code=f2b9c0062b48a795' % (
            hash, type)).text
    if len(response) != 0 and not response.startswith("CODE ERREUR"):
        return response
    else:
        return False


if __name__ == '__main__':
    while True:
        print('1. Hash', flush=True)
        print('2. Crack hash', flush=True)
        choice = input('\nPick an option: ')
        if choice not in ['1', '2']:
            print("\nInvalid choice.\n")
            continue
        if choice == '1':
            x = input('\nEnter a string: ')
            print("\nMD5: " + md5(x))
            print("SHA1: " + sha1(x))
            print("SHA224: " + sha224(x))
            print("SHA256: " + sha256(x))
            print("SHA384: " + sha384(x))
            print("SHA512: " + sha512(x))
        else:
            hash_map = {'1': 'md5', '2': 'sha1', '3': 'sha224', '4': 'sha256', '5': 'sha384', '6': 'sha512'}
            while True:
                print("\n1. MD5\n2. SHA1\n3. SHA224\n4. SHA256\n5. SHA384\n6. SHA512")
                choice = input("\nPick hash type: ")
                if choice in hash_map.keys():
                    break
                print("\nInvalid option.\n")
            hash = input("\nEnter hash: ")
            # prefers online hash lookup
            value = provider1(hash, hash_map[choice])
            if value:
                print("\nCracked.")
                print("%s -> %s" % (hash, value))
                break
            value = provider2(hash, hash_map[choice])
            if value:
                print("\nCracked.")
                print("%s -> %s" % (hash, value))
                break
            # offline
            print("Online cracking unsuccessful.\n")
            dictionary = input("Enter offline dictonary: ")
            func = globals()[hash_map[hash]]
            with open(dictionary) as f:
                for line in f:
                    if func(line.strip()) == hash:
                        print("\nCracked.")
                        print("%s -> %s" % (hash, line.strip()))
                        break
            print("Couldn't crack hash " + hash)
        break
