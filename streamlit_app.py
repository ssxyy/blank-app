import csv
import io
import os
from datetime import date, timedelta

import requests
import streamlit as st

API_BASE_URL = os.getenv(
    "API_BASE_URL",
    "http://127.0.0.1:8000"
)

MUSCLE_GROUPS = ["Chest", "Back", "Shoulders", "Arms", "Legs", "Core"]
SESSION_TYPES = ["Strength", "Cardio", "Conditioning", "Mobility"]
DEFAULT_DAYS_BY_ACTIVITY = {
    "Sedentary": 3,
    "Lightly Active": 3,
    "Moderately Active": 4,
    "Very Active": 5,
}

st.set_page_config(
    page_title="FitAgent AI",
    page_icon="💪",
    layout="wide"
)

if "workout_log" not in st.session_state:
    st.session_state["workout_log"] = []

st.title("FitAgent app")
st.caption("Your smart Fitness & nutrition assistant")

with st.sidebar:
    st.header("User Profile")

    age = st.number_input(
        "Age",
        min_value=18,
        max_value=100,
        value=30
    )

    height = st.number_input(
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

    fitness_goal = st.selectbox(
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

    st.divider()
    st.subheader("Training Preferences")

    experience = st.selectbox(
        "Training Experience",
        ["Beginner", "Intermediate", "Advanced"]
    )

    equipment = st.selectbox(
        "Equipment",
        ["Full Gym", "Dumbbells Only", "Bodyweight"]
    )

    days_per_week = st.slider(
        "Workout days per week",
        min_value=2,
        max_value=6,
        value=DEFAULT_DAYS_BY_ACTIVITY.get(activity_level, 3),
        help="Defaults from your activity level; adjust as you like."
    )

    st.divider()
    st.success("Profile Ready!")
    st.caption(
        f"Age: {age} | "
        f"Weight: {weight} lb"
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


def build_profile() -> dict:
    profile = {
        "age": age,
        "height_feet": height,
        "weight_lb": weight,
        "fitness_goal": fitness_goal,
        "activity_level": activity_level,
        "dietary_preference": dietary_preference
    }
    if fitness_goal == "Weight Loss":
        profile["target_weight_lb"] = target_weight
        profile["timeline_weeks"] = timeline_weeks
    return profile


def check_weight_loss_goal() -> bool:
    if fitness_goal != "Weight Loss":
        return True

    if target_weight is None or timeline_weeks is None:
        st.error("Please set a weight loss target.")
        return False

    if target_weight >= weight:
        st.error("Target weight must be lower than current weight.")
        return False

    try:
        assessment_response = requests.post(
            f"{API_BASE_URL}/api/v1/fitness/assess-goal",
            json={
                "current_weight_lb": weight,
                "target_weight_lb": target_weight,
                "timeline_weeks": timeline_weeks
            },
            timeout=15
        )
    except requests.RequestException as e:
        st.error(f"Goal Assessment API error: {e}")
        return False

    if assessment_response.status_code != 200:
        st.error("Goal Assessment API Failed")
        st.json(assessment_response.json())
        return False

    assessment = assessment_response.json()

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
        return False
    return True


def render_meals(meals: list[dict]) -> None:
    for meal in meals:
        with st.container(border=True):
            st.subheader(meal["meal_name"])

            st.write("Foods")

            for food in meal["foods"]:
                st.write(f"- {food}")

            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Calories", meal["calories"])
            c2.metric("Protein", f"{meal['protein_g']} g")
            c3.metric("Carbs", f"{meal['carbs_g']} g")
            c4.metric("Fat", f"{meal['fat_g']} g")


def meal_plan_markdown(plan: dict) -> str:
    lines = [
        f"# {plan['plan_days']}-Day Meal Plan",
        "",
        f"Daily target: ~{plan['target_daily_calories']} kcal, "
        f"{plan['target_daily_protein_g']} g protein",
        "",
    ]
    for day in plan["days"]:
        lines.append(
            f"## {day['day']} ({day['daily_calories']} kcal, "
            f"{day['daily_protein_g']} g protein)"
        )
        for meal in day["meals"]:
            lines.append(
                f"### {meal['meal_name']} - {meal['calories']} kcal "
                f"(P {meal['protein_g']}g / C {meal['carbs_g']}g / "
                f"F {meal['fat_g']}g)"
            )
            lines += [f"- {food}" for food in meal["foods"]]
        lines.append("")
    lines.append("## Grocery List")
    lines += [f"- [ ] {item}" for item in plan["grocery_list"]]
    lines.append("")
    lines.append("## Meal Prep Tips")
    lines += [f"- {tip}" for tip in plan["prep_tips"]]
    return "\n".join(lines)


def add_log_entry(log_date, session_type, muscle_groups, rpe, duration):
    st.session_state["workout_log"].append({
        "date": log_date.isoformat() if hasattr(log_date, "isoformat")
        else str(log_date),
        "session_type": session_type,
        "muscle_groups": list(muscle_groups),
        "rpe": int(rpe),
        "duration_min": int(duration),
    })
    st.session_state["workout_log"].sort(key=lambda e: e["date"])
    st.session_state.pop("strength_check", None)


def strength_sessions_this_week() -> int:
    today = date.today()
    week_start = today - timedelta(days=today.weekday())
    return len({
        e["date"] for e in st.session_state["workout_log"]
        if e["session_type"] == "Strength"
        and week_start.isoformat() <= e["date"] <= today.isoformat()
    })


def log_to_csv(log: list[dict]) -> str:
    buffer = io.StringIO()
    writer = csv.DictWriter(
        buffer,
        fieldnames=["date", "session_type", "muscle_groups",
                    "rpe", "duration_min"]
    )
    writer.writeheader()
    for e in log:
        writer.writerow({**e, "muscle_groups": ";".join(e["muscle_groups"])})
    return buffer.getvalue()


def csv_to_log(text: str) -> list[dict]:
    entries = []
    for row in csv.DictReader(io.StringIO(text)):
        groups = [
            g.strip() for g in (row.get("muscle_groups") or "").split(";")
            if g.strip() in MUSCLE_GROUPS
        ]
        entries.append({
            "date": date.fromisoformat(row["date"].strip()).isoformat(),
            "session_type": row.get("session_type", "Strength").strip()
            or "Strength",
            "muscle_groups": groups,
            "rpe": int(float(row.get("rpe") or 7)),
            "duration_min": int(float(row.get("duration_min") or 45)),
        })
    return sorted(entries, key=lambda e: e["date"])


tab1, tab2, tab3, tab4 = st.tabs(
    ["Dashboard", "Nutrition Planner", "Workout Planner", "AI Coach"]
)

with tab1:
    st.header("Fitness Dashboard")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Age", age)

    with col2:
        st.metric("Weight", f"{weight} lb")
    with col3:
        st.metric("Height", f"{height} feet")

    st.subheader("Your Fitness Goals")

    st.write(f"Fitness Goal: {fitness_goal}")
    st.write(f"Activity Level: {activity_level}")
    st.write(f"Dietary Preference: {dietary_preference}")
    st.write(
        f"Training: {experience}, {equipment}, "
        f"{days_per_week} days/week"
    )

    st.subheader("This Week")
    d1, d2 = st.columns(2)
    d1.metric("Strength sessions logged", strength_sessions_this_week())
    d2.metric("Total workouts logged", len(st.session_state["workout_log"]))

    if "strength_check" in st.session_state:
        st.info(
            f"AI Coach: **{st.session_state['strength_check']['recommendation']}**"
        )

with tab2:
    st.header("AI Nutrition Planner")
    st.write("Generate a personalized meal plan "
             "based on your fitness profile")

    plan_length = st.radio(
        "Plan length",
        ["1 day", "3 days", "7 days"],
        horizontal=True
    )
    plan_days = int(plan_length.split()[0])

    if st.button("Generate Meal Plan"):
        st.session_state.pop("meal_plan", None)
        st.session_state.pop("multi_day_plan", None)
        profile = build_profile()

        if check_weight_loss_goal():
            spinner_text = (
                "Generating your meal plan.." if plan_days == 1
                else f"Generating your {plan_days}-day meal plan "
                     "(this can take up to a minute).."
            )
            with st.spinner(spinner_text):
                try:
                    if plan_days == 1:
                        response = requests.post(
                            f"{API_BASE_URL}/api/v1/nutrition/meal-plan",
                            json=profile,
                            timeout=120
                        )
                    else:
                        response = requests.post(
                            f"{API_BASE_URL}/api/v1/nutrition/"
                            "meal-plan/multi-day",
                            json={**profile, "days": plan_days},
                            timeout=300
                        )

                    if response.status_code == 422:
                        st.error("Nutrition API Validation Failed")
                        st.json(response.json())
                        st.write("Request payload:")
                        st.json(profile)
                    else:
                        response.raise_for_status()
                        key = "meal_plan" if plan_days == 1 \
                            else "multi_day_plan"
                        st.session_state[key] = response.json()
                        st.success("Meal plan generated!")
                except requests.RequestException as e:
                    st.error(f"Nutrition API error: {e}")

    if "meal_plan" in st.session_state:
        plan = st.session_state["meal_plan"]

        st.subheader("Daily Nutrition Summary")

        col1, col2 = st.columns(2)

        col1.metric(
            "Daily Calories",
            f"{plan['daily_calories']} kcal"
        )

        col2.metric(
            "Daily Protein",
            f"{plan['daily_protein_g']} g"
        )
        st.subheader("Your Meal Plan")
        render_meals(plan["meals"])

    if "multi_day_plan" in st.session_state:
        plan = st.session_state["multi_day_plan"]
        n_days = plan["plan_days"]
        avg_cal = round(
            sum(d["daily_calories"] for d in plan["days"]) / n_days
        )
        avg_protein = round(
            sum(d["daily_protein_g"] for d in plan["days"]) / n_days, 1
        )

        st.subheader(f"{n_days}-Day Nutrition Summary")
        c1, c2, c3 = st.columns(3)
        c1.metric("Daily Target", f"{plan['target_daily_calories']} kcal")
        c2.metric("Average Calories", f"{avg_cal} kcal")
        c3.metric("Average Protein", f"{avg_protein} g")

        day_tabs = st.tabs([d["day"] for d in plan["days"]])
        for day_tab, day in zip(day_tabs, plan["days"]):
            with day_tab:
                m1, m2 = st.columns(2)
                m1.metric("Calories", f"{day['daily_calories']} kcal")
                m2.metric("Protein", f"{day['daily_protein_g']} g")
                render_meals(day["meals"])

        with st.expander("🛒 Grocery List", expanded=True):
            for item in plan["grocery_list"]:
                st.checkbox(item, key=f"grocery_{item}")

        with st.expander("🍱 Meal Prep Tips"):
            for tip in plan["prep_tips"]:
                st.write(f"- {tip}")

        st.download_button(
            "Download meal plan (Markdown)",
            data=meal_plan_markdown(plan),
            file_name=f"meal_plan_{n_days}_days.md",
            mime="text/markdown"
        )

    if "meal_plan" in st.session_state or \
            "multi_day_plan" in st.session_state:
        st.caption(
            "Nutrition values are AI-generated estimates "
            "and are not a substitute for professional advice."
        )

with tab3:
    st.header("Workout Planner")
    st.write(
        f"A weekly plan built for **{fitness_goal}** - "
        f"{days_per_week} days/week, {experience.lower()}, "
        f"{equipment.lower()}. Change these in the sidebar."
    )

    if st.button("Generate Workout Plan"):
        try:
            response = requests.post(
                f"{API_BASE_URL}/api/v1/workout/plan",
                json={
                    "fitness_goal": fitness_goal,
                    "activity_level": activity_level,
                    "days_per_week": days_per_week,
                    "experience": experience,
                    "equipment": equipment,
                },
                timeout=30
            )
            response.raise_for_status()
            st.session_state["workout_plan"] = response.json()
        except requests.RequestException as e:
            st.error(f"Workout API error: {e}")

    if "workout_plan" in st.session_state:
        wp = st.session_state["workout_plan"]

        if wp["fitness_goal"] != fitness_goal or \
                wp["days_per_week"] != days_per_week or \
                wp["experience"] != experience or \
                wp["equipment"] != equipment:
            st.warning(
                "Your profile changed since this plan was made - "
                "click Generate Workout Plan to update it."
            )

        st.info(wp["training_focus"])
        c1, c2, c3 = st.columns(3)
        c1.metric("Training days", wp["days_per_week"])
        c2.metric("Strength sessions", wp["strength_sessions_per_week"])
        c3.metric(
            "Weekly training time",
            f"{sum(d['duration_min'] for d in wp['weekly_schedule'])} min"
        )

        st.subheader("Week at a Glance")
        st.dataframe(
            [
                {
                    "Day": d["day"],
                    "Session": d["session_type"],
                    "Focus": d["focus"],
                    "Minutes": d["duration_min"] or "-",
                }
                for d in wp["weekly_schedule"]
            ],
            hide_index=True
        )

        st.subheader("Daily Sessions")
        for d in wp["weekly_schedule"]:
            if d["session_type"] == "Rest":
                continue
            with st.expander(
                f"{d['day']} - {d['focus']} ({d['duration_min']} min)"
            ):
                st.dataframe(
                    [
                        {
                            "Exercise": e["name"],
                            "Sets": e["sets"],
                            "Reps": e["reps"],
                            "Rest (s)": e["rest_sec"] or "-",
                            "Notes": e["notes"],
                        }
                        for e in d["exercises"]
                    ],
                    hide_index=True
                )
                if st.button(
                    "✅ Log this session as done today",
                    key=f"log_{d['day']}"
                ):
                    add_log_entry(
                        date.today(), d["session_type"],
                        d["muscle_groups"], 7, d["duration_min"]
                    )
                    st.success(
                        "Logged! The AI Coach will use it to plan "
                        "your next strength day."
                    )

        with st.expander("Coaching tips"):
            for tip in wp["tips"]:
                st.write(f"- {tip}")

        st.caption(
            "General fitness guidance. Check with a healthcare "
            "professional before starting a new program if you have "
            "injuries or medical conditions."
        )

with tab4:
    st.header("AI Coach")

    st.subheader("🏋️ Strength Training Monitor")
    st.write(
        "Log your workouts and tell the coach how you feel. It checks "
        "your recovery and weekly progress, and tells you whether today "
        "is a strength day."
    )

    with st.expander("➕ Log a workout", expanded=not st.session_state["workout_log"]):
        with st.form("log_workout", clear_on_submit=True):
            l1, l2 = st.columns(2)
            log_date = l1.date_input("Date", value=date.today(),
                                     max_value=date.today())
            log_type = l2.selectbox("Session type", SESSION_TYPES)
            log_groups = st.multiselect(
                "Muscle groups trained (for strength sessions)",
                MUSCLE_GROUPS
            )
            l3, l4 = st.columns(2)
            log_rpe = l3.slider(
                "Effort (RPE 1-10)", 1, 10, 7,
                help="10 = absolute max effort, 7 = hard but ~3 reps left"
            )
            log_duration = l4.number_input(
                "Duration (min)", min_value=5, max_value=300, value=45
            )
            if st.form_submit_button("Add to log"):
                if log_type == "Strength" and not log_groups:
                    st.error("Pick at least one muscle group.")
                else:
                    add_log_entry(log_date, log_type, log_groups,
                                  log_rpe, log_duration)
                    st.success("Workout logged.")

    log = st.session_state["workout_log"]
    if log:
        st.dataframe(
            [
                {
                    "Date": e["date"],
                    "Session": e["session_type"],
                    "Muscle groups": ", ".join(e["muscle_groups"]) or "-",
                    "RPE": e["rpe"],
                    "Minutes": e["duration_min"],
                }
                for e in reversed(log)
            ],
            hide_index=True
        )
        b1, b2, b3 = st.columns(3)
        if b1.button("Remove last entry"):
            log.pop()
            st.session_state.pop("strength_check", None)
            st.rerun()
        b2.download_button(
            "Export log (CSV)",
            data=log_to_csv(log),
            file_name="workout_log.csv",
            mime="text/csv"
        )
        if b3.button("Clear log"):
            st.session_state["workout_log"] = []
            st.session_state.pop("strength_check", None)
            st.rerun()

    uploaded = st.file_uploader(
        "Import a saved workout log (CSV)",
        type="csv",
        help="Your log lives in this browser session. Export it to keep "
             "it, and import it next time."
    )
    if uploaded is not None and st.button("Import log"):
        try:
            st.session_state["workout_log"] = csv_to_log(
                uploaded.getvalue().decode("utf-8")
            )
            st.session_state.pop("strength_check", None)
            st.success(
                f"Imported {len(st.session_state['workout_log'])} workouts."
            )
            st.rerun()
        except (KeyError, ValueError) as e:
            st.error(f"Could not read that CSV: {e}")

    st.markdown("**How do you feel today?**")
    r1, r2, r3 = st.columns(3)
    sleep_hours = r1.number_input(
        "Sleep last night (hours)", min_value=0.0, max_value=16.0,
        value=7.5, step=0.5
    )
    soreness = r2.slider(
        "Muscle soreness", 1, 5, 2,
        help="1 = none, 5 = very sore"
    )
    energy = r3.slider(
        "Energy", 1, 5, 3,
        help="1 = exhausted, 5 = great"
    )

    if st.button("Should I strength train today?", type="primary"):
        with st.spinner("Coach is reviewing your training.."):
            try:
                response = requests.post(
                    f"{API_BASE_URL}/api/v1/coach/strength-check",
                    json={
                        "fitness_goal": fitness_goal,
                        "activity_level": activity_level,
                        "days_per_week": days_per_week,
                        "workout_log": log,
                        "sleep_hours": sleep_hours,
                        "soreness": soreness,
                        "energy": energy,
                        "today": date.today().isoformat(),
                    },
                    timeout=60
                )
                response.raise_for_status()
                st.session_state["strength_check"] = response.json()
            except requests.RequestException as e:
                st.error(f"Coach API error: {e}")

    if "strength_check" in st.session_state:
        sc = st.session_state["strength_check"]

        headline = f"### {sc['recommendation']}"
        if sc["should_strength_train"]:
            st.success(
                f"{headline}\n**Focus:** {sc['focus']} "
                f"({', '.join(sc['focus_muscle_groups'])})  \n"
                f"**Intensity:** {sc['intensity']}"
            )
        elif sc["recommendation"] == "Rest & recover":
            st.error(headline)
        else:
            st.warning(headline)

        st.write(sc["coach_message"])
        if not sc["ai_generated"]:
            st.caption("(AI message unavailable - showing rule-based summary)")

        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Readiness", f"{sc['readiness_score']}/100")
        m2.metric(
            "Strength this week",
            f"{sc['strength_sessions_this_week']}/"
            f"{sc['weekly_strength_target']}"
        )
        m3.metric(
            "Days since last lift",
            sc["days_since_last_strength"]
            if sc["days_since_last_strength"] is not None else "-"
        )
        next_day = date.fromisoformat(sc["next_strength_day"])
        m4.metric(
            "Next strength day",
            "Today" if next_day == date.today()
            else next_day.strftime("%a %b %d")
        )

        with st.expander("Why this recommendation?"):
            for reason in sc["reasons"]:
                st.write(f"- {reason}")

        with st.expander("Muscle recovery status"):
            st.dataframe(
                [
                    {
                        "Muscle group": m["muscle_group"],
                        "Status": ("🟢 " if m["status"] == "Recovered"
                                   else "🟠 ") + m["status"],
                        "Last trained": m["last_trained"] or "-",
                        "Ready on": m["ready_on"],
                    }
                    for m in sc["muscle_status"]
                ],
                hide_index=True
            )

    st.divider()

    st.subheader("💬 Ask your AI Coach")
    question = st.text_input("Ask your AI Coach",
                             placeholder="What should i eat after workout?")
    if st.button("Ask AI"):
        if question.strip():
            with st.spinner("AI is thinking"):
                try:
                    response = requests.post(
                        f"{API_BASE_URL}/api/v1/fitness/chat",
                        json={
                            "question": question,
                            "profile": {
                                "age": age,
                                "height_feet": height,
                                "weight_lb": weight,
                                "fitness_goal": fitness_goal,
                                "activity_level": activity_level,
                                "dietary_preference": dietary_preference
                            },
                            "recent_workouts": log[-14:] or None,
                        },
                        timeout=30
                    )
                    response.raise_for_status()
                    result = response.json()

                    st.success("Response received!")
                    st.write(result["answer"])

                    st.subheader("AI Performance Metrics")

                    col1, col2, col3 = st.columns(3)

                    col1.metric("Input Tokens", result["input_tokens"])
                    col2.metric("Output Tokens", result["output_tokens"])
                    col3.metric("Latency", f"{result['latency']}s")

                except requests.RequestException as e:
                    st.error(f"Backend API error: {e}")
        else:
            st.warning("Please enter a question.")
