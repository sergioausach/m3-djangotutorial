from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.contrib.auth.models import User
from polls.models import Question, Choice
from django.utils import timezone
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
 
class MySeleniumTests(StaticLiveServerTestCase):
    # carregar una BD de test
    fixtures = ['testdb.json',]
 
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        User.objects.create_superuser(
            username='isard',
            email='isard@test.com',
            password='pirineus'
        )

        question = Question.objects.create(
            question_text="Pregunta de prova",
            pub_date=timezone.now()
        )
        Choice.objects.create(
            question=question,
            choice_text="Opció 1",
            votes=0
        )

        opts = Options()
        cls.selenium = WebDriver(options=opts)
        cls.selenium.implicitly_wait(5)
 
    @classmethod
    def tearDownClass(cls):
        # tanquem browser
        # comentar la propera línia si volem veure el resultat de l'execució del navegador
        cls.selenium.quit()
        super().tearDownClass()
 
    def test_login(self):
        # anem directament a la pàgina d'accés a l'admin panel
        self.selenium.get('%s%s' % (self.live_server_url, '/admin/login/'))
 
        # comprovem que el títol de la pàgina és el que esperem
        self.assertEqual(self.selenium.title, "Log in | Django site admin")
 
        # introduïm dades de login i cliquem el botó "Log in" per entrar
        username_input = self.selenium.find_element(By.NAME, "username")
        username_input.send_keys('isard')
        password_input = self.selenium.find_element(By.NAME, "password")
        password_input.send_keys('pirineus')
        self.selenium.find_element(By.XPATH, '//input[@value="Log in"]').click()
 
        # comprovem si hem aconseguit entrar a l'admin panel pel títol de la pàgina
        self.assertEqual(
            self.selenium.title,
            "Site administration | Django site admin"
        )
