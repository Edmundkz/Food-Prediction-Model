import random
import pandas as pd
import datetime

# データを生成する関数



def generate_data(n):
    #女性の平均の一日消費カロリー
    woman_calory=2300
    #男性の平均の一日消費カロリー
    man_calory=3000

    data = []
    for _ in range(n):
        age = random.randint(18, 80)
        gender = random.choice(["男性", "女性"])
        if gender=='女性':
            height = 155+round(random.uniform(0,100)/10, 1)
        else:
            height = 165+round(random.uniform(0,100)/10, 1)

        weight =round((height*height*22)/10000+random.uniform(0,10)/10,1)

        now = datetime.datetime.now()
        eat_time= now.replace(hour=random.randint(1,23), minute=random.randint(1,59), second=0, microsecond=0)

        before_eat_time=round(random.uniform(1,23),1)

        before_eat_kind=round(random.uniform(300,800),1)

        after_eat_kind=round(random.uniform(300,800),1)

        
        man_all_calory=(weight*13.397+height*4.799-5.677*age+88.362)*0.8

        woman_all_calory=(weight*9.247+height*3.098-4.33*age+447.593)*0.8

        if gender==0:
            if after_eat_kind+before_eat_kind-(woman_calory*before_eat_time/24)>woman_all_calory*0.6:
                complete_eat=0
            else:
                complete_eat=1
            
        else:
            if after_eat_kind+before_eat_kind-(woman_calory*before_eat_time/24)>man_all_calory*0.6:
                complete_eat=0
            else:
                complete_eat=1

        data.append([age, gender, height, weight,eat_time,before_eat_time,before_eat_kind,after_eat_kind,complete_eat])
    return data

# データを生成
data = generate_data(10000)

validate_data=generate_data(500)

# データをDataFrameに変換
df = pd.DataFrame(data, columns=["年齢", "性別", "身長", "体重","今の時間帯","空いた時間","食べたカロリー","これから食べるカロリー","食べれたか"])

df_validate = pd.DataFrame(data, columns=["年齢", "性別", "身長", "体重","今の時間帯","空いた時間","食べたカロリー","これから食べるカロリー","食べれたか"])


# データをCSVファイルに保存
df.to_csv("dataset.csv", index=False)
df_validate.to_csv("validate_data.csv",index=False)



