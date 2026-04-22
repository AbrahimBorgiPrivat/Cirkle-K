SET search_path TO "default_data", public;
DROP VIEW IF EXISTS "default_data"."simple_date_view_2017_18";
CREATE OR REPLACE VIEW "default_data"."simple_date_view_2017_18" AS
SELECT date_actual,
    day_name,
    day_of_week,
    day_of_month,
    day_of_quarter,
    day_of_year,
    week_of_month,
    week_of_year,
        CASE
            WHEN week_of_year <> 1 AND month_actual = 1 AND week_of_month = 1 THEN 0
            WHEN week_of_year = 1 AND month_actual = 12 THEN 53
            ELSE week_of_year
        END AS week_of_year_conv,
    "substring"(week_of_year_iso::text, 1, 8) AS week_year,
    month_actual,
    month_name,
    quarter_actual,
    concat('Q', quarter_actual) AS quarter,
    year_actual,
    first_day_of_week,
    last_day_of_week,
    first_day_of_month,
    last_day_of_month,
    first_day_of_quarter,
    last_day_of_quarter,
    first_day_of_year,
    last_day_of_year,
        CASE
            WHEN month_actual < 10 THEN concat(year_actual, '0', month_actual)::bigint
            ELSE concat(year_actual, month_actual)::bigint
        END AS yyyymm,
    weekend_indr
   FROM default_data.d_date
  WHERE date_part('year'::text, date_actual) >= 2017::double precision AND date_part('year'::text, date_actual) <= '2018'::double precision;
RESET search_path;
