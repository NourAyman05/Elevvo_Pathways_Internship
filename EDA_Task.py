import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv("train.csv")

# Renaming columns
df.rename(columns={'Sex': 'Gender'}, inplace=True)
df.rename(columns={'SibSp': 'Siblings_Spouses_Aboard'}, inplace=True)
df.rename(columns={'Parch': 'Parents_Children_Aboard'}, inplace=True)

print(df.head())
print("\nShape of dataset:", df.shape)
print("\nColumns in dataset:", df.columns)

print("\nMissing values per column before cleaning:\n", df.isnull().sum())

# Cleaning
df['Age'] = df['Age'].fillna(df['Age'].median())
df['Embarked'] = df['Embarked'].fillna(df['Embarked'].mode()[0])
df.drop(columns=['Cabin'], inplace=True, errors='ignore')

print("\nMissing values after cleaning and deleting Cabin column:\n", df.isnull().sum())
print("\nFinal dataset shape:", df.shape)
print("\nFinal columns:", df.columns.tolist())

print("-------------------------------------------")
print(df.dtypes)

# Convert Gender to numeric
df['Gender'] = df['Gender'].map({'male': 0, 'female': 1})
print("\nUpdated after converting Gender:")
print(df.dtypes)

print("\n//////////////////// Summary Statistics ///////////////////////")
print(df.describe())
print(df['Embarked'].value_counts())
print(df['Pclass'].value_counts())


print("\n//////////////////// Group-Based Insights ///////////////////////")
print("Survival by Gender:\n", df.groupby('Gender')['Survived'].mean())
print("\nSurvival by Class:\n", df.groupby('Pclass')['Survived'].mean())
print("\nSurvival by Embarkation Point:\n", df.groupby('Embarked')['Survived'].mean())
print("\nBonus: Survival by Pclass and Gender:\n", df.groupby(['Pclass', 'Gender'])['Survived'].mean())

# ------------------- Visualizations -------------------

# Survival by Gender
plt.figure(figsize=(6,4))
sns.barplot(x='Gender', y='Survived', data=df)
plt.title("Survival Rate by Gender")
plt.xticks([0, 1], ['Male', 'Female'])
plt.tight_layout()
plt.savefig("survival_by_gender.png")  
plt.close() 


# Survival by Class
plt.figure(figsize=(6,4))
sns.barplot(x='Pclass', y='Survived', data=df)
plt.title("Survival Rate by Class")
plt.tight_layout()
plt.savefig("survival_by_class.png")
plt.close()


# Survival by Embarkation Point
plt.figure(figsize=(6,4))
sns.barplot(x='Embarked', y='Survived', data=df)
plt.title("Survival Rate by Embarkation Point")
plt.tight_layout()
plt.savefig("survival_by_embarked.png")
plt.close()


# Age Distribution
plt.figure(figsize=(6,4))
sns.histplot(df['Age'], bins=20, kde=True)
plt.title("Age Distribution")
plt.tight_layout()
plt.savefig("age_distribution.png")
plt.close()


# Heatmap of Correlations
plt.figure(figsize=(10,6))
numeric_df = df.select_dtypes(include=[np.number])
sns.heatmap(numeric_df.corr(), annot=True, cmap='coolwarm')
plt.title("Feature Correlation Heatmap")
plt.tight_layout()
plt.savefig("correlation_heatmap.png")
plt.close()

#-------------------------------------------------------------------------
# Feature Engineering: FamilySize and IsAlone
df['FamilySize'] = df['Siblings_Spouses_Aboard'] + df['Parents_Children_Aboard']
df['IsAlone'] = (df['FamilySize'] == 0).astype(int)

print("\nSurvival by IsAlone:\n", df.groupby('IsAlone')['Survived'].mean())

# Visualization: Survival Rate by IsAlone
plt.figure(figsize=(6,4))
sns.barplot(x='IsAlone', y='Survived', data=df)
plt.title("Survival Rate: Alone vs. With Family")
plt.xlabel("Is Alone (1 = Yes, 0 = No)")
plt.ylabel("Survival Rate")
plt.xticks([0, 1], ['With Family', 'Alone'])
plt.tight_layout()
plt.savefig("survival_by_isalone.png")
plt.close()

