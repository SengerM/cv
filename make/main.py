import dominate # https://github.com/Knio/dominate
import dominate.tags as tags
from pathlib import Path
import json
import datetime
import humanize
import pandas

BORDER_RADIUS = '0.5em'
LIGHTER_TEXT_COLOR = '#878787'

def responsive_logo(**image_attributes):
	with tags.div(style='flex-shrink: 0; width: 50px;', cls='responsive_logo'):
		tags.img(width='100%',**image_attributes)

def generate_personal_data():
	with open('data/personal.json') as ifile:
		personal_data = json.load(ifile)
	with tags.div(style='display: flex; flex-direction: column;'):
		for data in personal_data:
			with tags.div(
				style = f'display: flex; flex-direction: row; gap: 10px; padding: 10px; border-radius: {BORDER_RADIUS};',
				cls = 'highlight_on_hover'
			):
				with tags.div(style='flex-shrink: 0; width: 1em;'):
					tags.img(
						style = 'width: 100%;',
						alt = data['field_name'], 
						title = data['field_name'], 
						**data['icon'],
					)
				with tags.div(style='display: flex; flex-direction: column;'):
					for s in data['content']:
						if data['field_name']=='Email':
							tags.a(s, href=f'mailto:{s}')
						elif data['field_name'] in {'Website','LinkedIn'}:
							tags.a(s, href=s)
						else:
							tags.div(s)

def generate_experience():
	with open('data/experience/experience.json') as ifile:
		experience_data = json.load(ifile)
	with open('data/experience/employers.json') as ifile:
		employers_data = json.load(ifile)
	
	tags.h1('Experience')
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
						tags.span('·')
						tags.span(experience['work_load'])
					with tags.div(style=f'font-weight: 100; color: {LIGHTER_TEXT_COLOR}'):
						start_date = datetime.datetime.strptime(experience['start_date'], '%b %Y')
						if experience['end_date'].lower() == 'present':
							end_date = datetime.datetime.today()
						else:
							end_date = datetime.datetime.strptime(experience['end_date'], '%b %Y')
						tags.span(start_date.strftime('%b %Y'))
						tags.span('→')
						tags.span(end_date.strftime('%b %Y') if end_date.date()!=datetime.datetime.today().date() else 'Present')
						tags.span('·')
						tags.span(humanize.precisedelta(end_date-start_date, minimum_unit='months', format="%0.0f"))
					
					with tags.div(style=f'font-weight: 100; color: {LIGHTER_TEXT_COLOR}'):
						tags.span(employers_data[employer_key]['location'])
						tags.span('·')
						tags.span(experience['modality'])
					tags.div(experience['description'])

def generate_education():
	with open('data/education/education.json') as ifile:
		education_data = json.load(ifile)
	with open('data/education/schools.json') as ifile:
		schools_data = json.load(ifile)
	
	tags.h1('Education')
	with tags.div(style='display: flex; flex-direction: column;'):
		for education in education_data:
			with tags.div(
				style = f'display: flex; flex-direction: row; gap: 10px; padding: 10px; border-radius: {BORDER_RADIUS};',
				cls = 'highlight_on_hover',
			):
				school_key = education['school']
				responsive_logo(
					alt = schools_data[school_key]['name'], 
					title = schools_data[school_key]['name'], 
					**schools_data[school_key]['logo'],
				)
				with tags.div(style='display: flex; flex-direction: column; gap: 5px;'):
					tags.div(schools_data[school_key]['name'], style='font-weight: bolder;')
					with tags.div():
						tags.span(education['degree_level'])
						tags.span('·')
						tags.span(education['field'])
					with tags.div(style=f'font-weight: 100; color: {LIGHTER_TEXT_COLOR}'):
						end_date = datetime.datetime.strptime(education['end_date'], '%b %Y')
						tags.span(end_date.strftime('%b %Y') if end_date.date()!=datetime.datetime.today().date() else 'Present')

def generate_publications():
	with open('data/publications.json') as ifile:
		publications_data = json.load(ifile)
	
	tags.h1('Publications')
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
					style = 'max-width: 100%; max-height: 100%;',
					alt = 'Publication icon',
					src = 'https://static.thenounproject.com/png/1143700-200.png',
				)
				with tags.div(style='display: flex; flex-direction: column; gap: 1px;'):
					tags.div(publication['title'], style='font-weight: bold;')
					with tags.div():
						tags.span(publication['journal'])
						tags.span(',')
						tags.span(publication['publisher'])
					with tags.div(style=f'font-weight: 100; color: {LIGHTER_TEXT_COLOR}'):
						tags.span(publication['publication_date'])
					with tags.div(style=f'font-weight: 100; color: {LIGHTER_TEXT_COLOR}'):
						tags.span('DOI: ')
						tags.a(publication['DOI'], href=f'https://doi.org/{publication["DOI"]}')
	
	with tags.div(style='display: flex; flex-direction: row; gap: 10px; padding: 10px;'):
		tags.a('Google scholar', cls='button', href='https://scholar.google.com/citations?user=WDjszAYAAAAJ&hl')
		tags.a('iNSPIRE', cls='button', href='https://inspirehep.net/literature?sort=mostrecent&size=25&page=1&q=find%20a%20matias%20senger')
		tags.a('arXiv', cls='button', href='https://arxiv.org/search/?query=matias+senger&searchtype=author&abstracts=show&order=-announced_date_first&size=50')

def generate_skills():
	def generate_skill_bubble(skill):
		n_stars = 2 if skill['Skillfulness (1-10)']>=9 else 1 if skill['Skillfulness (1-10)']>=6 else 0
		tags.div(
			skill['skill_name'] + (' '+'⭐'*n_stars)*(n_stars>0),
			cls = 'skill_bubble',
			title = skill['description'] if not isinstance(skill['description'], float) else None,
		)
	
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
	
	tags.h1('Skills')
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
						

doc = dominate.document(title='Matias Senger curriculum vitae')

with doc.head:
	tags.link(rel='stylesheet', href='css/style.css')
	tags.link(rel='preconnect', href='https://fonts.googleapis.com')
	tags.link(rel='preconnect', href='https://fonts.gstatic.com', crossorigin=True)
	tags.link(rel='stylesheet', href='https://fonts.googleapis.com/css2?family=Ubuntu&display=swap')
	tags.link(rel='stylesheet', href='https://fonts.googleapis.com/css2?family=Source+Serif+4:opsz@8..60&display=swap')
	tags.meta(name='viewport', content='width=device-width, initial-scale=1')

with doc:
	with tags.div(cls='sidenav'):
		with tags.div(id='my_name_and_header_container'):
			tags.div('Matias Senger', id='my_name')
			tags.div('Physicist 🔭 and electronics engineer💡', style='color:#696969;')
		generate_personal_data()
	with tags.div(cls='main'):
		generate_experience()
		generate_education()
		generate_publications()
		generate_skills()

	
with open('../test.html', 'w') as ofile:
	print(doc, file=ofile)
