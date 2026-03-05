# def my_generator():
#     for i in range(0, 1000000):
#         if str(i)[0] == str(i)[-1]:
#             yield i

# data = my_generator()
# print(next(data))
# print(next(data))
# print(next(data))
# print(next(data))
# print(next(data))
# print(next(data))
# print(next(data))
# print(next(data))
# print(next(data))
# print(next(data))
# print(next(data))
# print(next(data))
# print(next(data))
# print(next(data))
# print(next(data))
# print(next(data))
# print(next(data))


# def tub_son(n: int):
#     if n <= 1:
#         return False
#     for i in range(2, int(n**0.5) + 1):
#         if n % i == 0:
#             return False
#     return True

# def tub_sonmi(son: int):
#     if son <= 1:
#         return False
#     for i in range(2, son):
#         if son % i == 0:
#             return False
#     return True

# def tub_son_from_file(oraliq: int):
#     with open("numbers.txt","r") as file:
#         try:
#             for _ in range(oraliq):
#                 data = file.readline()
#                 if tub_son(int(data)):
#                         yield data
#         except StopIteration:
#             return

# data = tub_son_from_file(6)
# for d in data:
#     print(d)
