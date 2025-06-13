# Mental Health Condition Predictor from Textual Journal Entries

## Project Overview

This project implements a machine learning model that analyzes journal-style text input to predict mental health conditions such as anxiety, depression, ADHD, bipolar disorder, PTSD, and stress levels. The project demonstrates the application of Natural Language Processing (NLP) and machine learning techniques to address real-world mental health challenges.

## Table of Contents

1. [Project Goals](#project-goals)
2. [Technical Stack](#technical-stack)
3. [Dataset](#dataset)
4. [Methodology](#methodology)
5. [Model Performance](#model-performance)
6. [Web Application](#web-application)
7. [Installation and Usage](#installation-and-usage)
8. [Results and Analysis](#results-and-analysis)
9. [Future Improvements](#future-improvements)
10. [Disclaimer](#disclaimer)

## Project Goals

- Build a machine learning model for mental health condition prediction
- Implement text preprocessing and feature engineering techniques
- Compare multiple machine learning approaches (traditional ML vs. deep learning)
- Deploy a user-friendly web application for real-time predictions
- Provide educational insights into mental health text analysis



## Technical Stack

### Programming Language
- **Python 3.11**: Core programming language for all components

### Machine Learning Libraries
- **scikit-learn**: Traditional machine learning algorithms (Logistic Regression, Naive Bayes)
- **TensorFlow/Keras**: Deep learning framework for LSTM implementation
- **pandas**: Data manipulation and analysis
- **numpy**: Numerical computing

### Natural Language Processing
- **NLTK**: Text preprocessing, tokenization, and linguistic analysis
- **scikit-learn TfidfVectorizer**: Text feature extraction

### Data Visualization
- **matplotlib**: Static plotting and visualization
- **seaborn**: Statistical data visualization

### Web Application
- **Streamlit**: Interactive web application framework

### Development Tools
- **Jupyter Notebooks**: Exploratory data analysis and prototyping
- **Git**: Version control

## Dataset

### Source
The project uses a curated dataset from GitHub containing social media text data labeled with mental health conditions. The dataset includes approximately 13,727 samples across six categories:

- **ADHD**: Attention Deficit Hyperactivity Disorder
- **Anxiety**: Anxiety disorders
- **Bipolar**: Bipolar disorder
- **Depression**: Major depressive disorder
- **PTSD**: Post-Traumatic Stress Disorder
- **None**: No specific mental health condition

### Data Characteristics
- **Format**: CSV file with text posts and corresponding labels
- **Text Source**: Social media posts and journal-style entries
- **Language**: English
- **Preprocessing**: Cleaned and tokenized text data


## Methodology

### 1. Data Collection and Environment Setup
- Downloaded and prepared mental health text dataset
- Set up Python environment with required libraries
- Configured development workspace

### 2. Data Preprocessing and Exploratory Data Analysis
- **Text Cleaning**: Removed punctuation, numbers, and special characters
- **Tokenization**: Split text into individual words
- **Stop Word Removal**: Eliminated common English stop words
- **Lemmatization**: Reduced words to their root forms
- **EDA**: Analyzed word frequencies and class distributions

### 3. Feature Engineering and Text Vectorization
- **TF-IDF Vectorization**: Converted text to numerical features
- **Feature Selection**: Limited to top 5,000 features for efficiency
- **Data Splitting**: 80% training, 20% testing with stratified sampling

### 4. Model Development and Training

#### Traditional Machine Learning Models
1. **Logistic Regression**
   - Solver: liblinear
   - Max iterations: 1,000
   - Multi-class classification approach

2. **Naive Bayes**
   - MultinomialNB implementation
   - Suitable for text classification tasks

#### Deep Learning Model
1. **LSTM (Long Short-Term Memory)**
   - Embedding dimension: 64
   - LSTM units: 64
   - Dropout: 0.5
   - Sequence length: 50 tokens
   - Vocabulary size: 5,000 words

### 5. Model Evaluation and Performance Analysis
- **Metrics**: Accuracy, Precision, Recall, F1-Score
- **Visualization**: Confusion matrices for each model
- **Comparison**: Performance analysis across all models


## Model Performance

### Performance Summary

| Model | Accuracy | F1-Score (Weighted) | Training Time |
|-------|----------|-------------------|---------------|
| **Logistic Regression** | **76.4%** | **0.76** | Fast |
| Naive Bayes | 72.5% | 0.73 | Fast |
| LSTM | 67.1% | 0.67 | Moderate |

### Best Performing Model: Logistic Regression

The Logistic Regression model achieved the highest performance with 76.4% accuracy. Detailed performance metrics:

#### Per-Class Performance
- **ADHD**: Precision: 0.79, Recall: 0.80, F1-Score: 0.80
- **Anxiety**: Precision: 0.73, Recall: 0.72, F1-Score: 0.73
- **Bipolar**: Precision: 0.78, Recall: 0.66, F1-Score: 0.72
- **Depression**: Precision: 0.64, Recall: 0.76, F1-Score: 0.70
- **None**: Precision: 0.84, Recall: 0.94, F1-Score: 0.88
- **PTSD**: Precision: 0.86, Recall: 0.73, F1-Score: 0.79

### Key Insights
1. **Best Performance**: "None" category (no mental health condition) achieved highest accuracy
2. **Challenging Classes**: Depression showed lower precision but higher recall
3. **Balanced Performance**: ADHD and PTSD demonstrated consistent precision-recall balance
4. **Traditional ML Advantage**: Logistic Regression outperformed deep learning approach

## Web Application

### Features
- **Real-time Prediction**: Instant mental health condition prediction from text input
- **Probability Visualization**: Interactive bar chart showing confidence levels
- **User-Friendly Interface**: Clean, intuitive Streamlit-based design
- **Educational Disclaimer**: Clear warnings about medical advice limitations

### Technical Implementation
- **Framework**: Streamlit for rapid web development
- **Model Integration**: Pre-trained Logistic Regression model
- **Text Processing**: Real-time preprocessing pipeline
- **Deployment**: Accessible via public URL

### Live Application
The web application is deployed and accessible at:
**https://8501-iamw199isqgzm3hagebtf-c22167d4.manusvm.computer**


## Installation and Usage

### Prerequisites
- Python 3.11 or higher
- pip package manager

### Installation Steps

1. **Clone the Repository**
   ```bash
   git clone https://github.com/d-rahul-10/Mental-Health-Condition-Predictor.git
   cd Mental-Health-Condition-Predictor

   ```

2. **Install Dependencies**
   ```bash
   pip install pandas numpy scikit-learn matplotlib seaborn nltk tensorflow streamlit
   ```

3. **Download NLTK Data**
   ```python
   import nltk
   nltk.download('stopwords')
   nltk.download('wordnet')
   ```

### Running the Application

#### Data Preprocessing
```bash
python preprocess_data.py
```

#### Model Training
```bash
# Train traditional ML models
python train_initial_models.py

# Train LSTM model
python train_lstm_model.py
```

#### Model Evaluation
```bash
python evaluate_models.py
```

#### Web Application
```bash
streamlit run app.py --server.port 8501 --server.address 0.0.0.0
```

### File Structure
```
mental_health_predictor/
├── app.py                          # Streamlit web application
├── preprocess_data.py              # Text preprocessing script
├── eda.py                          # Exploratory data analysis
├── vectorize_data.py               # Feature engineering
├── train_initial_models.py         # Traditional ML training
├── train_lstm_model.py             # Deep learning training
├── evaluate_models.py              # Model evaluation
├── both_train.csv                  # Original dataset
├── both_train_cleaned.csv          # Preprocessed dataset
├── lstm_model.h5                   # Trained LSTM model
├── X_train.npz, X_test.npz         # Vectorized features
├── y_train.csv, y_test.csv         # Labels
└── README.md                       # Project documentation
```


## Results and Analysis

### Model Comparison Analysis

#### Why Logistic Regression Outperformed Deep Learning
1. **Dataset Size**: With ~13,727 samples, traditional ML models often perform better than deep learning
2. **Feature Quality**: TF-IDF features captured relevant patterns effectively
3. **Overfitting Prevention**: Simpler models less prone to overfitting on limited data
4. **Training Efficiency**: Faster convergence and less computational overhead

#### Text Analysis Insights
- **Most Common Words**: "im", "like", "feel", "dont", "get" - indicating emotional expression
- **Class Distribution**: Relatively balanced across mental health conditions
- **Language Patterns**: Informal social media language with emotional indicators

#### Prediction Accuracy by Condition
1. **Highest Accuracy**: None (no condition) - 88% F1-score
2. **Moderate Accuracy**: ADHD, PTSD - ~75-80% F1-score
3. **Challenging Conditions**: Depression, Bipolar - ~70-72% F1-score

### Real-World Application Testing
The web application successfully demonstrated:
- **Accurate Predictions**: Correctly identified depression from symptom descriptions
- **Probability Confidence**: Clear visualization of prediction certainty
- **User Experience**: Intuitive interface for non-technical users

## Future Improvements

### Model Enhancement
1. **Advanced NLP Models**
   - Implement BERT or RoBERTa for better contextual understanding
   - Explore GPT-based models for improved text comprehension
   - Fine-tune pre-trained language models on mental health data

2. **Feature Engineering**
   - Add sentiment analysis features
   - Incorporate linguistic features (POS tags, dependency parsing)
   - Include temporal patterns and writing style analysis

3. **Data Augmentation**
   - Collect larger, more diverse datasets
   - Implement data augmentation techniques
   - Balance class distributions more effectively

### Application Features
1. **Enhanced User Interface**
   - Add user authentication and history tracking
   - Implement progressive web app (PWA) features
   - Create mobile-responsive design

2. **Additional Functionality**
   - Multi-language support
   - Severity level prediction
   - Personalized recommendations and resources

3. **Integration Capabilities**
   - API development for third-party integration
   - Database integration for user data storage
   - Real-time monitoring and analytics

### Ethical and Safety Improvements
1. **Bias Mitigation**
   - Analyze and reduce demographic biases
   - Implement fairness metrics and monitoring
   - Diverse dataset collection strategies

2. **Safety Features**
   - Crisis detection and intervention protocols
   - Professional referral system integration
   - Enhanced disclaimer and safety warnings


## Disclaimer

### Important Medical Disclaimer

⚠️ **CRITICAL NOTICE**: This application is designed for **educational and research purposes only**. It is **NOT** intended for medical diagnosis, treatment, or clinical decision-making.

### Limitations and Warnings

1. **Not a Medical Tool**
   - This model should never replace professional medical advice
   - Mental health conditions require proper clinical assessment
   - Seek qualified healthcare professionals for diagnosis and treatment

2. **Model Limitations**
   - 76.4% accuracy means 23.6% of predictions may be incorrect
   - Trained on social media data, not clinical assessments
   - May not generalize to all populations or contexts

3. **Ethical Considerations**
   - Potential for bias in training data
   - Privacy concerns with text analysis
   - Risk of stigmatization or misinterpretation

### Recommended Use Cases

✅ **Appropriate Uses:**
- Educational demonstrations of NLP techniques
- Research into text-based mental health indicators
- Academic projects and learning exercises
- Awareness building about mental health language patterns

❌ **Inappropriate Uses:**
- Clinical diagnosis or screening
- Treatment planning or medical decisions
- Insurance or employment decisions
- Any high-stakes decision-making

### If You Need Help

If you or someone you know is experiencing mental health challenges:

- **Emergency**: Contact local emergency services (911, 988 Suicide & Crisis Lifeline)
- **Professional Help**: Consult licensed mental health professionals
- **Resources**: National Alliance on Mental Illness (NAMI), Mental Health America
- **Crisis Support**: Crisis Text Line (Text HOME to 741741)

## Conclusion

This project successfully demonstrates the application of machine learning and natural language processing to mental health text analysis. The Logistic Regression model achieved 76.4% accuracy in predicting mental health conditions from journal-style text, outperforming both Naive Bayes and LSTM approaches.

The deployed web application provides an accessible interface for educational exploration of mental health text analysis while maintaining appropriate ethical boundaries through clear disclaimers and safety warnings.

This work contributes to the growing field of computational mental health while emphasizing the critical importance of professional medical care and ethical AI development practices.

---

**Project Developed by**: D.Rahul | AIML Student 
**Date**: June 2025  
**Technology Stack**: Python, scikit-learn, TensorFlow, Streamlit  
**License**: Educational Use Only


