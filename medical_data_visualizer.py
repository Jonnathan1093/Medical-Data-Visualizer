import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# Import data
df = pd.read_csv("./medical_examination.csv")

# Add column 'overweight'
df['overweight'] = (df["weight"] / ((df["height"] / 100) ** 2)) > 25
df['overweight'] = df['overweight'].astype(int)  # Convertir a 0 y 1

# Normalize 'cholesterol' and 'gluc'
df['cholesterol'] = df['cholesterol'].apply(lambda x: 0 if x == 1 else 1)
df['gluc'] = df['gluc'].apply(lambda x: 0 if x == 1 else 1)

# Function to draw the categorical graph
def draw_cat_plot():
# Create DataFrame for categorical chart using 'pd.melt'
    df_cat = df.melt(id_vars=["cardio"], value_vars=[
                     "cholesterol", "gluc", "smoke", "alco", "active", "overweight"])

# Group and reorder data for the chart
    df_cat = df_cat[["cardio", "variable", "value"]].value_counts().reset_index(name="total").sort_values("variable")

# Draw the categorical graph using seaborn
    cat_plot = sns.catplot(data=df_cat, x="variable", y="total",
                           hue="value", col="cardio", kind="bar")

# Get the graph figure
    fig = cat_plot.figure

# Label the y-axis as "total"
    cat_plot.set_axis_labels("variable", "total")

# Save the figure
    fig.savefig('catplot.png')
    return fig

# Function to draw the heat map
def draw_heat_map():
# Clear data
    df_heat = df[
        (df['ap_lo'] <= df['ap_hi']) &
        (df['height'] >= df['height'].quantile(0.025)) &
        (df['height'] <= df['height'].quantile(0.975)) &
        (df['weight'] >= df['weight'].quantile(0.025)) &
        (df['weight'] <= df['weight'].quantile(0.975))
    ]

# Calculate the correlation matrix
    corr = df_heat.corr()

# Generate a mask for the upper triangle
    mask = np.triu(np.ones_like(corr, dtype=bool))

# Configure the heat chart
    fig, ax = plt.subplots(figsize=(10, 8))
    
# Draw the heatmap with 'sns.heatmap()'
    sns.heatmap(data=corr, annot=True, fmt=".1f", mask=mask, cmap='coolwarm', cbar_kws={'shrink': 0.8})

# Save the figure
    fig.savefig('heatmap.png')
    return fig
