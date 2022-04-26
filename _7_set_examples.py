from dis import dis


def show_use_case_of_set_intersection():
    list_1 = [i for i in range(100)]
    list_2 = [i for i in range(34, 67)]
    print(len(set(list_1) & set(list_2)))


def check_hashability_set():
    try:
        my_set = {1, 2, [4, 5]}
    except TypeError as e:
        print(e)


def show_set_constructs_using_disassembler():
    dis('{1}')
    dis('{[1]}')


def show_difference_between_discard_and_remove():
    my_set = {1, 2, 3, 4, 5}
    try:
        my_set.remove(10)
    except KeyError as e:
        print("Remove using remove() throws exception")
    try:
        my_set.discard(10)
        print("When removed using discard() no exception is thrown")
    except Exception as e:
        print("Couldn't remove using discard too")


if __name__ == "__main__":
    show_difference_between_discard_and_remove()