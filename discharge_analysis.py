import pandas as pd


#from XXXX import XXFunction
from plot_discharge import plot_discharge
from plot_result import plot_q_return_period, plot_q_freq

# load data
df = pd.read_csv("flow-data/daily-flow-series.csv",
                 header=36,
                 sep=";",
                 names=["Date", "Q (CMS)"],
                 usecols=[0, 2],
                 parse_dates=[0],
                 index_col="Date")
print(df.head())

 # Plot the Data
from plot_discharge import plot_discharge
plot_discharge(df.index, df["Q (CMS)"], title="Daily Flows 1826 - 2016")

## Construct Series of Annual Maximum Discharge
#Callculate the maximum Discharge
annual_max_df = df.resample(rule="A", kind="period").max()

#Definiiton of time und Ausgabe der maximalen Jahre
annual_max_df["year"] = annual_max_df.index.year
annual_max_df.reset_index(inplace=True, drop=True)
print(annual_max_df.head())


##Calculate Exceedance Probability and Recurrence Intervals
#Sort the velues
annual_max_df_sorted = annual_max_df.sort_values(by="Q (CMS)")

#
n = annual_max_df_sorted.shape[0]
annual_max_df_sorted.insert(0, "rank", range(1, 1 + n))

#
annual_max_df_sorted["pr"] = (n - annual_max_df_sorted["rank"] + 1) / (n + 1)

annual_max_df_sorted["return-period"] = 1 / annual_max_df_sorted["pr"]

print(annual_max_df_sorted.tail())

plot_q_freq(annual_max_df_sorted)
plot_q_return_period(annual_max_df_sorted)
