"""BMI Calculator Project in Python"""

"""BMI = (Weight in pounds * 703) / (Height in inches * Height in inches)"""


weight = int(input("Enter your weight in pounds: "))

height = int(input("Enter your height in inches: "))

'''print("You're weight is : ", weight, " and height is: ", height)'''

BMI = (weight * 703) / (height * height)

print("Your BMI is: ", BMI)

if BMI>0:
    if BMI<18.5:
        print("You are underweight. However, there is minimal health risk.")
    elif BMI<=24.9:
        print("You are of normal weight. There is minimal health risk.")
    elif BMI<=29.9:
        print("You are overweight. There is increased health risk.")
    elif BMI<=34.9:
        print("You are obese. There is a high health risk.")
    elif BMI<=39.9:
        print("You are severely obese. There is very high health risk.")
    elif BMI>=40:
        print("You are morbidly obese. There is extremely high health risk.")
