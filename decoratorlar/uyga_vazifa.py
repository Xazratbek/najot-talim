from functools import wraps

# Uyga vazifa 1:
# def log_decorator(base_fn):
#     @wraps(base_fn)
#     def wrapper(*args):
#         print(f"{base_fn.__name__}-funcsiyasining argumentlari: {args}")
#         return base_fn(*args)

#     return wrapper

# @log_decorator
# def kvadratga_oshir(*args):
#     return list(map(lambda x: x**2, args))
# print(kvadratga_oshir(1,2,3,4,5))

# Uyga vazifa 2:
# class CallCounter:
#     def __init__(self, func):
#         self.func = func
#         self.count = 0

#     def __call__(self, *args, **kwargs):
#         self.count += 1
#         print(f" {self.func.__name__} {self.count}-martta chaqirildi")
#         return self.func(*args, **kwargs)


# @CallCounter
# def salom_ber(ism: str) -> str:
#     print("Hello!")

# salom_ber("Xazratbek")
# salom_ber("Ali")
# salom_ber("Hasan")


# Uyga vazifa 3
# from getpass import getpass

# password = 1411
# login = "xazratbek"

# def require_login(base_fn):
#     @wraps(base_fn)
#     def wrapper(profile: str,password: int):
#         if profile == login and password == password:
#             return base_fn(profile,password)
#         else:
#             return "Notog'ri login parol"

#     return wrapper

# @require_login
# def view_profile(login: str, parol: int):
#     return f"Hi {login} welcome"

# print(view_profile("ism",124124))
# print(view_profile("xazratbek",1411))

# Uyga vazifa 4:
# def format_function_str(base_fn):
#     @wraps(base_fn)
#     def wrapper(*args):
#         return str(base_fn(*args))

#     return wrapper

# @format_function_str
# def calculate_plus(*args):
#     return sum(args)

# print(calculate_plus(1,2,3,4,5))
# print(type(calculate_plus(1,2,3,4,5)))

# Uyga vazifa 5:

# from functools import wraps

# def log_function(base_fn):
#     @wraps(base_fn)
#     def wrapper(*args, **kwargs):
#         with open("./log.txt", "a") as file:
#             file.write(f"Funksiya: {base_fn.__name__} | args={args} kwargs={kwargs}\n")
#         return base_fn(*args, **kwargs)
#     return wrapper

# @log_function
# def sonni_kubi(*args):
#     return [x**3 for x in args]

# print(sonni_kubi(1,2,3,4,5))

# Uyga vazifa 6:

# def log_function(base_fn):
#     @wraps(base_fn)
#     def wrapper(*args, **kwargs):
#         with open("./log.txt", "a") as file:
#             file.write(f"Funksiya: {base_fn.__name__} | args={args} kwargs={kwargs} | Funksiya natijasi: {base_fn(*args, **kwargs)}\n")
#         return base_fn(*args, **kwargs)
#     return wrapper

# @log_function
# def sonni_kubi(*args):
#     return [x**3 for x in args]

# print(sonni_kubi(1,2,3,4,5))