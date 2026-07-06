import pandas as pd
from sklearn.preprocessing import StandardScaler, LabelEncoder
import os


# LOAD DATA

def load_data(file_path):

    # Project root directory
    BASE_DIR = os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )

    # Full dataset path
    full_path = os.path.join(BASE_DIR, file_path)

    # Debug path
    print("Looking for dataset at:", full_path)

    # Check existence
    if not os.path.exists(full_path):
        raise FileNotFoundError(
            f"Dataset not found at: {full_path}"
        )

    # Read CSV
    df = pd.read_csv(full_path)

    # RENAME YOUR DATASET COLUMNS

    df.rename(columns={

        'Environment': 'EnvironmentSatisfaction',
        'JobInvolveme': 'JobInvolvement',
        'JobSatisf': 'JobSatisfaction',
        'MonthlyI': 'MonthlyIncome',
        'MonthlyR': 'MonthlyRate',
        'NumComp': 'NumCompaniesWorked',
        'PercentS': 'PercentSalaryHike',
        'Performa': 'PerformanceRating',
        'Relations': 'RelationshipSatisfaction',
        'StockOpti': 'StockOptionLevel',
        'TotalWor': 'TotalWorkingYears',
        'TrainingT': 'TrainingTimesLastYear',
        'WorkLife': 'WorkLifeBalance',
        'YearsAtC': 'YearsAtCompany',
        'YearsInC': 'YearsInCurrentRole',
        'YearsSinc': 'YearsSinceLastPromotion'

    }, inplace=True)

    return df

# ENCODE CATEGORICAL DATA
def encode_data(df):

    df = df.copy()

    categorical_cols = df.select_dtypes(
        include=['object']
    ).columns

    le = LabelEncoder()

    for col in categorical_cols:

        df[col] = le.fit_transform(
            df[col].astype(str)
        )

    return df

# SCALE FEATURES

def scale_features(df, features):

    scaler = StandardScaler()

    df[features] = scaler.fit_transform(
        df[features]
    )

    return df

# REMOVE OUTLIERS

def remove_outliers(df, columns):

    for col in columns:

        q1 = df[col].quantile(0.25)
        q3 = df[col].quantile(0.75)

        iqr = q3 - q1

        lower = q1 - 1.5 * iqr
        upper = q3 + 1.5 * iqr

        df = df[
            (df[col] >= lower) &
            (df[col] <= upper)
        ]

    return df