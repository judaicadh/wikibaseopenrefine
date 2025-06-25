# Wikibase Open Refine Reconciliation Tutorial Files
Tutorial for creating a reconciliation service for wikibase.cloud for OpenRefine. For step-by-step documentation see https://www.library.upenn.edu/kislak/judaicadh/blog/wikibasecloudreconcile

* wikibase_namespace_id = 120
* wikibase_namespace_prefix = 'Item:'
* mediawiki_api_endpoint   = 'https://<your-instance>.wikibase.cloud/w/api.php'
* wikibase_sparql_endpoint = 'https://<your-instance>.wikibase.cloud/query/sparql'
* qid_url_pattern = 'https://<your-instance>.wikibase.cloud/wiki/Item:{{id}}'

| **Section / Variable**                        | **Purpose**                                                                                       |
|----------------------------------------------|---------------------------------------------------------------------------------------------------|
| `mediawiki_api_endpoint`                     | URL of your Wikibase Cloud API (used to search and fetch data).                                  |
| `wikibase_sparql_endpoint`                   | SPARQL endpoint for querying data from your Wikibase instance.                                    |
| `wikibase_name`                              | Display name of your Wikibase instance.                                                           |
| `wikibase_main_page`                         | Link to the main page of your Wikibase site (for documentation or UI linking).                   |
| `wikibase_namespace_id`                      | Numeric ID of the item namespace (usually 120 for Wikibase Cloud).                               |
| `wikibase_namespace_prefix`                  | Text prefix for items (e.g., `Item:`). Used to format links and lookups.                         |
| `user_agent`                                 | User agent string for API requests (good practice for bots/tools).                               |
| `q_re`, `p_re` and `_group_id`               | Regex patterns to extract Q-IDs and P-IDs from URLs.                                              |
| `identifier_space`, `schema_space`           | Used to define identifier and property IRIs in RDF output.                                       |
| `qid_url_pattern`                            | Template to create clickable URLs for Q-IDs.                                                      |
| `avoid_items_of_class`                       | Filters out internal/disambiguation items (e.g., categories).                                     |
| `service_name`                               | Human-readable name of your reconciliation service.                                               |
| `this_host`                                  | URL where your reconciliation service is running.                                                 |
| `default_num_results`                        | Default number of reconciliation candidates returned.                                             |
| `wd_api_max_search_results`                  | Max search results to fetch from Wikibase search (useful for fuzzy matches).                      |
| `validation_threshold`                       | Minimum score (0–100) for automatically matching an item.                                         |
| `redis_uri`, `redis_key_prefix`              | Redis connection URI and key prefix used for caching.                                             |
| `headers`                                    | HTTP headers (typically for identifying your bot).                                                |
| `zoom_ratio`, `preview_height`, `preview_width` | UI settings for preview card display in OpenRefine.                                            |
| `image_properties`                           | List of P-IDs that contain image values (e.g., `P18` in Wikidata).                               |
| `image_download_pattern`                     | URL template to retrieve images from filenames.                                                   |
| `fallback_image_url`, `fallback_image_alt`   | Image shown if an item has no image.                                                             |
| `autodescribe_endpoint`                      | Optional endpoint to auto-generate item descriptions.                                             |
| `default_type_entity`                        | Default item type to assume for reconciliation (e.g., "entity").                                 |
| `type_property_path`                         | Property used to infer the type of an item (e.g., `P39`).                                         |
| `property_for_this_type_property`            | Property used to get recommended properties for a given type (e.g., `P116`).                     |
| `wdt_prefix`                                 | Prefix used when generating SPARQL property paths (`wdt:` for direct claims).                     |
| `sparql_query_to_fetch_subclasses`           | Query to retrieve subclasses of a given class (`P40` used as subclass-of in your schema).         |
| `sparql_query_to_fetch_unique_id_properties` | Finds all properties that are external identifiers (used for reconciliation keys).               |
| `sparql_query_to_propose_properties`         | BFS query to suggest additional useful properties to show in OpenRefine UI.                      |
