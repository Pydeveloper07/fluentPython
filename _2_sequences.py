# x's value is preserved when using listcomphs
import array
import bisect
from random import random


def listcomph_example():
    x = "ABCDEFG"

    dummy = [ord(x) for x in x]

    print(dummy)
    print(x)


# Cartesian Product using listcomphs
def calculate_cartesian_product():
    colors = ["Black", "White"]
    sizes = ["L", "M", "S"]
    cartesian_product = [(color, size) for color in colors for size in sizes]
    print(cartesian_product)


# Using * to grab excess items
def grab_items():
    a, b, *rest = range(5)
    print(a, b, rest)
    a, *body, c, d = range(6)
    print(a, body, c, d)


# Unpack nested tuples, get longitude
def unpack_tuple():
    metro_areas = [
        ('Tokyo', 'JP', 36.933, (35.689722, 139.691667)),
        ('Delhi NCR', 'IN', 21.935, (28.613889, 77.208889)),
        ('Mexico City', 'MX', 20.142, (19.433333, -99.133333)),
        ('New York-Newark', 'US', 20.104, (40.808611, -74.020386)),
        ('Sao Paulo', 'BR', 19.649, (-23.547778, -46.635833)),
    ]
    for _, _, _, (longitude, latitude) in metro_areas:
        print(longitude)


# Slice objects
def slice_example():
    invoice = """
    0.....6.................................40........52...55........
     1909    Pimoroni PiBrella                $17.50    3    $52.50
     1489    6mm Tactile Switch x20           $4.95     2    $9.90
     1510    Panavise Jr. - PV-201            $28.00    1    $28.00
     1601    PiTFT Mini Kit 320x240           $34.95    1    $34.95
    """
    SKU = slice(0, 6)
    DESCRIPTION = slice(6, 40)
    UNIT_PRICE = slice(40, 52)
    QUANTITY = slice(52, 55)
    ITEM_TOTAL = slice(55, None)
    line_items = invoice.split('\n')[2:]
    for line_item in line_items:
        print(f"{line_item[UNIT_PRICE]}   {line_item[DESCRIPTION]}")


def grade(score, breakpoints=(60, 70, 80, 90), grades='FDCBA'):
    i = bisect.bisect(breakpoints, score)
    return grades[i]


# Grade according to score
def print_grades():
    scores = [50, 62, 63, 78, 82, 68, 95, 83, 74]
    grades = []
    for score in scores:
        grades.append(grade(score))
    print(grades)


# array experiment instead of lists
def make_array_and_save_read():
    SIZE = 10**7
    my_array = array.array('d', [random() for i in range(SIZE)])
    last_number = my_array[-1]
    fp = open("floats.bin", 'wb')
    my_array.tofile(fp)
    fp.close()
    my_array2 = array.array('d')
    fp2 = open("floats.bin", 'rb')
    my_array2.fromfile(fp2, SIZE)
    fp2.close()
    assert my_array2[-1] == last_number
    print(last_number)


def create_pattern_of_ones_using_list_comphs():
    my_list = [0 if j < i + 1 else 1 for i in range(10) for j in range(10)]
    my_new_list = [my_list[i*10:(i+1)*10] for i in range(10)]
    for l in my_new_list:
        print(l)


def create_pattern_of_ones_using_list_comphs_shorter_way():
    size = 10
    my_list = [[0]*i + [1]*(size-i) for i in range(size)]
    for l in my_list:
        print(l)


def make_list_of_numbers():
    my_list = [[1] * 10] * 10
    for l in my_list:
        print(l)


def show_tuple_immutability():
    my_tuple = (1, 2, [4, 5], {"one": 1})
    try:
        my_tuple[2] += [6]
    except TypeError as e:
        print(e)
    my_tuple[2].append(6)
    my_tuple[3]["two"] = 2
    print(my_tuple)


if __name__ == "__main__":
    show_tuple_immutability()
