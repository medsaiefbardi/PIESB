# Base Étudiant Analysis

## **Project Overview**

**Title**: Analyse base étudiant\
**Objective**: Analyze and interpret student data using exploratory data analysis (EDA), clustering, visualizations, and predictive modeling to generate actionable insights.

---

## **Project Structure**

```
Projet Base-Etudiant/
├── data/
│   ├── raw/               # Original dataset
│   ├── processed/         # Cleaned and transformed data
│
├── scripts/               # Python scripts
│   ├── eda_preprocessing.py
│   ├── kmeans_clustering.py
│   ├── clustering_analysis.py
│   ├── visualizations.py
│   ├── main_program.py
│
├── outputs/               # Generated outputs
│   ├── eda_plots/         # Visualizations from EDA
│   ├── clustering_plots/  # Clustering visualizations
│
└── README.md              # Documentation file
```

---

## **Tasks Accomplished**

### **1. EDA and Data Preprocessing**

- **Objective**: Clean and prepare the dataset for analysis.
- **Steps Completed**:
  - Identified and handled missing values.
  - Removed duplicates and irrelevant columns (e.g., `score_final`).
  - Transformed and cleaned data, saved as `updated_cleaned_data.csv`.
- **Visualizations**:
  - Gender distribution.
  - Student distribution by `gouvernorat`.
  - Performance (`moy_bac`) by academic level.
  - Birth year trends.

### **2. Clustering**

- **Objective**: Group students into clusters based on key features.
- **Steps Completed**:
  - Applied K-Means clustering on features like `moy_bac`, `niveau_courant_et`, and `gouvernorat`.
  - Visualized clusters using PCA and interactive scatter plots.
  - Generated cluster summaries for insights.

### **3. Visualizations**

- **Objective**: Create presentation-ready visualizations.
- **Steps Completed**:
  - Generated bar charts, pie charts, and line plots for key insights.
  - Created interactive visualizations for better communication.

### **4. Main Program**

- **Objective**: Automate the entire pipeline.
- **Steps Completed**:
  - Developed `main_program.py` to sequentially run:
    - EDA and preprocessing.
    - Clustering.
    - Visualizations.
  - Integrated error handling and streamlined execution.

---

## **Next Steps**

### **1. Predictive Modeling**

- Define a problematic for analysis.
- Select relevant indicators (e.g., `moy_bac`, `resultat_annee_prec`, etc.).
- Test and compare models (e.g., Decision Trees, Logistic Regression).

### **2. Finalize Documentation**

- Update the README with:
  - Predictive modeling results.
  - Key insights and learnings.

### **3. Presentation Preparation**

- Create slides summarizing:
  - Project overview.
  - Visualizations and insights.
  - Clustering and predictive modeling results.

---

## **How to Run the Project**

1. Clone the repository:

   ```bash
   git clone <repository-link>
   cd Projet-Base-Etudiant
   ```

2. Set up the environment:

   ```bash
   pip install -r requirements.txt
   ```

3. Run the main program:

   ```bash
   python scripts/main_program.py
   ```

4. Check the outputs:

   - Processed data in `data/processed/`
   - Visualizations in `outputs/`

---

## **Authors and Acknowledgments**

**Author**: Skander Hassan\
**Acknowledgments**: Special thanks to Esprit School for providing the dataset and project guidelines.
