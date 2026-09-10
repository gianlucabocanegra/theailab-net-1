"""Unit tests: every page loads auth-nav.js, and auth-nav.js offers a Log In
link to anonymous visitors (not just My Account/Log Out to authenticated ones).

auth-nav.js runs client-side JS with no DOM test harness in this repo, so the
anonymous-branch check is a static assertion on the script source rather than
an executed-behavior test.
"""
from pathlib import Path

SITE_ROOT = Path(__file__).parent.parent
AUTH_NAV_JS = SITE_ROOT / "css" / "auth-nav.js"


def _rel(path):
    return str(path.relative_to(SITE_ROOT))


class TestAuthNavScriptIncludedEverywhere:
    def test_every_page_includes_auth_nav_script(self, parsed_pages):
        """Every HTML page must load css/auth-nav.js so the nav reflects
        login state consistently site-wide (previously missing on index.html,
        404.html, login.html, register.html, forgot-password.html, and
        reset-password.html)."""
        failures = []
        for path, _, soup in parsed_pages:
            scripts = [
                tag.get("src", "") for tag in soup.find_all("script")
                if tag.get("src", "").endswith("auth-nav.js")
            ]
            if not scripts:
                failures.append(_rel(path))
        assert not failures, f"Pages missing the auth-nav.js include: {failures}"


class TestAuthNavOffersLogInLink:
    def test_auth_nav_js_exists(self):
        assert AUTH_NAV_JS.exists(), "css/auth-nav.js is missing"

    def test_auth_nav_js_renders_a_login_link_for_anonymous_visitors(self):
        """auth-nav.js must inject a Log In link when the visitor is not
        authenticated, not just silently do nothing (the previous behavior)."""
        text = AUTH_NAV_JS.read_text(encoding="utf-8")
        assert "login.html" in text, (
            "auth-nav.js does not appear to reference login.html anywhere; "
            "it should render a Log In link for anonymous visitors."
        )
        assert "Log In" in text, (
            "auth-nav.js does not appear to render a 'Log In' label for "
            "anonymous visitors."
        )

    def test_auth_nav_js_still_handles_authenticated_and_admin_cases(self):
        """Guard against a rewrite accidentally dropping the existing
        authenticated-user behavior (My Account / Log Out / Admin Dashboard)."""
        text = AUTH_NAV_JS.read_text(encoding="utf-8")
        assert "My Account" in text
        assert "Log Out" in text
        assert "admin-dashboard-link" in text
