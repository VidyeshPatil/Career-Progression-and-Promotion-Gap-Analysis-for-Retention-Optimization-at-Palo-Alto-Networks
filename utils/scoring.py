import numpy as np


def calculate_risk(df):

    conditions = [
        (df['PromotionGapRatio'] < 0.3),
        (df['PromotionGapRatio'] >= 0.3) &
        (df['PromotionGapRatio'] < 0.7),
        (df['PromotionGapRatio'] >= 0.7)
    ]

    labels = ['Low Risk', 'Medium Risk', 'High Risk']

    df['PromotionGapRisk'] = np.select(
    conditions,
    labels,
    default="Unknown"
)

    return df