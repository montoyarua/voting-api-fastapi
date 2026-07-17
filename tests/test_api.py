def create_voter(client, name="Juan Perez", email="juan@example.com"):
    return client.post("/voters", json={"name": name, "email": email})


def create_candidate(client, name="Ana Lopez", party="Verde"):
    return client.post("/candidates", json={"name": name, "party": party})


def test_vote_updates_statistics_and_candidate_counter(client):
    voter = create_voter(client).json()
    candidate = create_candidate(client).json()

    response = client.post(
        "/votes",
        json={"voter_id": voter["id"], "candidate_id": candidate["id"]},
    )
    assert response.status_code == 201

    candidate_response = client.get(f"/candidates/{candidate['id']}")
    assert candidate_response.json()["votes"] == 1

    statistics = client.get("/votes/statistics").json()
    assert statistics["total_votes"] == 1
    assert statistics["total_voters_voted"] == 1
    assert statistics["by_candidate"][0]["percentage"] == 100.0


def test_voter_cannot_vote_twice(client):
    voter = create_voter(client).json()
    first_candidate = create_candidate(client).json()
    second_candidate = create_candidate(client, "Maria Diaz", "Azul").json()

    assert client.post(
        "/votes",
        json={"voter_id": voter["id"], "candidate_id": first_candidate["id"]},
    ).status_code == 201

    response = client.post(
        "/votes",
        json={"voter_id": voter["id"], "candidate_id": second_candidate["id"]},
    )
    assert response.status_code == 409


def test_people_with_same_normalized_name_cannot_have_both_roles(client):
    assert create_voter(client, "  Juan   Perez  ").status_code == 201
    response = create_candidate(client, "juan perez", "Verde")
    assert response.status_code == 409


def test_email_is_normalized_and_unique(client):
    assert create_voter(client, email="JUAN@EXAMPLE.COM").status_code == 201
    response = create_voter(client, name="Otro Juan", email="juan@example.com")
    assert response.status_code == 409


def test_blank_names_are_rejected(client):
    assert create_voter(client, name="   ").status_code == 422
    assert create_candidate(client, name="   ").status_code == 422


def test_entities_with_votes_cannot_be_deleted(client):
    voter = create_voter(client).json()
    candidate = create_candidate(client).json()
    client.post(
        "/votes",
        json={"voter_id": voter["id"], "candidate_id": candidate["id"]},
    )

    assert client.delete(f"/voters/{voter['id']}").status_code == 409
    assert client.delete(f"/candidates/{candidate['id']}").status_code == 409


def test_entities_without_votes_can_be_deleted(client):
    voter = create_voter(client).json()
    candidate = create_candidate(client).json()

    assert client.delete(f"/voters/{voter['id']}").status_code == 204
    assert client.delete(f"/candidates/{candidate['id']}").status_code == 204
