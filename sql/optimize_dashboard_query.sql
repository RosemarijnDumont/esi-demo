SELECT
  dd.id,
  dd.user_id,
  dd.data_field_1,
  dd.data_field_2,
  dd.created_at
FROM
  dashboard_data dd
WHERE
  dd.user_id = :user_id
  AND dd.created_at >= NOW() - INTERVAL 1 MONTH
ORDER BY
  dd.created_at DESC;