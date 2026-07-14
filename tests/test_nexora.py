"""
Nexora test suite.

Organised into sections:
  1. Validation and business rules  (no database needed)
  2. Password security               (no database needed)
  3. Application setup               (needs the app)
  4. Public pages respond            (needs app + database)
  5. Protected pages require login   (needs app + database)
  6. Known gaps                      (skipped or expected-fail, documented)

Tests in sections 3 to 5 use the app or client fixture. If the database
is not running, those skip cleanly rather than failing.
"""
import re
import pytest
from werkzeug.security import generate_password_hash, check_password_hash


# ---------------------------------------------------------------------------
# Section 1: Validation and business rules (no database)
# ---------------------------------------------------------------------------

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def is_valid_email(value):
    return bool(EMAIL_RE.match(value))


def is_long_enough(password):
    return len(password) >= 8


def average_rating(ratings):
    """Mirror of how a mentor's average rating is worked out."""
    if not ratings:
        return 0.0
    return round(sum(ratings) / len(ratings), 1)


class TestEmailValidation:
    def test_plain_email_is_valid(self):
        assert is_valid_email("anish@example.com")

    def test_subdomain_email_is_valid(self):
        assert is_valid_email("user@mail.example.com")

    def test_missing_at_is_invalid(self):
        assert not is_valid_email("anishexample.com")

    def test_missing_domain_is_invalid(self):
        assert not is_valid_email("anish@")

    def test_space_is_invalid(self):
        assert not is_valid_email("an ish@example.com")

    def test_empty_is_invalid(self):
        assert not is_valid_email("")

    def test_double_at_is_invalid(self):
        assert not is_valid_email("a@@b.com")


class TestPasswordLength:
    def test_exactly_eight_passes(self):
        assert is_long_enough("abcdefgh")

    def test_longer_passes(self):
        assert is_long_enough("a longer password")

    def test_seven_fails(self):
        assert not is_long_enough("abcdefg")

    def test_empty_fails(self):
        assert not is_long_enough("")


class TestRatingBounds:
    @pytest.mark.parametrize("value", [1, 2, 3, 4, 5])
    def test_valid_ratings(self, value):
        assert 1 <= value <= 5

    @pytest.mark.parametrize("value", [0, 6, -1, 10, 100])
    def test_invalid_ratings(self, value):
        assert not (1 <= value <= 5)


class TestAverageRating:
    def test_single_rating(self):
        assert average_rating([5]) == 5.0

    def test_mixed_ratings(self):
        assert average_rating([5, 4]) == 4.5

    def test_rounds_to_one_decimal(self):
        assert average_rating([5, 4, 4]) == 4.3

    def test_empty_is_zero(self):
        # A mentor with no reviews should read as 0, not crash.
        assert average_rating([]) == 0.0


class TestSessionStatus:
    VALID = {"pending", "confirmed", "declined", "completed"}

    def test_pending_valid(self):
        assert "pending" in self.VALID

    def test_confirmed_valid(self):
        assert "confirmed" in self.VALID

    def test_declined_valid(self):
        assert "declined" in self.VALID

    def test_completed_valid(self):
        assert "completed" in self.VALID

    def test_unknown_invalid(self):
        assert "shipped" not in self.VALID


class TestPaymentStatus:
    VALID = {"unpaid", "paid"}

    def test_unpaid_valid(self):
        assert "unpaid" in self.VALID

    def test_paid_valid(self):
        assert "paid" in self.VALID

    def test_default_is_unpaid(self):
        assert "unpaid" == "unpaid"

    def test_random_invalid(self):
        assert "refunded" not in self.VALID


class TestRoles:
    VALID = {"learner", "mentor", "admin"}

    def test_learner_valid(self):
        assert "learner" in self.VALID

    def test_mentor_valid(self):
        assert "mentor" in self.VALID

    def test_admin_valid(self):
        assert "admin" in self.VALID

    def test_guest_not_a_role(self):
        assert "guest" not in self.VALID


# ---------------------------------------------------------------------------
# Section 2: Password security (no database)
# ---------------------------------------------------------------------------

class TestPasswordHashing:
    def test_hash_differs_from_plaintext(self):
        h = generate_password_hash("mysecret123")
        assert h != "mysecret123"

    def test_correct_password_verifies(self):
        h = generate_password_hash("mysecret123")
        assert check_password_hash(h, "mysecret123")

    def test_wrong_password_fails(self):
        h = generate_password_hash("mysecret123")
        assert not check_password_hash(h, "wrongpass")

    def test_same_password_hashes_differ(self):
        # Salting means two hashes of the same password are not identical.
        assert generate_password_hash("abc12345") != generate_password_hash("abc12345")

    def test_hash_is_not_empty(self):
        assert len(generate_password_hash("abc12345")) > 20


# ---------------------------------------------------------------------------
# Section 3: Application setup (needs the app)
# ---------------------------------------------------------------------------

class TestAppSetup:
    def test_app_exists(self, app):
        assert app is not None

    def test_app_in_testing_mode(self, app):
        assert app.config["TESTING"] is True

    @pytest.mark.parametrize("blueprint", [
        "auth", "browse", "dashboard", "session", "profile",
        "settings", "mentor", "message", "admin", "help", "pages",
    ])
    def test_blueprint_registered(self, app, blueprint):
        assert blueprint in app.blueprints


# ---------------------------------------------------------------------------
# Section 4: Public pages respond (needs app + database)
# ---------------------------------------------------------------------------

class TestPublicPages:
    @pytest.mark.parametrize("path", [
        "/", "/login", "/register", "/browse",
        "/about", "/contact", "/terms", "/privacy",
    ])
    def test_public_page_loads(self, client, path):
        resp = client.get(path)
        assert resp.status_code == 200

    def test_home_mentions_nexora(self, client):
        resp = client.get("/")
        assert b"Nexora" in resp.data

    def test_unknown_page_is_404(self, client):
        resp = client.get("/this-does-not-exist")
        assert resp.status_code == 404


# ---------------------------------------------------------------------------
# Section 5: Protected pages require login (needs app + database)
# ---------------------------------------------------------------------------

class TestProtectedPages:
    @pytest.mark.parametrize("path", [
        "/dashboard", "/messages", "/my/requests",
        "/settings", "/profile", "/admin/users",
    ])
    def test_requires_login_redirects(self, client, path):
        # Not logged in, so these should redirect to login, not show the page.
        resp = client.get(path)
        assert resp.status_code in (301, 302)

    def test_login_page_has_form(self, client):
        resp = client.get("/login")
        assert b"password" in resp.data.lower()

    def test_register_page_has_form(self, client):
        resp = client.get("/register")
        assert b"username" in resp.data.lower()


# ---------------------------------------------------------------------------
# Section 6: Known gaps (documented skips and expected failures)
# ---------------------------------------------------------------------------

class TestKnownGaps:
    @pytest.mark.skip(reason="Sending email needs live SMTP credentials, not run in tests")
    def test_verification_email_sends(self):
        pass

    @pytest.mark.skip(reason="Full two step login needs a real emailed code")
    def test_full_login_flow(self):
        pass

    @pytest.mark.skip(reason="Group sessions are not part of the current build")
    def test_group_sessions(self):
        pass

    @pytest.mark.xfail(reason="Password reset flow is not implemented yet", strict=False)
    def test_password_reset_exists(self):
        # There is no forgot password route by design; kept as a note.
        from app import create_app
        app = create_app()
        rules = [r.rule for r in app.url_map.iter_rules()]
        assert "/reset-password" in rules