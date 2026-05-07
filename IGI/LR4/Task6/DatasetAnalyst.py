import pandas as pd
from pandas.api.types import CategoricalDtype
import numpy as np

class DatasetAnalysist:
    def __init__(self):
        self.df = pd.read_csv("Task6/dataset/SuperMarket Analysis.csv")
        self.series = pd.get_dummies(self.df=='Product line')

    def __parse_time_str(self, st: str):
        return int(st.split(':')[0]) if st.split(' ')[1] == 'AM' else int(st.split(':')[0]) + 12

    def times_earnings(self):
        """Во сколько раз доход в самые продаваемые 
            часы больше дохода в самые непродаваемые"""

        self.df['Hour'] = self.df['Time'].apply(self.__parse_time_str)

        groups = self.df.groupby('Hour').agg(income=('gross income', 'sum'))
        
        print("Тотальный доход по часовым группам:")
        print(groups.head(15))
        
        print("Самые доходные часы:")
        best_incoming = groups[groups['income'] > groups['income'].quantile(0.75)]
        print(best_incoming)

        print("Самые недоходные часы:")
        worst_incoming = groups[groups['income'] < groups['income'].quantile(0.25)]
        print(worst_incoming)

        print(f"Искомая средняя разница в доходах между самыми прибыльными часами {
            list(best_incoming['income'].index)} и самыми неприбыльными {
            list(worst_incoming['income'].index)}:  {np.round(
            best_incoming['income'].mean() / worst_incoming['income'].mean(), 2)}")       




