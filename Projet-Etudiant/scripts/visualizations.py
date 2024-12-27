# Refactored Visualization Notebook

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import os

# Path to the cleaned dataset
CLEANED_DATA_PATH = (
    "C:/Users/Skander/Desktop/Projet-Etudiant/data/processed/updated_cleaned_data.csv"
)
VISUALIZATION_OUTPUT_PATH = "../outputs/visualizations"
os.makedirs(VISUALIZATION_OUTPUT_PATH, exist_ok=True)


# Load the dataset
def load_data():
    try:
        data = pd.read_csv(CLEANED_DATA_PATH)
        print("Dataset loaded successfully!")
        return data
    except FileNotFoundError:
        print(f"Error: File not found at {CLEANED_DATA_PATH}")
        return None


# Save plots
def save_plot(output_path):
    plt.savefig(output_path)
    print(f"Plot saved to {output_path}")


# 1. Gender Distribution


def plot_gender_distribution(data):
    sex_counts = data["sexe"].value_counts()
    fig = px.pie(
        names=sex_counts.index,
        values=sex_counts.values,
        title="Gender Distribution",
        labels={"names": "Gender", "values": "Count"},
    )
    fig.update_traces(
        hovertemplate="Gender: %{label}<br>Count: %{value}<br>Percentage: %{percent}"
    )
    fig.show()


# 2. Gouvernorat Distribution


def plot_gouvernorat_distribution(data):
    filtered_data = data[data["gouvernorat"] != "Inconnu"]
    gouvernorat_counts = filtered_data["gouvernorat"].value_counts()
    fig = px.bar(
        x=gouvernorat_counts.values,
        y=gouvernorat_counts.index,
        orientation="h",
        title="Student Distribution by Gouvernorat (Excluding Inconnu)",
        labels={"x": "Student Count", "y": "Gouvernorat"},
        color=gouvernorat_counts.values,
        color_continuous_scale="Viridis",
    )
    fig.update_traces(hovertemplate="Gouvernorat: %{y}<br>Student Count: %{x}")
    fig.show()


# 3. Performance by Academic Level


def plot_performance_by_academic_level(data):
    filtered_data = data[data["moy_bac"] <= 20]
    bins = [10, 12, 14, 16, 18, 20]
    labels = ["10-12", "12-14", "14-16", "16-18", "18-20"]
    filtered_data["moy_bac_range"] = pd.cut(
        filtered_data["moy_bac"], bins=bins, labels=labels, include_lowest=True
    )
    moy_bac_counts = filtered_data["moy_bac_range"].value_counts().sort_index()

    plt.figure(figsize=(10, 6))
    bar_plot = sns.barplot(
        x=moy_bac_counts.index, y=moy_bac_counts.values, palette="coolwarm"
    )
    for index, value in enumerate(moy_bac_counts.values):
        plt.text(index, value + 1, str(value), ha="center", fontsize=10, color="black")
    plt.title("Student Count by Moy Bac Range", fontsize=14)
    plt.xlabel("Moy Bac Range", fontsize=12)
    plt.ylabel("Student Count", fontsize=12)
    plt.tight_layout()
    save_plot(
        os.path.join(VISUALIZATION_OUTPUT_PATH, "student_count_by_moy_bac_range.png")
    )
    plt.show()


# 4. Average Moy Bac by Gender


def plot_average_moy_bac_by_gender(data):
    filtered_data = data[data["moy_bac"] <= 20]
    mean_moy_bac = filtered_data.groupby("sexe")["moy_bac"].mean().reset_index()

    plt.figure(figsize=(10, 6))
    sns.barplot(x="sexe", y="moy_bac", data=mean_moy_bac, palette="coolwarm")
    plt.title("Average Moy Bac by Gender", fontsize=14)
    plt.xlabel("Sexe", fontsize=12)
    plt.ylabel("Average Moy Bac", fontsize=12)
    plt.tight_layout()
    save_plot(os.path.join(VISUALIZATION_OUTPUT_PATH, "average_moy_bac_by_gender.png"))
    plt.show()


# 5. Distribution of Birth Years


def plot_birth_year_distribution(data):
    data["date_nais_et"] = pd.to_datetime(data["date_nais_et"], errors="coerce")
    data["birth_year"] = data["date_nais_et"].dt.year
    filtered_data = data.dropna(subset=["birth_year"])

    plt.figure(figsize=(10, 6))
    sns.histplot(filtered_data["birth_year"], bins=20, kde=False, color="blue")
    plt.title("Distribution of Birth Years", fontsize=14)
    plt.xlabel("Birth Year", fontsize=12)
    plt.ylabel("Student Count", fontsize=12)
    plt.tight_layout()
    save_plot(os.path.join(VISUALIZATION_OUTPUT_PATH, "birth_year_distribution.png"))
    plt.show()


# 6. Number of Students Born Per Year


def plot_students_born_per_year(data):
    data["date_nais_et"] = pd.to_datetime(data["date_nais_et"], errors="coerce")
    data["birth_year"] = data["date_nais_et"].dt.year
    filtered_data = data.dropna(subset=["birth_year"])
    birth_year_counts = (
        filtered_data["birth_year"].value_counts().sort_index(ascending=False)
    )

    fig = px.line(
        x=birth_year_counts.index,
        y=birth_year_counts.values,
        labels={"x": "Birth Year", "y": "Student Count"},
        title="Trend of Students Born Per Year",
        markers=True,
    )
    fig.update_traces(hovertemplate="Year: %{x}<br>Count: %{y}")
    fig.update_layout(xaxis=dict(autorange="reversed"))
    fig.show()


if __name__ == "__main__":
    data = load_data()
    if data is not None:
        plot_gender_distribution(data)
        plot_gouvernorat_distribution(data)
        plot_performance_by_academic_level(data)
        plot_average_moy_bac_by_gender(data)
        plot_birth_year_distribution(data)
        plot_students_born_per_year(data)
        print("All visualizations completed and saved.")
