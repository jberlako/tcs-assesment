with open('hundred.txt', 'w') as hundred_file:
    for i in range(1, 101):
        hundred_file.write(str(i) + ' ')