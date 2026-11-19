from urllib.parse import urlparse
import ipaddress
import re


def extract_url_features(url):
    """Extract the 9 features used by url_only_model.joblib."""

    original_url = url.strip()

    if not original_url:
        raise ValueError("Please enter a URL.")

    if any(char.isspace() for char in original_url):
        raise ValueError("Please enter a valid URL without spaces.")

    # Add http:// when scheme is missing
    normalized_url = (
        original_url
        if re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*://", original_url)
        else "http://" + original_url
    )

    parsed = urlparse(normalized_url)
    hostname = (parsed.hostname or "").lower()

    if not hostname:
        raise ValueError("Please enter a valid URL with a hostname.")

    # Validate port
    try:
        port_number = parsed.port
    except ValueError:
        raise ValueError("Please enter a valid port number.")

    # Check whether hostname is an IP address
    try:
        ipaddress.ip_address(hostname)
        is_ip_address = True
        has_ip = 1
    except ValueError:
        is_ip_address = False
        has_ip = -1

    # Basic hostname validation
    if not is_ip_address and hostname != "localhost":

        if "." not in hostname:
            raise ValueError(
                "Please enter a valid domain name or IP address."
            )

        if (
            hostname.startswith(".")
            or hostname.endswith(".")
            or ".." in hostname
            or any(
                not re.fullmatch(r"[a-zA-Z0-9-]+", part)
                or part.startswith("-")
                or part.endswith("-")
                for part in hostname.rstrip(".").split(".")
            )
        ):
            raise ValueError("Please enter a valid hostname.")

    # ---------------------------------------------------------
    # 1. IP Address
    # ---------------------------------------------------------
    having_ip = has_ip

    # ---------------------------------------------------------
    # 2. URL Length
    # Dataset:
    # -1 = short
    #  0 = medium
    #  1 = long
    # ---------------------------------------------------------
    url_length = len(original_url)

    if url_length < 54:
        url_length_feature = -1
    elif url_length <= 75:
        url_length_feature = 0
    else:
        url_length_feature = 1

    # ---------------------------------------------------------
    # 3. URL Shortening Service
    # ---------------------------------------------------------
    shortening_domains = {
        "bit.ly",
        "tinyurl.com",
        "t.co",
        "goo.gl",
        "ow.ly",
        "is.gd",
        "buff.ly",
        "cutt.ly",
        "shorturl.at",
        "rebrand.ly",
    }

    shortening_feature = (
        1 if hostname in shortening_domains else -1
    )

    # ---------------------------------------------------------
    # 4. @ Symbol
    # ---------------------------------------------------------
    at_symbol_feature = (
        1 if "@" in original_url else -1
    )

    # ---------------------------------------------------------
    # 5. Double slash redirecting
    # ---------------------------------------------------------
    double_slash_feature = (
        1 if "//" in parsed.path else -1
    )

    # ---------------------------------------------------------
    # 6. Prefix / Suffix
    #
    # Dataset:
    # -1 = hyphen exists
    #  1 = no hyphen
    # ---------------------------------------------------------
    prefix_suffix_feature = (
        -1 if "-" in hostname else 1
    )

    # ---------------------------------------------------------
    # 7. Subdomain
    #
    # IP address / localhost -> no subdomain
    # ---------------------------------------------------------
    if is_ip_address or hostname == "localhost":
        subdomain_feature = -1
    else:
        host_parts = hostname.rstrip(".").split(".")
        subdomain_count = max(0, len(host_parts) - 2)

        if subdomain_count == 0:
            subdomain_feature = -1
        elif subdomain_count == 1:
            subdomain_feature = 0
        else:
            subdomain_feature = 1

    # ---------------------------------------------------------
    # 8. Port
    #
    # Only explicit non-standard port is flagged.
    # ---------------------------------------------------------
    standard_port = (
        443 if parsed.scheme.lower() == "https" else 80
    )

    port_feature = (
        1
        if port_number is not None and port_number != standard_port
        else -1
    )

    # ---------------------------------------------------------
    # 9. HTTPS token
    #
    # Checks whether "https" appears in hostname.
    # ---------------------------------------------------------
    https_token_feature = (
        1 if "https" in hostname else -1
    )

    # ---------------------------------------------------------
    # FINAL 9 FEATURES
    # Order MUST match the trained model
    # ---------------------------------------------------------
    features = {
        "having_IPhaving_IP_Address": having_ip,
        "URLURL_Length": url_length_feature,
        "Shortining_Service": shortening_feature,
        "having_At_Symbol": at_symbol_feature,
        "double_slash_redirecting": double_slash_feature,
        "Prefix_Suffix": prefix_suffix_feature,
        "having_Sub_Domain": subdomain_feature,
        "port": port_feature,
        "HTTPS_token": https_token_feature,
    }

    return features