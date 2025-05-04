from starlette.testclient import TestClient

from app.main import app

client = TestClient(app)


def test():
    response = client.post(
        "auth/login",
        json={"email": "test@test.com", "password": "$2b$12$M8kKhFQ1sh/fjiZF7bvpBegM4FXG73zy0z2kBjGcEps0xWzpQ8Om2"}
    )

    assert response.status_code == 200

    response_data = response.json()



    assert response_data
    assert response_data is not None
    assert isinstance(response_data, str)

