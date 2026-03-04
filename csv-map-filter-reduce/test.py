nom = ["Lenova", "HP", "Asus", "Acer", "Apple"]
narx = [650, 200, 350, 700, 600 ]
mahsulot_haqida = ""
for i in range(len(nom)):
    if narx[i] >= 500:
        mahsulot_haqida += f"{i}. {nom[i]} - Narxi: {narx[i]}\n"
with open("masala11.txt", "w") as fayl:
        fayl.write(f"Narxi 500 dan katta mahsulotlarni {mahsulot_haqida}")
        print("masala11.txt Failiga saqlandi")