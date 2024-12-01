import pandas as pd
from sqlalchemy import text

from src.db_conn import session


query = text('''
SELECT
  CONCAT('https://vk.com/id', CAST(u.id_vk AS INTEGER)) AS "Автор",
  CONCAT('https://vk.com/', LOWER(p.type::TEXT), u.id_vk, '_', p.id_vk) as "Ссылка на публикацию",
  ps.views AS "Просмотры",
  CONCAT(
    'https://vk.com/id',
    CAST((SELECT u3.id_vk from users u3 where u3.id = a.user_id LIMIT 1) AS INTEGER)
  ) 
  AS "Профиль активного пользователя",
  p.type AS "Тип публикации",
  a.type AS "Тип активности",
  u2.sex AS "Пол",
  COALESCE(ct.name, c.name) AS "Регион или город",
  CASE WHEN u2.birthday > CURRENT_DATE - INTERVAL '18' YEAR THEN 1 ELSE 0 END AS "до 18",
  CASE WHEN u2.birthday BETWEEN CURRENT_DATE - INTERVAL '25' YEAR AND CURRENT_DATE - INTERVAL '18' YEAR THEN 1 ELSE 0 END AS "18-25",
  CASE WHEN u2.birthday BETWEEN CURRENT_DATE - INTERVAL '35' YEAR AND CURRENT_DATE - INTERVAL '25' YEAR THEN 1 ELSE 0 END AS "25-35",
  CASE WHEN u2.birthday BETWEEN CURRENT_DATE - INTERVAL '45' YEAR AND CURRENT_DATE - INTERVAL '35' YEAR THEN 1 ELSE 0 END AS "35-45",
  CASE WHEN u2.birthday < CURRENT_DATE - INTERVAL '45' YEAR THEN 1 ELSE 0 END AS "после 45"
FROM publications p
JOIN users u ON u.id = p.user_id
JOIN publication_snapshots ps ON ps.publication_id = p.id
JOIN activities a ON a.publication_id = p.id
JOIN users u2 ON u2.id = a.user_id
LEFT JOIN cities ct ON ct.id = u2.city_id
LEFT JOIN countries c ON c.id = u2.country_id
''')


params = []
filename = "report.xlsx"


data_frame = pd.read_sql(query, session.connection(), params=params)

xlsx_params = {'strings_to_urls': False}

with pd.ExcelWriter(filename, engine="xlsxwriter", engine_kwargs={'options': xlsx_params}) as writer:
    data_frame.to_excel(writer, index=False, sheet_name='Ozon')