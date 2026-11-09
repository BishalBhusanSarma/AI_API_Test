import requests

from req import (
    BASE_URL,
    employee_headers,
    manager_headers,
    create_leave_payload
)


def test_TC_01_create_leave_request_successfully():
    payload = create_leave_payload(
        "2029-11-01",
        "2029-11-02"
    )

    response = requests.post(
        BASE_URL,
        json=payload,
        headers=employee_headers
    )

    assert response.status_code == 201

    data = response.json()

    assert data["status"] == "pending"
    assert data["employee_id"] == "EMP001"

    print("TC_01 successfully passed.")


def test_TC_02_retrieve_leave_request_successfully():
    payload = create_leave_payload(
        "2029-11-04",
        "2029-11-04"
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
        headers=employee_headers
    )

    assert response.status_code == 200
    assert response.json()["id"] == leave_id

    print("TC_02 successfully passed.")


def test_TC_05_manager_approves_leave_request():
    payload = create_leave_payload(
        "2029-11-06",
        "2029-11-07"
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
        headers=manager_headers
    )

    assert response.status_code == 200
    assert response.json()["status"] == "approved"

    print("TC_05 successfully passed.")


def test_TC_06_verify_approver_details():
    payload = create_leave_payload(
        "2029-11-09",
        "2029-11-10"
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
        headers=manager_headers
    )

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "approved"
    assert data["approved_by"] == "MGR001"

    print("TC_06 successfully passed.")


def test_TC_10_verify_approved_status_persists():
    payload = create_leave_payload(
        "2029-11-12",
        "2029-11-13"
    )

    create_response = requests.post(
        BASE_URL,
        json=payload,
        headers=employee_headers
    )

    assert create_response.status_code == 201

    leave_id = create_response.json()["id"]

    approve_response = requests.put(
        f"{BASE_URL}/{leave_id}/approve",
        headers=manager_headers
    )

    assert approve_response.status_code == 200

    get_response = requests.get(
        f"{BASE_URL}/{leave_id}",
        headers=employee_headers
    )

    assert get_response.status_code == 200
    assert get_response.json()["status"] == "approved"

    print("TC_10 successfully passed.")