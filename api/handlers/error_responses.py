"""
Module to return missing fields
"""
from flask import jsonify, request


class ReturnError:
    """
    Class with methods to return specific error messages
    """

    @staticmethod
    def missing_fields(keys):
        return jsonify({"status": "fail",
                        "error_message": "This field/fields are missing",
                        "data": keys}), 400

    @staticmethod
    def invalid_data_type(data_type, field):
        if data_type == "int":
            response_object = {
                "status": "fail",
                "error_message": "Only {} data type supported for {}".format(data_type, field),
                "data": False}
        else:
            response_object = {
                "status": "fail",
                "error_message": "Only {} data type supported for {}".format(data_type, field),
                "data": False}

        return jsonify(response_object), 400

    @staticmethod
    def empty_fields(value):
        response_object = {
            "status": "fail",
            "error_message": "{} is a required field".format(value)}
        return jsonify(response_object), 400

    @staticmethod
    def invalid_password():
        response_object = {
            "status": "fail",
            "error_message": "Password is wrong. It should be at-least 6 characters"
                             " long, and alphanumeric."}
        return jsonify(response_object), 400

    @staticmethod
    def invalid_email():
        req = request.get_json()
        response_object = {
            "status": "fail",
            "error_message": "User email {0} is wrong, It should be "
                             "in the format (xxxxx@xxxx.xxx)".format(req['email'])
        }
        return jsonify(response_object), 400

    @staticmethod
    def email_already_exists():
        response_object = {
            'status': 'fail',
            'error_message': 'email already exists',
        }
        return jsonify(response_object), 409

    @staticmethod
    def invalid_name():
        response_object = {
            "status": "fail",
            "error_message": "A name should consist of only alphabetic characters"
        }
        return jsonify(response_object), 400

    @staticmethod
    def invalid_user_type():
        req = request.get_json()
        response_object = {
            "status": "fail",
            "error_message": "User type {0} does not exist ".format(req['user_type'])
        }
        return jsonify(response_object), 400
