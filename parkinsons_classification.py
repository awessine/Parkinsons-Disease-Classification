# -*- coding: utf-8 -*-
"""Обнаружение болезни паркинсона с помощью XGBoost

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1GSHEJdQ0VeM7cM9R1Debi_0LzOLBivFX
"""

!pip install seaborn

# Импорт необходимых библиотек
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os, sys
import xgboost as xgb
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.linear_model import LogisticRegression
from imblearn.over_sampling import SMOTE

# Импорт данных из CSV файла
df = pd.read_csv('/content/parkinsons.data')

df = df.drop(columns=['name'])

# Создание тепловой карты корреляции

plt.figure(figsize=(17,8))
sns.heatmap(df.corr(),annot=True,cmap='cubehelix_r')
plt.show()

# Извлечение всех признаков (кроме колонки 'status')
all_features=df.loc[:,df.columns!='status'].values[:,1:]#all featueres
# Извлечение целевой переменной (статус: больной/здоровый)
out_come=df.loc[:,'status'].values

# Нормализация признаков в диапазоне от -1 до 1 с помощью MinMaxScaler
scaler=MinMaxScaler((-1,1))
# масштабируем признаки
X=scaler.fit_transform(all_features)
# сохраняем целевую переменную
y=out_come

# Разделение данных на обучающую и тестовую выборки (80% обучение, 20% тест)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=1, stratify=y)

# Инициализация классификатора XGBoost
xgb_clf = xgb.XGBClassifier()
xgb_clf = xgb_clf.fit(X_train, y_train)

# Применение SMOTE для увеличения данных (синтетическое дополнение меньшего класса)
smote = SMOTE(random_state=1)
X_resampled, y_resampled = smote.fit_resample(X_train, y_train)

# Обучаем модель на увеличенных данных
xgb_clf.fit(X_resampled, y_resampled)

# Оценка точности
y_pred = xgb_clf.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

print('Точность модели на обучающей выборке : %.2f' % (xgb_clf.score(X_train, y_train)*100))
print('Точность модели на тестовой выборке : %.2f' % (xgb_clf.score(X_test, y_test)*100))