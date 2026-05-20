numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
even = [x for x in numbers if x % 2 ==0]
print(even)

names = ["Alex",
        "Alexandra",
        "Ben",
        "Benjamin",
        "Cat",
        "Catherine",
        "Dan"]

long_names = [name for name in names if len(name) > 5]
print(long_names)

sentence = "I love learning Python"
words = sentence.split()
words[::-1]
reversed_sentence = " ".join(words)
print(reversed_sentence)