WEEK_DAYS = [
    "Monday", "Tuesday", "Wednesday", "Thursday",
    "Friday", "Saturday", "Sunday",
]

TRAINING_DAY_SLOTS = {
    2: [0, 3],
    3: [0, 2, 4],
    4: [0, 1, 3, 4],
    5: [0, 1, 2, 4, 5],
    6: [0, 1, 2, 3, 4, 5],
}

DEFAULT_DAYS_BY_ACTIVITY = {
    "Sedentary": 3,
    "Lightly Active": 3,
    "Moderately Active": 4,
    "Very Active": 5,
}

EXPERIENCE_LEVELS = ["Beginner", "Intermediate", "Advanced"]
EQUIPMENT_OPTIONS = ["Full Gym", "Dumbbells Only", "Bodyweight"]

MUSCLE_GROUPS = ["Chest", "Back", "Shoulders", "Arms", "Legs", "Core"]

SESSIONS = {
    "full_body_a": {
        "name": "Full Body A",
        "kind": "strength",
        "muscle_groups": ["Legs", "Chest", "Back", "Core"],
        "slots": ["squat", "horizontal_push", "horizontal_pull",
                  "hinge", "core"],
    },
    "full_body_b": {
        "name": "Full Body B",
        "kind": "strength",
        "muscle_groups": ["Legs", "Shoulders", "Back", "Core"],
        "slots": ["hinge", "vertical_push", "vertical_pull",
                  "lunge", "core"],
    },
    "upper": {
        "name": "Upper Body",
        "kind": "strength",
        "muscle_groups": ["Chest", "Back", "Shoulders", "Arms"],
        "slots": ["horizontal_push", "horizontal_pull", "vertical_push",
                  "vertical_pull", "biceps", "triceps"],
    },
    "lower": {
        "name": "Lower Body",
        "kind": "strength",
        "muscle_groups": ["Legs", "Core"],
        "slots": ["squat", "hinge", "lunge", "hamstring_curl",
                  "calves", "core"],
    },
    "push": {
        "name": "Push (Chest, Shoulders, Triceps)",
        "kind": "strength",
        "muscle_groups": ["Chest", "Shoulders", "Arms"],
        "slots": ["horizontal_push", "vertical_push", "incline_push",
                  "lateral_raise", "triceps"],
    },
    "pull": {
        "name": "Pull (Back, Biceps)",
        "kind": "strength",
        "muscle_groups": ["Back", "Arms"],
        "slots": ["vertical_pull", "horizontal_pull", "rear_delt",
                  "biceps", "core"],
    },
    "legs": {
        "name": "Legs",
        "kind": "strength",
        "muscle_groups": ["Legs", "Core"],
        "slots": ["squat", "hinge", "lunge", "calves", "core"],
    },
    "cardio": {
        "name": "Steady Cardio (Zone 2)",
        "kind": "cardio",
        "muscle_groups": [],
    },
    "conditioning": {
        "name": "Interval Conditioning",
        "kind": "conditioning",
        "muscle_groups": [],
    },
    "mobility": {
        "name": "Mobility & Core",
        "kind": "mobility",
        "muscle_groups": ["Core"],
    },
}

GOAL_SPLITS = {
    "Build Muscle": {
        2: ["full_body_a", "full_body_b"],
        3: ["full_body_a", "full_body_b", "full_body_a"],
        4: ["upper", "lower", "upper", "lower"],
        5: ["push", "pull", "legs", "upper", "lower"],
        6: ["push", "pull", "legs", "push", "pull", "legs"],
    },
    "Fat Loss & Muscle Retention": {
        2: ["full_body_a", "full_body_b"],
        3: ["full_body_a", "conditioning", "full_body_b"],
        4: ["upper", "lower", "cardio", "full_body_a"],
        5: ["upper", "lower", "cardio", "upper", "lower"],
        6: ["upper", "lower", "cardio", "upper", "lower", "conditioning"],
    },
    "Weight Loss": {
        2: ["full_body_a", "full_body_b"],
        3: ["full_body_a", "cardio", "full_body_b"],
        4: ["full_body_a", "cardio", "full_body_b", "cardio"],
        5: ["full_body_a", "cardio", "full_body_b", "full_body_a",
            "cardio"],
        6: ["full_body_a", "cardio", "full_body_b", "cardio",
            "full_body_a", "mobility"],
    },
    "General Fitness": {
        2: ["full_body_a", "full_body_b"],
        3: ["full_body_a", "cardio", "full_body_b"],
        4: ["full_body_a", "cardio", "full_body_b", "mobility"],
        5: ["full_body_a", "cardio", "full_body_b", "conditioning",
            "mobility"],
        6: ["upper", "cardio", "lower", "mobility", "full_body_a",
            "cardio"],
    },
    "Maintain Weight": {
        2: ["full_body_a", "full_body_b"],
        3: ["full_body_a", "cardio", "full_body_b"],
        4: ["full_body_a", "cardio", "full_body_b", "cardio"],
        5: ["upper", "cardio", "lower", "full_body_a", "mobility"],
        6: ["upper", "cardio", "lower", "mobility", "full_body_a",
            "cardio"],
    },
}

GOAL_PRESCRIPTION = {
    "Build Muscle": {
        "sets": 4, "reps": "8-12", "rest_sec": 90,
        "focus": "Hypertrophy: moderate weight, close to failure "
                 "(1-2 reps in reserve).",
    },
    "Fat Loss & Muscle Retention": {
        "sets": 3, "reps": "6-10", "rest_sec": 120,
        "focus": "Keep lifting heavy to hold on to muscle while "
                 "in a calorie deficit.",
    },
    "Weight Loss": {
        "sets": 3, "reps": "10-15", "rest_sec": 60,
        "focus": "Build the habit, burn energy and keep muscle with "
                 "full-body sessions and regular cardio.",
    },
    "General Fitness": {
        "sets": 3, "reps": "8-12", "rest_sec": 75,
        "focus": "Balanced strength, cardio and mobility.",
    },
    "Maintain Weight": {
        "sets": 3, "reps": "8-12", "rest_sec": 75,
        "focus": "Maintain strength and fitness with a sustainable "
                 "routine.",
    },
}

ACCESSORY_SLOTS = {
    "core", "biceps", "triceps", "lateral_raise", "calves",
    "hamstring_curl", "rear_delt",
}

EXERCISES = {
    "squat": {
        "Full Gym": "Barbell Back Squat",
        "Dumbbells Only": "Dumbbell Goblet Squat",
        "Bodyweight": "Bodyweight Squat (slow tempo)",
    },
    "hinge": {
        "Full Gym": "Romanian Deadlift",
        "Dumbbells Only": "Dumbbell Romanian Deadlift",
        "Bodyweight": "Single-Leg Hip Hinge / Glute Bridge",
    },
    "lunge": {
        "Full Gym": "Walking Lunge",
        "Dumbbells Only": "Dumbbell Reverse Lunge",
        "Bodyweight": "Reverse Lunge",
    },
    "horizontal_push": {
        "Full Gym": "Barbell Bench Press",
        "Dumbbells Only": "Dumbbell Floor/Bench Press",
        "Bodyweight": "Push-Up",
    },
    "incline_push": {
        "Full Gym": "Incline Dumbbell Press",
        "Dumbbells Only": "Incline Dumbbell Press",
        "Bodyweight": "Decline (feet-elevated) Push-Up",
    },
    "horizontal_pull": {
        "Full Gym": "Seated Cable Row",
        "Dumbbells Only": "One-Arm Dumbbell Row",
        "Bodyweight": "Inverted Row (table or bar)",
    },
    "vertical_push": {
        "Full Gym": "Overhead Press",
        "Dumbbells Only": "Seated Dumbbell Shoulder Press",
        "Bodyweight": "Pike Push-Up",
    },
    "vertical_pull": {
        "Full Gym": "Lat Pulldown / Pull-Up",
        "Dumbbells Only": "Dumbbell Pullover",
        "Bodyweight": "Pull-Up or Towel Door Row",
    },
    "biceps": {
        "Full Gym": "Cable Biceps Curl",
        "Dumbbells Only": "Dumbbell Curl",
        "Bodyweight": "Chin-Up Hold / Towel Curl",
    },
    "triceps": {
        "Full Gym": "Cable Triceps Pushdown",
        "Dumbbells Only": "Dumbbell Overhead Triceps Extension",
        "Bodyweight": "Bench Dip",
    },
    "lateral_raise": {
        "Full Gym": "Cable Lateral Raise",
        "Dumbbells Only": "Dumbbell Lateral Raise",
        "Bodyweight": "Wall Slide / Y-Raise",
    },
    "rear_delt": {
        "Full Gym": "Face Pull",
        "Dumbbells Only": "Dumbbell Rear-Delt Fly",
        "Bodyweight": "Prone Y-T-W Raise",
    },
    "hamstring_curl": {
        "Full Gym": "Lying Leg Curl",
        "Dumbbells Only": "Dumbbell Hamstring Curl",
        "Bodyweight": "Sliding Hamstring Curl",
    },
    "calves": {
        "Full Gym": "Standing Calf Raise",
        "Dumbbells Only": "Dumbbell Calf Raise",
        "Bodyweight": "Single-Leg Calf Raise",
    },
    "core": {
        "Full Gym": "Cable Pallof Press + Plank",
        "Dumbbells Only": "Dumbbell Dead Bug + Plank",
        "Bodyweight": "Plank + Dead Bug",
    },
}

NON_STRENGTH_CONTENT = {
    "cardio": {
        "duration_min": 35,
        "exercises": [
            {"name": "Brisk walk, cycle, row or easy jog",
             "sets": 1, "reps": "30-40 min", "rest_sec": 0,
             "notes": "Zone 2: you can still hold a conversation."},
            {"name": "Light stretching", "sets": 1, "reps": "5 min",
             "rest_sec": 0, "notes": "Hips, hamstrings, chest."},
        ],
    },
    "conditioning": {
        "duration_min": 25,
        "exercises": [
            {"name": "Warm-up (easy cardio)", "sets": 1,
             "reps": "5 min", "rest_sec": 0, "notes": ""},
            {"name": "Intervals: bike, rower, or jumping jacks/"
                     "mountain climbers",
             "sets": 8, "reps": "30s hard / 60s easy", "rest_sec": 60,
             "notes": "Hard but controlled (about 8/10 effort)."},
            {"name": "Cool-down walk", "sets": 1, "reps": "5 min",
             "rest_sec": 0, "notes": ""},
        ],
    },
    "mobility": {
        "duration_min": 25,
        "exercises": [
            {"name": "Cat-Cow + Thoracic Rotations", "sets": 2,
             "reps": "10 each", "rest_sec": 0, "notes": ""},
            {"name": "World's Greatest Stretch", "sets": 2,
             "reps": "5 per side", "rest_sec": 0, "notes": ""},
            {"name": "90/90 Hip Switches", "sets": 2, "reps": "10",
             "rest_sec": 0, "notes": ""},
            {"name": "Side Plank", "sets": 2, "reps": "30s per side",
             "rest_sec": 30, "notes": ""},
            {"name": "Bird Dog", "sets": 2, "reps": "8 per side",
             "rest_sec": 30, "notes": ""},
        ],
    },
}


def default_days_per_week(activity_level: str) -> int:
    return DEFAULT_DAYS_BY_ACTIVITY.get(activity_level, 3)


def get_split(goal: str, days_per_week: int) -> list[str]:
    days = min(max(int(days_per_week), 2), 6)
    splits = GOAL_SPLITS.get(goal, GOAL_SPLITS["General Fitness"])
    return list(splits[days])


def strength_sessions_per_week(goal: str, days_per_week: int) -> int:
    return sum(
        1 for key in get_split(goal, days_per_week)
        if SESSIONS[key]["kind"] == "strength"
    )


def _build_strength_exercises(
    session_key: str,
    goal: str,
    experience: str,
    equipment: str,
) -> list[dict]:
    rx = GOAL_PRESCRIPTION.get(goal, GOAL_PRESCRIPTION["General Fitness"])
    exercises = []

    for slot in SESSIONS[session_key]["slots"]:
        accessory = slot in ACCESSORY_SLOTS
        sets = rx["sets"] - 1 if accessory else rx["sets"]
        if experience == "Beginner":
            sets -= 1
        elif experience == "Advanced" and not accessory:
            sets += 1
        sets = max(sets, 2)

        reps = "12-15" if accessory else rx["reps"]
        if slot == "core":
            reps = "30-45s / 10 reps"
        rest = 60 if accessory else rx["rest_sec"]

        notes = ""
        if equipment == "Bodyweight" and not accessory:
            notes = "Too easy? Slow the tempo or use a harder variation."
        if experience == "Beginner" and not accessory:
            notes = "Focus on form; stop with 2-3 reps in reserve."

        exercises.append({
            "name": EXERCISES[slot].get(equipment, EXERCISES[slot]["Full Gym"]),
            "sets": sets,
            "reps": reps,
            "rest_sec": rest,
            "notes": notes,
        })
    return exercises


def _estimate_strength_minutes(exercises: list[dict]) -> int:
    seconds = sum(e["sets"] * (45 + e["rest_sec"]) for e in exercises)
    return int(round(seconds / 60 / 5) * 5) + 10


def generate_workout_plan(
    fitness_goal: str,
    days_per_week: int | None = None,
    activity_level: str = "Lightly Active",
    experience: str = "Beginner",
    equipment: str = "Full Gym",
) -> dict:

    if fitness_goal not in GOAL_SPLITS:
        fitness_goal = "General Fitness"
    if experience not in EXPERIENCE_LEVELS:
        experience = "Beginner"
    if equipment not in EQUIPMENT_OPTIONS:
        equipment = "Full Gym"
    if days_per_week is None:
        days_per_week = default_days_per_week(activity_level)
    days_per_week = min(max(int(days_per_week), 2), 6)

    split = get_split(fitness_goal, days_per_week)
    slots = TRAINING_DAY_SLOTS[days_per_week]
    schedule = []

    for index, day_name in enumerate(WEEK_DAYS):
        if index in slots:
            key = split[slots.index(index)]
            session = SESSIONS[key]
            if session["kind"] == "strength":
                exercises = _build_strength_exercises(
                    key, fitness_goal, experience, equipment
                )
                duration = _estimate_strength_minutes(exercises)
                session_type = "Strength"
            else:
                content = NON_STRENGTH_CONTENT[session["kind"]]
                exercises = [dict(e) for e in content["exercises"]]
                duration = content["duration_min"]
                session_type = {
                    "cardio": "Cardio",
                    "conditioning": "Conditioning",
                    "mobility": "Mobility",
                }[session["kind"]]

            schedule.append({
                "day": day_name,
                "session_type": session_type,
                "focus": session["name"],
                "muscle_groups": list(session["muscle_groups"]),
                "duration_min": duration,
                "exercises": exercises,
            })
        else:
            schedule.append({
                "day": day_name,
                "session_type": "Rest",
                "focus": "Rest / light walk",
                "muscle_groups": [],
                "duration_min": 0,
                "exercises": [],
            })

    rx = GOAL_PRESCRIPTION[fitness_goal]
    strength_count = sum(
        1 for d in schedule if d["session_type"] == "Strength"
    )

    tips = [
        "Warm up 5-10 minutes before every strength session.",
        "Progressive overload: when you hit the top of the rep range "
        "for all sets, add a little weight next time.",
        "Aim for 7-9 hours of sleep; recovery is when you get stronger.",
    ]
    if fitness_goal in ("Weight Loss", "Fat Loss & Muscle Retention"):
        tips.append(
            "Daily steps (7-10k) add up - keep moving on rest days."
        )
    if experience == "Beginner":
        tips.append(
            "Start lighter than you think for the first 2 weeks "
            "and learn the movements."
        )

    return {
        "fitness_goal": fitness_goal,
        "days_per_week": days_per_week,
        "strength_sessions_per_week": strength_count,
        "experience": experience,
        "equipment": equipment,
        "training_focus": rx["focus"],
        "weekly_schedule": schedule,
        "tips": tips,
    }
