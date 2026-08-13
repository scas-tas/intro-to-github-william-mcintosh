def encode(message: str, shift: int) -> str:
    result = ""
    for character in message:
        if character.isupper():
            result += chr((ord(character) - ord("A") + shift) % 26 + ord("A"))
            print (ord(character))
        elif character.islower():
            result += chr((ord(character) - ord("a") + shift) % 26 + ord("a"))
            print (ord(character))
        else:
            result += character
    return result

def decode(message: str, shift: int) -> str:
    return encode(message, -shift)

test1 = (encode("xyz", 3))
print(test1)
test1 = (decode(test1, 3))
print(test1)