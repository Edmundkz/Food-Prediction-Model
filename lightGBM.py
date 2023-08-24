import pandas as pd
import lightgbm as lgb
import pickle
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score

# データセットを読み込む
train_data = pd.read_csv('dataset.csv')
valid_data = pd.read_csv('validate_data.csv')

# ラベルエンコーダの初期化
le = LabelEncoder()

# Replacing Japanese gender tags with English ones
train_data['性別'] = train_data['性別'].replace({"男性": "male", "女性": "female"})
valid_data['性別'] = valid_data['性別'].replace({"男性": "male", "女性": "female"})

# Convert genders to numerical values
train_data['性別'] = le.fit_transform(train_data['性別'])
valid_data['性別'] = le.transform(valid_data['性別'])

# Extract hour from the timestamp
train_data['hour'] = pd.to_datetime(train_data['今の時間帯']).dt.hour
valid_data['hour'] = pd.to_datetime(valid_data['今の時間帯']).dt.hour

train_data.drop('今の時間帯', axis=1, inplace=True)
valid_data.drop('今の時間帯', axis=1, inplace=True)

# Split features and target
X_train = train_data.drop('食べれたか', axis=1)
y_train = train_data['食べれたか']
X_valid = valid_data.drop('食べれたか', axis=1)
y_valid = valid_data['食べれたか']

lgb_train = lgb.Dataset(X_train, y_train)
lgb_valid = lgb.Dataset(X_valid, y_valid, reference=lgb_train)

# Parameter settings
params = {
    'boosting_type': 'gbdt',
    'objective': 'binary',
    'metric': 'binary_logloss',
    'num_leaves': 31,
    'learning_rate': 0.05,
    'feature_fraction': 0.9
}

verbose_eval = 0
num_round = 100

bst = lgb.train(params, lgb_train, num_round, valid_sets=[lgb_valid], 
                callbacks=[lgb.early_stopping(stopping_rounds=10, verbose=True), lgb.log_evaluation(verbose_eval)])

# Save the model
pickle.dump(bst, open('parameter.sav', 'wb'))

# Make predictions
y_pred = bst.predict(X_valid, num_iteration=bst.best_iteration)
y_pred_binary = [1 if prob >= 0.5 else 0 for prob in y_pred]

# Calculate accuracy
accuracy = accuracy_score(y_valid, y_pred_binary)
print(f"Validation Accuracy: {accuracy:.4f}")

sample_data = {
    '年齢': [25],
    '性別': ['female'],
    '身長': [168.0],
    '体重': [60.0],
    '今の時間帯': ['2023-08-25 19:30:00'],
    '空いた時間': [6.5],
    '食べたカロリー': [1000.0],
    'これから食べるカロリー': [800.0]
}

df_sample = pd.DataFrame(sample_data)
df_sample['性別'] = le.transform(df_sample['性別'])
df_sample['hour'] = pd.to_datetime(df_sample['今の時間帯']).dt.hour
df_sample.drop('今の時間帯', axis=1, inplace=True)

pred_prob = bst.predict(df_sample, num_iteration=bst.best_iteration)
pred_binary = 1 if pred_prob[0] >= 0.5 else 0

print(f"Predicted Probability: {pred_prob[0]:.4f}")
print(f"Predicted Class: {pred_binary}")
