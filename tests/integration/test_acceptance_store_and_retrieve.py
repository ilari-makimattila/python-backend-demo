from functools import reduce
import random
from datetime import datetime, timedelta
from faker import Faker
from fastapi.testclient import TestClient

fake = Faker()


def the_app_should_store_and_allow_fetch_of_averages(test_client: TestClient):
    rooms = set(fake.name() for _ in range(random.randint(1, 100)))
    measurements = {
        room: [
            {
                "v": random.randint(270, 300) + random.randint(0, 100) / 100,
                "ts": (datetime.utcnow() - timedelta(minutes=random.randint(0, 20))).isoformat(),
            }
            for _ in range(random.randint(1, 50))
        ]
        for room
        in rooms
    }

    expected_averages = {
        room: sum(
            m["v"]
            for m
            in measurements[room]
            if m["ts"] > (datetime.utcnow() - timedelta(minutes=15)).isoformat()
            ) / max(reduce(
                lambda a, b: a + 1 if b["ts"] > (datetime.utcnow() - timedelta(minutes=15)).isoformat() else a,
                measurements[room],
                0,
            ), 1)
        for room
        in rooms
    }

    for room, measurements in measurements.items():
        for measurement in measurements:
            response = test_client.post(f"/measurements/{room}", json=measurement)
            assert response.status_code == 200

    for room, expected_average in expected_averages.items():
        response = test_client.get(
            f"/measurements/{room}/average/PT15M",
            headers={"Accept": "application/json"},
        )
        assert response.status_code == 200
        assert response.json().items() >= {
            "v": expected_average,
            "u": "K",
        }.items()
