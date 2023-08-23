import sys

from sklearn.preprocessing import LabelEncoder
import pickle
import pandas as pd

"""
$pythonPath = *.~. "/lightGBM_model.py";
$cmd = "python3 " . $pythonPath . " " . implode(" ", $data);

//Pythonのファイルにデータを送信(dataを受取って、outに返す)
//dataはarrayで要素だけを送って受け取るか、jsonにしてファイルに書き込んでから、python側で参照して取り込む
exec($cmd, $out);
"""
#モデルのパラメータをロード
load_model_lightGBM=pickle.load(open('/Users/edmund/code/rakuten_intern/parameter.sav','rb'))

df_single = pd.DataFrame([])

le = LabelEncoder()
sexlabels=['女性','男性']
sexlabels_id=le.fit_transform(sexlabels)

df_single['hour'] = pd.to_datetime(df_single['今の時間帯']).dt.hour
df_single['性別'] = le.transform(df_single['性別'])
df_single.drop('今の時間帯', axis=1, inplace=True)

X_single = df_single


#モデルから推論
pred_prob = load_model_lightGBM.predict(X_single, num_iteration=load_model_lightGBM.best_iteration)
prediction = 1 if pred_prob[0] >= 0.5 else 0
if prediction == 1:
    print("食事を完食する可能性が高いです")
else:
    print("完食しない可能性が高いです")


