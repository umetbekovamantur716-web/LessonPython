data = []
for i in range (100):
    if i % 2== 0:
        data.append(i)
print(data)
############ генаратор списков 
data2 = [i for i in range (100) if i%2== 0]
print(data2)
###########
marks = {
    'gena':40,
    'anna':50,
    'bini':30,
}
newMarks = [v for k, v in marks.items()]
print(newMarks)


import re 
my_str= "djitu8476t347t9"
nums = re.findall('[0-9]+',my_str)
numbers = []
for i in nums:
    numbers.append(int(i))
print(numbers)



##################

nums = []
temp = []
for i in my_str:
    if i.isdigit():
        temp+=i
    elif temp:
        nums.append(int(temp))
        temp = ''
    nums.append(int(temp))
print(nums)


