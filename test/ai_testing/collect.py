
import csv
import json
import requests
from datetime import datetime

# Configuration
API_URL = "http://127.0.0.1:8000/ai/chat"
AUTH_TOKEN = "emp1"  # Replace with a valid employee token

CSV_FILE = "/test/testcases/ai_test.csv"
OUTPUT_FILE = "/test/actual_responses.json"

HEADERS = {
    "Authorization": f"Bearer {AUTH_TOKEN}",
    "Content-Type": "application/json"
}


def main():

    with open(CSV_FILE, "r", encoding="utf-8-sig") as file:
        test_cases = list(csv.DictReader(file))

    report = {
        "created_at": datetime.now().isoformat(),
        "endpoint": API_URL,
        "total_cases": len(test_cases),
        "responses": {}
    }

    for index, case in enumerate(test_cases, start=1):

        test_id = case["test_case_id"]
        prompt = case["prompt"]

        print(f"Running {index}/{len(test_cases)}: {test_id}")

        try:
            response = requests.post(
                API_URL,
                headers=HEADERS,
                json={"message": prompt},
                timeout=90
            )

            try:
                actual_response = response.json()
            except ValueError:
                actual_response = {"raw_response": response.text}

            if response.ok:
                report["responses"][test_id] = {
                    "prompt": prompt,
                    "api_status": "SUCCESS",
                    "actual_response": actual_response
                }
                print("SUCCESS")

            else:
                report["responses"][test_id] = {
                    "prompt": prompt,
                    "api_status": "ERROR",
                    "http_status": response.status_code,
                    "error": actual_response
                }
                print("API ERROR")

        except requests.RequestException as error:

            report["responses"][test_id] = {
                "prompt": prompt,
                "api_status": "ERROR",
                "error": str(error)
            }

            print("REQUEST ERROR:", error)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
        json.dump(report, file, indent=4, ensure_ascii=False)

    print("\nResponse collection completed.")
    print(f"Total prompts: {len(test_cases)}")
    print(f"Saved to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
