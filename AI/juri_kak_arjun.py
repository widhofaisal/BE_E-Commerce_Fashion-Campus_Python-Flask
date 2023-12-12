from main import Main

# IMAGE TEST DARI KAK ARJUN

temp=[]
temp.append(Main.run_search_by_image("jury_test_kak_arjun/mnist_1.png"))
temp.append(Main.run_search_by_image("jury_test_kak_arjun/mnist_5.png"))
temp.append(Main.run_search_by_image("jury_test_kak_arjun/mnist_89.png"))
temp.append(Main.run_search_by_image("jury_test_kak_arjun/mnist_894.png"))
temp.append(Main.run_search_by_image("jury_test_kak_arjun/mnist_401.png"))
temp.append(Main.run_search_by_image("jury_test_kak_arjun/mnist_411.png"))
temp.append(Main.run_search_by_image("jury_test_kak_arjun/hat_1.jpg"))
temp.append(Main.run_search_by_image("jury_test_kak_arjun/hat_2.jpg"))
temp.append(Main.run_search_by_image("jury_test_kak_arjun/sandal.jpeg"))
temp.append(Main.run_search_by_image("jury_test_kak_arjun/trouser_2.jpg"))

temp_answer = [
    'Dress\t\t','Pullover\t','Ankle Boot\t','Bag\t\t','Sandals\t\t','Bag\t\t'
    ,'Hat\t\t','Hat\t\t','Sandals\t\t','Trouser\t\t'
    ]

print("\n========================\nUsing image from Kak Arjun\n")
print("IMAGE \t\t | PREDICTION")
for i in range(10):
    print(temp_answer[i],"=",temp[i])
print("\n")