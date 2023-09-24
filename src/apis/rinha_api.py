# -*- coding: utf-8 -*-

import json
import traceback
from database import db
from sqlalchemy.sql import or_
from models.rinha_model import Pessoa
from flask import Blueprint, make_response, jsonify, request


api_rinha_backend_bp = Blueprint("rinha_api", __name__)


@api_rinha_backend_bp.route("/pessoas", methods=["GET", "POST", "DELETE"])
async def api_rinha_backend_pessoas() -> make_response:
    try:
        if request.method == "GET":
            url_param_id = request.args.get("id")
            url_param_t = request.args.get("t")
            pessoas = []
            # invalid pattern
            if not url_param_id and not url_param_t:
                return make_response(
                    jsonify({
                        "message": "400 - bad",
                        "response": "Invalid query params",
                        "status": 400}), 400)
            with db.session() as session:
                # find by id
                if url_param_id:
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
                # find by term
                if url_param_t:
                    search_objects = session.query(
                        Pessoa).filter(or_(
                            Pessoa.nome.match(url_param_t),
                            Pessoa.apelido.match(url_param_t),
                            Pessoa.stack.any(url_param_t.lower()))).all()
                    for search_object in search_objects:
                        pessoas.append({
                            "id": search_object.id,
                            "apelido": search_object.apelido,
                            "nome": search_object.nome,
                            "nascimento": search_object.nascimento,
                            "stack": [
                                x.capitalize() for x in search_object.stack] \
                                if search_object.stack else None})
                if pessoas:
                    return make_response(
                        jsonify({
                            "message": "200 - OK",
                            "response": pessoas,
                            "status": 200}), 200)
                else:
                    return make_response(
                        jsonify({
                            "message": "404 - NOT FOUND",
                            "response": [],
                            "status": 404}), 404)
        elif request.method == "POST":
            body = request.data
            if not body:
                return make_response(
                    jsonify({
                        "response": "Invalid body request",
                        "message": "422 - Unprocessable Entity/Content.",
                        "status": 422}), 422)
            body_parse = json.loads(body)
            try:
                with db.session() as session:
                    new_pessoa = Pessoa(
                        apelido=body_parse.get("apelido"),
                        nome=body_parse.get("nome"),
                        nascimento=body_parse.get("nascimento"),
                        stack=[x.lower() for x in body_parse.get("stack")] \
                               if body_parse.get("stack") else None)
                    session.add(new_pessoa)
                    session.commit()
                    return make_response(
                        jsonify({
                            "response":
                                f"http://localhost:80" \
                                f"/pessoas?id={new_pessoa.id}",
                            "message": "201 - created",
                            "status": 201}), 201)
            except Exception as error:
                session.rollback()
                traceback.print_exc()
                return make_response(
                    jsonify({
                        "response": str(error),
                        "message": "422 - Unprocessable Entity/Content.",
                        "status": 422}), 422)
        elif request.method == "DELETE":
            url_param_id = request.args.get("id")
            # invalid pattern
            if not url_param_id:
                return make_response(
                    jsonify({
                        "message": "400 - bad",
                        "response": "Invalid query params",
                        "status": 400}), 400)
            try:
                with db.session() as session:
                    session.query(Pessoa).filter_by(id=url_param_id).delete()
                    session.commit()
                    return make_response(
                        jsonify({
                            "message": "200 - OK",
                            "response": "Record was deleted with successfully",
                            "status": 200}), 200)
            except Exception as error:
                return make_response(
                    jsonify({
                        "response": str(error),
                        "message": "422 - Unprocessable Entity/Content.",
                        "status": 422}), 422)
    except Exception:
        traceback.print_exc()
        return make_response(
            jsonify({
                "response": "Internal server error!!!",
                "status": 503}), 503)

@api_rinha_backend_bp.route("/contagem-pessoas", methods=["GET"])
async def api_rinha_backend_contagem_pessoas():
    try:
        if request.method == "GET":
            with db.session() as session:
                total_pessas = session.query(Pessoa).count()
                return make_response(
                    jsonify({
                        "response": total_pessas,
                        "message": "200 - OK",
                        "status": 200}), 200)
    except Exception:
        return make_response(
            jsonify({
                "response": "Internal server error!!!",
                "status": 503}), 503)
