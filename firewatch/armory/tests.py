from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from armory.models import Firearm, WatchType, Magazine, ServiceMember, Armorer, Watch

class IndexViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')

        self.firearm = Firearm.objects.create(firearm_type='M4A1', serial_number='12345')
        self.watch_type = WatchType.objects.create(name='Type A')
        self.magazine = Magazine.objects.create(total_9mm=100, total_556=200, total_762=300)
        self.servicemember = ServiceMember.objects.create(first='John', last='Doe')

    def test_index_view(self):
        response = self.client.get(reverse('armory:index'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'armory/index.html')

        self.assertContains(response, 'M4A1')
        self.assertContains(response, 'Type A')
        self.assertContains(response, '100')
        self.assertContains(response, 'John Doe')




class CheckoutViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')

        self.firearm = Firearm.objects.create(firearm_type='M4A1', serial_number='12345', available=True)
        self.watch_type = WatchType.objects.create(name='Type A')
        self.magazine = Magazine.objects.create(total_9mm=100, total_556=200, total_762=300)
        self.servicemember = ServiceMember.objects.create(first='John', last='Doe')
        self.armorer = Armorer.objects.create(name="Armorer 1")

    def test_checkout_view(self):
        data = {
            "form_type": "checkout",
            "watch": self.watch_type.name,
            "servicemember": self.servicemember.id,
            "longarm": self.firearm.serial_number,
            "handgun": None,
            "556-ammo": 50,
            "762-ammo": 0,
            "9mm-ammo": 0,
            "mag-556": self.magazine.id,
            "mag-762": self.magazine.id,
            "mag-9mm": self.magazine.id
        }

        response = self.client.post(reverse('armory:index'), data)

        self.assertEqual(response.status_code, 302)  

        self.firearm.refresh_from_db()
        self.assertFalse(self.firearm.available) 

        self.assertEqual(Watch.objects.count(), 1)
        watch = Watch.objects.first()
        self.assertEqual(watch.watch_type, self.watch_type)
        self.assertEqual(watch.member_id, self.servicemember)
        self.assertEqual(watch.ammunition_count, 50)

        self.magazine.refresh_from_db()
        self.assertEqual(self.magazine.total_556, 150)
        self.assertEqual(self.magazine.total_762, 300)
        self.assertEqual(self.magazine.total_9mm, 100)


import datetime

class CheckinViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')

        self.firearm = Firearm.objects.create(firearm_type='M4A1', serial_number='12345', available=False)
        self.watch_type = WatchType.objects.create(name='Type A')
        self.magazine = Magazine.objects.create(total_9mm=100, total_556=200, total_762=300)
        self.servicemember = ServiceMember.objects.create(first='John', last='Doe')

        self.watch = Watch.objects.create(
            watch_type=self.watch_type,
            is_qualified=True,
            check_out=datetime.datetime.now(),
            check_in=None,
            ammunition_count=50,
            armory_id=None,
            member_id=self.servicemember,
        )
        self.watch.firearm_id.add(self.firearm)
        self.watch.save()

    def test_checkin_view(self):
        data = {
            'ammunition_count': 50,
            'magazine_id': self.magazine.id
        }

        response = self.client.post(reverse('armory:checkin', args=[self.watch.id]), data)

        self.assertEqual(response.status_code, 302)  

        self.watch.refresh_from_db()
        self.assertIsNotNone(self.watch.check_in)

        self.firearm.refresh_from_db()
        self.assertTrue(self.firearm.available)

        self.magazine.refresh_from_db()
        self.assertEqual(self.magazine.total_556, 250)
