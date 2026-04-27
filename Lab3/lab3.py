import pandas as pd
from scipy import stats

# 1. 加载数据
file_path = 'WorldEnergy.csv'
df = pd.read_csv(file_path)

# 2. 筛选数据：2010-2020年间，新加坡、马来西亚和泰国
countries = ['Singapore', 'Malaysia', 'Thailand']
years = range(2010, 2021)

filtered_df = df[(df['country'].isin(countries)) & (df['year'].isin(years))]

# 3. 准备各国人均能源消耗量数据，并去除空值
sg_energy = filtered_df[filtered_df['country'] == 'Singapore']['energy_per_capita'].dropna()
my_energy = filtered_df[filtered_df['country'] == 'Malaysia']['energy_per_capita'].dropna()
th_energy = filtered_df[filtered_df['country'] == 'Thailand']['energy_per_capita'].dropna()

# 4. 计算并打印均值
print("--- Average energy consumption per capita from 2010 to 2020 ---")
print(f"新加坡 (Singapore): {sg_energy.mean():.2f}")
print(f"马来西亚 (Malaysia): {my_energy.mean():.2f}")
print(f"泰国 (Thailand):   {th_energy.mean():.2f}")
print("-" * 40)

# 5. 进行 ANOVA 方差分析
# 零假设 (H0): 三个国家的平均人均能源消耗量没有显著差异
# 备择假设 (H1): 至少有两个国家的平均值存在显著差异
f_stat, p_value = stats.f_oneway(sg_energy, my_energy, th_energy)

print("--- ANOVA results ---")
print(f"F统计量 (F-statistic): {f_stat:.4f}")
print(f"P值 (P-value):       {p_value:.4e}")

# 6. 结果解释
alpha = 0.05
if p_value < alpha:
    print("\nConclusion: At a significance level of 0.05, the null hypothesis is rejected.")
    print("There are significant differences in the average per capita energy consumption among these three countries.")
else:
    print("\nConclusion: At a significance level of 0.05, the null hypothesis cannot be rejected.")
    print("No significant differences were found in the average per capita energy consumption among the three countries.")