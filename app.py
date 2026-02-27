import streamlit as st
import os
from google import genai
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

# --- Configuration ---
api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    st.error("Google API Key not found. Please create a .env file with GOOGLE_API_KEY='your_key'")
    st.stop()

try:
    # NEW SDK: Initialize the client
    client = genai.Client(api_key=api_key)
    
    # LATEST FREE MODEL: gemini-2.5-flash is the latest, fastest model available on the free tier
    model_id = 'gemini-2.5-flash' 
except Exception as e:
    st.error(f"Failed to configure Google AI Client: {e}")
    st.stop()


# --- Streamlit App UI ---
st.set_page_config(page_title="AI Fitness Planner", layout="wide")

st.title("💪 Personalized Workout & Diet Planner with AI")
st.write("Fill in your details below to generate a personalized fitness and diet plan tailored to your student lifestyle.")

st.markdown("---")

# --- User Inputs ---
st.subheader("Tell Me About Yourself")

col1, col2 = st.columns(2)

with col1:
    goal = st.selectbox("What is your primary fitness goal?", ('Lose Weight', 'Gain Muscle', 'Improve Cardiovascular Health', 'Maintain Current Fitness'))
    workout_days = st.slider("How many days a week can you work out?", 1, 7, 3)
    equipment = st.text_area("What workout equipment do you have access to?", "e.g., Dumbbells, resistance bands, yoga mat, or just bodyweight.")

with col2:
    diet_pref = st.selectbox("What are your dietary preferences?", ('No Preference', 'Vegetarian', 'Vegan', 'Pescatarian', 'Gluten-Free'))
    budget = st.selectbox("What is your approximate weekly budget for food?", ('Low (Budget-friendly)', 'Medium (Standard)', 'High (Flexible)'))
    allergies = st.text_input("List any food allergies or foods you dislike (comma-separated):", placeholder="e.g., Nuts, dairy, spicy food")


st.markdown("---")

generate_button = st.button("✨ Generate My Personalized Plan", use_container_width=True, type="primary")

st.markdown("---")


# --- Backend Logic ---
if generate_button:
    if not all([goal, workout_days, diet_pref, budget, equipment]):
        st.warning("Please fill in all the details above to get the best plan.")
    else:
        st.subheader("🚀 Here is Your AI-Generated Plan")

        prompt = f"""
        Act as an expert fitness and nutrition coach. Create a personalized workout and diet plan for a student with the following details:

        **1. Student's Profile:**
        - **Primary Goal:** {goal}
        - **Workout Frequency:** {workout_days} days per week.
        - **Available Equipment:** {equipment}
        - **Dietary Preference:** {diet_pref}
        - **Weekly Food Budget:** {budget}
        - **Allergies or Dislikes:** {allergies if allergies else "None specified"}

        **2. Your Task:**
        Generate a practical, effective, and budget-friendly plan that is easy for a student to follow. The output must be clearly structured with the following two sections:

        **- Workout Plan:**
          - Create a weekly schedule outlining the exercises for each of the {workout_days} workout days.
          - For each exercise, suggest a number of sets and reps.
          - The exercises should be suitable for the available equipment mentioned.

        **- Diet Plan:**
          - Provide a sample 3-day meal plan (Day 1, Day 2, Day 3).
          - Each day should include suggestions for Breakfast, Lunch, Dinner, and one or two healthy Snacks.
          - The meal plan MUST be budget-friendly and strictly adhere to the dietary preferences and allergies.
          - Offer simple and easy-to-prepare meal ideas.

        Please format the response using markdown for clarity and readability.
        """

        try:
            with st.spinner("🤖 Generating your personalized plan... This may take a moment."):
                # NEW SDK: Generating content
                response = client.models.generate_content(
                    model=model_id,
                    contents=prompt
                )
                st.markdown(response.text)
        except Exception as e:
            st.error(f"An error occurred while generating your plan: {e}")
