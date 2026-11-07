from pr_security_demo import create_app


def test_health_endpoint_returns_ok():
    response = create_app().test_client().get("/health")

    assert response.status_code == 200
    assert response.get_json() == {"status": "ok"}
