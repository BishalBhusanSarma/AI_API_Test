BASE_URL = "http://127.0.0.1:8000/leave"

employee_headers = {
    "Authorization": "Bearer emp1"
}

employee2_headers = {
    "Authorization": "Bearer emp2"
}

employee3_headers = {
    "Authorization": "Bearer emp3"
}

employee4_headers = {
    "Authorization": "Bearer emp4"
}

manager_headers = {
    "Authorization": "Bearer man"
}


def create_leave_payload(
    start_date,
    end_date,
    reason="Personal work",
    leave_type="casual"
):
    return {
        "start_date": start_date,
        "end_date": end_date,
        "reason": reason,
        "leave_type": leave_type
    }