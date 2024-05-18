from django.urls import reverse
from budget.models import Project, Category, Expense
import json
import pytest

@pytest.fixture
def project1(db):
    return Project.objects.create(name='project1', budget=10000)

#Vérifie si la page de liste des projets se charge correctement.
@pytest.mark.django_db
def test_project_list_get(client):
    url = reverse('list')
    response = client.get(url)
    assert response.status_code == 200
    assert 'budget/project-list.html' in [template.name for template in response.templates]

#Vérifie si la page de détail d'un projet se charge correctement.
@pytest.mark.django_db
def test_project_detail_get(client, project1):
    url = reverse('detail', args=[project1.slug])
    response = client.get(url)
    assert response.status_code == 200
    assert 'budget/project-detail.html' in [template.name for template in response.templates]

#Vérifie si l'ajout d'une nouvelle dépense à un projet fonctionne correctement.
@pytest.mark.django_db
def test_project_detail_adds_new_expense(client, project1):
    category = Category.objects.create(project=project1, name='development')
    url = reverse('detail', args=[project1.slug])
    data = {
        'title': 'expense1',
        'amount': 1000,
        'category': 'development'
    }
    response = client.post(url, data)
    assert response.status_code == 302
    assert project1.expenses.first().title == 'expense1'

#Vérifie le comportement lorsqu'aucune donnée n'est envoyée lors de la création d'une dépense.
@pytest.mark.django_db
def test_project_detail_POST_no_data(client, project1):
    url = reverse('detail', args=[project1.slug])
    response = client.post(url)
    assert response.status_code == 302
    assert project1.expenses.count() == 0

#Vérifie si la suppression d'une dépense d'un projet fonctionne correctement.
@pytest.mark.django_db
def test_project_detail_DELETE_deletes_expense(client, project1):
    category = Category.objects.create(project=project1, name='development')
    expense = Expense.objects.create(project=project1, title='expense1', amount=1000, category=category)
    url = reverse('detail', args=[project1.slug])
    response = client.delete(url, json.dumps({'id': expense.id}), content_type='application/json')
    assert response.status_code == 204
    assert project1.expenses.count() == 0

#Vérifie le comportement lorsqu'aucun identifiant de dépense n'est spécifié lors de la suppression.
@pytest.mark.django_db
def test_project_detail_DELETE_no_id(client, project1):
    category = Category.objects.create(project=project1, name='development')
    Expense.objects.create(project=project1, title='expense1', amount=1000, category=category)
    url = reverse('detail', args=[project1.slug])
    response = client.delete(url, content_type='application/json')  # Ajoutez content_type='application/json'
    assert response.status_code == 404
    assert project1.expenses.count() == 1


#Ce test vérifie que lorsqu'un nouveau projet est créé avec des catégories spécifiées, 
#les catégories sont correctement associées au projet
@pytest.mark.django_db
def test_project_create_POST(client):
    url = reverse('add')
    data = {
        'name': 'project2',
        'budget': 10000,
        'categoriesString': 'design,development'
    }
    response = client.post(url, data)
    project2 = Project.objects.get(name='project2')
    assert project2.name == 'project2'
    assert Category.objects.filter(project=project2, name='design').exists()
    assert Category.objects.filter(project=project2, name='development').exists()