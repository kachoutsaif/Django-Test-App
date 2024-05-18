from django.test import SimpleTestCase
from django.urls import reverse,resolve
from budget.views import project_list, ProjectCreateView, project_detail
import unittest
#Test  les urls 
#SimpleTestCase est definir pour les tests URLS 
class TestUrls(SimpleTestCase):
    #Vérifie si l'URL de la liste des projets est correctement résolue
    def test_list_url_is_resolved(self):
        url = reverse('list')
        self.assertEqual(resolve(url).func,project_list)
    #Vérifie si l'URL de création de projet est correctement résolue
    def test_project_creat_url_resolved(self):
        url = reverse('add')
        self.assertEqual(resolve(url).func.view_class,ProjectCreateView)
    #Vérifie si l'URL de détail d'un projet est correctement résolue
    def test_project_detail_url_resolved(self):
        url = reverse('detail',args=['some-slug'])
        self.assertEqual(resolve(url).func,project_detail)
    
    
 
      