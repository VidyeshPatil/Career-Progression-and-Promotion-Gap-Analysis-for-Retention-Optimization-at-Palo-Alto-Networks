import numpy as np


def create_features(df):

    df['PromotionGapRatio'] = (
        df['YearsSinceLastPromotion'] /
        (df['YearsAtCompany'] + 1)
    )

    df['RoleStagnationIndex'] = (
        df['YearsInCurrentRole'] /
        (df['YearsAtCompany'] + 1)
    )

    df['TrainingIntensityScore'] = (
        df['TrainingTimesLastYear'] /
        (df['YearsAtCompany'] + 1)
    )

    df['ManagerStabilityIndicator'] = (
        df['YearsWithCurrManager'] /
        (df['YearsAtCompany'] + 1)
    )

    df['RetentionOpportunityIndex'] = (
        (1 - df['PromotionGapRatio']) +
        (1 - df['RoleStagnationIndex']) +
        df['TrainingIntensityScore']
    )

    return df