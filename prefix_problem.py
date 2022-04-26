def main():
    words = []
    n = int(input("Input number of words: "))
    for i in range(n):
        word = str(input("Enter word %s: " % (i + 1)))
        words.append(word)

    words.sort()
    if words[0] in words[-1]:
        print("Longest prefix: %s" % words[0])

    longest_prefix = ""
    for i, char in enumerate(words[0]):
        if char == words[-1][i]:
            longest_prefix += char
        else:
            break
    if not longest_prefix:
        print("Longest prefix is None!")
        return

    print("Longest prefix: {}".format(longest_prefix))


if __name__ == "__main__":
    main()


