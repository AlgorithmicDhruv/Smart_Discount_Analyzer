import streamlit as st
import pickle
import numpy as np

# Load model and encoders
with open("model.pkl", "rb") as f:
    model = pickle.load(f)
with open("le_scheme.pkl", "rb") as f:
    le_scheme = pickle.load(f)
with open("le_cat.pkl", "rb") as f:
    le_cat = pickle.load(f)
with open("le_intent.pkl", "rb") as f:
    le_intent = pickle.load(f)

st.title("🧠 Smart Marketing Scheme Recommender")
st.write("Predict which discount schemes are least likely to trigger customer complaints.")

# User Inputs
product_category = st.selectbox("Select Product Category", le_cat.classes_)
discount_percent = st.slider("Select Discount Percent", 5, 60, 25)
purchase_intent = st.radio("Customer Intended to Buy?", le_intent.classes_)

# Check when to recommend
if st.button("🔍 Recommend Best Scheme"):
    risky_schemes = []
    safe_schemes = []

    for scheme in le_scheme.classes_:
        # Encode inputs
        scheme_enc = le_scheme.transform([scheme])[0]
        cat_enc = le_cat.transform([product_category])[0]
        intent_enc = le_intent.transform([purchase_intent])[0]

        features = np.array([[scheme_enc, cat_enc, discount_percent, intent_enc]])
        pred = model.predict(features)[0]

        if pred == -1:
            safe_schemes.append(scheme)
        else:
            risky_schemes.append(scheme)

    if safe_schemes:
        st.success(f"✅ Recommended schemes with lowest complaint risk: {safe_schemes}")
    else:
        st.warning(f"⚠️ No zero-complaint schemes found. Least risky options: {le_scheme.classes_}")
