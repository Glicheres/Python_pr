def get_with_id(name):
    for i in range(len(name)):
        print(i,"->",name[i])

def binary_search(array, element, start, end):
    if start > end:
        return -1
    mid = (start + end) // 2

    print("\nЦентр = ", mid, "||\tНачало = ", start, "||\tЭТО КОНЕЦ! ", end)
    # draww
    i_s = start
    while (i_s<=end):
        print(array[i_s],end = " ")
        i_s = i_s + 1
    print("")

    if element == array[mid]:
        return mid

    if element < array[mid]:
        return binary_search(array, element, start, mid-1)
    else:
        return binary_search(array, element, mid+1, end)

print("Дайте длинну):")
N = int(input())
a = []
for i in range(N):
    g = i # Генератор)
    a.append(g)
print("А сейчас что ищем?")
inp = int(input())
result = binary_search(a,inp, 0, len(a)-1)
if (result!= -1):
    print("found",inp," here: ", result)
else:
    print("НЕТ!")
