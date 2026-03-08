# MultiThreading bo‘yicha 10 ta masala

from multiprocessing import Process, Pool, Queue
from threading import Thread
from functools import reduce

# 1.
# def sonlar_print(son: int, son2: int):
#     for i in range(son, son2):
#         print(i)

# t1 = Thread(target=sonlar_print,args=(1,51))
# t2 = Thread(target=sonlar_print,args=(51,100))

# t1.start()
# t2.start()

# t1.join()
# t2.join()

# 2.
# def get_juft_and_toq_sonlar(son: int,juft_or_toq: str):
#     toq_sonlar = []
#     juft_sonlar = []
#     for i in range(son):
#         if i & 1 == 1:
#             toq_sonlar.append(i)
#         else:
#             juft_sonlar.append(i)

#     if juft_or_toq == "juft":
#         print("\nJuft sonlar chiqishi boshlandi: \n")
#         for son in juft_sonlar:
#             print(son,end=" ")
#     else:
#         print("\Toq sonlar chiqishi boshlandi: \n")
#         for son in toq_sonlar:
#             print(son,end=" ")

# t1 = Thread(target=get_juft_and_toq_sonlar,args=(101,"juft"))
# t2 = Thread(target=get_juft_and_toq_sonlar,args=(101,"toq"))

# t1.start()
# t2.start()

# t1.join()
# t2.join()

# 3.
# def sonlar_yigindisi(sonlar: list[int], q: Queue):
#     q.put(sum(sonlar))

# sonlar = [1,2,3,4,5,6,7,8,9,10]
# q = Queue()
# t1 = Thread(target=sonlar_yigindisi,args=(sonlar[:len(sonlar) // 2], q))
# t2 = Thread(target=sonlar_yigindisi,args=(sonlar[(len(sonlar) // 2):], q))

# t1.start()
# t2.start()
# t1.join()
# t2.join()
# natija1 = q.get()
# natija2 = q.get()
# print(natija1+natija2)

# 4.
# def calculate_factorial(n: int, q: Queue):
#     if n < 0:
#         return "Manfiy son mumkin emas"
#     if n == 0:
#         return 1

#     factorial = 1
#     for i in range(1, n + 1):
#         factorial *= i
#     q.put(factorial)

# q = Queue()
# t1 = Thread(target=calculate_factorial,args=(5, q))
# t2 = Thread(target=calculate_factorial,args=(7, q))

# t1.start()
# t2.start()
# t1.join()
# t2.join()
# natija1 = q.get()
# natija2 = q.get()
# print(natija1)
# print(natija2)

# 5.
# def get_word_count(word: str, q: Queue,shart: str):
#     data = []
#     for harf in word:
#         if shart == "unli" and harf.lower() in ["a", "e", "i", "o", "u"]:
#             data.append(harf)

#         elif shart == "undosh" and harf.lower() not in ["a", "e", "i", "o", "u"]:
#             data.append(harf)

#     q.put(len(data))

# q = Queue()
# t1 = Thread(target=get_word_count,args=("python multithreading", q,"unli"))
# t2 = Thread(target=get_word_count,args=("python multithreading", q,"undosh"))

# t1.start()
# t2.start()
# t1.join()
# t2.join()
# natija1 = q.get()
# natija2 = q.get()
# print(natija1)
# print(natija2)

# 6.
# def eng_katta_son(sonlar: list[int],q: Queue):
#     eng_kattasi = 0
#     for son in sonlar:
#         if son > eng_kattasi:
#             eng_kattasi = son

#     q.put(eng_kattasi)

# sonlar = [12,45,67,23,89,90,34,22]
# q = Queue()
# t1 = Thread(target=eng_katta_son,args=(sonlar[:len(sonlar) // 2],q))
# t2= Thread(target=eng_katta_son,args=(sonlar[(len(sonlar) // 2):],q))
# t1.start()
# t2.start()
# t1.join()
# t2.join()
# natija1 = q.get()
# natija2 = q.get()
# print(natija1 if natija1 > natija2 else natija2)


# 7.  Kvadratlar hisoblash List: [1,2,3,4,5,6,7,8] 2 thread yarating: Biri
#     1 dan 4 gacha elementlarni kvadratga oshirsin. Biri 5 dan 8 gacha
#     elementlarni kvadratga oshirsin.

# def kvadrat(sonlar: list[int], q: Queue):
#     q.put([son * 2 for son in sonlar])

# sonlar = [1,2,3,4,5,6,7,8]
# q = Queue()
# t1 = Thread(target=kvadrat,args=(sonlar[:len(sonlar) // 2],q))
# t2= Thread(target=kvadrat,args=(sonlar[(len(sonlar) // 2):],q))
# t1.start()
# t2.start()
# t1.join()
# t2.join()
# natija1 = q.get()
# natija2 = q.get()
# print(natija1)
# print(natija2)


# 8.
# def tub_sonmi(son: int):
#     if son <= 1:
#         return False
#     for i in range(2, son):
#         if son % i == 0:
#             return False
#     return True

# def get_tub_sonlar(sonlar: list[int], q: Queue):
#     tub_sonlar = []
#     for son in sonlar:
#         if tub_sonmi(son):
#             tub_sonlar.append(son)

#     q.put(tub_sonlar)

# sonlar = [son for son in range(1,101)]
# q = Queue()
# t1 = Thread(target=get_tub_sonlar,args=(sonlar[:len(sonlar) // 2],q))
# t2= Thread(target=get_tub_sonlar,args=(sonlar[(len(sonlar) // 2):],q))
# t1.start()
# t2.start()
# t1.join()
# t2.join()
# natija1 = q.get()
# natija2 = q.get()
# print(natija1)
# print(natija2)

# 9.
# def katta_harf(word_list: list[str], q: Queue):
#     q.put(list(map(lambda word: word.upper(),word_list)))

# sozlar = ["python","django","backend","fastapi"]
# q = Queue()
# t1 = Thread(target=katta_harf,args=(sozlar[:len(sozlar) // 2],q))
# t2= Thread(target=katta_harf,args=(sozlar[(len(sozlar) // 2):],q))
# t1.start()
# t2.start()
# t1.join()
# t2.join()
# natija1 = q.get()
# natija2 = q.get()
# print(natija1)
# print(natija2)

# 10.
# def is_palindrome(s):
#     return s == s[::-1]

# def get_palindrome_sozlar(sozlar: list[str],q: Queue):
#     psozlar = []
#     for soz in sozlar:
#         if is_palindrome(soz):
#             psozlar.append(soz)

#     q.put(psozlar)

# sozlar = ["level","ona","radar","hello",]
# q = Queue()
# t1 = Thread(target=get_palindrome_sozlar,args=(sozlar[:len(sozlar) // 2],q))
# t2= Thread(target=get_palindrome_sozlar,args=(sozlar[(len(sozlar) // 2):],q))
# t1.start()
# t2.start()
# t1.join()
# t2.join()
# natija1 = q.get()
# natija2 = q.get()
# print(natija1)
# print(natija2)

# MultiProcessing bo‘yicha 10 ta masala

# 1.
# def yigindi(son1: int, son2: int) -> int:
#     print(sum(range(son1,son2)))

# if __name__ == "__main__":
#     p1 = Process(target=yigindi,args=(1,50000,))
#     p2 = Process(target=yigindi,args=(50000,100001))
#     p1.start()
#     p2.start()
#     p1.join()
#     p2.join()

# 2.
# def calculate_factorial(n):
#     if n < 0:
#         return "Manfiy son mumkin emas"
#     if n == 0:
#         return 1

#     factorial = 1
#     for i in range(1, n + 1):
#         factorial *= i
#     print(factorial)

# if __name__ == "__main__":
#     p1 = Process(target=calculate_factorial,args=(10,))
#     p2= Process(target=calculate_factorial,args=(12,))
#     p1.start()
#     p2.start()
#     p1.join()
#     p2.join()

# 3.
# def tub_sonmi(son: int):
#     if son <= 1:
#         return False
#     for i in range(2, son):
#         if son % i == 0:
#             return False
#     return True

# def get_tub_sonlar(x: int, y: int):
#     tub_sonlar = []
#     for son in range(x, y):
#         if tub_sonmi(son):
#             tub_sonlar.append(son)

#     print(tub_sonlar)

# if __name__ == "__main__":
#     p1 = Process(target=get_tub_sonlar,args=(1,5000,))
#     p2= Process(target=get_tub_sonlar,args=(5000,10001))
#     p1.start()
#     p2.start()
#     p1.join()
#     p2.join()

# 4.
# def fibonacci(n):
#     a, b = 0, 1
#     for _ in range(n):
#         print(a, end=' ')
#         a, b = b, a + b

# if __name__ == "__main__":
#     p1 = Process(target=fibonacci,args=(30,))
#     p2= Process(target=fibonacci,args=(35,))
#     p1.start()
#     p2.start()
#     p1.join()
#     p2.join()


# 5.
# def eng_katta_son(sonlar: list[int],q: Queue):
#     eng_kattasi = 0
#     for son in sonlar:
#         if son > eng_kattasi:
#             eng_kattasi = son

#     q.put(eng_kattasi)

# if __name__ == "__main__":
#     sonlar = [12,45,67,23,89,90,34,22]
#     q = Queue()
#     p1 = Process(target=eng_katta_son,args=(sonlar[:len(sonlar) // 2],q))
#     p2= Process(target=eng_katta_son,args=(sonlar[len(sonlar) // 2:],q))
#     p1.start()
#     p2.start()
#     p1.join()
#     p2.join()
#     natija1 = q.get()
#     natija2 = q.get()
#     print(natija1 if natija1 > natija2 else natija2)


# 6.
# def kvadratlar_yigindisi(sonlar: list[int],q: Queue):
#     yigindi = 0
#     for son in sonlar:
#         yigindi += (son**2)

#     q.put(yigindi)

# if __name__ == "__main__":
#     sonlar = range(1,1000001)
#     q = Queue()
#     p1 = Process(target=kvadratlar_yigindisi,args=(sonlar[:len(sonlar) // 2],q))
#     p2= Process(target=kvadratlar_yigindisi,args=(sonlar[len(sonlar) // 2:], q))
#     p1.start()
#     p2.start()
#     p1.join()
#     p2.join()
#     natija1 = q.get()
#     natija2 = q.get()
#     print(natija1)
#     print(natija2)

# 7.
# def tartibla(sonlar: list[int], q: Queue):
#     q.put(sorted(sonlar))

# if __name__ == "__main__":
#     sonlar = [34,12,76,23,89,11,90,45]
#     q = Queue()
#     p1 = Process(target=tartibla,args=(sonlar[:len(sonlar) // 2],q))
#     p2= Process(target=tartibla,args=(sonlar[len(sonlar) // 2:], q))
#     p1.start()
#     p2.start()
#     p1.join()
#     p2.join()
#     natija1 = q.get()
#     natija2 = q.get()
#     print(sorted(natija1 + natija2))


# 8.
# def yigindisi(sonlar: list[int], q: Queue):
#     yigindi = 0
#     for son in sonlar:
#         for raqam in str(son):
#             yigindi += int(raqam)

#     q.put(yigindi)

# if __name__ == "__main__":
#     sonlar = [123456, 987654, 567890,345678]
#     q = Queue()
#     p1 = Process(target=yigindisi,args=(sonlar[:len(sonlar) // 2],q))
#     p2= Process(target=yigindisi,args=(sonlar[len(sonlar) // 2:], q))
#     p1.start()
#     p2.start()
#     p1.join()
#     p2.join()
#     natija1 = q.get()
#     natija2 = q.get()
#     print(natija1)
#     print(natija2)

# 9.
# def eng_katta_son(sonlar: list[int],q: Queue):
#     q.put(min(sonlar))

# if __name__ == "__main__":
#     sonlar = [45,23,67,12,89,34,10]
#     q = Queue()
#     p1 = Process(target=eng_katta_son,args=(sonlar[:len(sonlar) // 2],q))
#     p2= Process(target=eng_katta_son,args=(sonlar[len(sonlar) // 2:],q))
#     p1.start()
#     p2.start()
#     p1.join()
#     p2.join()
#     natija1 = q.get()
#     natija2 = q.get()
#     print(min(natija1,natija2))

# 10.
# def tub_sonmi(son: int):
#     if son <= 1:
#         return False
#     for i in range(2, son):
#         if son % i == 0:
#             return False
#     return True

# def get_tub_sonlar_count(sonlar: list[int], q: Queue):
#     tub_sonlar = 0
#     for son in sonlar:
#         if tub_sonmi(son):
#             tub_sonlar += 1
#     q.put(tub_sonlar)


# if __name__ == "__main__":
#     sonlar = range(1,20)
#     q = Queue()
#     p1 = Process(target=get_tub_sonlar_count,args=(sonlar[:len(sonlar) // 2],q))
#     p2= Process(target=get_tub_sonlar_count,args=(sonlar[len(sonlar) // 2:],q))
#     p1.start()
#     p2.start()
#     p1.join()
#     p2.join()
#     natija1 = q.get()
#     natija2 = q.get()
#     print(natija1)
#     print(natija2)
#     print(natija1 + natija2)
