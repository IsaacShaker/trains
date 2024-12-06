#my first python yay
x = {1, 5, 7, 9}
y = 10

for n in range(0, 21, 5):
     if n == y:
        print(y)

a = "hello"
print(len(a))

e = ["lala", "micah"] #list
f = ("lala", "micah") #tuple
g = {"lala", "micah"} #list, does not allow duplicates


dictionary = {             #ignores duplicate key values
      "brand" : "ford",
      "model" : "f-150",
      "year"  : 2020
}

print(dictionary)
print(dictionary["brand"])
print(dictionary["model"])
print(dictionary["year"])

A = 5
B = 5

if A > B:
    print("A is greater than B")
elif A == B:                        #else if 
    print ("A is equal to B")
else:
   print(("A is less than B"))


fruits = ["apple", "peach", "banana", "orange", "pear"]

for i in fruits:
    print(i)
else:
    print("No more fruit")

#this for loop will skip i's and break once
for j in "mississippi":
    if j == "p":
        break
    elif j== "i":
        continue
    print(j)

#function and classes
def funct(name):
    print(name)


#testing functions and classes
funct("Micah")

class Class1:
    #default constructor
    def __init__(self, name="Micah", age=20, home="Pittsburgh"):
        self.name = name  # Use self to assign to instance variables
        self.age = age
        self.home = home

person1 = Class1()
print(person1.name)
print(person1.age)
print(person1.home)

person2 = Class1("Gunnar", 23, "Baltimore")
print(person2.name)
print(person2.age)
print(person2.home)




