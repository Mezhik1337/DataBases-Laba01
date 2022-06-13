SELECT M.name
FROM sportsman M
WHERE M.name != 'Voloshin Dmitro'
AND NOT EXISTS
(SELECT sportsman_skill.skill_id
  FROM sportsman_skill
	INNER JOIN sportsman ON sportsman_skill.sportsman_id = sportsman.id
  WHERE sportsman.name = 'Voloshin Dmitro'
 AND sportsman_skill.skill_id Not In
(SELECT sportsman_skill.skill_id
  FROM sportsman_skill
  WHERE sportsman_skill.sportsman_id = M.id))