"""
rename cols:
    BL:
    stage_name - comp_discipline
    stage_score - overall_score_boulder_and_lead
    stage_rank - discipline_rank
    score - discipline_score
    

add cols:
    B:
    comp_type - all=="Boulder"
    L:
    comp_type - all=="Lead"

merge the 4 datasets
add comp_discipline col with "Boulder", "Lead" acc to dataset source
merge stage_name from BL with comp_type 

delete unncessary columns: 
- category_round_id
- route_id


vital cols:
comp_discipline, str, '"Boulder" or "Lead"'
athlete_id, int, 'key variable: athlete identifier'
rank, int, '(order by) overall ranking within competition; different athlete_id can have the same rank for round_name being "Qualification" or "Semi-final" within one competition'
comp_name, str, '(group by 1) name of competition including city name and year'
round_name, str, '(group by 2) one of "Qualification", "Semi-final", or "Final"'

other cols:
- firstname, str, 'first name of athlete with first letter capitalized'
- lastname, str, 'last name of athlete in all capital letters'
- country, str, '_____ three-letter code of country'
- federation_id, int, '________'
- overall_score_boulder_and_lead, int, 'overall competition score for boulder'

create variables:

LATER:
create relational athlete datasets with
- athlete_id (key)
- firstname
- lastname

QUESTIONS:
order by vs group by
athlete_id vs federation_id
cols like overall_score_boulder_and_lead have ints and none, or 0 for none?

"""




# delete cols


# create variables: 
# % tops, 
# %finals made, 
# %semis, 
# cumulative participation count


# order according to "modified"? can't - incomplete data
# order according to comp, qual, semi, final
# (need comp list in order)
# % tops

# boulder 
# delete columns: 'status', 'category_round_id', 'speed_elimination_stages.participant.id', 'speed_elimination_stages.participant.lastname', 'speed_elimination_stages.participant.confirmed', 'speed_elimination_stages.participant.firstname', 'speed_elimination_stages.participant.dns', 'speed_elimination_stages.participant.athlete_id', 'speed_elimination_stages.participant.bib_number'

# move to right: 'route_id', 'category_round_id', 'federation_id'


1. per athlete # create variables: 
# % tops, 
# %finals made, 
# %semis, 
# cumulative participation count

2. regression

3. create time sensitive cumulative `% tops,  %finals made, %semis variables for predictive analysis