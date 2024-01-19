>>> theseus = s2py.user('theseus2')

>>> theseus.exists()
True

>>> theseus.getStatus()
''
>>> theseus.getProjects()
{'ring6': [25635894, '2021-03-27T00:52:57.000Z'], 'recpipe': [55922182,
'2015-04-11T03:24:17.000Z'], 'ring6 copy': [25636022, '2014-08-20T03:58:
47.000Z']}

>>> ring = s2py.project('25635894')

>>> ring.
ring.getAssets(    ring.getComments(  ring.getInfo(      ring.getStats(
ring.id

>>> ring.getStats()
{'views': 2, 'loves': 0, 'favorites': 0, 'remixes': 0}

>>> ring.getComments()
[{'id': 379563672, 'parent_id': None, 'commentee_id': None, 'content':
'Awesome.', 'datetime_created': '2024-01-19T16:27:57.000Z',
'datetime_modified': '2024-01-19T16:27:57.000Z', 'visibility': 'visible',
'author': {'id': 17958708, 'username': 'Mechachleopteryx', 'scratchteam':
False, 'image': 'https:
//cdn2.scratch.mit.edu/get_image/user/17958708_60x60.png'},
'reply_count': 0}]
