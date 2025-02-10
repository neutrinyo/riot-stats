from pulsefire.schemas import RiotAPISchema


def patch_bounty_gold(match: RiotAPISchema.LolMatchV5Match) ->  RiotAPISchema.LolMatchV5Match:
    '''
        Temporary patching measure - Riot's new bounty system uses float values for bounty gold now,
        Pulsefire is still using integers. Will be removed once the type gets replaced.
    '''

    for participant in match['info']['participants']:
        participant['challenges']['bountyGold'] = round(participant['challenges']['bountyGold'])

    return match

def get_champions_list(match_data: RiotAPISchema.LolMatchV5Match) -> list[str]:
    champions = []
    for participant in match_data['info']['participants']:
        champions.append(participant['championName'])

    return champions

def filter_match_events_based_on_type(match_timeline: RiotAPISchema.LolMatchV5MatchTimeline,
                                      event_types: list[str]
                                     ) -> list[RiotAPISchema.LolMatchV5MatchTimelineInfoFrameEvent]:
    #todo - zmienic te obrzydliwa definicje
    filtered_events = []
    for frame in match_timeline['info']['frames']:
        for event in frame['events']:
            if event['type'] in event_types:
                filtered_events.append(event)

    return filtered_events
