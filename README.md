# THREATVISION – Phishing URL Detection System

 1. About the Project

THREATVISION is a Machine Learning-based Phishing URL Detection System. It analyzes a website URL and predicts whether it is **Legitimate** or **Phishing**.

The main aim of this project is to help users identify suspicious URLs and reduce the risk of visiting potentially harmful websites.

2. Project Objectives

- Detect potentially suspicious URLs using Machine Learning.
- Analyze URL characteristics to identify phishing indicators.
- Classify URLs as Legitimate or Phishing.
- Provide a simple and user-friendly web interface.
- Display model evaluation metrics through a dashboard.

 3. Technologies Used

- **Programming Language:** Python
- **Machine Learning Algorithm:** Random Forest Classifier
- **Web Framework:** Streamlit
- **Data Processing:** Pandas
- **Machine Learning Library:** Scikit-learn
- **Model Storage:** Joblib
- **Dataset Format:** CSV

4. Dataset

We used a phishing website dataset containing **11,055 records and 31 columns**.

The dataset contains 30 URL-related features and one target column named `Result`.

- `Result = -1` represents Phishing.
- `Result = 1` represents Legitimate.

The dataset was prepared and cleaned before training the model.

5. Project Workflow

1. **Dataset Preparation:** Load and prepare the phishing website dataset.
2. **Feature Selection:** Select 9 URL-related features for the URL-only model.
3. **Data Splitting:** Split the dataset into training and testing sets using an 80:20 ratio.
4. **Model Training:** Train a Random Forest Classifier using the selected features.
5. **Model Evaluation:** Evaluate the model using accuracy, precision, recall and F1-score.
6. **URL Analysis:** Extract the selected features from a user-entered URL.
7. **Prediction:** Use the trained model to classify the URL.
8. **Web Dashboard:** Display the prediction and model evaluation metrics using Streamlit.

 6. Features Used by the URL-Only Model

The model uses these 9 features:

1. IP Address in URL
2. URL Length
3. URL Shortening Service
4. `@` Symbol in URL
5. Double Slash Redirecting
6. Prefix-Suffix in Domain
7. Number of Subdomains
8. Port Information
9. HTTPS Token in Hostname

These characteristics are extracted from the entered URL and passed to the trained model for prediction.

7. Machine Learning Model

We used the **Random Forest Classifier** algorithm.

Random Forest combines the predictions of multiple decision trees to make a classification. In our project, it learns patterns from labelled URL-related features and uses those patterns to predict whether a URL is legitimate or phishing.

 8. Model Evaluation Results

The URL-only model achieved the following results on the held-out test dataset:

| Metric | Score |
|---|---:|
| Accuracy | 74.17% |
| Precision | 83.67% |
| Recall | 66.61% |
| F1-score | 74.17% |

The dataset was split using an 80:20 ratio, with 2,211 records in the test set.

**Note:** These results represent performance on the held-out dataset. They do not guarantee that every real-world URL will be classified correctly.

 9. Web Application

The project includes a Streamlit dashboard where users can:

- Enter a URL for analysis.
- View the predicted classification.
- Inspect the extracted URL features.
- View the model's evaluation metrics.

The prediction depends on the features extracted from the entered URL and the patterns learned during training.

10. Project Structure

```text
Phishing URL Detection/
│
├── dataset/
│   ├── PhishingData.csv
│   └── phishingdata_clean.csv
│
├── models/
│   ├── random_forest_model.joblib
│   └── url_only_model.joblib
│
├── src/
│   ├── app.py
│   ├── prepare_dataset.py
│   ├── train_model.py
│   ├── train_url_model.py
│   ├── test_predict.py
│   └── url_analyzer.py
│
└── README.md
```

11. How to Run the Project

Step 1: Open the project folder

Open PowerShell in the project directory.

Step 2: Activate the virtual environment

```powershell
.\.venv\Scripts\Activate.ps1
```

 Step 3: Install dependencies

If a `requirements.txt` file is available:

```powershell
pip install -r requirements.txt
```

 Step 4: Run the Streamlit application

```powershell
python -m streamlit run src/app.py
```

Step 5: Open the dashboard

Open the local URL displayed in the terminal, usually:

```text
http://localhost:8501
```

Enter a URL in the dashboard and click the analysis button to view the prediction.

 12. Future Enhancements

- Improve model accuracy using additional URL features.
- Test the model on more diverse, independently labelled URLs.
- Integrate trusted threat intelligence sources.
- Add more detailed risk indicators and prediction explanations.
- Improve the dashboard and user experience.

13. Conclusion

THREATVISION demonstrates how Machine Learning can be used to analyze URL characteristics and classify URLs as potentially phishing or legitimate.

The project combines Python, a Random Forest Classifier, URL feature extraction and Streamlit to provide a simple web-based phishing URL detection system.

Disclaimer: This project is developed for educational purposes. Predictions may be incorrect, so users should not rely on the model alone to determine whether a website is safe.

