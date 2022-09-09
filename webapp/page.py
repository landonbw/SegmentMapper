from flask import current_app, request, Blueprint

bp = Blueprint("pages", __name__, url_prefix='/pages')

@bp.route('/test')
def test():
    return "testing"