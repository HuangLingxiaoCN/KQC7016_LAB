import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 1. 加载数据
try:
    df = pd.read_csv('WorldEnergy.csv')
except FileNotFoundError:
    print("请确保 WorldEnergy.csv 文件在当前目录下。")
    exit()

# 设置绘图风格
sns.set_theme(style="whitegrid")
plt.rcParams['font.sans-serif'] = ['SimHei']  # 正常显示中文
plt.rcParams['axes.unicode_minus'] = False 

# --- 数据清洗与预处理 ---
# 筛选全球（World）数据，用于观察整体趋势
world_data = df[df['country'] == 'World'].sort_values('year')

# 筛选最近一年（2021或2022）的主要经济体数据进行对比
recent_year = df['year'].max()
top_countries = ['China', 'United States', 'India', 'Germany', 'Japan', 'Brazil']
comparison_df = df[(df['country'].isin(top_countries)) & (df['year'] == recent_year)]

# --- 图表 1: 全球电力结构演变 (化石燃料 vs 可再生能源) ---
plt.figure(figsize=(12, 6))
plt.plot(world_data['year'], world_data['fossil_share_elec'], label='Fossil energy share (%)', linewidth=2)
# 假设数据集中包含低碳能源或可再生能源占比，若无直接字段则可用 100 - fossil_share
if 'renewables_share_elec' in world_data.columns:
    plt.plot(world_data['year'], world_data['renewables_share_elec'], label='Renewable energy share (%)', linewidth=2)
else:
    plt.plot(world_data['year'], 100 - world_data['fossil_share_elec'], label='Non-fossil energy share (%)', linestyle='--')

plt.title('Evolution of Global Electricity (1900 - 2022)', fontsize=15)
plt.xlabel('Year')
plt.ylabel('Percentage (%)')
plt.legend()
plt.grid(True, alpha=0.3)
plt.show()

# --- 图表 2: 人均能源消耗与人均 GDP 的关系 (散点图) ---
# 选取 2018 年的数据（避免近年异常波动），并剔除空值
scatter_df = df[df['year'] == 2018].dropna(subset=['gdp', 'energy_per_capita', 'population'])
# 计算人均 GDP
scatter_df['gdp_per_capita'] = scatter_df['gdp'] / scatter_df['population']

plt.figure(figsize=(10, 6))
sns.scatterplot(data=scatter_df, x='gdp_per_capita', y='energy_per_capita', 
                size='population', sizes=(20, 1000), alpha=0.6, hue='gdp_per_capita', palette='viridis')

plt.title('GDP per capita and energy consumption per capita in 2018', fontsize=15)
plt.xlabel('GDP per capita (purchasing power parity)')
plt.ylabel('Energy consumption per capita (kWh)')
plt.xscale('log') # 使用对数刻度更清晰
plt.yscale('log')
plt.show()

# --- 图表 3: 主要经济体电力来源对比 (柱状图) ---
fuel_types = ['coal_share_elec', 'gas_share_elec', 'biofuel_share_elec']
# 检查是否存在这些列
available_fuels = [f for f in fuel_types if f in comparison_df.columns]

comparison_melted = comparison_df.melt(id_vars='country', value_vars=available_fuels, 
                                      var_name='能源类型', value_name='占比')

plt.figure(figsize=(12, 6))
sns.barplot(data=comparison_melted, x='country', y='占比', hue='能源类型')
plt.title(f'Electricity Sources by major economies in {recent_year}', fontsize=15)
plt.xlabel('Country')
plt.ylabel('Percentage (%)')
plt.xticks(rotation=45)
plt.legend(title='Fuel Type')
plt.tight_layout()
plt.show()