from dataclasses import dataclass, asdict
from typing import List, Dict


@dataclass
class SetupSuggestion:
    area: str
    adjustment: str
    reason: str


BASE_SUGGESTIONS = {
    "baseline": [
        SetupSuggestion("tires", "Use Racing Medium for balanced pace and consistency.", "Stable baseline for mixed stint lengths."),
        SetupSuggestion("brakes", "Start with brake balance at -1 (slightly rearward).", "Helps rotation without excessive front lockups."),
        SetupSuggestion("differential", "Set initial torque to a moderate value.", "Improves consistency on throttle transitions."),
    ],
    "rain": [
        SetupSuggestion("tires", "Switch to Wet or Intermediate based on standing water.", "Maximizes grip and reduces aquaplaning risk."),
        SetupSuggestion("suspension", "Soften anti-roll bars by 1-2 clicks.", "Improves mechanical grip on low-traction surfaces."),
        SetupSuggestion("differential", "Reduce acceleration sensitivity slightly.", "Smoother power delivery on corner exit in low grip."),
    ],
    "night": [
        SetupSuggestion("brakes", "Increase braking margin and avoid aggressive front bias.", "Lower visibility makes late braking riskier."),
    ],
    "high-rpm turbo": [
        SetupSuggestion("transmission", "Lengthen 2nd and 3rd gears slightly.", "Helps manage sudden boost spikes on corner exit."),
        SetupSuggestion("differential", "Increase deceleration sensitivity by 1 click.", "Adds stability on lift-off into corners."),
    ],
    "racing suspension": [
        SetupSuggestion("suspension", "Lower ride height moderately and keep slight rake.", "Improves aero efficiency without bottoming out."),
    ],
    "understeer": [
        SetupSuggestion("suspension", "Soften front anti-roll bar or stiffen rear by 1 click.", "Increases front bite or rear rotation mid-corner."),
        SetupSuggestion("differential", "Lower front/rear LSD acceleration sensitivity where applicable.", "Reduces push when applying throttle."),
        SetupSuggestion("aero", "Increase front downforce if available.", "Improves turn-in and sustained cornering grip."),
    ],
    "oversteer": [
        SetupSuggestion("suspension", "Soften rear anti-roll bar or stiffen front by 1 click.", "Calms rear slip at corner entry/mid-corner."),
        SetupSuggestion("differential", "Increase acceleration sensitivity slightly.", "Reduces one-wheel spin and sudden yaw."),
    ],
    "traction": [
        SetupSuggestion("differential", "Reduce acceleration lock and short-shift earlier.", "Prevents wheelspin on corner exit."),
        SetupSuggestion("tires", "If legal, run softer rear compound or fresher rears.", "Improves rear grip under throttle."),
    ],
    "braking": [
        SetupSuggestion("brakes", "Move brake balance 1 click rearward and reduce pressure spikes.", "Mitigates front lockups and instability."),
        SetupSuggestion("suspension", "Slightly increase front rebound damping.", "Stabilizes pitch under heavy braking."),
    ],
}


def _keyword_match(struggles: List[str]) -> List[str]:
    lowered = " ".join(struggles).lower()
    matches: List[str] = []

    if "understeer" in lowered:
        matches.append("understeer")
    if "oversteer" in lowered:
        matches.append("oversteer")
    if "traction" in lowered or "wheelspin" in lowered or "exit" in lowered:
        matches.append("traction")
    if "brak" in lowered or "lockup" in lowered:
        matches.append("braking")

    return matches


def generate_recommendations(
    car: str,
    track: str,
    weather: str,
    time_of_day: str,
    custom_parts: List[str],
    struggles: List[str],
) -> Dict[str, object]:
    suggestions: List[SetupSuggestion] = []
    suggestions.extend(BASE_SUGGESTIONS["baseline"])

    weather_key = weather.strip().lower()
    if weather_key == "rain":
        suggestions.extend(BASE_SUGGESTIONS["rain"])

    tod_key = time_of_day.strip().lower()
    if tod_key == "night":
        suggestions.extend(BASE_SUGGESTIONS["night"])

    for part in custom_parts:
        key = part.strip().lower()
        if key in BASE_SUGGESTIONS:
            suggestions.extend(BASE_SUGGESTIONS[key])

    for issue in _keyword_match(struggles):
        suggestions.extend(BASE_SUGGESTIONS[issue])

    unique = []
    seen = set()
    for item in suggestions:
        sig = (item.area, item.adjustment)
        if sig in seen:
            continue
        seen.add(sig)
        unique.append(item)

    prompt = build_llm_prompt(
        car=car,
        track=track,
        weather=weather,
        time_of_day=time_of_day,
        custom_parts=custom_parts,
        struggles=struggles,
        draft_suggestions=unique,
    )

    return {
        "car": car,
        "track": track,
        "weather": weather,
        "time_of_day": time_of_day,
        "recommendations": [asdict(s) for s in unique],
        "llm_prompt": prompt,
    }


def build_llm_prompt(
    car: str,
    track: str,
    weather: str,
    time_of_day: str,
    custom_parts: List[str],
    struggles: List[str],
    draft_suggestions: List[SetupSuggestion],
) -> str:
    lines = [
        "You are a professional Gran Turismo 7 race engineer.",
        f"Car: {car}",
        f"Track: {track}",
        f"Weather: {weather}",
        f"Time of day: {time_of_day}",
        f"Custom parts: {', '.join(custom_parts) if custom_parts else 'None'}",
        f"Driver struggles: {', '.join(struggles) if struggles else 'None'}",
        "",
        "Use the following draft setup ideas and refine them with specific click/value ranges:",
    ]

    for suggestion in draft_suggestions:
        lines.append(f"- [{suggestion.area}] {suggestion.adjustment} ({suggestion.reason})")

    lines.extend(
        [
            "",
            "Output format:",
            "1) Prioritized setup changes (max 8)",
            "2) Why each change helps this driver",
            "3) One conservative and one aggressive variant",
            "4) 3-lap validation plan for the driver",
        ]
    )

    return "\n".join(lines)
