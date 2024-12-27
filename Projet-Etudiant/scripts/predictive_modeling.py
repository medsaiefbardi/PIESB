import os
import logging
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.metrics import accuracy_score, mean_squared_error, r2_score
import matplotlib.pyplot as plt
import seaborn as sns

# Paths
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CLEANED_DATA_PATH = os.path.join(
    PROJECT_ROOT, "data", "processed", "updated_cleaned_data.csv"
)
OUTPUT_PATH = os.path.join(PROJECT_ROOT, "outputs", "feature_importance_analysis")

# Create necessary directories
os.makedirs(OUTPUT_PATH, exist_ok=True)

# Logging setup
logging.basicConfig(
    filename=os.path.join(OUTPUT_PATH, "feature_importance.log"),
    level=logging.INFO,
    format="%(asctime)s - %(message)s",
)

# Load dataset
logging.info("Loading dataset...")
data = pd.read_csv(CLEANED_DATA_PATH)

# Preprocess dataset
logging.info("Preprocessing dataset...")
data = data.dropna()  # Drop rows with missing values for simplicity

# Select relevant features and targets
features = ["niveau_courant_et", "gouvernorat", "sexe", "classe_prec_et"]
target_class = "resultat_annee_prec"  # Classification target
target_reg = "moy_bac"  # Regression target

X = data[features]
y_classification = data[target_class]
y_regression = data[target_reg]

# Encode categorical variables
categorical_features = ["gouvernorat", "sexe", "classe_prec_et"]
numerical_features = ["niveau_courant_et"]

preprocessor = ColumnTransformer(
    transformers=[
        (
            "num",
            StandardScaler(with_mean=False),
            numerical_features,
        ),  # Fix for sparse matrices
        ("cat", OneHotEncoder(), categorical_features),
    ]
)

X = preprocessor.fit_transform(X)

# Split the data
X_train, X_test, y_class_train, y_class_test = train_test_split(
    X, y_classification, test_size=0.2, random_state=42
)
_, _, y_reg_train, y_reg_test = train_test_split(
    X, y_regression, test_size=0.2, random_state=42
)

# Logistic Regression Feature Importance
logging.info("Analyzing feature importance from Logistic Regression...")
log_reg = LogisticRegression(max_iter=1000)
log_reg.fit(X_train, y_class_train)

# Get feature importance from Logistic Regression
coefficients = log_reg.coef_[0]
feature_names = preprocessor.get_feature_names_out()
log_reg_importances = pd.DataFrame(
    {"Feature": feature_names, "Importance": coefficients}
).sort_values(by="Importance", key=abs, ascending=False)

# Save and visualize
log_reg_importances.to_csv(
    os.path.join(OUTPUT_PATH, "logistic_regression_importances.csv"), index=False
)
plt.figure(figsize=(10, 6))
sns.barplot(
    data=log_reg_importances.head(10), x="Importance", y="Feature", palette="coolwarm"
)
plt.title("Top Features (Logistic Regression)")
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_PATH, "logistic_regression_importances.png"))
plt.show()

# Random Forest Classifier Feature Importance
logging.info("Analyzing feature importance from Random Forest Classifier...")
rf_classifier = RandomForestClassifier(n_estimators=100, random_state=42)
rf_classifier.fit(X_train, y_class_train)
rf_importances = pd.DataFrame(
    {
        "Feature": feature_names,
        "Importance": rf_classifier.feature_importances_,
    }
).sort_values(by="Importance", ascending=False)

# Save and visualize
rf_importances.to_csv(
    os.path.join(OUTPUT_PATH, "rf_classifier_importances.csv"), index=False
)
plt.figure(figsize=(10, 6))
sns.barplot(
    data=rf_importances.head(10), x="Importance", y="Feature", palette="viridis"
)
plt.title("Top Features (Random Forest Classifier)")
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_PATH, "rf_classifier_importances.png"))
plt.show()

# Random Forest Regressor Feature Importance
logging.info("Analyzing feature importance from Random Forest Regressor...")
rf_regressor = RandomForestRegressor(n_estimators=100, random_state=42)
rf_regressor.fit(X_train, y_reg_train)
rf_reg_importances = pd.DataFrame(
    {
        "Feature": feature_names,
        "Importance": rf_regressor.feature_importances_,
    }
).sort_values(by="Importance", ascending=False)

# Save and visualize
rf_reg_importances.to_csv(
    os.path.join(OUTPUT_PATH, "rf_regressor_importances.csv"), index=False
)
plt.figure(figsize=(10, 6))
sns.barplot(
    data=rf_reg_importances.head(10), x="Importance", y="Feature", palette="magma"
)
plt.title("Top Features (Random Forest Regressor)")
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_PATH, "rf_regressor_importances.png"))
plt.show()

# Correlation with Regression Target
logging.info("Analyzing correlation with regression target...")
X_df = pd.DataFrame(X.toarray(), columns=feature_names)
correlations = X_df.corrwith(pd.Series(y_regression)).sort_values(ascending=False)
correlations.to_csv(os.path.join(OUTPUT_PATH, "correlation_with_regression_target.csv"))

plt.figure(figsize=(10, 6))
sns.barplot(
    x=correlations.head(10).values, y=correlations.head(10).index, palette="cool"
)
plt.title("Top Correlations with Moy Bac")
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_PATH, "correlation_with_moy_bac.png"))
plt.show()

logging.info("Feature importance analysis completed. Results saved.")
print("Feature importance analysis completed. Check outputs for details.")
