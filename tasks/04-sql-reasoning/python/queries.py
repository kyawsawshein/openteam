# tasks/04‑sql‑reasoning/python/queries.py
from pathlib import Path

# --- path to donations.db --------------------------------------------------
DB_PATH = Path(__file__).resolve().parent.parent / "donations.db"

# --- Task A ---------------------------------------------------------------
SQL_A = """
        SELECT * FROM (
            SELECT  cp.id AS campaign_id
            ,       SUM(amount_thb) AS total_thb
            ,       ROUND(SUM(ROUND(amount_thb, 4))/cp.target_thb, 4) AS pct_of_target
            FROM campaign cp
                INNER JOIN pledge pd ON pd.campaign_id=cp.id
            GROUP BY cp.id
        )
        ORDER BY pct_of_target DESC
"""
# Solution: Select the total_thb and pct_of_targe join pledge  group with campaing_id
#.          and then wrape the get total select and order with pct_of_target
# --- Task B ---------------------------------------------------------------
SQL_B = """
        WITH scope_pledges AS (
            SELECT  'global' AS scope
            ,       p.amount_thb
            FROM pledge AS p

            UNION ALL

            SELECT  'thailand' AS scope
            ,       p.amount_thb
            FROM pledge AS p
                JOIN donor AS d ON d.id = p.donor_id
            WHERE d.country = 'Thailand'
        ),
        ranked_pledges AS (
            SELECT	scope
            ,		amount_thb
            ,		ROW_NUMBER() OVER (PARTITION BY scope ORDER BY amount_thb) AS row_num
            ,		COUNT(*) OVER (PARTITION BY scope) AS total_count
            FROM scope_pledges
        )
        SELECT	scope
        ,		amount_thb AS p90_thb
        FROM ranked_pledges
        WHERE row_num = CEILING(0.9 * total_count)
        ORDER BY CASE scope WHEN 'global' THEN 0 ELSE 1 END;
"""
# Solution :  Select subquery using WITH for the scope and amount_thb to temp scope_pledges
#             and then select the  row and count from scope_pledges with window functions to temp ranked_pledges
#             after select scope and p90_thb of ceil(0.9 * n) and order the global first
#             Taken time: 2hr
#             ref: ChatGPT

# --- (skipped) indexes -----------------------------------------------------
INDEXES: list[str] = ["CREATE INDEX index_campaign_target_thb ON campaign (target_thb)",  # using in WHERE CLAUSE
                      "CREATE INDEX index_donor_country ON donor (country)"               # using in WHERE CLAUSE
                    ]
# left empty on purpose
