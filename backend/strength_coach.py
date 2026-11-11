from datetime import date, datetime, timedelta

from backend.workout_service import MUSCLE_GROUPS, strength_sessions_per_week

MAJOR_GROUPS = ["Legs", "Chest", "Back"]
UPPER_GROUPS = {"Chest", "Back", "Shoulders", "Arms"}

BASE_RECOVERY_DAYS = 2
HARD_SESSION_RECOVERY_DAYS = 3
MAX_CONSECUTIVE_STRENGTH_DAYS = 3


def _parse_date(value) -> date:
    if isinstance(value, datetime):
        return value.date()
    if isinstance(value, date):
        return value
    return date.fromisoformat(str(value)[:10])


def readiness_score(sleep_hours: float, soreness: int, energy: int) -> int:
    if 7 <= sleep_hours <= 9:
        sleep_pts = 40
    elif sleep_hours > 9:
        sleep_pts = 35
    else:
        sleep_pts = max(0.0, 40 - (7 - sleep_hours) * 10)

    soreness = min(max(int(soreness), 1), 5)
    energy = min(max(int(energy), 1), 5)
    soreness_pts = (5 - soreness) / 4 * 30
    energy_pts = (energy - 1) / 4 * 30
    return int(round(sleep_pts + soreness_pts + energy_pts))


def _intensity_for(score: int) -> str:
    if score >= 75:
        return "Hard - work at RPE 8 (about 2 reps in reserve)"
    if score >= 55:
        return "Moderate - RPE 6-7, stick to planned weights"
    return "Light - RPE 5-6, drop one set per exercise and focus on form"


def _week_start(day: date) -> date:
    return day - timedelta(days=day.weekday())


def analyze_strength_readiness(
    workout_log: list[dict],
    fitness_goal: str,
    days_per_week: int,
    sleep_hours: float,
    soreness: int,
    energy: int,
    today=None,
) -> dict:
    today = _parse_date(today) if today else date.today()
    reasons: list[str] = []

    entries = []
    for item in workout_log or []:
        try:
            entry_date = _parse_date(item["date"])
        except (KeyError, ValueError):
            continue
        if entry_date > today:
            continue
        entries.append({
            "date": entry_date,
            "session_type": item.get("session_type", "Strength"),
            "muscle_groups": [
                g for g in (item.get("muscle_groups") or [])
                if g in MUSCLE_GROUPS
            ],
            "rpe": item.get("rpe") or 7,
        })
    strength = [e for e in entries if e["session_type"] == "Strength"]
    strength.sort(key=lambda e: e["date"])

    weekly_target = strength_sessions_per_week(fitness_goal, days_per_week)
    week_start = _week_start(today)
    strength_dates_this_week = {
        e["date"] for e in strength if e["date"] >= week_start
    }
    trained_today = today in strength_dates_this_week
    done_this_week = len(strength_dates_this_week)

    past_strength = [e for e in strength if e["date"] < today]
    days_since_last = (
        (today - past_strength[-1]["date"]).days if past_strength else None
    )

    strength_days = {e["date"] for e in strength}
    streak = 0
    cursor = today - timedelta(days=1)
    while cursor in strength_days:
        streak += 1
        cursor -= timedelta(days=1)

    muscle_status = []
    for group in MUSCLE_GROUPS:
        sessions = [
            e for e in past_strength if group in e["muscle_groups"]
        ]
        if not sessions:
            muscle_status.append({
                "muscle_group": group,
                "last_trained": None,
                "days_since": None,
                "status": "Recovered",
                "ready_on": today.isoformat(),
            })
            continue
        last = sessions[-1]
        needed_days = (
            HARD_SESSION_RECOVERY_DAYS if last["rpe"] >= 9
            else BASE_RECOVERY_DAYS
        )
        days_since = (today - last["date"]).days
        ready_on = last["date"] + timedelta(days=needed_days)
        recovered = days_since >= needed_days
        muscle_status.append({
            "muscle_group": group,
            "last_trained": last["date"].isoformat(),
            "days_since": days_since,
            "status": "Recovered" if recovered else "Recovering",
            "ready_on": today.isoformat() if recovered
            else ready_on.isoformat(),
        })

    recovered_groups = [
        m["muscle_group"] for m in muscle_status
        if m["status"] == "Recovered"
    ]
    recovered_major = [g for g in MAJOR_GROUPS if g in recovered_groups]

    score = readiness_score(sleep_hours, soreness, energy)

    should_train = False
    focus = None
    focus_groups: list[str] = []
    intensity = None

    if trained_today:
        recommendation = "Done for today"
        reasons.append(
            "You already logged a strength session today. "
            "Recover and refuel."
        )
    elif score < 40:
        recommendation = "Rest & recover"
        reasons.append(
            f"Readiness is low ({score}/100) - poor sleep, high "
            "soreness or low energy raise injury risk and limit gains."
        )
    elif streak >= MAX_CONSECUTIVE_STRENGTH_DAYS:
        recommendation = "Active recovery"
        reasons.append(
            f"You've lifted {streak} days in a row. A light walk or "
            "mobility session today will help you come back stronger."
        )
    elif done_this_week >= weekly_target:
        recommendation = "Optional - cardio or mobility"
        reasons.append(
            f"Weekly strength target reached ({done_this_week}/"
            f"{weekly_target}). Extra lifting isn't needed for your goal."
        )
    elif len(recovered_major) == 0:
        recommendation = "Active recovery"
        reasons.append(
            "Your major muscle groups (legs, chest, back) are still "
            "recovering from recent sessions."
        )
    else:
        should_train = True
        recommendation = "Strength train today"
        legs_ready = "Legs" in recovered_groups
        upper_ready = [g for g in recovered_groups if g in UPPER_GROUPS]

        if legs_ready and len(upper_ready) >= 3:
            focus = "Full body"
            focus_groups = ["Legs"] + upper_ready + (
                ["Core"] if "Core" in recovered_groups else []
            )
        elif legs_ready:
            focus = "Lower body"
            focus_groups = ["Legs"] + (
                ["Core"] if "Core" in recovered_groups else []
            )
        else:
            focus = "Upper body"
            focus_groups = upper_ready

        intensity = _intensity_for(score)
        remaining = weekly_target - done_this_week
        reasons.append(
            f"{done_this_week}/{weekly_target} strength sessions done "
            f"this week - {remaining} to go."
        )
        if days_since_last is None:
            reasons.append("No recent strength sessions logged - "
                           "a great day to start.")
        elif days_since_last >= 3:
            reasons.append(
                f"It's been {days_since_last} days since your last "
                "strength session."
            )
        reasons.append(
            f"Recovered and ready: {', '.join(focus_groups)}."
        )
        reasons.append(f"Readiness score {score}/100.")

    still_recovering = [
        m["muscle_group"] for m in muscle_status
        if m["status"] == "Recovering"
    ]
    if still_recovering and should_train:
        reasons.append(
            f"Give these more time: {', '.join(still_recovering)}."
        )

    if should_train:
        next_day = today
    else:
        next_day = today + timedelta(days=1)
        major_ready_dates = [
            _parse_date(m["ready_on"]) for m in muscle_status
            if m["muscle_group"] in MAJOR_GROUPS
        ]
        if major_ready_dates:
            next_day = max(next_day, min(major_ready_dates))
        if done_this_week >= weekly_target:
            next_day = max(next_day, week_start + timedelta(days=7))

    return {
        "date": today.isoformat(),
        "recommendation": recommendation,
        "should_strength_train": should_train,
        "focus": focus,
        "focus_muscle_groups": focus_groups,
        "intensity": intensity,
        "readiness_score": score,
        "strength_sessions_this_week": done_this_week,
        "weekly_strength_target": weekly_target,
        "days_since_last_strength": days_since_last,
        "consecutive_strength_days": streak,
        "next_strength_day": next_day.isoformat(),
        "reasons": reasons,
        "muscle_status": muscle_status,
    }


def fallback_coach_message(analysis: dict) -> str:
    if analysis["should_strength_train"]:
        return (
            f"Today is a strength day. Train {analysis['focus'].lower()} "
            f"({', '.join(analysis['focus_muscle_groups'])}). "
            f"Intensity: {analysis['intensity']}."
        )
    return (
        f"{analysis['recommendation']}. Your next strength session is "
        f"planned for {analysis['next_strength_day']}."
    )
