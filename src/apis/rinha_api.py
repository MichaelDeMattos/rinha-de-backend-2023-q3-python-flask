# -*- coding: utf-8 -*-

import json
import traceback
from database import db, redis_client
from sqlalchemy.sql import or_
from models.rinha_model import Pessoa
from utils.rinha_util import date_is_valid, stack_is_valid, generate_uuid
from flask import Blueprint, make_response, jsonify, request


api_rinha_backend_bp = Blueprint("rinha_api", __name__)

@api_rinha_backend_bp.route("/pessoas", methods=["POST"])
def api_rinha_backend_create_pessoa() -> make_response:
    try:
        if request.method == "POST":
            body = request.data
            if not body:
                return make_response(
                    "422 - Unprocessable Entity/Content."), 422
            body_parse = json.loads(body)
            is_valid_request = True
            message = ""
            if not isinstance(body_parse.get("apelido"), str) or \
              redis_client.get(body_parse.get("apelido")) or \
              len(body_parse.get("apelido")) == 0 or \
              len(body_parse.get("apelido")) > 32:
                is_valid_request = False
                message += " | apelido is invalid | "
            if not isinstance(body_parse.get("nome"), str) or \
              len(body_parse.get("nome")) == 0 or \
               len(body_parse.get("nome")) > 100:
                is_valid_request = False
                message += " | nome is invalid | "
            if not isinstance(body_parse.get("nascimento"), str) or \
              len(body_parse.get("nascimento").split("-")) != 3 or \
              not date_is_valid(date=body_parse.get("nascimento")):
                is_valid_request = False
                message += " | nascimento is invalid | "
            if not stack_is_valid(stack=body_parse.get("stack")):
                is_valid_request = False
                message += " | stack is invalid | "
            if not is_valid_request:
                return make_response(
                    "422 - Unprocessable Entity/Content."), 422
            try:
                with db.session() as session:
                    uuid1 = generate_uuid()
                    cache_pessoa_object = json.dumps([{
                        "id": uuid1,
                        "apelido": body_parse.get("apelido"),
                        "nome": body_parse.get("nome"),
                        "nascimento": body_parse.get("nascimento"),
                        "stack": body_parse.get("stack")}])
                    redis_client.set(uuid1, cache_pessoa_object)
                    redis_client.set(body_parse.get("apelido"), "1")
                    new_pessoa = Pessoa(
                        id=uuid1,
                        apelido=body_parse.get("apelido"),
                        nome=body_parse.get("nome"),
                        nascimento=body_parse.get("nascimento"),
                        stack=[x.lower() for x in body_parse.get("stack")] \
                               if body_parse.get("stack") else None)
                    session.add(new_pessoa)
                    session.commit()
                    resp = make_response(
                        f"http://localhost:9999/pessoas/{uuid1}")
                    resp.headers["location"] = f"http://localhost:9999" \
                                               f"/pessoas/{uuid1}"
                    return resp, 201
            except Exception as error:
                session.rollback()
                return make_response(
                    "422 - Unprocessable Entity/Content."), 422
    except Exception:
        return make_response("503 - Internal server error!!!"), 503

@api_rinha_backend_bp.route("/pessoas/<string:pessoa_id>", methods=["DELETE"])
def api_rinha_backend_delete_pessoa(
    pessoa_id: str = None) -> make_response:
    try:
        url_param_id = pessoa_id
        # invalid pattern
        if not url_param_id or not isinstance(url_param_id, str):
            return make_response("400 - bad"), 400
        try:
            with db.session() as session:
                pessoa = session.query(Pessoa).filter_by(
                    id=url_param_id).first()
                redis_client.delete(url_param_id)
                redis_client.delete(pessoa.apelido)
                session.query(Pessoa).filter_by(
                    id=url_param_id).delete()
                session.commit()
                return make_response("200 - OK"), 200
        except Exception as error:
            return make_response("422 - Unprocessable Entity/Content."), 422
    except Exception:
        return make_response("503 - Internal server error!!!"), 503

@api_rinha_backend_bp.route("/pessoas", methods=["GET"])
def api_rinha_backend_get_pessoa_by_term(
    pessoa_id: str = None) -> make_response:
    try:
        url_param_t = request.args.get("t")
        pessoas = []
        # invalid pattern
        if not url_param_t or not isinstance(url_param_t, str):
            return make_response("400 - bad"), 400
        with db.session() as session:
            search_objects = session.query(
                    Pessoa).filter(or_(
                        Pessoa.nome.match(url_param_t),
                        Pessoa.apelido.match(url_param_t),
                        Pessoa.stack.any(url_param_t.lower()))).limit(50).all()
            for search_object in search_objects:
                pessoas.append({
                    "id": search_object.id,
                    "apelido": search_object.apelido,
                    "nome": search_object.nome,
                    "nascimento": search_object.nascimento,
                    "stack": [
                        x.capitalize() for x in search_object.stack] \
                        if search_object.stack else None})
            return make_response(pessoas, 200)
    except Exception:
        return make_response("503 - Internal server error!!!"), 503

@api_rinha_backend_bp.route("/pessoas/<string:pessoa_id>", methods=["GET"])
def api_rinha_backend_get_pessoa_by_id(
    pessoa_id: str = None) -> make_response:
    try:
        url_param_id = pessoa_id
        pessoas = []
        # invalid pattern
        if not url_param_id or not isinstance(url_param_id, str):
            return make_response("400 - bad"), 400
        # check redis cache by search_id
        if url_param_id and \
            isinstance(url_param_id, str) and \
            redis_client.get(url_param_id):
            return make_response(json.loads(
                redis_client.get(url_param_id)), 200)
        with db.session() as session:
            search_object = session.query(
                Pessoa).filter_by(id=url_param_id).first()
            if search_object:
                pessoas.append({
                    "id": search_object.id,
                    "apelido": search_object.apelido,
                    "nome": search_object.nome,
                    "nascimento": search_object.nascimento,
                    "stack": [
                        x.capitalize() for x in search_object.stack] \
                        if search_object.stack else None})
            if pessoas:
                return make_response(pessoas, 200)
            else:
                return make_response([], 404)
    except Exception:
        return make_response("503 - Internal server error!!!"), 503

@api_rinha_backend_bp.route("/contagem-pessoas", methods=["GET"])
def api_rinha_backend_contagem_pessoas():
    try:
        if request.method == "GET":
            with db.session() as session:
                total_pessas = session.query(Pessoa).count()
                return f"{total_pessas}", 200
    except Exception:
        return make_response("503 - Internal server error!!!"), 503
