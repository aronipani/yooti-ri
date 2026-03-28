-- Apache AGE extension init
-- Runs automatically on first docker compose up
CREATE EXTENSION IF NOT EXISTS age;
LOAD 'age';
SET search_path = ag_catalog, "$user", public;

-- Create default graph
SELECT create_graph('yooti-ri_graph');
