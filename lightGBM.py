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
# 性別を数値に変換
train_data['性別'] = le.fit_transform(train_data['性別'])
valid_data['性別'] = le.transform(valid_data['性別'])  

# 今の時間帯から時間を抽出
train_data['hour'] = pd.to_datetime(train_data['今の時間帯']).dt.hour
valid_data['hour'] = pd.to_datetime(valid_data['今の時間帯']).dt.hour


train_data.drop('今の時間帯', axis=1, inplace=True)
valid_data.drop('今の時間帯', axis=1, inplace=True)

# 特徴量とターゲットを分割
X_train = train_data.drop('食べれたか', axis=1)
y_train = train_data['食べれたか']
X_valid = valid_data.drop('食べれたか', axis=1)
y_valid = valid_data['食べれたか']

lgb_train = lgb.Dataset(X_train, y_train)
lgb_valid = lgb.Dataset(X_valid, y_valid, reference=lgb_train)

# パラメータの設定
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


#bst = lgb.train(params, lgb_train, num_round, valid_sets=[lgb_valid])
bst = lgb.train(params, lgb_train, num_round, valid_sets=[lgb_valid], callbacks=[lgb.early_stopping(stopping_rounds=10, verbose=True),lgb.log_evaluation(verbose_eval)])


# モデルを保存
pickle.dump(bst, open('parameter.sav', 'wb'))

# 予測を実行
y_pred = bst.predict(X_valid, num_iteration=bst.best_iteration)
y_pred_binary = [1 if prob >= 0.5 else 0 for prob in y_pred]  

# 精度を計算
accuracy = accuracy_score(y_valid, y_pred_binary)
print(f"Validation Accuracy: {accuracy:.4f}")






