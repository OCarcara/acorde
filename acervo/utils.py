"""Utilidades gerais do app acervo."""

from __future__ import annotations

from urllib.parse import urljoin

from django.conf import settings


def build_absolute_media_url(path: str | None, request=None) -> str:
    """Retorna uma URL absoluta para um recurso de mídia."""
    if not path:
        return ""

    if hasattr(path, "url"):
        path = path.url  # type: ignore[assignment]

    if not isinstance(path, str):
        return ""

    if path.startswith(("http://", "https://")):
        return path

    site_base = getattr(settings, "SITE_BASE_URL", "").strip()
    if site_base:
        base = site_base if site_base.endswith("/") else f"{site_base}/"
        return urljoin(base, path.lstrip("/"))

    if request is not None:
        try:
            return request.build_absolute_uri(path)
        except Exception:  # noqa: BLE001
            pass

    return path

