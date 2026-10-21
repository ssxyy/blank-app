import streamlit as st
import requests

st.set_page_config(
    page_title="FitAgent AI",
    page_icon=" $",
    layout="wide"
)

st.title("FitAgent app")
st.caption("Your smart Fitness & nutrition assistant")

#User profile sidebar
with st.sidebar:
    st.header("User Profile")

    age = st.number_input(
        "Age",
        min_value=18,
        max_value=100,
        value=30
    )

    height=st.number_input(
        "Height(feet)",
           min_value=4.0,
           max_value=8.0,
           value=5.0

    )

    weight = st.number_input(
            "Weight(lb)",
            min_value=50,
            max_value=300,
            value=100
        )

    fitness_goal=st.selectbox(
        "Fitness Goal",
        [
            "General Fitness",
            "Weight Loss",
            "Build Muscle",
            "Fat Loss & Muscle Retention",
            "Maintain Weight"
        ]
    )

    dietary_preference = st.selectbox(
        "Dietary Preference",
        [
            "Balanced",
            "Vegetarian",
            "High Protein",
            "Mediterranean"
        ]
    )

    activity_level = st.selectbox(
        "Activity Level",
        [
            "Sedentary",
            "Lightly Active",
            "Moderately Active",
            "Very Active"
        ]
)


# Only show weight loss target when needed
target_weight = None
timeline_weeks = None

if fitness_goal == "Weight Loss":
    st.subheader("🎯 Weight Loss Target")

    target_weight = st.number_input(
        "Target Weight (lb)",
        min_value=25.0,
        max_value=300.0,
        value=60.0,
        step=0.5
    )

    timeline_weeks = st.number_input(
        "Target Timeline (weeks)",
        min_value=1,
        max_value=104,
        value=12
    )

    if target_weight >= weight:
        st.warning(
            "Target weight must be lower than current weight."
        )
    else:
        total_loss = weight - target_weight
        weekly_loss = total_loss / timeline_weeks

        st.write(f"Weight to lose: {total_loss:.1f} lb")
        st.write(
            f"Average weekly loss: {weekly_loss:.2f} lb/week"
        )



    activity_level=st.selectbox(
          "Ativity Level",
          [
              "Sedentary",
              "Lightly Active",
              "Moderately Active",
              "Very Active"
          ]
        )
    dietary_preference=st.selectbox(
        "Diet Preference",
        [
            "Balanced",
            "High Protein",
            "Vegetarian",
            "Mediterranean"
        ]
    )

    st.divider()
    st.success("Profile Ready!")
    st.caption(
        f"Age:{age} |"
        f"Weight:{weight} lb"
    )

tab1,tab2,tab3=st.tabs(["Dashboard","Nutrition Planner","AI Coach"])

with tab1:
    st.header("Fitness Dashboard")

    col1,col2,col3 =st.columns(3)

    with col1:
        st.metric("Age",age)

    with col2:
        st.metric("Weight",f"{weight} lb")
    with col3:
        st.metric("Height",f"{height} feet")

    st.subheader("Your Fitness Goals")

    st.write(f"Fitness Goal: {fitness_goal}")
    st.write(f"Activity Level: {activity_level}")
    st.write(f"Dietary Preference: {dietary_preference}")

with tab2:
    st.header("AI Nutrition Planner")
    st.write("Generate a personalized one-day meal plan"
             "based on your fitness profile")

    if st.button("Generate Meal Plan"):
        st.session_state.pop("meal_plan", None)
        profile = {
            "age": age,
            "height_feet": height,
            "weight_lb": weight,
            "fitness_goal": fitness_goal,
            "activity_level": activity_level,
            "dietary_preference": dietary_preference
        }
        if fitness_goal == "Weight Loss":
          
          if target_weight is None or timeline_weeks is None:
                st.error("Please set a weight loss target.")
                st.stop()

          if target_weight >= weight:
              st.error("Target weight must be lower than current weight.")
              st.stop()

          profile["target_weight_lb"] = target_weight
          profile["timeline_weeks"] = timeline_weeks

          assessment_response = requests.post(
                "http://127.0.0.1:8000/api/v1/fitness/assess-goal",
                json={
                    "current_weight_lb": weight,
                    "target_weight_lb": target_weight,
                    "timeline_weeks": timeline_weeks
                },
                timeout=15
            )
          st.write("Assessment Status:", assessment_response.status_code)

          if assessment_response.status_code != 200:
                st.error("Goal Assessment API Failed")
                st.json(assessment_response.json())
                st.stop()

          assessment = assessment_response.json()

          st.write("Assessment Response:")
          st.json(assessment)

          st.subheader("Weight Loss Goal Assessment")
          st.metric(
            "Average Weekly Loss",
            f"{assessment['weekly_loss_lb']} lb/week"
          )
          st.info(assessment["message"])

          if assessment["needs_review"]:
            st.warning(
                "Please adjust the timeline or seek "
                "individualized guidance before generating "
                "a weight-loss meal plan."
            )
            st.stop()

        with st.spinner("Generating your meal plan.."):
            try:
                response = requests.post(
                    "http://127.0.0.1:8000/api/v1/nutrition/meal-plan",
                    json=profile,
                    timeout=120
                )


                if response.status_code == 422:
                    st.error("Nutrition API Validation Failed")
                    st.json(response.json())
                    st.write("Request payload:")
                    st.json(profile)
                    st.stop()

                response.raise_for_status()
                st.session_state["meal_plan"] = response.json()
                st.success("Meal plan generated!")
            except requests.RequestException as e:
                st.error(f"Nutrition API error: {e}")

    if "meal_plan" in st.session_state:
                plan= st.session_state["meal_plan"]

                st.subheader("Daily Nutrition Summary")

                col1,col2 = st.columns(2)

                col1.metric(
                    "Daily Calories",
                    f"{plan['daily_calories']} kcal"
                )

                col2.metric(
                            "Daily Protein",
                            f"{plan['daily_protein_g']} g"
                                )
                st.subheader("Your Meal Plan")

                for meal in plan["meals"]:
                    with st.container(border=True):
                        st.subheader(meal["meal_name"])

                        st.write("Foods")

                        for food in meal["foods"]:
                            st.write(f"-{food}")

                        c1,c2,c3,c4 = st.columns(4)
                        c1.metric("Calories", meal["calories"])
                        c2.metric("Protein", f"{meal['protein_g']} g")
                        c3.metric("Carbs", f"{meal['carbs_g']} g")
                        c4.metric("Fat", f"{meal['fat_g']} g")
                st.caption(
                    "Nutrition values are AI-generated estimates "
                    "and are not a substitute for professional advice."
            )
                        
                
    with tab3:
        st.header("AI Coach")
        question=st.text_input("Ask your AI Coach",
                            placeholder="What should i eat after workout?")
        if st.button("Ask AI"):
         if question.strip():
            with st.spinner("AI is thinking"):
                try:
                    response=requests.post("http://127.0.0.1:8000/api/v1/fitness/chat",
                                            json={
                                                    "question": question,
                                                    "profile": {
                                                        "age": age,
                                                        "height_feet": height,
                                                        "weight_lb": weight,
                                                        "fitness_goal": fitness_goal,
                                                        "activity_level": activity_level,
                                                        "dietary_preference": dietary_preference
                                                    }
                                                },
                                            timeout=30
                            )
                    response.raise_for_status()
                    result=response.json()

                    st.success("Response received!")
                    st.write(result["answer"])

                    st.subheader("AI Performance Metrics")

                    col1,col2,col3 = st.columns(3)

                    col1.metric("Input Tokens",result["input_tokens"])
                    col2.metric("Output Tokens",result["output_tokens"])
                    col3.metric("Latency", f"{result['latency']}s")


                except requests.RequestException as e:
                    st.error(f"Backend API error:{e}")
        else:
            st.warning("Please enter a question.")
