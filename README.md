# Wikibase OpenRefine Reconciliation Service

A reconciliation service that lets [OpenRefine](https://openrefine.org/) match tabular data against items in a [wikibase.cloud](https://www.wikibase.cloud/) instance. It is an adaptation of the [openrefine-wikibase](https://github.com/wetneb/openrefine-wikibase) service, configured here for a Wikibase instance hosted on wikibase.cloud (`shira.wikibase.cloud`).

For a step-by-step tutorial, see the accompanying blog post:
https://www.library.upenn.edu/kislak/judaicadh/blog/wikibasecloudreconcile

## What it does

OpenRefine's reconciliation feature matches cells in a dataset to entities in a knowledge base. This service exposes a [Reconciliation API](https://reconciliation-api.github.io/specs/latest/) backed by your Wikibase instance, so you can:

- Match column values to existing Wikibase items
- Disambiguate matches using values from other columns
- Preview matched items inline in OpenRefine

## Requirements

The target Wikibase instance should have:

- An associated SPARQL query service
- A type system analogous to Wikidata's `instance of` / `subclass of` (configurable in `config.py`)
- (Recommended) the [CirrusSearch extension](https://www.mediawiki.org/wiki/Extension:CirrusSearch) for better search

Locally you need **Python 3.7+**. Redis is optional — the service falls back to an in-process `fakeredis` cache when no Redis server is configured.

## Installation

```bash
# 1. Clone the repository
git clone https://github.com/<your-username>/wikibaseopenrefine
cd wikibaseopenrefine

# 2. Create and activate a virtual environment
python3 -m venv env
source env/bin/activate          # on Windows: env\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt
```

## Configuration

All settings live in [`config.py`](config.py). Edit it to point at your own Wikibase instance — at minimum update:

- `wikibase_url` — base URL of your Wikibase (e.g. `https://shira.wikibase.cloud`)
- `wikibase_namespace_id` — `120` for most wikibase.cloud instances (`0` for Wikidata)
- The property/item IDs used for the type system (`type_property_path`, the SPARQL queries, etc.)

To use a real Redis server instead of the in-process fallback, set:

```python
redis_uri = 'redis://localhost:6379/0?encoding=utf-8'
```

## Running

```bash
python app.py
```

The service starts on `http://localhost:8000/`. In OpenRefine, open the **Start reconciling** dialog, add a standard reconciliation service, and enter:

```
http://localhost:8000/en/api
```

(replace `en` with another language code as needed).

## Testing

```bash
pip install -r requirements.txt   # includes pytest and test deps
pytest
```

## Documentation

Further documentation (architecture, scoring, configuration details) is in the [`docs/`](docs/) directory and can be built with Sphinx:

```bash
pip install -r docs/requirements.txt
make -C docs html
```

## License

See [LICENSE](LICENSE).
