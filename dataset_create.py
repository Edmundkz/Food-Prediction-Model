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
    
    # Initialize remaining_hours_before_eating based on the time of the day
    remaining_hours_before_eating = np.random.uniform(1, 20, n)
    for i in range(n):
        hour = times[i].hour
        if 7 <= hour < 11:  # Morning
            remaining_hours_before_eating[i] = np.random.uniform(7, 12)
        elif 11 <= hour < 14:  # Noon
            remaining_hours_before_eating[i] = np.random.uniform(2, 3) if np.random.rand() > 0.5 else np.random.uniform(5, 6)
        elif 14 <= hour < 18:  # Afternoon
            remaining_hours_before_eating[i] = np.random.uniform(3, 5)
        elif 18 <= hour < 24:  # Evening
            remaining_hours_before_eating[i] = np.random.uniform(2, 4)
    
    # Calculate daily caloric needs
    daily_needs = np.array([compute_bmr(ages[i], genders[i], heights[i], weights[i]) for i in range(n)]) * 1.2
    calories_eaten = np.random.uniform(0, daily_needs)
    next_meal_calories = np.random.uniform(300, 800, n)
    
    can_eat = []
    for i in range(n):
        hour = times[i].hour
        if 7 <= hour < 11:  # Morning
            can_eat.append(int((calories_eaten[i] + next_meal_calories[i]) <= daily_needs[i] * 0.2))
        elif 11 <= hour < 14:  # Noon
            can_eat.append(int((calories_eaten[i] + next_meal_calories[i]) <= daily_needs[i] * 0.5))
        elif 14 <= hour < 18:  # Afternoon
            can_eat.append(int((calories_eaten[i] + next_meal_calories[i]) <= daily_needs[i] * 0.7))
        elif 18 <= hour < 24:  # Evening
            can_eat.append(int((calories_eaten[i] + next_meal_calories[i]) <= daily_needs[i] * 0.8))
        else:  # Other times
            can_eat.append(int((calories_eaten[i] + next_meal_calories[i]) <= daily_needs[i]))
    
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

if __name__ == '__main__':
    data = generate_data(10000)
    write_to_csv(data, 'dataset.csv')
    
    validate_data = generate_data(500)
    write_to_csv(validate_data, 'validate_data.csv')