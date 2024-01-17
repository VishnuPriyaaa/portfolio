import sqlalchemy.exc
from flask import (render_template, url_for, redirect, request)

from models import db, Project, app
from datetime import datetime


@app.context_processor
def inject_projects():
    projects = Project.query.all()
    return dict(projects=projects)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/project/<id>')
def detail_view(id):
    project = Project.query.get_or_404(id)
    formatted_date = project.date.strftime("%b %Y")
    print("SKILLSS", project.skills, project.repo_link)
    return render_template('detail.html', project=project, formatted_date=formatted_date)


@app.route('/project/<id>/edit', methods=['GET', 'POST'])
def edit_view(id):
    project = Project.query.get_or_404(id)
    if project:
        new_date = project.date.strftime("%Y-%m")
        print("NEW DATA", new_date)

    if request.method == 'POST':
        project.title = request.form.get('title')
        project.description = request.form.get('desc')
        project.skills = request.form.get('skills')
        project.repo_link = request.form.get('github')
        date_str = request.form.get('date')
        try:
            if len(date_str) == 7 and date_str.count('-') == 1:
                date_str = date_str + '-01'
                project.date = datetime.strptime(date_str, "%Y-%m-%d")
                db.session.commit()
                return redirect(url_for('detail_view', id=id))
        except ValueError:
            return render_template('editform.html', project=project, new_date=new_date)

    return render_template('editform.html', project=project, new_date=new_date)


@app.route('/project/new')
def new_view():
    return render_template('projectform.html')


@app.route('/project/add', methods=['GET', 'POST'])
def add_view():
    if request.method == 'POST':
        title = request.form.get('title')
        date_str = request.form.get('date')
        description = request.form.get('desc')
        skills = request.form.get('skills')
        repo_link = request.form.get('repo_link')

        try:
            if len(date_str) == 7 and date_str.count('-') == 1:
                date_str = date_str + '-01'
            date = datetime.strptime(date_str, "%Y-%m-%d")
            project = Project(title=title, date=date, description=description, skills=skills, repo_link=repo_link)
            db.session.add(project)
            db.session.commit()
            return redirect(url_for('index'))
        except ValueError:
            return render_template('projectform.html')
    return render_template('projectform.html')


@app.route('/project/<id>/delete')
def delete_view(id):
    project = Project.query.get_or_404(id)
    db.session.delete(project)
    db.session.commit()
    return redirect(url_for('index'))


def clean_date(date_str):
    try:
        modified_date = datetime.strptime(date_str, "%Y-%m-%d")
        # format : Jan 2021
    except sqlalchemy.exc.StatementError:
        input('''Please enter the date only in %Y-%m-%d format (eg: 2023-12-05)
        Press Enter to continue...''')
    else:
        return modified_date


def add_projects():
    projects_to_add = [
        {
            "title": "Number Guessing Game",
            "date": clean_date("2023-12-05"),
            "description": "A game which challenges the user to guess a number which is randomly generated",
            "skills": "Python",
            "repo_link": "https://github.com/VishnuPriyaaa/Number-Guessing-Game",
        },
        {
            "title": "BasketBall Stats Tool",
            "date": clean_date("2023-12-27"),
            "description": "Displays the statistics related to players and teams associated with Basketball Game",
            "skills": "Python, Lists, Dictionaries",
            "repo_link": "https://github.com/VishnuPriyaaa/basketball_stats_tool",
        },
        {
            "title": "Phrase Hunter",
            "date": clean_date("2024-01-04"),
            "description": "A game where the user has to guess all the letters from a random phrase",
            "skills": "Python, OOP",
            "repo_link": "https://github.com/VishnuPriyaaa/phrase_hunter",
        },
        {
            "title": "Store Inventory",
            "date": clean_date("2024-01-10"),
            "description": "An inventory application which allows us to maintain the store records related to various products available",
            "skills": "Python, SQLAlchemy",
            "repo_link": "https://github.com/VishnuPriyaaa/store_inventory",
        },
    ]

    for project_data in projects_to_add:
        existing_project = Project.query.filter_by(title=project_data["title"]).first()
        if not existing_project:
            project = Project(**project_data)
            db.session.add(project)
            db.session.commit()
    for project in db.session.query(Project).all():
        print(project)


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        add_projects()
    app.run(debug=True, port=8000, host='127.0.0.1')
