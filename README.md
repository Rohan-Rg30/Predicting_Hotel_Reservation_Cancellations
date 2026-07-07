# 🏨 Predicting Hotel Reservation Cancellations

Predict whether a hotel booking will be **cancelled** before it happens — using EDA, six ML models, SMOTE-based imbalance handling, hyperparameter tuning, and SHAP explainability.

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Rohan-Rg30/Predicting_Hotel_Reservation_Cancellations/blob/main/Notebook/Predicting_Hotel_Reservation_Cancellations.ipynb)

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white)](https://www.python.org/)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-ML-orange?logo=scikitlearn)](https://scikit-learn.org/)
[![XGBoost](https://img.shields.io/badge/XGBoost-boosting-green)](https://xgboost.readthedocs.io/)
![License](https://img.shields.io/badge/License-Proprietary-lightgrey)
[![Status](https://img.shields.io/badge/status-active-success)](https://github.com/Rg30/Predicting_Hotel_Reservation_Cancellations)

---

## 📌 Overview

Hotel cancellations disrupt revenue forecasting, room inventory, and staffing. This project builds a full, leakage-audited machine learning pipeline that predicts, at the time of booking, whether a reservation is likely to be **cancelled** or **honored** — so hotels can act early (e.g. overbook strategically, send targeted retention offers, or adjust pricing).

The notebook takes a dataset of **36,275 hotel bookings** and walks through the complete data-science lifecycle: exploratory analysis → preprocessing → class-imbalance correction → model benchmarking → hyperparameter tuning → explainability → an interactive prediction tool.

---

## 🎯 Key Results

Six models were benchmarked on a held-out, untouched 20% test set (**7,255 bookings**). The preprocessor, scaler, and SMOTETomek resampling were all fit **only on the training set** to avoid data leakage.

| Model | Accuracy | Precision | Recall | F1-Score | ROC-AUC |
|---|---|---|---|---|---|
| Logistic Regression | 0.7862 | 0.6446 | 0.7745 | 0.7036 | 0.8712 |
| Decision Tree | 0.8622 | 0.7703 | 0.8254 | 0.7969 | 0.9292 |
| **Random Forest** 🏆 | **0.9021** | **0.8591** | 0.8389 | **0.8489** | **0.9558** |
| Gradient Boosting | 0.8848 | 0.8305 | 0.8145 | 0.8224 | 0.9460 |
| XGBoost | 0.8805 | 0.8175 | 0.8178 | 0.8177 | 0.9448 |
| AdaBoost | 0.7989 | 0.6559 | 0.8124 | 0.7258 | 0.8783 |

**🏆 Best model: Random Forest** — 90.2% accuracy and 0.956 AUC on unseen data.

After `GridSearchCV` hyperparameter tuning (5-fold stratified CV, scored on ROC-AUC):

| Model | Best CV AUC | Best Parameters |
|---|---|---|
| Random Forest | **0.9812** | `n_estimators=500, max_depth=None, min_samples_leaf=1, class_weight='balanced'` |
| XGBoost | 0.9803 | `n_estimators=300, learning_rate=0.1, max_depth=7, subsample=0.8, colsample_bytree=1.0` |
| Gradient Boosting | 0.9792 | `n_estimators=300, learning_rate=0.1, max_depth=6, subsample=0.8` |
| Logistic Regression | 0.8703 | `C=10, penalty='l2', solver='lbfgs'` |

---

## 🧠 What This Project Demonstrates

- **Leakage-free ML pipeline** — train/test split happens *before* any preprocessing; encoder, scaler, and SMOTETomek are fit exclusively on training data, then verified with a dedicated leakage audit (duplicate-row checks, encoder/scaler scope checks).
- **Exploratory Data Analysis** — booking status distribution, monthly booking trends, lead-time analysis, market segment & room type breakdowns, loyalty/pricing patterns, and a full feature correlation heatmap.
- **Class imbalance handling** — `SMOTETomek` (combined over/under-sampling) applied only to the training fold.
- **Model benchmarking** — 6 algorithms (Logistic Regression, Decision Tree, Random Forest, Gradient Boosting, XGBoost, AdaBoost) compared on Accuracy, Precision, Recall, F1, and ROC-AUC.
- **Overfitting/underfitting diagnostics** — 5-fold stratified cross-validation with train/test gap analysis for every model.
- **Hyperparameter tuning** — exhaustive `GridSearchCV` search per model, scored on ROC-AUC.
- **Explainability** — SHAP `TreeExplainer` on the tuned Random Forest to surface which features drive cancellation risk.
- **Interactive prediction tool** — a CLI function (`predict_custom_reservation()`) that takes live reservation details and returns a cancellation prediction.

---

## 📂 Dataset

**Source:** [Hotel Reservations Dataset (Kaggle)](https://www.kaggle.com/datasets/ahsan81/hotel-reservations-classification-dataset)

| Property | Value |
|---|---|
| Rows | 36,275 bookings |
| Columns | 19 (18 features + target) |
| Target | `booking_status` → `Canceled` / `Not_Canceled` |
| Missing values | None |

**Feature groups:**
- **Stay details:** `no_of_adults`, `no_of_children`, `no_of_weekend_nights`, `no_of_week_nights`, `type_of_meal_plan`, `room_type_reserved`, `required_car_parking_space`
- **Booking behavior:** `lead_time`, `arrival_year`, `arrival_month`, `arrival_date`, `market_segment_type`, `no_of_special_requests`
- **Guest history:** `repeated_guest`, `no_of_previous_cancellations`, `no_of_previous_bookings_not_canceled`
- **Pricing:** `avg_price_per_room`

> Place `Hotel Reservations.csv` in the working directory (or Colab's `/content/`) before running the notebook — see [Setup](#-setup--usage) below.

---

## 🛠️ Tech Stack

| Category | Tools |
|---|---|
| Language | Python 3.10+ |
| Data handling | pandas, NumPy |
| Visualization | Matplotlib, Seaborn |
| ML models | scikit-learn, XGBoost |
| Imbalance handling | imbalanced-learn (SMOTETomek) |
| Explainability | SHAP |
| Environment | Jupyter / Google Colab |

---

## 📁 Repository Structure

```
.
├── Predicting_Hotel_Reservation_Cancellations.ipynb   # Full pipeline notebook
├── Hotel Reservations.csv                             # Dataset (add locally or via Kaggle)
├── README.md                                           # Project documentation
└── requirements.txt                                    # Python dependencies
```

---

## 🚀 Setup & Usage

### Option 1 — Run in Google Colab (recommended, zero setup)

1. Click the **"Open In Colab"** badge at the top of this README.
2. Upload `Hotel Reservations.csv` to the Colab session (`/content/`), or mount Google Drive.
3. Run all cells top to bottom (**Runtime → Run all**).

### Option 2 — Run locally

```bash
# 1. Clone the repository
git clone https://github.com/YOUR_USERNAME/YOUR_REPO.git
cd YOUR_REPO

# 2. Create a virtual environment (recommended)
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Launch Jupyter
jupyter notebook Predicting_Hotel_Reservation_Cancellations.ipynb
```

Make sure `Hotel Reservations.csv` is in the same directory as the notebook (or update the `pd.read_csv(...)` path in the "Load Dataset" cell).

---

## 📦 requirements.txt

```
numpy
pandas
matplotlib
seaborn
scikit-learn
xgboost
imbalanced-learn
shap
```

---

## 🔍 Notebook Walkthrough

| Section | What happens |
|---|---|
| 1. Install & Import Libraries | Loads all dependencies and sets a consistent color palette/style |
| 2. Load Dataset | Reads the CSV, checks shape, dtypes, missing values, target balance |
| 3. Exploratory Data Analysis | Booking status split, monthly trends, lead-time bins, market segment & room type, loyalty/pricing, correlation heatmap |
| 4. Model Training | Leak-free train/test split → encode → scale → SMOTETomek → train 6 baseline models |
| 5. Confusion Matrices & ROC-AUC | Visual comparison of model performance |
| 6. Cross-Validation | 5-fold stratified CV to check over/underfitting |
| 7. Hyperparameter Tuning | `GridSearchCV` per model, optimized for ROC-AUC |
| 8. Leakage & Validation Audit | Confirms no train/test contamination anywhere in the pipeline |
| 9. SHAP Explainability | Feature-importance and impact analysis for the tuned Random Forest |
| 10. Reservation Prediction System | Interactive function to score a brand-new hypothetical booking |

---

## 💡 Key Business Insights

- Longer **lead time** between booking and arrival correlates strongly with a higher cancellation rate.
- Bookings made through **Online** market segments cancel more often than **Corporate** or **Offline** channels.
- Guests with **more special requests** are less likely to cancel — a signal of stronger intent.
- **Repeated guests** and those with a clean cancellation history are markedly more reliable.
- **Room price** and **parking space requirement** both shift cancellation likelihood, as revealed by SHAP.

---

## 🗺️ Roadmap / Future Work

- [ ] Deploy the tuned Random Forest as a REST API (FastAPI/Flask)
- [ ] Build a lightweight Streamlit dashboard for hotel staff
- [ ] Add time-based/seasonal features and holiday flags
- [ ] Experiment with stacking/ensembling the top 3 models
- [ ] Model monitoring for drift as booking patterns change

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome. Feel free to check the [issues page](https://github.com/YOUR_USERNAME/YOUR_REPO/issues) or open a pull request.

## 📜 License

This project is licensed under the [MIT License](LICENSE).

## 🙋 Author

**Your Name** — [GitHub](https://github.com/YOUR_USERNAME) · [LinkedIn](https://linkedin.com)

---

<p align="center">⭐ If you found this project useful, consider giving it a star!</p>
