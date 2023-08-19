import dominate # https://github.com/Knio/dominate
import dominate.tags as tags
from pathlib import Path
import json
import datetime
import humanize

BORDER_RADIUS = '0.5em'
LIGHTER_TEXT_COLOR = '#878787'

with open('data/personal.json') as ifile:
	personal_data = json.load(ifile)

doc = dominate.document(title='Matias Senger curriculum vitae')

with doc.head:
	tags.link(rel='stylesheet', href='css/style.css')
	tags.link(rel='preconnect', href='https://fonts.googleapis.com')
	tags.link(rel='preconnect', href='https://fonts.gstatic.com', crossorigin=True)
	tags.link(rel='stylesheet', href='https://fonts.googleapis.com/css2?family=Ubuntu&display=swap')
	tags.link(rel='stylesheet', href='https://fonts.googleapis.com/css2?family=Source+Serif+4:opsz@8..60&display=swap')
	tags.meta(name='viewport', content='width=device-width, initial-scale=1')

with doc:
	with tags.div(id='sticky_header'):
		tags.span('Matias Senger', id='my_name')
	tags.p('Physicist 🔭 and electronics engineer💡', style='color:#696969;')
	
	# Personal data ---
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
	
	tags.h1('Experience')
	with open('data/experience/experience.json') as ifile:
		experience_data = json.load(ifile)
	with open('data/experience/employers.json') as ifile:
		employers_data = json.load(ifile)
	with tags.div(style='display: flex; flex-direction: column;'):
		for experience in experience_data:
			with tags.div(
				style = f'display: flex; flex-direction: row; gap: 10px; padding: 10px; border-radius: {BORDER_RADIUS};',
				cls = 'highlight_on_hover',
			):
				employer_key = experience['employer']
				with tags.div(style='flex-shrink: 0; width: 50px;'):
					tags.img(
						style = 'width: 100%;',
						alt = employers_data[employer_key]['name'], 
						title = employers_data[employer_key]['name'], 
						**employers_data[employer_key]['logo'],
					)
				with tags.div(style='display: flex; flex-direction: column; gap: 5px;'):
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
	
	tags.h1('Education')
	with open('data/education/education.json') as ifile:
		education_data = json.load(ifile)
	with open('data/education/schools.json') as ifile:
		schools_data = json.load(ifile)
	with tags.div(style='display: flex; flex-direction: column;'):
		for education in education_data:
			with tags.div(
				style = f'display: flex; flex-direction: row; gap: 10px; padding: 10px; border-radius: {BORDER_RADIUS};',
				cls = 'highlight_on_hover',
			):
				school_key = education['school']
				with tags.div(style='flex-shrink: 0; width: 50px;'):
					tags.img(
						style = 'width: 100%;',
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
	
	tags.h1('Publications')
	tags.p('Publications with main participation:')
	with open('data/publications.json') as ifile:
		publications_data = json.load(ifile)
	with tags.div(style='display: flex; flex-direction: column;'):
		for publication in publications_data:
			if publication['title'] == '':
				break
			with tags.div(
				style = f'display: flex; flex-direction: row; gap: 10px; padding: 10px; border-radius: {BORDER_RADIUS};',
				cls = 'highlight_on_hover',
			):
				with tags.div(style='flex-shrink: 0; height: 3em; opacity: 0.5;'):
					tags.img(
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


	
with open('../test.html', 'w') as ofile:
	print(doc, file=ofile)
