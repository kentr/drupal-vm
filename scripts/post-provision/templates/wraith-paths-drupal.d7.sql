SET SESSION group_concat_max_len = 1000000;
SELECT
  GROUP_CONCAT(
    CONCAT(
      '  ', TYPE, '..__',   REPLACE(path, '/', '__'), ':', "\n"
      '    ', 'path: ', '/', path
    )
    ORDER BY TYPE, path
    SEPARATOR "\n"
  ) as `paths:`
FROM (
  -- NODES
  SELECT
    t.title
    , CONCAT('node..', `type`) AS `type`
    , t.path
  FROM (
    SELECT
      n.title
      , n.type
      , alias.alias AS path
    FROM
      node n
      JOIN node_revision nr
        USING(nid)
      JOIN url_alias alias
        ON alias.source = CONCAT('node/', n.nid)
    WHERE (
        n.nid IN (
          SELECT
            *
          FROM (
            SELECT
              nid
            FROM
              node nids
            WHERE
              nids.title LIKE 'about%'
              AND nids.status = 1
            ORDER BY
              nids.nid
            LIMIT 1
          ) t
        )
      )
      OR (
        n.nid IN (
          SELECT
            *
          FROM (
            SELECT
              nid
            FROM
              node nids
            WHERE
              nids.title LIKE '%staff%'
              AND nids.status = 1
            ORDER BY
              nids.nid
            LIMIT 1
          ) t
        )
      )
      OR (
        n.nid IN (
          SELECT
            *
          FROM (
            SELECT
              nid
            FROM
              node nids
            WHERE
              nids.title LIKE '%mission%'
              AND nids.status = 1
            ORDER BY
              nids.nid
            LIMIT 1
          ) t
        )
      )
      OR (
        n.nid IN (
          SELECT
            MIN(nid)
          FROM
            node nids
          WHERE
            nids.status = 1
          GROUP BY
            nids.type
        )
      )
      AND alias.pid IN (
        SELECT
          MAX(pid)
        FROM
          url_alias pids
        WHERE
          pids.source = CONCAT('node/', n.nid)
      ) -- /AND alias.pid IN
    ORDER BY
      n.type
      , n.changed DESC
  ) t
  -- /NODES

{% if page_manager_table_exists | default(False) %}
  UNION

  -- PANELS
  SELECT
    admin_title AS `title`
    , 'panels_page' AS TYPE
    , path
  FROM page_manager_pages
  WHERE
    access = 'a:0:{}'
  -- /PANELS
{% endif %}

  UNION

  -- VIEWS
  SELECT
    CONCAT(human_name, '..', display_title) AS `title`
    , 'view' AS `type`
    , PREG_CAPTURE('/}s:4:"path";s:\\d+:"(.*?)";/', display_options, 1) AS path
  FROM views_display
  JOIN views_view
    USING (vid)
  WHERE
    display_plugin = 'page'
  HAVING path NOT LIKE 'admin/%'
  -- VIEWS

  ) AS `ALL`
