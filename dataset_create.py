import numpy as np
import csv
from datetime import datetime, timedelta

def generate_data(n):
    data = []
    sample_date = datetime.strptime('2023-08-25', '%Y-%m-%d')
    ages = np.random.randint(20, 80, n)
    genders = np.random.choice(['男性', '女性'], n)
    heights = np.random.uniform(150, 190, n)
    weights = np.random.uniform(45, 90, n)
    times = [sample_date + timedelta(hours=np.random.uniform(0, 24), minutes=np.random.uniform(0, 60)) for _ in range(n)]
    remaining_hours_before_eating = np.random.uniform(1, 20, n)
    
    daily_needs = np.array([compute_bmr(ages[i], genders[i], heights[i], weights[i]) for i in range(n)]) * 1.2
    calories_eaten = np.random.uniform(0, daily_needs)
    next_meal_calories = np.array([adjust_for_remaining_time_before_eating(remaining_hours_before_eating[i], daily_needs[i], calories_eaten[i]) for i in range(n)])
    can_eat = (calories_eaten + next_meal_calories <= daily_needs).astype(int)
    
    for i in range(n):
        data.append({
            '年齢': ages[i], 
            '性別': genders[i], 
            '身長': heights[i], 
            '体重': weights[i], 
            '今の時間帯': times[i].strftime('%Y-%m-%d %H:%M:%S'), 
            '空いた時間': remaining_hours_before_eating[i], 
            '食べたカロリー': calories_eaten[i], 
            'これから食べるカロリー': next_meal_calories[i], 
            '食べれたか': can_eat[i]
        })
    return data

def write_to_csv(data, filename):
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['年齢', '性別', '身長', '体重', '今の時間帯', '空いた時間', '食べたカロリー', 'これから食べるカロリー', '食べれたか']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in data:
            writer.writerow(row)

def compute_bmr(age, gender, height, weight):
    if gender == '男性':
        return (10 * weight) + (6.25 * height) - (5 * age) + 5
    else:
        return (10 * weight) + (6.25 * height) - (5 * age) - 161

def adjust_for_remaining_time_before_eating(hours, daily_needs, current_calories):
    if hours < 2:
        intake = daily_needs * np.random.uniform(0.25, 0.5) - current_calories
    elif 2 <= hours < 5:
        intake = (daily_needs - current_calories) * np.random.uniform(0.5, 0.75)
    else:
        intake = (daily_needs - current_calories) * np.random.uniform(0.75, 1.5)  

    if np.random.rand() < 0.5:
        intake *= np.random.uniform(1.1, 1.5)
    return intake



if __name__ == "__main__":
    data = generate_data(10000)
    write_to_csv(data, 'dataset.csv')
    
    validate_data = generate_data(500)
    write_to_csv(validate_data, 'validate_data.csv')
