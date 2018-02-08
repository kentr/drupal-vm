SET SESSION group_concat_max_len = 1000000;
SELECT
  CONCAT(
    "  home:\n"
    , "    path: /\n"
    , GROUP_CONCAT(
      CONCAT(
      '  ', TYPE, '..__',   REPLACE(path, '/', '__'), ':', "\n"
      '    ', 'path: ', '/', path
      )
      ORDER BY TYPE, path
      SEPARATOR "\n"
    )
  ) AS `paths`
FROM
  (
  SELECT
  *
  FROM
    -- Pages
    (
    SELECT
      post_title AS title
      , post_name AS path
      , post_type AS `type`
    FROM
      wp_posts
    WHERE
      post_status = 'publish'
      AND post_type = 'page'
      AND post_parent = 0
    ORDER BY post_date ASC
    LIMIT 10
    ) t

    UNION

    (
    SELECT
      post.post_title AS title
      , CONCAT(parent.post_name, '/', post.post_name) AS path
      , post.post_type AS `type`
    FROM
      wp_posts post
      JOIN wp_posts parent
        ON parent.ID = post.post_parent
    WHERE
      post.post_status = 'publish'
      AND post.post_type = 'page'
    ORDER BY post.post_date ASC
    LIMIT 5
    )

    UNION

    -- Posts
    (
    SELECT
      post_title AS title
      , CONCAT(wt.slug, '/', post_name) AS path
      , post_type AS `type`
    FROM
      wp_posts p
    JOIN wp_term_relationships wtr
      ON wtr.object_id = p.ID
    JOIN wp_term_taxonomy wtt
      USING(term_taxonomy_id)
    JOIN wp_terms wt
      USING(term_id)
    WHERE
      post_status = 'publish'
      AND post_type = 'post'
      AND wtt.taxonomy = 'category'

    ORDER BY post_date ASC
    LIMIT 5
    )

    UNION

    -- Categories
    (
    SELECT
      wt.name AS title
      , CONCAT('category/', wt.slug) AS path
      , 'category' AS `type`
    FROM
      wp_posts p
    JOIN wp_term_relationships wtr
      ON wtr.object_id = p.ID
    JOIN wp_term_taxonomy wtt
      USING(term_taxonomy_id)
    JOIN wp_terms wt
      USING(term_id)
    WHERE
      post_status = 'publish'
      AND post_type = 'post'
      AND wtt.taxonomy = 'category'

    ORDER BY post_date ASC
    LIMIT 3
    )
  ORDER BY `type`
  ) `all`
