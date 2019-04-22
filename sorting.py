# region Sorting Algorithms
def partition(numbers, first, last):
    pivotvalue = numbers[first]
    leftmark = first + 1
    rightmark = last
    done = False

    while not done:
        while leftmark <= rightmark and numbers[leftmark] <= pivotvalue:
            leftmark = leftmark + 1

        while numbers[rightmark] >= pivotvalue and rightmark >= leftmark:
            rightmark = rightmark - 1

        if rightmark < leftmark:
            done = True
        else:
            temp = numbers[leftmark]
            numbers[leftmark] = numbers[rightmark]
            numbers[rightmark] = temp

    temp = numbers[first]
    numbers[first] = numbers[rightmark]
    numbers[rightmark] = temp

    return rightmark


def qsort(numbers, first, last):
    if first < last:
        splitpoint = partition(numbers, first, last)
        qsort(numbers, first, splitpoint - 1)
        qsort(numbers, splitpoint + 1, last)


def quicksort(numbers):
    qsort(numbers, 0, len(numbers) - 1)
    return numbers


def bubblesort(numbers):
    length = len(numbers)  # type: int

    # repeat length-1 times
    for j in range(length - 1):
        # start checking for swapping in second position of array
        for i in range(1, length):
            # if current number is smaller than the previous one then move it down, or swap
            if numbers[i - 1] > numbers[i]:
                bubble = numbers[i - 1]
                numbers[i - 1] = numbers[i];
                numbers[i] = bubble
    return numbers


# endregion


if __name__ == "__main__":
    values = [5, 2, 7, 6, 1, 9, 4, 8]
    print(values)
    print("bubble sort:", bubblesort(values))
    values = [5, 2, 7, 6, 1, 9, 4, 8]
    print("quick sort:", quicksort(values))
