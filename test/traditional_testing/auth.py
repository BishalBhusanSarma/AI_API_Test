import requests

from req import (
    BASE_URL,
    employee_headers,
    employee2_headers,
    manager_headers,
    create_leave_payload
)


def test_TC_17_employee_cannot_approve_leave_request():
    payload = create_leave_payload(
        "2030-01-01",
        "2030-01-02"
    )

    create_response = requests.post(
        BASE_URL,
        json=payload,
        headers=employee_headers
    )

    assert create_response.status_code == 201

    leave_id = create_response.json()["id"]

    response = requests.put(
        f"{BASE_URL}/{leave_id}/approve",
        headers=employee_headers
    )

    assert response.status_code == 403

    print("TC_17 successfully passed.")


def test_TC_18_employee_cannot_view_another_employees_leave():
    payload = create_leave_payload(
        "2030-01-04",
        "2030-01-05"
    )

    create_response = requests.post(
        BASE_URL,
        json=payload,
        headers=employee_headers
    )

    assert create_response.status_code == 201

    leave_id = create_response.json()["id"]

    response = requests.get(
        f"{BASE_URL}/{leave_id}",
        headers=employee2_headers
    )

    assert response.status_code == 403

    print("TC_18 successfully passed.")


def test_TC_28_reject_request_without_authentication():
    payload = create_leave_payload(
        "2030-01-07",
        "2030-01-08"
    )

    response = requests.post(
        BASE_URL,
        json=payload
    )

    assert response.status_code == 401

    print("TC_28 successfully passed.")


def test_TC_29_reject_request_with_invalid_token():
    payload = create_leave_payload(
        "2030-01-10",
        "2030-01-11"
    )

    invalid_headers = {
        "Authorization": "Bearer invalid-token"
    }

    response = requests.post(
        BASE_URL,
        json=payload,
        headers=invalid_headers
    )

    assert response.status_code == 401

    print("TC_29 successfully passed.")