# Get training data from a list of companies
import pandas as pd
import numpy as np
import sys
sys.path.append("..")
import os

from data.scripts.simplified_finance_stats.fin_stats import fin_stats
from data.scripts.simplified_finance_stats.fin_ratios import get_ratios
from data.scripts.simplified_finance_stats.fin_stats_2 import fin_stats_2
from report_13f.brk.company_13f import company_13f


class train_data(object):

    def __init__(self,c_df):
        # c_list is the company list
        self.c_df = c_df
        self.base_path = '../data/combined_simplified/'
        # Set up paths for data source
        self.fin_data1 = self.base_path + 'combined_all_us.csv'
        self.fin_data2 = self.base_path + 'others_all_us.csv'

        # Instantiate the all dataframe
        self.finances = fin_stats(self.fin_data1)
        self.other_fin = fin_stats_2(self.fin_data2)

    def get_hist_data(self,n_years):
        # n_years: Most recent history of n_years

        hist_data = {}

        c_list = self.c_df['ticker'].values
        c_year = self.c_df['r_year'].values

        for i,c in enumerate(c_list):

            c_b = self.finances.get_sheet(c,"balance_sheet")
            c_i = self.finances.get_sheet(c,"income_sheet")
            c_c = self.finances.get_sheet(c,"cashflow_sheet")
            c_o = self.other_fin.get_sheet(c)
            c_fin_stats = pd.concat([c_b,c_i,c_c,c_o])
            c_ratio = get_ratios(c_b,c_i,c_c)
            c_df = pd.concat([c_fin_stats,c_ratio])

            # select the last n_years data
            year = c_year[i]
            strt_year = year - n_years
            time_range  = range(strt_year,year+1)

            try:
                c_df = c_df[time_range]
                hist_data[c] = c_df
            except Exception as e:
                print e
                print("Data range requested %g to %g" %(strt_year,year))
                print("Data only available from %g" %c_df.columns.tolist()[0])
                print("\n")
                hist_data[c] = "No data"

        return hist_data


if __name__ == '__main__':

    brk_path = "D:\\FA\\report_13f\\brk\\13f_brk.csv"
    c = company_13f(brk_path)
    y_2016 = c.get_positive(2016)

    t_data = train_data(y_2016)

    inp_data_10 = t_data.get_hist_data(50)

    #print inp_data_10['AAPL']
