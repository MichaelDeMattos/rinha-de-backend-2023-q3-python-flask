# -*- coding: utf-8 -*-

import os
import sys
import json
import time
import pytest
import os.path
sys.path.append(os.path.abspath(os.path.join(
    os.path.dirname(__file__), os.path.pardir)))
from app import app as my_app

records = [
    {
        "apelido" : "josé_silva",
        "nome" : "José Roberto",
        "nascimento" : "2000-10-01",
        "stack" : ["C#", "Node", "Oracle"]
    },
    {
        "apelido" : "ana_barbosa",
        "nome" : "Ana Barbosa",
        "nascimento" : "1985-09-23",
        "stack" : None
    }
]

created_records_id = []
terms_find_records = []

@pytest.fixture()
def app():
    app = my_app
    app.config.update({
        "TESTING": True,
    })
    yield app

@pytest.fixture()
def client(app):
    return app.test_client()

@pytest.fixture()
def runner(app):
    return app.test_cli_runner()

def test_create_record(client):
    for record in records:
        resp = client.post(
            "/pessoas",
            data=json.dumps(record))
        assert resp.status_code == 201
        resp_json = json.loads(resp.data)
        created_records_id.append(resp_json.get("response").split("?id=")[1])

def test_find_record_by_id(client):
    for record_id in created_records_id:
        resp = client.get(
            f"/pessoas?id={record_id}")
        assert resp.status_code == 200
        resp_json = json.loads(resp.data)
        terms_find_records.append(resp_json.get("response")[0].get("nome"))
        terms_find_records.append(
            resp_json.get("response")[0].get("apelido"))
        if resp_json.get("response")[0].get("stack"):
            for stack in resp_json.get("response")[0].get("stack"):
                terms_find_records.append(stack)

def test_find_record_by_term(client):
    for term in terms_find_records:
        resp = client.get(
            f"/pessoas?", query_string={"t": term})
        assert resp.status_code == 200

def test_count_total_records(client):
    resp = client.get("/contagem-pessoas")
    assert resp.status_code == 200
    resp_json = json.loads(resp.data)
    assert resp_json.get("response") >= len(records)

def test_delete_created_records(client):
    for record_id in created_records_id:
        resp = client.delete(
            f"/pessoas?id={record_id}")
        assert resp.status_code == 200
