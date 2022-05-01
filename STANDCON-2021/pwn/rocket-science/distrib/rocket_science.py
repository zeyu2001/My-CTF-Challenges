#!/usr/bin/env python

import lambdaJSON as lj
import random


ASCII_ART = """
                                       _,'/
                                  _.-''._:
                          ,-:`-.-'    .:.|
                         ;-.''       .::.|
          _..------.._  / (:.       .:::.|
       ,'.   .. . .  .`/  : :.     .::::.|
     ,'. .    .  .   ./    \\ ::. .::::::.|
   ,'. .  .    .   . /      `.,,::::::::.;\\
  /  .            . /       ,',';_::::::,:_:
 / . .  .   .      /      ,',','::`--'':;._;
: .             . /     ,',',':::::::_:'_,'
|..  .   .   .   /    ,',','::::::_:'_,'
|.              /,-. /,',':::::_:'_,'
| ..    .    . /) /-:/,'::::_:',-'
: . .     .   // / ,'):::_:',' ;
 \ .   .     // /,' /,-.','  ./
  \ . .  `::./,// ,'' ,'   . /
   `. .   . `;;;,/_.'' . . ,'
    ,`. .   :;;' `:.  .  ,'
   /   `-._,'  ..  ` _.-'
  (     _,'``------''  
   `--''
"""

print(ASCII_ART)
print("Welcome to Rocket Science! In this class, we will learn all about rockets.")
print("For our first lesson, we will start with the basics of mathematics.")

while True:
	print("1) Test your knowledge\n2) Save numbers\n3) Load numbers")
	
	ipt = input("> ")
	
	if ipt == '1':
	
		print("Do you know your numbers?")
		num_to_word = {1: 'one', 2: 'two', 3: 'three', 4: 'four', 5: 'five'}
		
		num = random.randint(1, 5)
		print(f"What is {num} in words?")
		
		ans = input("> ")
		
		if ans == num_to_word[num]:
			print("You're right! Good job!")
		else:
			print(f"The correct answer is {num_to_word[num]}. Try again!")
	
	elif ipt == '2':
	
		print("Enter 5 numbers to save:")
		numbers = []
		
		try:
			for _ in range(5):
				numbers.append(int(input('> ')))
		except:
			print("Invalid number!")
		
		else:
			print("Sorry, this functionality is disabled at the moment.")
			print("Perhaps you could find us a better library for this?")
		
	elif ipt == '3':
	
		print("Enter saved numbers:")
		
		try:
			numbers = lj.deserialize(input('> '))
			
			if type(numbers) == tuple and all(type(x) == int for x in numbers):
				print(numbers)
				
			else:
				print("Don't you know what numbers are?")
			
		except:
			print("Invalid input!")	
	
