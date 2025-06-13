import streamlit as st
import pandas as pd
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import joblib
import os

# Download NLTK data if not already present
try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

try:
    nltk.data.find('corpora/wordnet')
except LookupError:
    nltk.download('wordnet')

# Initialize NLTK components
stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()

# Function to preprocess text
def preprocess_text(text):
    text = text.lower()  # Lowercasing
    text = re.sub(r'[^a-z\s]', '', text)  # Remove punctuation and numbers
    words = text.split()  # Tokenization
    words = [word for word in words if word not in stop_words]  # Remove stop words
    words = [lemmatizer.lemmatize(word) for word in words]  # Lemmatization
    return ' '.join(words)

# Load and train the model (in a real app, you'd load a pre-trained model)
@st.cache_data
def load_model():
    # Load the cleaned dataset
    df = pd.read_csv("both_train_cleaned.csv")
    df.dropna(subset=['cleaned_text', 'class_name'], inplace=True)
    
    # Feature Engineering: TF-IDF Vectorization
    tfidf_vectorizer = TfidfVectorizer(max_features=5000)
    X = tfidf_vectorizer.fit_transform(df["cleaned_text"])
    y = df["class_name"]
    
    # Train Logistic Regression model
    model = LogisticRegression(max_iter=1000, solver="liblinear")
    model.fit(X, y)
    
    return model, tfidf_vectorizer

# Streamlit app
def main():
    st.title("Mental Health Condition Predictor")
    st.write("This application analyzes journal-style text input to predict mental health conditions.")
    
    # Load model and vectorizer
    model, vectorizer = load_model()
    
    # Text input
    user_input = st.text_area("Enter your journal entry or text:", height=200)
    
    if st.button("Predict Mental Health Condition"):
        if user_input:
            # Preprocess the input text
            cleaned_input = preprocess_text(user_input)
            
            # Vectorize the input
            input_vector = vectorizer.transform([cleaned_input])
            
            # Make prediction
            prediction = model.predict(input_vector)[0]
            prediction_proba = model.predict_proba(input_vector)[0]
            
            # Display results
            st.subheader("Prediction Results")
            st.write(f"**Predicted Mental Health Condition:** {prediction}")
            
            # Display probabilities for all classes
            st.subheader("Prediction Probabilities")
            classes = model.classes_
            proba_df = pd.DataFrame({
                'Mental Health Condition': classes,
                'Probability': prediction_proba
            }).sort_values('Probability', ascending=False)
            
            st.bar_chart(proba_df.set_index('Mental Health Condition'))
            
            # Display disclaimer
            st.warning("⚠️ **Disclaimer:** This is a machine learning model for educational purposes only. It should not be used as a substitute for professional medical advice, diagnosis, or treatment. If you are experiencing mental health issues, please consult with a qualified healthcare professional.")
        else:
            st.error("Please enter some text to analyze.")
    
    # Additional information
    st.sidebar.header("About")
    st.sidebar.write("This application uses a Logistic Regression model trained on social media text data to predict mental health conditions including:")
    st.sidebar.write("- ADHD")
    st.sidebar.write("- Anxiety")
    st.sidebar.write("- Bipolar")
    st.sidebar.write("- Depression")
    st.sidebar.write("- PTSD")
    st.sidebar.write("- None (no specific condition)")
    
    st.sidebar.header("Model Performance")
    st.sidebar.write("**Accuracy:** 76.4%")
    st.sidebar.write("**Model Type:** Logistic Regression with TF-IDF features")

if __name__ == "__main__":
    main()

