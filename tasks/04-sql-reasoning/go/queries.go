// tasks/04‑sql‑reasoning/go/queries.go
package queries

// Task A
const SQLA = `
		SELECT * FROM (
			SELECT  cp.id AS campaign_id
			,       SUM(amount_thb) AS total_thb
			,       ROUND(SUM(ROUND(amount_thb, 4))/cp.target_thb, 4) AS pct_of_target
			FROM campaign cp
				INNER JOIN pledge pd ON pd.campaign_id=cp.id
			GROUP BY cp.id
		)
		ORDER BY pct_of_target DESC
`

// Task B
const SQLB = `
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
        WHERE row_num = ROUND(0.9 * total_count + 0.5)
        ORDER BY CASE scope WHEN 'global' THEN 0 ELSE 1 END;
`

var Indexes = []string{"CREATE INDEX index_campaign_target_thb ON campaign (target_thb)",
						"CREATE INDEX index_donor_country ON donor (country)"} // skipped
