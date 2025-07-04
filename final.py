import pandas as pd
import random
import json
import numpy as np
from datascience import *
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')

class User: 

    """
    Asks the user to input their name, height, weight, age, sport, daily activity, and goal

    Attributes:
       name (str) = The user's name
       height (int) = The user's height
       weight (int) = The user's weight
       age (int) = The user's age
       sport (str) = The user's sport intensity
       daily_activity (str) = The user's active activity
       goal (str) = The user's prefered goal

    Raises:
        ValueErrors: If the input datatype is wrong
        
    """
    
    def get_user_info(self):
        self.name = input("Name: ")
        self.height = float(input("Height (in meters): "))
        self.weight = float(input("Weight (in kg): "))
        self.age = int(input("Age: "))
        
        # Sport
        sport = input("Sport (high-intensity/moderate-intensity/low-intensity): ")
        self.sport = sport if sport in ["high-intensity", "moderate-intensity", "low-intensity"] else "invalid input"
        
        if self.sport == "invalid input": 
            exit()
            
        # Daily Activities
        daily_activity = input("Daily Activities (lightly active/average/very active): ")
        self.daily_activity = daily_activity if daily_activity in ["lightly active", "average", "very active"] else "invalid input"

        if self.daily_activity == "invalid input": 
            exit()
            
        # Goal
        intent = input("Goal (shred/bulk/maintenance): ")
        self.goal = intent if intent in ["shred", "bulk", "maintenance"] else "invalid input"
        
        if self.goal == "invalid input": 
            exit()
        
        print(f"This is {self.name}. Their height is {self.height}. Their weight is {self.weight}. Their age is {self.age}. The sport they play is {self.sport}. Their daily activities include {self.daily_activity}. Their goal is to {self.goal}.")

class Calories: 
    """
    Given user information this class calculates calories based on their desired goal. 
    Takes in height, weight, age, sport, daily activity and goal and spits out a personalized target number for them.
    Source used for calorie calculator: https://www.calculator.net/calorie-calculator.html
    
    Attributes:
        guidelines_file (txt file): the txt file to shred, maintenance or bulk.
        height (str): the user's height.
        weight (str): the user's weight.
        age (str): the user's age.
        sport (str): the user's sport intensity.
        daily_activity (str): the user's activilty level on a daily basis.
        goal (str): the user's goal.
    """
    def __init__(self, guidelines_file, user_height, user_weight, user_age, user_sport, user_daily_activity, user_goal):
        self.guidelines_file = guidelines_file
        self.height = user_height
        self.weight = user_weight
        self.age = user_age  
        self.sport = user_sport
        self.daily_activity = user_daily_activity
        self.goal = user_goal
    
    def _read_guidelines(self, goal):
        """Reads the guideline text file
        
        Args:
            goal (str): either shred, maintenance, or bulk
        """
  
        with open(self.guidelines_file, 'r', encoding='utf-8') as file:
            for line in file:
                if line.startswith(goal):
                    return next(file).strip()

   
    def calculate_calories(self):
        """Function used to determine which calories to calulate based on the user's goal.
        
        Returns:
            Number of calories personalized for the user
        """
        if self.goal == "maintenance":
            guidelines = self._read_guidelines("maintenance")
        if self.goal == "shred":
            guidelines = self._read_guidelines("shred")
        if self.goal == "bulk":
            guidelines = self._read_guidelines("bulk")
            
        return self.calculate_custom_calories(guidelines)
        

    def calculate_custom_calories(self, guidelines):
        """This function gets called by calculate_calories that does the math
        behind the printed out number of calories.
        
        Args:
            guidelines (str): scans the txt file for shred, maintenance, or bulk.
            That information is used to calculate calories.
            
        """
       # comprehensions, parse guidelines from the file
        
        guideline_values = [float(val) for val in guidelines.split(',')[1:]]
        maintenance_calories = (9.56 * self.weight) + (6.25 * self.height * 100) - (5 * self.age) + 5
        shred_calories = maintenance_calories - 200
        bulk_calories = maintenance_calories + 200

        if self.sport.lower() == "high-intensity":
            maintenance_calories *= 1.3
            shred_calories *= 1.3
            bulk_calories *= 1.3
        elif self.sport.lower() == "moderate-intensity":
            maintenance_calories *= 1.2
            shred_calories *= 1.2
            bulk_calories *= 1.2
        elif self.sport.lower() == "low-intensity": 
            maintenance_calories *= 1.1
            shred_calories *= 1.1
            bulk_calories *= 1.1
        if self.daily_activity.lower() == "lightly active":
            maintenance_calories *= 1.2
            shred_calories *= 1.2
            bulk_calories *= 1.2
        elif self.daily_activity.lower() == "average":
            maintenance_calories *= 1.3
            shred_calories *= 1.3
            bulk_calories *= 1.3
        elif self.daily_activity.lower() == "very active":
            maintenance_calories *= 1.4
            shred_calories *= 1.4
            bulk_calories *= 1.4
        return {
            "maintenance": maintenance_calories,
            "shred": shred_calories,
            "bulk": bulk_calories
        }
        
    def bmi_calculation(self): 
    
        '''
        This method calculates the Body Mass Index (BMI) of the user and compare it with the average BMI of their age group based on a small sample dataset. 

        This method reads BMI data from a CSV file, calculates the user's BMI using their stored height and weight attributes, 
        retrieves the average BMI of their age group from the dataset, and compares the user's BMI with the average.
        
        Sources: 
        - Centers for Disease Control and Prevention, https://www.cdc.gov/nccdphp/dnpao/growthcharts/training/bmiage/page5_1.html
        The equation for calculating Body Mass Index in metric form was incorporated into this code with no modifications. 
        '''
        
        df = pd.read_csv("bmi.csv")
        new = df.groupby('Age')['Bmi'].mean()
        real_age = int(self.age)
        calculated_bmi = (self.weight) / ((self.height)**2)
        mean_bmi = new.loc[real_age]

        if int(calculated_bmi) >= int(mean_bmi): 
            print(f"The user's calculated BMI is {calculated_bmi}. The user's BMI is less than or equal to the average BMI of their age group.")
        else: 
            print(f"The user's calculated BMI is {calculated_bmi}. The user's BMI is greater than the average BMI of their age group.")
    
class Meals: 
    def get_meals_data():
    
        """
        Gets meals data from JSON file.

        Returns:
            dict: A dictionary containing meal number as
            keys and ingredients as values.
        """
        with open('meals_data.json', 'r', encoding='utf-8') as meals_list:
            meals_data = json.load(meals_list)
        return meals_data
    def get_meal_options(user_allergies=None, user_preferences=None):

        """
        Gives meal options based on user's allergies and preferences

        Args:
            user_allergies (list, optional): A list of user's allergies.
            Defaults to None
            user_preferences (list, optional): A list of user's meal preferences.
            Defaults to None

        Returns:
            list or None: A list of tuples that have meal options 
            (meal name and ingredients), or None if no meal options are found
        """
        with open('meals_data.json', 'r', encoding='utf-8') as meals_list:
            meals_data = json.load(meals_list)
        if user_allergies is None:
            user_allergies = input("Enter your allergies (comma-separated): ").strip().split(', ')
        if user_preferences is None:
            user_preferences = input("Enter your meal preferences (comma-separated): ").strip().split(', ')

        meals_data = Meals.get_meals_data()

        possible_meals = []
        for meal, ingredients in meals_data.items():
            allergies_present = any(allergy in ingredients for allergy in user_allergies)
            if allergies_present:
                continue
            match_count = sum(1 for preference in user_preferences if preference in ingredients)
            possible_meals.append((meal, ingredients, match_count))

        if len(possible_meals) == 0:
            return None

        sorted_meals = sorted(possible_meals, key=lambda x: (x[2], x[0]), reverse=True)
        num_meals_to_select = min(3, len(sorted_meals))
        meal_options = random.sample(sorted_meals[:num_meals_to_select], num_meals_to_select)

        if meal_options:
            print("Here are your meal options for today:")
            for meal_index in range(len(meal_options)):
                meal, ingredients, _ = meal_options[meal_index]
                print(f"{meal}: {', '.join(ingredients)}")
        else:
            print("Sorry, we couldn't find suitable meal options for your allergies.")
        return meal_options
    
    def graph(self, current_weight, goal, calories):

        '''
        This method creates a line graph illustrating the expected weight change over time based on the user's current weight,
        weight change goal, and estimated caloric deficit or surplus.

        Parameters:
        - current_weight (float): The user's current weight in kilograms.
        - goal (str): The user's weight change goal. Should be one of: "lose" or "gain".
        - calories (int): The estimated caloric deficit (if goal is "lose") or surplus (if goal is "gain") per day.
        '''
        change = make_array()
        graph = Table.read_table('graph - Sheet1.csv')
        #want this graph to be of fifteen months time, with a tick every week on the x-axis 
        kilos = int(calories) / 3500
        kilos_per_week = kilos / graph.num_rows #this will give the kilo change per week

        if goal == "maintenance":
            for i in range(graph.num_rows):
                x_val = current_weight
                change = np.append(change, x_val)
        if goal == "shred":
            for i in range(graph.num_rows):
                x_val = current_weight - kilos_per_week * i
                change = np.append(change, x_val)

        if goal == "bulk":
            for i in range(graph.num_rows):
                x_val = current_weight + kilos_per_week * i
                change = np.append(change, x_val)

        x = np.arange(0, len(change), 1)

        new_graph = graph.with_column("Pounds", change)

        plt.plot(x, change)
        plt.xlabel("Weeks")
        plt.ylabel("Weight (kgs)")
        plt.title("Weight Change Over Time")
        plt.show()

class Nutrition: 
    """
    A class to calculate adjusted calorie intake and provide dietary advice based on the fitness goal.

    Attributes:
        calories (CalorieCalculator): An object capable of calculating calorie needs.
        goal (str): The fitness goal - 'shred', 'bulk', or 'maintenance'.
    """
    def calculate_nutrition_plan(calories, goal):
        """
        Calculates the recommended daily caloric intake and provides specific dietary advice
        according to the specified fitness goal.

        Parameters:
            calories (CalorieCalculator): An object capable of calculating calorie needs.
            goal (str): The desired fitness goal - options are 'shred', 'bulk', or 'maintenance'.

        Returns:
            tuple: A tuple containing the adjusted calories (float) and dietary advice (str).
        """
        if goal == 'shred':
            calories = calories.calculate_calories()
            advice = "Focus on high protein intake and increase cardio."
        elif goal == 'bulk':
            calories = calories.calculate_calories()
            advice = "Ensure you are getting enough carbs and protein for recovery."
        elif goal == 'maintenance':
            advice = "Maintain a balanced diet to keep your current body weight."
            calories = calories.calculate_calories()
        return calories, advice
    def display_nutrition_calories(calories, goal, detailed=True):
        """
        Displays the calculated caloric intake and, if requested, detailed dietary advice.

        Parameters:
            calories (CalorieCalculator): An object capable of calculating calorie needs.
            goal (str): The desired fitness goal.
            detailed (bool): If True, prints both caloric intake and dietary advice; if False, prints only caloric intake.

        Returns:
            None: This method prints the caloric intake and dietary advice directly and does not return any value.
        """
        calories, advice = Nutrition.calculate_nutrition_plan(calories, goal)
        caloric_intake_info = f"Your daily caloric intake should be approximately {calories[user.goal]:.2f} calories."
        if detailed:
            print(f"For your goal to {user.goal}, {caloric_intake_info}")
            print(advice)
        else:
            print(caloric_intake_info)

# Calls:
if __name__ == "__main__":
    user = User()
    user.get_user_info()
    calories = Calories("guidelines.txt", user.height, user.weight, user.age, user.sport, user.daily_activity, user.goal)
    Calories.bmi_calculation(self=user)
    detailed_input = input("Do you want detailed dietary advice? (yes/no): ").strip().lower() == 'yes'
    Nutrition.display_nutrition_calories(calories, user.goal, detailed=detailed_input)
    Meals.get_meal_options()
    meals_instance = Meals()
    meals_instance.graph(user.weight, user.goal, 200)