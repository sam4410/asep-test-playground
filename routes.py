import base64
import hashlib
import hmac
import json
import re
import secrets
import time
from datetime import date, datetime, timezone
from decimal import Decimal, InvalidOperation

from functools import wraps

from flask import Blueprint, current_app, g, jsonify, request
from sqlalchemy.exc import IntegrityError

from models import Product, Transaction, User, db
from models import Product, User, db

bp = Blueprint('products', __name__)

@bp.route('/api/products', methods=['GET'])
def get_products():
    products = Product.query.all()
    return jsonify([{'id': product.id, 'name': product.name, 'price': product.price} for product in products])

@bp.route('/api/products', methods=['POST'])
def create_product():
    data = request.get_json()
    name = data.get('name')
    price = data.get('price')

    if not name or price is None:
        return jsonify({'error': 'Name and price are required'}), 400

    try:
        product = Product(name=name, price=price)
        db.session.add(product)
        db.session.commit()
    except Exception as e:
        return jsonify({'error': str(e)}), 400

    return jsonify({'id': product.id, 'name': product.name, 'price': product.price}), 201

def register_routes(app):
    app.register_blueprint(bp)


_EMAIL_RE = re.compile(
    r"^[A-Za-z0-9.!#$%&'*+/=?^_`{|}~-]+@[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}"
    r"[A-Za-z0-9])?(?:\.[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?)+$"
)
_PASSWORD_ITERATIONS = 310_000


def _json_error(message, status):
    return jsonify({"error": message}), status


def _user_payload(user):
    return {
        "id": user.id,
        "email": user.email,
        "created_at": user.created_at.isoformat() if user.created_at else None,
    }


def _hash_password(password):
    salt = secrets.token_bytes(16)
    digest = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt,
        _PASSWORD_ITERATIONS,
    )
    return "pbkdf2_sha256${}${}${}".format(
        _PASSWORD_ITERATIONS,
        _b64encode(salt),
        _b64encode(digest),
    )


def _verify_password(password, encoded):
    try:
        algorithm, iterations, salt, expected = encoded.split("$", 3)
        if algorithm != "pbkdf2_sha256":
            return False
        actual = hashlib.pbkdf2_hmac(
            "sha256",
            password.encode("utf-8"),
            _b64decode(salt),
            int(iterations),
        )
        return hmac.compare_digest(actual, _b64decode(expected))
    except (TypeError, ValueError):
        return False


def _b64encode(value):
    return base64.urlsafe_b64encode(value).rstrip(b"=").decode("ascii")


def _b64decode(value):
    return base64.urlsafe_b64decode(value + "=" * (-len(value) % 4))


def _issue_token(user):
    now = int(time.time())
    payload = {
        "sub": str(user.id),
        "iat": now,
        "exp": now + int(current_app.config.get("AUTH_TOKEN_TTL_SECONDS", 3600)),
        "jti": secrets.token_hex(16),    }
    encoded_payload = _b64encode(
        json.dumps(payload, separators=(",", ":"), sort_keys=True).encode("utf-8")
    )
    message = "v1." + encoded_payload
    signature = hmac.new(
        str(current_app.config["SECRET_KEY"]).encode("utf-8"),
        message.encode("ascii"),
        hashlib.sha256,
    ).digest()
    return message + "." + _b64encode(signature)


def _decode_token(token):
    try:
        version, encoded_payload, encoded_signature = token.split(".", 2)
        if version != "v1":
            return None
        message = version + "." + encoded_payload
        expected_signature = hmac.new(
            str(current_app.config["SECRET_KEY"]).encode("utf-8"),
            message.encode("ascii"),
            hashlib.sha256,
        ).digest()
        if not hmac.compare_digest(
            expected_signature,
            _b64decode(encoded_signature),
        ):
            return None
        payload = json.loads(_b64decode(encoded_payload))
        if (
            not isinstance(payload, dict)
            or not isinstance(payload.get("sub"), str)
            or not isinstance(payload.get("jti"), str)
            or int(payload.get("exp", 0)) <= int(time.time())
        ):
            return None
        revoked = current_app.extensions.setdefault("revoked_auth_tokens", set())
        if payload["jti"] in revoked:
            return None
        return payload
    except (TypeError, ValueError, KeyError, json.JSONDecodeError, OverflowError):
        return None


def _bearer_token():
    authorization = request.headers.get("Authorization", "")
    scheme, _, token = authorization.partition(" ")
    if scheme.lower() != "bearer" or not token:
        return None
    return token.strip()


def require_auth(view):
    """Require a valid bearer token and expose the authenticated user as g.current_user."""
    @wraps(view)
    def authenticated_view(*args, **kwargs):
        token = _bearer_token()
        payload = _decode_token(token) if token else None
        user = User.query.filter_by(id=payload["sub"]).first() if payload else None
        if user is None:
            return _json_error("Authentication required", 401)
        g.current_user = user
        g.auth_token = token
        return view(*args, **kwargs)

    return authenticated_view


@bp.route("/api/auth/signup", methods=["POST"])
def signup():
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return _json_error("A JSON object is required", 400)

    email = data.get("email")
    password = data.get("password")
    if not isinstance(email, str) or not _EMAIL_RE.fullmatch(email.strip()):
        return _json_error("A valid email is required", 400)
    if not isinstance(password, str) or not 8 <= len(password) <= 128:
        return _json_error("Password must be between 8 and 128 characters", 400)

    normalized_email = email.strip().lower()
    if User.query.filter_by(email=normalized_email).first():
        return _json_error("An account with that email already exists", 409)

    user = User(email=normalized_email, hashed_password=_hash_password(password))
    db.session.add(user)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return _json_error("An account with that email already exists", 409)

    return jsonify({
        "token": _issue_token(user),
        "user": _user_payload(user),
    }), 201


@bp.route("/api/auth/login", methods=["POST"])
def login():
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return _json_error("A JSON object is required", 400)
    email = data.get("email")
    password = data.get("password")
    if not isinstance(email, str) or not isinstance(password, str):
        return _json_error("Email and password are required", 400)

    user = User.query.filter_by(email=email.strip().lower()).first()
    if user is None or not _verify_password(password, user.hashed_password):
        return _json_error("Invalid email or password", 401)

    return jsonify({
        "token": _issue_token(user),
        "user": _user_payload(user),
    })


@bp.route("/api/auth/me", methods=["GET"])
@require_auth
def me():
    return jsonify({"user": _user_payload(g.current_user)})


@bp.route("/api/auth/logout", methods=["POST"])
@require_auth
def logout():
    payload = _decode_token(g.auth_token)
    current_app.extensions.setdefault("revoked_auth_tokens", set()).add(payload["jti"])
    return jsonify({"message": "Logged out successfully"})


def _parse_amount(value):
    """Return an integer number of cents, rejecting imprecise monetary values."""
    if isinstance(value, bool) or value is None:
        raise ValueError("amount must be a positive number")

    try:
        amount = Decimal(str(value).strip())
    except (InvalidOperation, AttributeError):
        raise ValueError("amount must be a positive number")

    if not amount.is_finite() or amount <= 0:
        raise ValueError("amount must be a positive number")
    if amount.as_tuple().exponent < -2:
        raise ValueError("amount must have no more than two decimal places")

    cents = amount * 100
    if cents != cents.to_integral_value() or cents > Decimal("999999999999"):
        raise ValueError("amount is out of range")
    return int(cents)


def _parse_transaction_date(value):
    if not isinstance(value, str) or not value.strip():
        raise ValueError("date must be an ISO-8601 date")
    try:
        return date.fromisoformat(value.strip())
    except ValueError:
        raise ValueError("date must be an ISO-8601 date")


def _parse_transaction_type(value):
    if not isinstance(value, str) or value not in ("income", "expense"):
        raise ValueError("type must be either income or expense")
    return value


def _parse_category(value):
    if not isinstance(value, str):
        raise ValueError("category is required")
    category = value.strip()
    if not category or len(category) > 100:
        raise ValueError("category must be between 1 and 100 characters")
    return category


def _parse_note(value):
    if value is None:
        return None
    if not isinstance(value, str) or len(value) > 2000:
        raise ValueError("note must be a string of at most 2000 characters")
    return value


def _transaction_payload(transaction):
    return {
        "id": transaction.id,
        "amount": f"{transaction.amount_cents / 100:.2f}",
        "type": transaction.transaction_type,
        "category": transaction.category,
        "date": transaction.transaction_date.isoformat(),
        "note": transaction.note,
        "created_at": (
            transaction.created_at.isoformat()
            if transaction.created_at
            else None
        ),
        "updated_at": (
            transaction.updated_at.isoformat()
            if transaction.updated_at
            else None
        ),
    }


def _transaction_error(message):
    return _json_error(message, 400)


@bp.route("/api/transactions", methods=["POST"])
@require_auth
def create_transaction():
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return _transaction_error("A JSON object is required")

    try:
        if "amount" not in data:
            raise ValueError("amount is required")
        if "type" not in data:
            raise ValueError("type is required")
        if "category" not in data:
            raise ValueError("category is required")
        if "date" not in data:
            raise ValueError("date is required")

        transaction = Transaction(
            user_id=g.current_user.id,
            amount_cents=_parse_amount(data["amount"]),
            transaction_type=_parse_transaction_type(data["type"]),
            category=_parse_category(data["category"]),
            transaction_date=_parse_transaction_date(data["date"]),
            note=_parse_note(data.get("note")),
        )
        db.session.add(transaction)
        db.session.commit()
    except ValueError as exc:
        db.session.rollback()
        return _transaction_error(str(exc))
    except Exception:
        db.session.rollback()
        return _json_error("Unable to create transaction", 400)

    return jsonify(_transaction_payload(transaction)), 201


@bp.route("/api/transactions", methods=["GET"])
@require_auth
def list_transactions():
    transactions = (
        Transaction.query
        .filter_by(user_id=g.current_user.id)
        .order_by(
            Transaction.transaction_date.desc(),
            Transaction.created_at.desc(),
        )
        .all()
    )
    return jsonify([_transaction_payload(item) for item in transactions])


@bp.route("/api/transactions/<transaction_id>", methods=["PATCH"])
@require_auth
def update_transaction(transaction_id):
    transaction = Transaction.query.filter_by(
        id=transaction_id,
        user_id=g.current_user.id,
    ).first()
    if transaction is None:
        return _json_error("Transaction not found", 404)

    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return _transaction_error("A JSON object is required")
    if not data:
        return _transaction_error("At least one field is required")

    allowed_fields = {"amount", "type", "category", "date", "note"}
    unknown_fields = set(data) - allowed_fields
    if unknown_fields:
        return _transaction_error("Unknown transaction field")

    try:
        if "amount" in data:
            transaction.amount_cents = _parse_amount(data["amount"])
        if "type" in data:
            transaction.transaction_type = _parse_transaction_type(data["type"])
        if "category" in data:
            transaction.category = _parse_category(data["category"])
        if "date" in data:
            transaction.transaction_date = _parse_transaction_date(data["date"])
        if "note" in data:
            transaction.note = _parse_note(data["note"])

        db.session.commit()
    except ValueError as exc:
        db.session.rollback()
        return _transaction_error(str(exc))
    except Exception:
        db.session.rollback()
        return _json_error("Unable to update transaction", 400)

    return jsonify(_transaction_payload(transaction))


@bp.route("/api/transactions/<transaction_id>", methods=["DELETE"])
@require_auth
def delete_transaction(transaction_id):
    transaction = Transaction.query.filter_by(
        id=transaction_id,
        user_id=g.current_user.id,
    ).first()
    if transaction is None:
        return _json_error("Transaction not found", 404)

    db.session.delete(transaction)
    try:
        db.session.commit()
    except Exception:
        db.session.rollback()
        return _json_error("Unable to delete transaction", 400)

    return jsonify({"message": "Transaction deleted successfully"})


def _dashboard_month(value):
    """Return an explicit UTC calendar-month range for a dashboard request."""
    if value is None:
        selected = datetime.now(timezone.utc).date()
    else:
        try:
            selected = datetime.strptime(value, "%Y-%m").date()
        except (TypeError, ValueError):
            raise ValueError("month must use YYYY-MM format")

    start = selected.replace(day=1)
    if start.month == 12:
        next_month = start.replace(
            year=start.year + 1,
            month=1,
        )
    else:
        next_month = start.replace(month=start.month + 1)
    return start, next_month.replace(day=next_month.day - 1)


def _currency_amount(amount_cents):
    """Serialize cents without passing through binary floating-point arithmetic."""
    return format(
        (Decimal(amount_cents) / Decimal("100")).quantize(Decimal("0.01")),
        "f",
    )


def _dashboard_transaction_payload(transaction):
    payload = _transaction_payload(transaction)
    payload["amount_cents"] = transaction.amount_cents
    payload["formatted_amount"] = (
        f"${_currency_amount(transaction.amount_cents)}"
    )
    return payload


@bp.route("/api/dashboard/summary", methods=["GET"])
@require_auth
def dashboard_summary():
    try:
        month_start, month_end = _dashboard_month(request.args.get("month"))
    except ValueError as exc:
        return _json_error(str(exc), 400)

    user_id = g.current_user.id
    all_transactions = Transaction.query.filter_by(user_id=user_id).all()
    monthly_transactions = (
        Transaction.query
        .filter(
            Transaction.user_id == user_id,
            Transaction.transaction_date >= month_start,
            Transaction.transaction_date <= month_end,
        )
        .order_by(
            Transaction.transaction_date.desc(),
            Transaction.created_at.desc(),
        )
        .all()
    )
    recent_transactions = (
        Transaction.query
        .filter_by(user_id=user_id)
        .order_by(
            Transaction.transaction_date.desc(),
            Transaction.created_at.desc(),
        )
        .limit(10)
        .all()
    )

    total_income_cents = sum(
        item.amount_cents
        for item in all_transactions
        if item.transaction_type == "income"
    )
    total_expense_cents = sum(
        item.amount_cents
        for item in all_transactions
        if item.transaction_type == "expense"
    )
    monthly_income_cents = sum(
        item.amount_cents
        for item in monthly_transactions
        if item.transaction_type == "income"
    )
    monthly_spending_cents = sum(
        item.amount_cents
        for item in monthly_transactions
        if item.transaction_type == "expense"
    )

    category_totals = {}
    for item in monthly_transactions:
        if item.transaction_type == "expense":
            category_totals[item.category] = (
                category_totals.get(item.category, 0) + item.amount_cents
            )

    category_spending = []
    for category, amount_cents in sorted(
        category_totals.items(),
        key=lambda entry: (-entry[1], entry[0].casefold()),
    ):
        percentage = (
            Decimal(amount_cents * 100) / Decimal(monthly_spending_cents)
            if monthly_spending_cents
            else Decimal("0")
        )
        category_spending.append({
            "category": category,
            "amount": _currency_amount(amount_cents),
            "amount_cents": amount_cents,
            "formatted_amount": f"${_currency_amount(amount_cents)}",
            "percentage": format(percentage.quantize(Decimal("0.01")), "f"),
        })

    return jsonify({
        "period": {
            "month": month_start.strftime("%Y-%m"),
            "start": month_start.isoformat(),
            "end": month_end.isoformat(),
            "timezone": "UTC",
        },
        "currency": "USD",
        "total_balance": _currency_amount(
            total_income_cents - total_expense_cents
        ),
        "total_balance_cents": total_income_cents - total_expense_cents,
        "monthly_income": _currency_amount(monthly_income_cents),
        "monthly_income_cents": monthly_income_cents,
        "monthly_spending": _currency_amount(monthly_spending_cents),
        "monthly_spending_cents": monthly_spending_cents,
        "category_spending": category_spending,
        "spending_by_category": category_spending,
        "recent_transactions": [
            _dashboard_transaction_payload(item)
            for item in recent_transactions
        ],
    })
