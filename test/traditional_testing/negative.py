import requests

from req import BASE_URL, employee_headers, create_leave_payload


def test_TC_11_reject_end_date_before_start_date():
    payload = create_leave_payload(
        "2026-12-10",
        "2026-12-05"
    )

    response = requests.post(
        BASE_URL,
        json=payload,
        headers=employee_headers
    )

    assert response.status_code == 422

    print("TC_11 successfully passed.")


def test_TC_15_reject_invalid_leave_type():
    payload = create_leave_payload(
        "2029-12-01",
        "2029-12-02",
        leave_type="maternity"
    )

    response = requests.post(
        BASE_URL,
        json=payload,
        headers=employee_headers
    )

    assert response.status_code == 422

    print("TC_15 successfully passed.")


def test_TC_19_retrieve_nonexistent_leave_request():
    response = requests.get(
        f"{BASE_URL}/999999",
        headers=employee_headers
    )

    assert response.status_code == 404

    print("TC_19 successfully passed.")