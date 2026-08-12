from fastapi.testclient import TestClient

from src.app import app

client = TestClient(app)


def test_unregister_participant_removes_email_from_activity():
    activity_name = "Chess Club"
    email = "newstudent@mergington.edu"

    before = client.get("/activities")
    assert before.status_code == 200
    activity = before.json()[activity_name]
    if email in activity["participants"]:
        response = client.delete(f"/activities/{activity_name}/unregister?email={email}")
        assert response.status_code == 200

    signup = client.post(f"/activities/{activity_name}/signup?email={email}")
    assert signup.status_code == 200

    response = client.delete(f"/activities/{activity_name}/unregister?email={email}")
    assert response.status_code == 200
    assert email not in response.json()["participants"]

    data = client.get("/activities")
    assert email not in data.json()[activity_name]["participants"]
