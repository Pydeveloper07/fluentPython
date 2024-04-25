import math
import re
import reprlib


def example_with_iterable():
    RE_WORD = re.compile("\w+")

    class Sentence:
        def __init__(self, text):
            self.text = text
            self.words = RE_WORD.findall(text)

        def __getitem__(self, index):
            return self.words[index]

        def __len__(self):
            return len(self.words)

        def __repr__(self):
            return "Sentence(%s)" % reprlib.repr(self.text)

    sentence = Sentence("They said that we must run.")
    print(sentence)
    print(len(sentence))
    print(sentence[0])
    print(list(sentence))


def example_with_classic_iterable():
    RE_WORD = re.compile("\w+")

    class Sentence:
        def __init__(self, text):
            self.text = text
            self.words = RE_WORD.findall(text)

        def __len__(self):
            return len(self.words)

        def __repr__(self):
            return "Sentence(%s)" % reprlib.repr(self.text)

        def __iter__(self):
            return SentenceIterator(self.words)

    class SentenceIterator:
        def __init__(self, words):
            self.words = words
            self.index = 0

        def __next__(self):
            try:
                word = self.words[self.index]
            except IndexError:
                raise StopIteration()
            self.index += 1
            return word

        def __iter__(self):
            return self

    sentence = Sentence("Hey! Why are you looking at me like that???")
    s_iterator = iter(sentence)
    print(next(s_iterator))
    print(next(s_iterator))
    print(next(s_iterator))
    print(next(s_iterator))
    print(next(s_iterator))


def example_with_generator():
    RE_WORD = re.compile("\w+")

    class Sentence:
        def __init__(self, text):
            self.text = text
            self.words = RE_WORD.findall(text)

        def __len__(self):
            return len(self.words)

        def __repr__(self):
            return "Sentence(%s)" % reprlib.repr(self.text)

        def __iter__(self):
            for word in self.words:
                yield word
            return

    sentence = Sentence("You are unbearably naive!")
    s_generator = iter(sentence)
    print(next(s_generator))
    print(next(s_generator))
    print(next(s_generator))
    print(list(sentence))


def example_with_generator_expression():
    RE_WORD = re.compile("\w+")

    class Sentence:
        def __init__(self, text):
            self.text = text

        def __iter__(self):
            return (match.group() for match in RE_WORD.finditer(self.text))

        def __repr__(self):
            return "Sentence(%s)" % reprlib.repr(self.text)

    sentence = Sentence("How to program a program to program programs?")
    s_iterator = iter(sentence)
    print(next(s_iterator))
    print(next(s_iterator))
    print(next(s_iterator))
    print(next(s_iterator))


def example_generator_arithmetic_progression():
    class ArithmeticProgression:
        def __init__(self, begin=0, step=1, end=math.inf):
            self.begin = begin
            self.step = step
            self.end = end

        def __iter__(self):
            result = self.begin
            index = 0
            while result <= self.end:
                yield result
                index += 1
                result = self.begin + self.step * index

    ap = ArithmeticProgression(1, 2, 10)
    print(ap)
    print(list(ap))


def example_with_arith_progress_gen_function():
    def arith_prog_gen(begin=0, step=1, end=math.inf):
        result = begin
        index = 0
        while result <= end:
            yield result
            index += 1
            result = begin + step * index

    print(arith_prog_gen(0, 2, 10))
    print(list(arith_prog_gen(0, 2, 10)))
    for i in arith_prog_gen(1, 2, 30):
        print(i, end=", ")


def example_with_custom_take_while_generator():
    import itertools

    def take_while(func, generator):
        while True:
            result = next(generator)
            if func(result):
                yield result
            else:
                return StopIteration

    iterator = itertools.count(1, 0.5)
    gen = take_while(lambda x: x < 5, iterator)
    print(gen)
    print(list(gen))


def example_with_custom_enumerator():
    from collections import abc

    def enumerate_(l):
        iterator = None
        if isinstance(l, abc.Iterable):
            iterator = iter(l)
        elif isinstance(l, abc.Iterator):
            iterator = l
        else:
            raise TypeError(f"type {type(l).__name__} not supported")

        index = 0
        for i in iterator:
            yield index, bool(i), i
            index += 1

    mixed_list = [1, 0, "h", "", 34, None, True]
    for i, truth_val, value in enumerate_(mixed_list):
        print(i, truth_val, value)

    print("*"*20)
    for i, truth_val, value in enumerate_(range(0, 4)):
        print(i, truth_val, value)

    try:
        print(next(enumerate_(1)))
    except TypeError as e:
        print(e)


if __name__ == "__main__":
    example_with_custom_enumerator()
