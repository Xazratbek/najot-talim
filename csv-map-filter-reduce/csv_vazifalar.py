# def contamination(text, char):
#     if len(text) == 0 or len(char) == 0:
#         return ""
#     else:
#         uzunlik = len(text)
#         return char * uzunlik

# print(contamination("avc"," "))

# def remove_char(s):
#     if len(s) == 2:
#         return ""
#     else:
#         s = s.replace(s[0],"",1)
#         s = s.replace(s[-1],"",1)
#         s = s.strip()
#         return s
# print(remove_char("eloquent"))

import csv

# Uyga vazifa 1:

# students = [
#     ["Ali", 18, "Python"],
#     ["Vali", 20, "Django"],
#     ["Hasan", 19, "FastAPI"]
# ]

# with open("students.csv","w",newline="") as file:
#     writer = csv.writer(file)
#     writer.writerows(students)

# with open("students.csv","r",newline="") as file:
#     data = csv.reader(file)
#     for i in data:
#         print(i)

# Uyga vazifa 2:
# products = [
#     {"name": "Laptop", "price": 1200, "qty": 5},
#     {"name": "Phone", "price": 800, "qty": 10},
#     {"name": "Mouse", "price": 20, "qty": 50}
# ]

# with open("products.csv","w",newline="") as file:
#     columns = ['name','price','qty']
#     writer = csv.DictWriter(file,fieldnames=columns,)
#     writer.writeheader()
#     writer.writerows(products)

# with open("products.csv","r",newline="") as file:
#     columns = ['name','price','qty']
#     read = csv.DictReader(file,fieldnames=columns)
#     data = list(read)
#     print(data)

# Uyga vazifa 3:

# with open("users.csv","r",newline="") as file:
#     reader = csv.DictReader(file)
#     natija: list[dict] = []
#     for row in reader:
#         username = row["username"]
#         age = row["age"]
#         natija.append({"username": username,"age": age})
#     print(natija)

# Uyga vazifa 4:

# numbers = [
#     [2, 5, 8],
#     [10, 3, 7],
#     [6, 6, 6]
# ]

# with open("numbers.csv","w",newline="") as writemode:
#     writer = csv.writer(writemode)
#     writer.writerows(numbers)

# with open("numbers.csv","r",newline="") as readmode:
#     reader = csv.reader(readmode)
#     for qator in reader:
#         print(sum([int(son) for son in qator]))

# Uyga vazifa 5:

# with open("results.csv","r",newline="") as file:
#     natija: list[dict] = []
#     reader = csv.DictReader(file,fieldnames=['name','score'])
#     next(reader)
#     for row in reader:
#         name = row["name"]
#         score = row["score"]
#         natija.append({"name": name,"score": score}) if int(score) >= 60 else ...
#     print(natija)

# Uyga vazifa 6:

# students = [
#     {"name": "Ali", "age": 18, "score": 75},
#     {"name": "Vali", "age": 19, "score": 90},
#     {"name": "Hasan", "age": 18, "score": 60},
#     {"name": "Olim", "age": 20, "score": 85}
# ]

# with open("sortstudents.csv","w",newline="") as file:
#     writer = csv.DictWriter(file,["name","age","score"])
#     writer.writeheader()
#     writer.writerows(students)

# with open("sortstudents.csv","r",newline="") as file:
#     reader = csv.DictReader(file,["name","age","score"])
#     data = []
#     for row in reader:
#         row["age"]  = int(row["age"])
#         row["score"] = int(row["score"])
#         data.append(row)
#     sorted_data = sorted(data,key=lambda x: x["score"], reverse=True)
#     print(sorted_data)
#     for s in sorted_data:
#         print(f'{s["name"]}: {s["score"]}')


# Uyga vazifa 7:
# data: list[dict] = []

# with open("employees.csv","r+",newline="") as file:
#     reader = csv.DictReader(file)
#     for row in reader:
#         if float(row["salary"] ) < 1000.00:
#             row["salary"]  = float(row["salary"]) * (1 + 20 / 100)
#             data.append(row)
#         else:
#             data.append(row)

# with open("employees.csv","w",newline="") as file:
#     writer = csv.DictWriter(file,fieldnames=["id","name","salary"])
#     writer.writeheader()
#     writer.writerows(data)

# Uyga vazifa 8:
# final_data: list[dict] = []

# with open("group1.csv","r",newline="") as file1,open("group2.csv","r",newline="") as file2:
#     freader1 = csv.DictReader(file1,fieldnames=["name","score"])
#     next(freader1)
#     for row in freader1:

#         final_data.append(row)

#     freader2 = csv.DictReader(file2,fieldnames=["name","score"])
#     next(freader2)
#     for row in freader2:
#         final_data.append(row)

#     with open("final_group_data.csv","a",newline="") as new_file:
#         writer = csv.DictWriter(new_file,fieldnames=["name","score"])
#         writer.writeheader()
#         writer.writerows(final_data)

# Uyga vazifa 9:

# final_data: dict = {}
# with open("orders.csv","r",newline="") as file:
#     reader = csv.DictReader(file,fieldnames=["user","amount"])
#     next(reader)
#     for row in reader:
#         if row["user"] in final_data:
#             final_data[row["user"]] = final_data.get(row['user'],0) + int(row["amount"])
#         else:
#             final_data[row["user"]] = int(row['amount'])
#     print(final_data)

# Uyga vazifa 10:

# error_data: list[dict] = []
# cleaned_data: list[dict] = []
# with open("studentlar.csv","r",newline="") as file:
#     reader = csv.DictReader(file,fieldnames=["name","age","score"])
#     next(reader)
#     for row in reader:
#         if int(row["age"]) < 0 or int(row["score"]) > 100:
#             error_data.append(row)
#         else:
#             cleaned_data.append(row)

#     with open("errors.csv","a",newline="") as errors:
#         errors = csv.DictWriter(errors,fieldnames=["name","age","score"])
#         errors.writeheader()
#         errors.writerows(error_data)

#     with open("clean_data.csv","a",newline="") as clean_data:
#         clean_data = csv.DictWriter(clean_data,fieldnames=["name","age","score"])
#         clean_data.writeheader()
#         clean_data.writerows(cleaned_data)