import asyncio
import config


class SparqlError(Exception):
    """Raised when the SPARQL endpoint cannot be queried successfully."""


# How many times to retry a query that is rate-limited (429) or
# temporarily unavailable (502/503/504) before giving up.
_MAX_RETRIES = 5
# Base delay (seconds) for the exponential backoff, used when the
# endpoint does not send a Retry-After header.
_BASE_BACKOFF = 1.0


def _with_prefixes(query_string):
    """
    Prepend the instance-specific PREFIX declarations from the config so
    that wd:/wdt: (and any other configured prefixes) resolve to this
    Wikibase's own entities rather than the endpoint's defaults. Declaring
    them at query level overrides any defaults injected by the endpoint.
    """
    prefixes = getattr(config, 'sparql_prefixes', {})
    if not prefixes:
        return query_string
    header = ''.join(
        'PREFIX %s: <%s>\n' % (name, uri) for name, uri in prefixes.items())
    return header + query_string


async def sparql_wikidata(http_session, query_string):
    query_string = _with_prefixes(query_string)
    last_error = None
    for attempt in range(_MAX_RETRIES + 1):
        async with http_session.post(
                config.wikibase_sparql_endpoint,
                data={'query': query_string},
                params={'format': 'json'},
                headers={'User-Agent': config.user_agent}
                ) as r:
            if r.status == 200:
                results = await r.json()
                return results['results']

            # Read the body so the connection is released, and keep a
            # snippet around for diagnostics.
            body = await r.text()

            # Retry on rate limiting / transient upstream errors.
            if r.status in (429, 502, 503, 504) and attempt < _MAX_RETRIES:
                delay = _retry_after_seconds(r) or _BASE_BACKOFF * (2 ** attempt)
                await asyncio.sleep(delay)
                last_error = (r.status, body)
                continue

            raise SparqlError(
                'SPARQL endpoint %s returned HTTP %s: %s' % (
                    config.wikibase_sparql_endpoint, r.status, body[:500]))

    status, body = last_error
    raise SparqlError(
        'SPARQL endpoint %s still returning HTTP %s after %d retries: %s' % (
            config.wikibase_sparql_endpoint, status, _MAX_RETRIES, body[:500]))


def _retry_after_seconds(response):
    """
    Parse the Retry-After header (delta-seconds form) if present.
    Returns None if the header is absent or not an integer number of seconds.
    """
    value = response.headers.get('Retry-After')
    if not value:
        return None
    try:
        return float(value)
    except ValueError:
        return None
