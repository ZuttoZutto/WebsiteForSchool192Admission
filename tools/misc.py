from flask import make_response

def make_resp(message, status):
    resp = make_response(message, status)
    resp.headers["Content-type"] = "application/json; charset=utf-8"
    return resp

def check_keys(dct, keys):
    return all(key in dct for key in keys)

