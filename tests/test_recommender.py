import unittest

from app.recommender import generate_recommendations


class RecommenderTests(unittest.TestCase):
    def test_includes_rain_and_understeer_suggestions(self):
        result = generate_recommendations(
            car="Toyota Supra",
            track="Spa",
            weather="rain",
            time_of_day="day",
            custom_parts=[],
            struggles=["mid-corner understeer"],
        )

        text = " ".join(r["adjustment"].lower() for r in result["recommendations"])
        self.assertIn("wet or intermediate", text)
        self.assertIn("front downforce", text)

    def test_builds_prompt_with_metadata(self):
        result = generate_recommendations(
            car="Mazda RX-7",
            track="Suzuka",
            weather="clear",
            time_of_day="night",
            custom_parts=["high-rpm turbo"],
            struggles=["traction on exit"],
        )

        prompt = result["llm_prompt"].lower()
        self.assertIn("mazda rx-7", prompt)
        self.assertIn("suzuka", prompt)
        self.assertIn("high-rpm turbo", prompt)


if __name__ == "__main__":
    unittest.main()
