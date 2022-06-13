SELECT G.skill
FROM skill AS G
WHERE NOT EXISTS(
	SELECT MG.sportsman_id
	FROM sportsman_skill AS MG INNER JOIN sportsman
	ON MG.sportsman_id = sportsman.id
	WHERE sportsman.weight>76
	
	And MG.sportsman_id not in (
	SELECT MG2.sportsman_id
	FROM sportsman_skill AS MG2
	WHERE MG2.skill_id = G.id
	)
)

