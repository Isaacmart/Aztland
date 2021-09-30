values = [90, 50, 30, 80, 35, 35]
total = 0
for value in values:
    total += value

secondValues = values
secondValues.append(40)

secondTotal = 0
for item in secondValues:
    secondTotal += item

percentage = (secondTotal * 100) / total


print(total)
print(secondTotal)
print(percentage)
