import pandas as pd
from django.conf import settings


def get_workers():
    df = pd.read_csv(settings.BASE_DIR / 'ftp/sotrudniki.csv', sep=';', encoding='utf8')
    return df.astype(object).where(pd.notnull(df), None).to_dict(orient="records") 
