import dominate # https://github.com/Knio/dominate
import dominate.tags as tags
from pathlib import Path
import json
import datetime
import humanize
import pandas
import logging

BORDER_RADIUS = '0.5em'
LIGHTER_TEXT_COLOR = '#878787'
DATES_FORMAT = '%b %Y'
FIELDS_SEPARATOR = '·'

def responsive_logo(**image_attributes):
	with tags.div(style='flex-shrink: 0; width: 50px;', cls='responsive_logo'):
		tags.img(width='100%',**image_attributes)

def generate_personal_data():
	with open('data/personal.json') as ifile:
		personal_data = json.load(ifile)
	with tags.div(style='display: flex; flex-direction: column; margin-top: 22px;'):
		for data in personal_data:
			with tags.div(
				style = f'display: flex; flex-direction: row; gap: 10px; padding: 10px; border-radius: {BORDER_RADIUS};',
				cls = 'highlight_on_hover'
			):
				with tags.div(style='flex-shrink: 0; width: 25px;'):
					tags.img(
						style = 'width: 100%; opacity: .7;',
						alt = data['field_name'],
						title = data['field_name'],
						**data['icon'],
					)
				with tags.div(style='display: flex; flex-direction: column;'):
					for s in data['content']:
						if data['field_name']=='Email':
							tags.a(s, href=f'mailto:{s}')
						elif data['field_name'] in {'Website','LinkedIn','GitHub','Stack Overflow'}:
							tags.a(s, href=s)
						else:
							tags.div(s)

def generate_experience():
	with open('data/experience/experience.json') as ifile:
		experience_data = json.load(ifile)
	with open('data/experience/employers.json') as ifile:
		employers_data = json.load(ifile)
	
	tags.h1('Experience', id='section_experience')
	with tags.div(style='display: flex; flex-direction: column;'):
		for experience in experience_data:
			with tags.div(
				style = f'display: flex; flex-direction: row; gap: 10px; padding: 10px; border-radius: {BORDER_RADIUS};',
				cls = 'highlight_on_hover',
			):
				employer_key = experience['employer']
				with tags.a(href=employers_data[employer_key]['website']):
					responsive_logo(
						alt = employers_data[employer_key]['name'], 
						title = employers_data[employer_key]['name'], 
						**employers_data[employer_key]['logo'],
					)
				with tags.div(style='display: flex; flex-direction: column; gap: 5px; max-width: 888px;'):
					tags.div(experience['position_name'], style='font-weight: bolder;')
					with tags.div():
						tags.span(employers_data[employer_key]['name'])
						tags.span(FIELDS_SEPARATOR)
						tags.span(experience['work_load'])
					with tags.div(style=f'font-weight: 100; color: {LIGHTER_TEXT_COLOR}'):
						start_date = datetime.datetime.strptime(experience['start_date'], '%b %Y')
						if experience['end_date'].lower() == 'present':
							end_date = datetime.datetime.today()
						else:
							end_date = datetime.datetime.strptime(experience['end_date'], '%b %Y')
						tags.span(start_date.strftime(DATES_FORMAT))
						tags.span('→')
						tags.span(end_date.strftime(DATES_FORMAT) if end_date.date()!=datetime.datetime.today().date() else 'Present')
						tags.span(FIELDS_SEPARATOR)
						tags.span(humanize.precisedelta(end_date-start_date, minimum_unit='months', format="%0.0f"))
					
					with tags.div(style=f'font-weight: 100; color: {LIGHTER_TEXT_COLOR}'):
						tags.span(employers_data[employer_key]['location'])
						tags.span(FIELDS_SEPARATOR)
						tags.span(experience['modality'])
					tags.div(experience['description'])
					if 'responsibilities' in experience:
						tags.div('Responsibilities:')
						with tags.ul(style='margin: 0px;'):
							for responsibility in experience['responsibilities']:
								tags.li(responsibility)

def generate_education(include_logos:bool=True):
	with open('data/education/education.json') as ifile:
		education_data = json.load(ifile)
	with open('data/education/schools.json') as ifile:
		schools_data = json.load(ifile)
	
	tags.h1('Education', id='section_education')
	with tags.div(style='display: flex; flex-direction: column;'):
		for education in education_data:
			with tags.div(
				style = f'display: flex; flex-direction: row; gap: 10px; padding: 10px; border-radius: {BORDER_RADIUS};',
				cls = 'highlight_on_hover',
			):
				school_key = education['school']
				if include_logos == True:
					responsive_logo(
						alt = schools_data[school_key]['name'], 
						title = schools_data[school_key]['name'], 
						**schools_data[school_key]['logo'],
					)
				with tags.div(style='display: flex; flex-direction: column; gap: 5px;'):
					with tags.div():
						tags.span(schools_data[school_key]['name'], style='font-weight: bolder;')
						with tags.span(style=f'font-weight: 100; color: {LIGHTER_TEXT_COLOR}'):
							tags.span(FIELDS_SEPARATOR)
							end_date = datetime.datetime.strptime(education['end_date'], '%b %Y')
							tags.span(end_date.strftime(DATES_FORMAT) if end_date.date()!=datetime.datetime.today().date() else 'Present')
					with tags.div():
						tags.span(education['degree_level'])
						tags.span(FIELDS_SEPARATOR)
						tags.span(education['field'])
					if 'thesis' in education:
						with tags.div():
							tags.span('Thesis: ' + education['thesis']['title'])

def generate_publications():
	with open('data/publications.json') as ifile:
		publications_data = json.load(ifile)
	
	tags.h1('Publications', id='section_publications')
	tags.p('Publications with main participation:')
	
	with tags.div(style='display: flex; flex-direction: column;'):
		for publication in publications_data:
			if publication['title'] == '':
				break
			with tags.div(
				style = f'display: flex; flex-direction: row; gap: 10px; padding: 10px; border-radius: {BORDER_RADIUS};',
				cls = 'highlight_on_hover',
			):
				responsive_logo(
					style = 'max-width: 100%; max-height: 100%; opacity: .4;',
					alt = 'Publication icon',
					src = 'https://static.thenounproject.com/png/1143700-200.png',
				)
				with tags.div(style='display: flex; flex-direction: column; gap: 1px;'):
					tags.div(publication['title'], style='font-weight: bold;')
					if all([_ in publication for _ in {'journal','publisher'}]):
						with tags.div():
							tags.span(publication['journal'])
							tags.span(FIELDS_SEPARATOR)
							tags.span(publication['publisher'])
					else:
						logging.warning(f'Publication {repr(publication["title"])} has no info for "journal" and or "publisher", will skip these fields for this particular publication.')
					with tags.div(style=f'font-weight: 100; color: {LIGHTER_TEXT_COLOR}'):
						tags.span(publication['publication_date'])
					if 'DOI' in publication:
						with tags.div(style=f'font-weight: 100; color: {LIGHTER_TEXT_COLOR}'):
							tags.span('DOI: ')
							tags.a(publication['DOI'], href=f'https://doi.org/{publication["DOI"]}')
					else:
						logging.warning(f'Publication {repr(publication["title"])} has no info for "DOI", will skip this field for this particular publication.')
	
	tags.p('More publications in which I participated can be found in my academic profiles:')
	with tags.div(style='display: flex; flex-direction: row; gap: 10px; padding: 10px;'):
		tags.a('Google scholar', cls='button', href='https://scholar.google.com/citations?user=WDjszAYAAAAJ&hl')
		tags.a('iNSPIRE', cls='button', href='https://inspirehep.net/literature?sort=mostrecent&size=25&page=1&q=find%20a%20matias%20senger')
		tags.a('arXiv', cls='button', href='https://arxiv.org/search/?query=matias+senger&searchtype=author&abstracts=show&order=-announced_date_first&size=50')

def generate_skill_bubble(skill):
	n_stars = 0#1 if skill['Skillfulness (1-10)']>=8 else 0
	tags.div(
		skill['skill_name'] + (' '+'⭐'*n_stars)*(n_stars>0),
		cls = 'skill_bubble',
		title = skill['description'] if not isinstance(skill['description'], float) else None,
	)

def generate_skills():
	skills_data = pandas.read_csv(
		'data/skills.csv',
		dtype = {
			'skill_name': str,
			'sub_skill_of': str,
			'kind': str,
			'category': str,
			'Skillfulness (1-10)': int,
			'description': str,
			'url': str,
		}
	)
	
	tags.h1('Skills', id='section_skills')
	with tags.div(style='display: flex; flex-direction: row; gap: 22px; row-gap: 22px; flex-wrap: wrap'):
		for category in ['programming languages','software tools','software apps','analytics','electronics','hardware design','operating systems']:
			with tags.div(style='display: flex; flex-direction: column; width: 333px; max-width: 100%; gap: 10px;'):
				tags.div(category.capitalize(), style='flex-shrink: 0; font-weight: bold;')
				with tags.div(style='display: flex; flex-direction: row; gap: 11px; flex-wrap: wrap;'):
					for _,skill in skills_data.query(f'kind=="hard" and category=={repr(category)}').sort_values("Skillfulness (1-10)", ascending=False).iterrows():
						if isinstance(skill['url'], str):
							with tags.a(href=skill['url'], target='_blank', style='color: inherit; text-decoration: none !important;'):
								generate_skill_bubble(skill)
						else:
							generate_skill_bubble(skill)

def generate_presentations_in_conferences_and_events():
	presentations_data = pandas.read_csv(
		'data/presentations.csv',
		date_parser = lambda x: datetime.datetime.strptime(x, '%m/%d/%y'),
		parse_dates = ['date'],
		dtype = {
			'event_name': str,
			'place': str,
			'type': str,
			'url': str,
			'presentation_title': str,
			'modality': str,
		},
		keep_default_na = False,
	)
	
	tags.h1('Presentations in conferences and events', id='section_conferences')
	with tags.div(style='display: flex; flex-direction: column;'):
		for _,presentation in presentations_data.sort_values('date', ascending=False).iterrows():
			with tags.div(
				style = f'display: flex; flex-direction: row; gap: 10px; padding: 10px; border-radius: {BORDER_RADIUS};',
				cls = 'highlight_on_hover',
			):
				LOGOS = {
					'presentation': 'https://cdn-icons-png.flaticon.com/512/4270/4270722.png',
					'lightning talk': 'https://cdn-icons-png.flaticon.com/512/4270/4270722.png',
					'poster': 'https://cdn.iconscout.com/icon/free/png-256/free-frame-poster-1835652-1556212.png',
					'functional prototype': 'https://cdn-icons-png.flaticon.com/512/60/60473.png',
				}
				responsive_logo(
					style = 'max-width: 100%; max-height: 100%; opacity: .4;',
					alt = 'Publication icon',
					title = presentation['type'].capitalize(),
					src = LOGOS[presentation['type']],
				)
				with tags.div(style='display: flex; flex-direction: column; gap: 1px;'):
					tags.div(presentation['presentation_title'], style='font-weight: bold;')
					tags.div(presentation['event_name'])
					with tags.div(style=f'font-weight: 100; color: {LIGHTER_TEXT_COLOR}'):
						tags.span(presentation['date'].strftime(DATES_FORMAT))
						tags.span(FIELDS_SEPARATOR)
						if presentation['place'] != '':
							tags.span(presentation['place'])
							tags.span(FIELDS_SEPARATOR)
						else:
							logging.warning(f'Presentation {repr(presentation["presentation_title"])} does not have a "place", skipping this info for this particular presentation.')
						tags.span(presentation['modality'].capitalize())
					with tags.div(style=f'font-weight: 100; color: {LIGHTER_TEXT_COLOR}'):
						tags.span(presentation['type'].capitalize())
						if 'url' in presentation:
							tags.span(FIELDS_SEPARATOR)
							tags.a(presentation['url'], href=presentation['url'])

def generate_projects():
	with open('data/projects/projects.json') as ifile:
		projects_data = json.load(ifile)
	
	tags.h1('Projects', id='section_projects')
	
	with tags.div(style='display: flex; flex-direction: row; gap: 22px; flex-wrap: wrap;'):
		for project in projects_data:
			with tags.div(style='display: flex; flex-direction: column; max-width: 100%; width: 45%; min-width: 333px; gap: 10px;'):
				with tags.div(style='display: flex; flex-direction: row; flex-wrap: wrap; gap: 5px; border-radius: 1em; height: 222px; overflow: hidden;'):
					for image in project['media'][0:1]:
						if image['media_type'] != 'image':
							continue
						tags.img(src=image['src'], alt=image['title'], title=image['title'], width='100%', style='border-radius: 1em;')
				tags.div(project['public_name'], style='font-weight: bold;')
				with tags.div(style=f'font-weight: 100; color: {LIGHTER_TEXT_COLOR}'):
					project_date = datetime.datetime.strptime(project['date'], '%b %Y')
					tags.span(project_date.strftime(DATES_FORMAT))
					tags.span(FIELDS_SEPARATOR)
					tags.span(f'Development time {project["development_time"]}')
				tags.div(project['description'])
				tags.a(f'Know more', href=project['url'])

def generate_contributions_to_open_source_projects(include_logos:bool=False):
	with open('data/contributions_to_open_source_projects.json') as ifile:
		contributions_data = json.load(ifile)
	
	tags.h1('Contributions to open source projects', id='section_open_source_projects')
	
	with tags.div(style='display: flex; flex-direction: row; gap: 22px; flex-wrap: wrap;'):
		for contribution in contributions_data:
			with tags.div(style='display: flex; flex-direction: row; max-width: 100%; width: 45%; min-width: 333px; gap: 10px;'):
				if include_logos == True:
					if 'project_logo' in contribution:
						responsive_logo(
							style = 'max-width: 100%; max-height: 100%;',
							alt = f'{contribution["project_name"]} logo',
							title = contribution["project_name"],
							src = contribution['project_logo'],
						)
					else:
						responsive_logo(
							style = 'max-width: 100%; max-height: 100%; opacity: 50%;',
							alt = 'Open source logo',
							title = 'Open source logo',
							src = 'https://cdn-icons-png.flaticon.com/512/888/888868.png',
						)
				with tags.div(style='display: flex; flex-direction: column; gap: 5px;'):
					with tags.div(style='display: flex; flex-direction: row; gap: 5px;'):
						tags.div(contribution['project_name'], style='font-weight: bold;')
						tags.div(FIELDS_SEPARATOR, style=f'color: {LIGHTER_TEXT_COLOR};')
						with tags.div(style='display: flex; flex-direction: row; gap: 5px;'):
							STATUS_IMAGES = {
								'open': dict(
									src = 'https://static-00.iconduck.com/assets.00/git-pull-request-icon-486x512-6ypq0sng.png',
									style = 'width: 1em; height: 1em; filter: brightness(0.9) invert(.7) sepia(.5) hue-rotate(100deg) saturate(200%);',
								),
								'merged': dict(
									src = 'https://upload.wikimedia.org/wikipedia/commons/thumb/c/c1/Octicons-git-merge.svg/1536px-Octicons-git-merge.svg.png',
									style = 'width: 1em; height: 1.3em; filter: brightness(0.9) invert(.7);',
								)
							}
							tags.img(**STATUS_IMAGES[contribution['status']])
							if contribution['status'] == 'open':
								tags.span('Open', style='color: #59d467;')
							elif contribution['status'] == 'merged':
								tags.span('Merged', style='color: #b5b5b5;')
					tags.div(contribution['description'])
					tags.a(contribution['my_contribution_url'], href=contribution['my_contribution_url'])

if __name__ == '__main__':
	import sys
	
	logging.basicConfig(
		stream = sys.stderr, 
		level = logging.WARNING,
		format = '%(asctime)s|%(levelname)s|%(funcName)s|%(message)s',
		datefmt = '%Y-%m-%d %H:%M:%S',
	)
	
	doc = dominate.document(title='Matias Senger curriculum vitae')

	with doc.head:
		tags.link(rel='stylesheet', href='css/style.css')
		tags.link(rel='preconnect', href='https://fonts.googleapis.com')
		tags.link(rel='preconnect', href='https://fonts.gstatic.com', crossorigin=True)
		tags.link(rel='stylesheet', href='https://fonts.googleapis.com/css2?family=Ubuntu&display=swap')
		tags.link(rel='stylesheet', href='https://fonts.googleapis.com/css2?family=Source+Serif+4:opsz@8..60&display=swap')
		tags.meta(name='viewport', content='width=device-width, initial-scale=1')
		tags.base(target="_blank") # All links open in new tab.

	with doc.body:
		with tags.div(cls='sidenav'):
			with tags.div(id='my_name_and_header_container'):
				tags.img(
					src = 'img/pic.png',
					style = 'max-width: 100%; max-height: 222px; border-radius: 50%; object-fit: cover;',
				)
				tags.div('Matias Senger', id='my_name')
			generate_personal_data()
			
		with tags.div(cls='main'):
			generate_experience()
			# ~ generate_projects()
			generate_contributions_to_open_source_projects()
			generate_skills()
			generate_education()
			generate_publications()
			generate_presentations_in_conferences_and_events()
			
	with open('../cv.html', 'w') as ofile:
		print(doc, file=ofile)
