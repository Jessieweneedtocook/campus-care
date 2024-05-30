from flask import jsonify, Blueprint

from flask_jwt_extended import jwt_required, get_jwt_identity
from extensions import db
from models import User

admin_bp = Blueprint('admin', __name__)


@admin_bp.route("/admin_delete_account", methods=["DELETE"])
@jwt_required()
def admin_delete_account(data):
    try:
        # Retrieve the current user's username
        current_user = get_jwt_identity()['username']
        # Find the current user in the database
        user = db.session.query(User).filter(User.username == current_user).first()
        # If the user has the Admin role, then search the database for the user to delete
        if user.role == "Admin":
            deleted_user = data.get("delete_username")
            deleted_user = db.session.query(User).filter(User.username == deleted_user).first()
            # If the deleted user is found then delete the user from the database and commit the changes
            if deleted_user:
                db.session.delete(deleted_user)
                db.session.commit()
                return jsonify({"status": "success", "message": "Account deleted successfully"}), 200
            else:
                # If the user is not found then throw error 404
                return jsonify({"status": "success", "message": "Account not found"}), 404
        else:
            # If the user does not have the Admin role, then throw error 403
            return jsonify({"status": "error", "message": "Role required is admin"}), 403
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@admin_bp.route("/view_users", methods=["GET"])
@jwt_required()
def view_users(data):
    try:
        # Retrieve and extract all the usernames from the database
        users = db.session.query(User.username).all()
        usernames = [user.username for user in users]
        # Return a list of all usernames
        return jsonify({"status": "success", "usernames": usernames})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


admin_actions = {
    "admin_delete_account": admin_delete_account,
    "view_users": view_users,
}
