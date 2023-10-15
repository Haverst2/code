with open("我的女友是恶劣大小姐.txt","r") as f:
    a = 1
    with open("a.txt","w") as e:
        for line in f:
            if line[:a].isdigit() == True:
                number = int(line[:a])
                print(line)
                #  if number == 9 :
                #     a = a + 1
                # elif number == 99:
                #     a = a + 1
                if number == 999:
                    a = a + 1
                e.write("===第"+str(number)+"章"+" "+line[3+a+1:])
            else:
                e.write(line)

            

            
        
        