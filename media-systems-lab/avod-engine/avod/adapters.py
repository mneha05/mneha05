from __future__ import annotations

from dataclasses import dataclass
from urllib.parse import urlencode

from .models import AdRequest


@dataclass(frozen=True)
class FreeWheelStyleAdapter:
    """Builds a vendor-shaped request boundary; does not perform a live vendor call."""

    network_id: str
    profile: str
    endpoint: str = "https://example.invalid/freewheel/ad/g/1"

    def build_request(self, request: AdRequest) -> dict[str, str]:
        params = {
            "nw": self.network_id,
            "prof": self.profile,
            "csid": request.placement,
            "caid": request.request_id,
            "metr": "1031",
            "country": request.country,
            "device": request.device,
            "genre": request.genre,
        }
        return {"method": "GET", "url": f"{self.endpoint}?{urlencode(params)}"}


@dataclass(frozen=True)
class GoogleAdManagerStyleAdapter:
    """Builds a GAM-shaped video ad tag boundary; no account or credential is implied."""

    ad_unit: str
    endpoint: str = "https://example.invalid/gampad/ads"

    def build_request(self, request: AdRequest) -> dict[str, str]:
        custom = urlencode(
            {"country": request.country, "device": request.device, "genre": request.genre}
        )
        params = {
            "iu": self.ad_unit,
            "env": "vp",
            "output": "vast",
            "unviewed_position_start": "1",
            "correlator": request.request_id,
            "cust_params": custom,
        }
        return {"method": "GET", "url": f"{self.endpoint}?{urlencode(params)}"}
