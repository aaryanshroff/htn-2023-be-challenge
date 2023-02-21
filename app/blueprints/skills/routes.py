from collections import defaultdict
from flask import current_app, jsonify, request
from app.blueprints.skills import bp
from app.models.skill import Skill
from app.extensions import cache

CacheKey = str


@bp.get('/')
def get_skills():
    '''Get all unique skill names and frequency of occurrence'''
    logger = current_app.logger

    min_freq = request.args.get('min_frequency')
    max_freq = request.args.get('max_frequency')

    # Check if the filtered skill counts are already cached
    cache_key = _get_cache_key(min_freq, max_freq)
    logger.info(f'Checking cache for key: {cache_key}')
    skill_freqs = cache.get(cache_key)
    if skill_freqs:
        return jsonify(skill_freqs)

    # Calculate the raw skill counts if they are not cached
    skills = Skill.query.all()
    skill_freqs = defaultdict(int)
    for skill in skills:
        skill_freqs[skill.name] += 1

    # Filter the skill counts based on min_freq and max_freq
    if min_freq:
        skill_freqs = {name: freq for name,
                       freq in skill_freqs.items() if freq >= int(min_freq)}
    if max_freq:
        skill_freqs = {name: freq for name,
                       freq in skill_freqs.items() if freq <= int(max_freq)}

    # Cache the filtered skill counts
    cache.set(cache_key, skill_freqs)

    # Convert the skill_counts dictionary to a list of dictionaries
    skill_list = [{'name': name, 'frequency': freq}
                  for name, freq in skill_freqs.items()]

    return jsonify(skill_list)


def _get_cache_key(min_freq: str, max_freq: str) -> CacheKey:
    '''Get the cache key for the current request'''

    if min_freq and max_freq:
        cache_key = f'skill_counts_{min_freq}_{max_freq}'
    elif min_freq:
        cache_key = f'skill_counts_{min_freq}'
    else:
        cache_key = 'skill_counts'

    return cache_key
