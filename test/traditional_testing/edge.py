import requests

from req import (
    BASE_URL,
    employee_headers,
    employee2_headers,
    employee3_headers,
    employee4_headers,
    create_leave_payload
)


def test_TC_21_submit_exactly_20_days_of_leave():
    payload = create_leave_payload(
        "2028-01-01",
        "2028-01-20"
    )

    response = requests.post(
        BASE_URL,
        json=payload,
        headers=employee_headers
    )

    assert response.status_code == 201

    print("TC_21 successfully passed.")


def test_TC_22_submit_more_than_20_days_of_leave():
    payload = create_leave_payload(
        "2028-01-01",
        "2028-01-21"
    )

    response = requests.post(
        BASE_URL,
        json=payload,
        headers=employee2_headers
    )

    assert response.status_code == 400

    print("TC_22 successfully passed.")


def test_TC_24_reject_overlapping_leave_request():
    first_payload = create_leave_payload(
        "2028-01-10",
        "2028-01-12"
    )

    first_response = requests.post(
        BASE_URL,
        json=first_payload,
        headers=employee3_headers
    )

    assert first_response.status_code == 201

    second_payload = create_leave_payload(
        "2028-01-12",
        "2028-01-14"
    )

    second_response = requests.post(
        BASE_URL,
        json=second_payload,
        headers=employee3_headers
    )

    assert second_response.status_code == 400

    print("TC_24 successfully passed.")


def test_TC_27_cross_year_leave_request():
    payload = create_leave_payload(
        "2026-12-15",
        "2027-01-20"
    )

    response = requests.post(
        BASE_URL,
        json=payload,
        headers=employee4_headers
    )

    # 2026: 17 days, 2027: 20 days.
    # Both years are within the 20-day annual limit.

    assert response.status_code == 201

    print("TC_27 successfully passed.")