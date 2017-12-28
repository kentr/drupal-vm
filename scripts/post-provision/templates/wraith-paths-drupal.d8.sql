SET SESSION group_concat_max_len = 1000000;
SELECT
  GROUP_CONCAT(
    CONCAT(
    '  ', TYPE, '..',   REPLACE(path, '/', '__'), ':', "\n"
    '    ', 'path: ', path
    )
    ORDER BY TYPE, path
    SEPARATOR "\n"
  ) AS `paths:`
FROM (
  -- NODES
  SELECT
    title
    , CONCAT('node..', `type`) AS `type`
    , path
  FROM
    (
    SELECT
      nfr.title
      , n.type
      , alias.alias AS path
    FROM
      node n
      JOIN node_field_revision nfr
        ON n.nid = nfr.nid
        AND n.vid = nfr.vid
      JOIN url_alias alias
        ON alias.source = CONCAT('/node/', n.nid)
    WHERE (
        n.nid IN (
          SELECT
            *
          FROM (
            SELECT
              nid
            FROM
              node_field_revision nids
            WHERE
              nids.title RLIKE '^[[:<:]]About[[:>:]]'
              AND nids.status = 1
            ORDER BY
              nids.nid
              , vid DESC
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
              node_field_revision nids
            WHERE
              nids.title RLIKE '[[:<:]]Mission[[:>:]]'
              AND nids.status = 1
            ORDER BY
              nids.nid
              , vid DESC
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
              node_field_revision nids
            WHERE
              nids.title RLIKE '[[:<:]]Services[[:>:]]'
              AND nids.status = 1
            ORDER BY
              nids.nid
              , vid DESC
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
              node_field_revision nids
            WHERE
              nids.title RLIKE '[[:<:]]Staff[[:>:]]'
              AND nids.status = 1
            ORDER BY
              nids.nid
              , vid DESC
            LIMIT 1
          ) t
        )
      )

      OR (
        n.nid IN (
          SELECT
            MIN(nids.nid)
          FROM
            node nids
            JOIN node_field_revision nfr
              USING(nid, vid)
          WHERE
            nfr.status = 1
          GROUP BY
            nids.type
        )
      )


    ORDER BY
      n.type
      , nfr.changed DESC
    ) t
  -- /NODES

  UNION

  -- MISC
  SELECT DISTINCT
    title
    , 'misc' AS `type`
    , REPLACE(link__uri, 'internal:', '') AS path
  FROM
    menu_link_content_data
    LEFT JOIN url_alias alias
      ON CONCAT('internal:', alias.alias) = link__uri
  WHERE
    link__uri NOT LIKE 'entity:node%'
    AND alias.source IS NULL
  -- /MISC

  ) AS `ALL`
