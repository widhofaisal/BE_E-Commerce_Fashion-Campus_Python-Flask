from main import Main

# IMAGE TEST DARI JURI TEST

temp=[]
temp.append(Main.run_search_by_image("penjurian_10img/1.jpg"))
temp.append(Main.run_search_by_image("penjurian_10img/2.jpg"))
temp.append(Main.run_search_by_image("penjurian_10img/3.jpeg"))
temp.append(Main.run_search_by_image("penjurian_10img/4.jpg"))
temp.append(Main.run_search_by_image("penjurian_10img/5.png"))
temp.append(Main.run_search_by_image("penjurian_10img/6.png"))
temp.append(Main.run_search_by_image("penjurian_10img/7.png"))
temp.append(Main.run_search_by_image("penjurian_10img/8.png"))
temp.append(Main.run_search_by_image("penjurian_10img/9.png"))
temp.append(Main.run_search_by_image("penjurian_10img/10.png"))
temp.append(Main.run_search_by_image("penjurian_10img/shirtmnist1.jpg"))
temp.append(Main.run_search_by_image("penjurian_10img/shirtmnist2.jpg"))

temp_answer = [
    'Hat\t\t','Hat\t\t','Sandals\t\t','Trousser\t','Ankle Boot\t','Bag\t\t'
    ,'Sneaker\t\t','Dress\t\t','Shirt\t\t','Bag\t\t','Coat\t\t','Shirt\t\t'
    ]

print("\n========================\nUsing image from Juri\n")
print("IMAGE \t\t | PREDICTION")
for i in range(12):
    print(temp_answer[i],"=",temp[i])
print("\n")