# -*- coding: utf-8 -*-

from flask import jsonify
from apps.messages import (
    MSG_INVALID_DATA, MSG_DOES_NOT_EXIST, MSG_EXCEPTION, MSG_ALREADY_EXISTS, MSG_MESSAGES_MUST_BE_STRING, MSG_PERMISSION_DENIED,
)

def resp_data_invalid(resource :str, errors :dict=[], msg :str= MSG_INVALID_DATA, description :str=""):
    """
    Responses 422
    """

    if not isinstance(resource, str):
        raise ValueError(MSG_MESSAGES_MUST_BE_STRING)

    resp = jsonify({
        "resource": resource,
        "message": msg,
        "errors": errors,
        "description": description,
    })

    resp.status_code = 422

    return resp

def resp_exception(resource :str, description :str="", msg :str = MSG_EXCEPTION):
    """
    Responses 500
    """

    if not isinstance(resource, str):
        raise ValueError(MSG_MESSAGES_MUST_BE_STRING)

    resp = jsonify({
        "resource": resource,
        "message": msg,
        "description": description
    })

    resp.status_code = 500

    return resp

def resp_resource_not_exists(resource : str, description :str, resource_id: str): 
    """
    Responses 404
    """

    if not isinstance(resource, str):
        raise ValueError(MSG_MESSAGES_MUST_BE_STRING)

    resp = jsonify({
        "resource": resource,
        "message": MSG_DOES_NOT_EXIST.format(description, resource_id) 
    })

    resp.status_code = 404

    return resp

def resp_does_not_exist_resources(resource : str, description :str):
    """
    Responses 404
    """

    if not isinstance(resource, str):
        raise ValueError(MSG_MESSAGES_MUST_BE_STRING)

    resp = jsonify({
        "resource": resource,
        "message": MSG_NO_RESOURCE_REGISTERED.format(description) 
    })

    resp.status_code = 404

    return resp
def resp_already_exists(resource :str, description :str):
    """
    Responses 400
    """

    if not isinstance(resource, str):
        raise ValueError(MSG_MESSAGES_MUST_BE_STRING)

    resp = jsonify({
        "resource": resource,
        "message": MSG_ALREADY_EXISTS.format(description),
    })

    resp.status_code = 400

    return resp

def resp_ok(resource :str, message :str, data=None, **extras):
    """
    responses 200
    """

    response = {"status": 200, "message": message, "resource": resource}

    if data:
        response["data"] = data

    response.update(extras)

    resp = jsonify(response)

    resp.status_code = 200

    return resp

def resp_ok_no_content():
    """
    Response 204 - No Content
    Used in response to delete operation
    """

    resp = jsonify()
    resp.status_code = 200

    return resp

def resp_notallowed_user(resource :str, msg :str=MSG_PERMISSION_DENIED):
    if not isinstance(resource, str):
        raise ValueError(MSG_MESSAGES_MUST_BE_STRING)

    resp = jsonify({
        "status": 401,
        "resourece": resource,
        "message": msg,
    })

    return resp
