from django.test import TestCase
from LocalCartBack import models
from django.http import QueryDict
import json
from django.contrib.auth import authenticate
import factory

class LindaUserFactory(factory.django.DjangoModelFactory):
	class Meta:
		model = models.User

	username = "Linda"
	password = "123"
	email = "funfunfunfunfunfunfun@gmail.com"

class RuthUserFactory(factory.django.DjangoModelFactory):
	class Meta:
		model = models.User

	username = "Ruth"
	password = "123"
	email = "rlzhang@berkeley.com"

class CustomerUserInfoFactory(factory.django.DjangoModelFactory):
	class Meta:
		model = models.UserInfo

	user = factory.SubFactory(LindaUserFactory)
	user_type = "customer"
	picture = 'images/default_user_image'

class MerchantUserInfoFactory(factory.django.DjangoModelFactory):
	class Meta:
		model = models.UserInfo

	user = factory.SubFactory(RuthUserFactory)
	user_type = "merchant"
	picture = 'images/default_user_image'


class UserInfoTestCase(TestCase):

	def setUp(self):
		user = CustomerUserInfoFactory()
		self.assertTrue(user.id is not None)

	def tearDown(self):
	    errors = []
	    try:
	        model = [
	                  models.User, 
	                  models.UserInfo,
	                  ]
	        for m in model:
	            m.objects.all().delete()
	    except Exception as e:
	        errors.append(e)
	    self.assertEqual(0, len(errors))
		
	def testCreateDuplicateUser(self):
		"""
		Make a second Linda customer. Should fail.
		"""
		username = "Linda"
		password = "123"
		email = "rlzhang@berkeley.edu"
		user_type = "customer"
		picture = 'images/default_user_image'
		new_user_info = models.UserInfo.create_new_user(username=username, password=password, email=email, 
			first_name='', last_name='', user_type=user_type, picture=picture)
		self.assertEqual(None, new_user_info)

	def testEditUserDoesNotExist(self):
		"""
		Edit user that does not exist. Should fail.
		"""
		edited_user_type = models.UserInfo.edit_user_info(username="Leila")
		self.assertEqual(None, edited_user_type)

###########################################################################################

class StoreFactory(factory.django.DjangoModelFactory):
	class Meta:
		model = models.Store

	user = factory.SubFactory(RuthUserFactory)
	name = "Ruth's Shop"
	address_street = "1921 Francisco St"
	address_city = "Berkeley"
	address_state = "CA"
	address_zip = "94709"
	phone_number = "(510)943-0591"
	description = "A shop for everyone."
	picture = 'images/default_user_image'

class StoreTestCase(TestCase):

	def setUp(self):
		store = StoreFactory()
		self.assertTrue(store.id is not None)

	def tearDown(self):
	    errors = []
	    try:
	        model = [
	                  models.User, 
	                  models.UserInfo, 
	                  models.Store,
	                  ]
	        for m in model:
	            m.objects.all().delete()
	    except Exception as e:
	        errors.append(e)
	    self.assertEqual(0, len(errors))

	def testGetStore(self):
		"""
		Get store with correct ID. Should succeed.
		"""
		storeID = models.Store.objects.all()[0].id
		hasError, store = models.Store.get_store(storeID)
		self.assertFalse(hasError)

	def testGetStoreWrongID(self):
		"""
		Get store with ID too big. Should fail.
		"""
		storeID = models.Store.objects.all()[0].id + 1
		hasError, store = models.Store.get_store(storeID)
		self.assertTrue(hasError)

######################################################################################

class InventoryFactory(factory.django.DjangoModelFactory):
	class Meta:
		model = models.Inventory

	store = factory.SubFactory(StoreFactory)

class InventoryTestCase(TestCase):

	def setUp(self):
		inventory = InventoryFactory()
		self.assertTrue(inventory.id is not None)

	def tearDown(self):
	    errors = []
	    try:
	        model = [
	                  models.User, 
	                  models.UserInfo, 
	                  models.Store, 
	                  models.Inventory,
	                  ]
	        for m in model:
	            m.objects.all().delete()
	    except Exception as e:
	        errors.append(e)
	    self.assertEqual(0, len(errors))

	def testGetInventory(self):
		"""
		Get inventory with correct ID. Should succeed.
		"""
		inventoryID = models.Inventory.objects.all()[0].id
		hasError, inventory = models.Inventory.get_inventory(inventoryID)
		self.assertFalse(hasError)

	def testGetInventoryWrongID(self):
		"""
		Get inventory with ID too big. Should fail.
		"""
		inventoryID = models.Inventory.objects.all()[0].id + 1
		hasError, inventory = models.Inventory.get_inventory(inventoryID)
		self.assertTrue(hasError)

####################################################################################

class ItemFactory(factory.django.DjangoModelFactory):
	class Meta:
		model = models.Item

	inventory = factory.SubFactory(InventoryFactory)
	store = factory.SubFactory(StoreFactory)
	name = 'apple'
	description = 'Fuji'
	price = 0.50
	picture = 'images/default_user_image'

class ItemTestCase(TestCase):

	def setUp(self):
		inventory = InventoryFactory()
		item = ItemFactory(inventory=inventory, store = inventory.store)
		self.assertTrue(item.id is not None)

	def tearDown(self):
	    errors = []
	    try:
	        model = [
	                  models.User, 
	                  models.UserInfo, 
	                  models.Store, 
	                  models.Inventory, 
	                  models.Item, 
	                  ]
	        for m in model:
	            m.objects.all().delete()
	    except Exception as e:
	        errors.append(e)
	    self.assertEqual(0, len(errors))

	def testBasicSearch(self):
		"""
		Make a perfect search for apple. Should succeed.
		"""
		items, errors = models.Item.basic_search_items('apple','94709')
		self.assertEqual(0, len(errors))
		self.assertTrue(items is not None)

	def testBasicSearchDifferentZIP(self):
		"""
		Make a search for apple in 94704. Should succeed but not return any items.
		"""
		items, errors = models.Item.basic_search_items('apple','94704')
		self.assertEqual(0, len(errors))
		self.assertFalse(items)

	def testBasicSearchEmptyZIP(self):
		"""
		Make a search for apple without ZIP. Should fail.
		"""
		items, errors = models.Item.basic_search_items('apple','')
		self.assertEqual(1, len(errors))
		self.assertFalse(items)

	def testBasicSearchNot5ZIP(self):
		"""
		Make a search for apple with 940. Should fail.
		"""
		items, errors = models.Item.basic_search_items('apple','940')
		self.assertEqual(1, len(errors))
		self.assertFalse(items)

	def testRelevantItemsFujiApple(self):
		"""
		Make a query with fuji apple. Should succeed and return item.
		"""
		items = models.Item.relevant_items('fuji apple')
		self.assertEqual(1, len(items))

	def testRelevantItemsFujiAppleDelicious(self):
		"""
		Make a query with fuji apple delicious. Should succeed and return no item.
		"""
		items = models.Item.relevant_items('fuji apple delicious')
		self.assertEqual(0, len(items))

	def testRelevantItemsFujiAppleDeliciousWithOneQuote(self):
		"""
		Create another apple. Make a query with fuji "apple. Should succeed and return item.
		"""
		items = models.Item.relevant_items('fuji "apple')
		self.assertEqual(1, len(items))

	def testRelevantItemsFujiAppleDeliciousWithOneQuoteAndPeriod(self):
		"""
		Create another apple. Make a query with fuji ."apple. Should succeed and return no item.
		"""
		items = models.Item.relevant_items('fuji ."apple')
		self.assertEqual(0, len(items))

	def testRelevantItemsApple(self):
		"""
		Create another apple. Make a query with apple. Should succeed and return 2 item.
		"""
		inventory = models.Item.objects.all()[0].inventory
		item = ItemFactory(inventory=inventory, store=inventory.store, name="granny apple", description="delicious")
		items = models.Item.relevant_items('apple')
		self.assertEqual(2, len(items))

	def testSearchItems(self):
		"""
		Search apple in 94709. Should succeed and return 1 item.
		"""
		items, errors = models.Item.search_items('apple', '94709')
		self.assertEqual(0, len(errors))
		self.assertEqual(1, len(items))

	def testSearchItemsEmptyName(self):
		"""
		Search in 94709. Should fail and return 1 error.
		"""
		items, errors = models.Item.search_items('', '94709')
		self.assertEqual(1, len(errors), errors)
		self.assertEqual(0, len(items))

	def testSearchItemsEmptyLocation(self):
		"""
		Search apple. Should fail and return 1 error.
		"""
		items, errors = models.Item.search_items('apple', '')
		self.assertEqual(1, len(errors), errors)
		self.assertEqual(0, len(items))

	def testSearchItemsInvalidLocation(self):
		"""
		Search apple in 938a.... Should fail and return 1 error.
		"""
		items, errors = models.Item.search_items('apple', '938aqweporiuasl;dkfjasl;kdjqowepiruoiasdjfl;kajsdklfjkaldjfklas;dfklajsdklfjqweirqwueoipruioqpweuifjasjf;lksdjfklnvklasdkfjadk;j')
		self.assertEqual(1, len(errors), errors)
		self.assertEqual(0, len(items))

	def testGetItem(self):
		"""
		Get item with correct ID. Should succeed.
		"""
		itemID = models.Item.objects.all()[0].id
		hasError, item = models.Item.get_item(itemID)
		self.assertFalse(hasError)

	def testGetItemWrongID(self):
		"""
		Get item with ID too big. Should fail.
		"""
		itemID = models.Item.objects.all()[0].id + 1
		hasError, item = models.Item.get_item(itemID)
		self.assertTrue(hasError)

#######################################################################################

class ReviewFactory(factory.django.DjangoModelFactory):
	class Meta:
		model = models.Review

	user = factory.SubFactory(LindaUserFactory)
	item = factory.SubFactory(ItemFactory)
	store = factory.SubFactory(StoreFactory)
	rating = 5
	text = "This store is great."

class ReviewTestCase(TestCase):

	def setUp(self):
		inventory = InventoryFactory()
		item = ItemFactory(inventory=inventory, store=inventory.store)
		review = ReviewFactory(user=inventory.store.user, item=item, store=inventory.store)
		self.assertTrue(review.id is not None)

	def tearDown(self):
	    errors = []
	    try:
	        model = [
	                  models.User, 
	                  models.UserInfo, 
	                  models.Store, 
	                  models.Inventory, 
	                  models.Item, 
	                  models.Review,
	                  ]
	        for m in model:
	            m.objects.all().delete()
	    except Exception as e:
	        errors.append(e)
	    self.assertEqual(0, len(errors))

	def testGetReview(self):
		"""
		Get review with correct ID. Should succeed.
		"""
		reviewID = models.Review.objects.all()[0].id
		hasError, review = models.Review.get_review(reviewID)
		self.assertFalse(hasError)

	def testGetReviewWrongID(self):
		"""
		Get review with ID too big. Should fail.
		"""
		reviewID = models.Review.objects.all()[0].id + 1
		hasError, review = models.Review.get_review(reviewID)
		self.assertTrue(hasError)

#########################################################################################

class CartListFactory(factory.django.DjangoModelFactory):
	class Meta:
		model = models.CartList

	user = factory.SubFactory(LindaUserFactory)
	name = "Linda's Shopping List"

class ListItemFactory(factory.django.DjangoModelFactory):
	class Meta:
		model = models.ListItem

	cartlist = factory.SubFactory(CartListFactory)
	item = factory.SubFactory(ItemFactory)
	item_name = "apple"
	list_position = factory.Sequence(lambda n: '%d' % n)

class CartListTestCase(TestCase):

	def setUp(self):
		inventory = InventoryFactory()
		store = inventory.store
		item = ItemFactory(inventory=inventory, store=store)
		userinfo = CustomerUserInfoFactory()
		cartlist = CartListFactory(user=userinfo.user)
		listitem = ListItemFactory(cartlist=cartlist, item=item)
		self.assertTrue(cartlist.id is not None)
		self.assertTrue(listitem.id is not None)
		item = ItemFactory(inventory=inventory, store=store, name='pear', description='amazing', price=0.8)
		listitem = ListItemFactory(cartlist=cartlist, item=None, item_name='pear')
		item = ItemFactory(inventory=inventory, store=store, name='banana', description='bonanza', price=0.8)
		listitem = ListItemFactory(cartlist=cartlist, item=None, item_name='banana')

	def tearDown(self):
	    errors = []
	    try:
	        model = [
	                  models.User, 
	                  models.UserInfo, 
	                  models.Store, 
	                  models.Inventory, 
	                  models.Item, 
	                  models.Review,
	                  models.CartList,
	                  models.ListItem,
	                  ]
	        for m in model:
	            m.objects.all().delete()
	    except Exception as e:
	        errors.append(e)
	    self.assertEqual(0, len(errors))

	def testRefillList(self):
		"""
		Give correct listID and content. Should succeed.
		"""
		cartlistID = models.CartList.objects.all()[0].id
		content = [ {'type': 'id', 'name': models.Item.objects.get(name='apple').id},
					{'type': 'name', 'name': 'pear'},
					{'type': 'name', 'name': 'banana'},
					]
		errors = models.CartList.refill_list(cartlistID, content)
		self.assertEqual('Success', errors, errors)

	def testRefillListWrongID(self):
		"""
		Give incorrect listID and content. Should fail.
		"""
		cartlistID = models.CartList.objects.all()[0].id+1
		content = [ {'type': 'id', 'name': models.Item.objects.get(name='apple').id},
					{'type': 'name', 'name': 'pear'},
					{'type': 'name', 'name': 'banana'},
					]
		errors = models.CartList.refill_list(cartlistID, content)
		self.assertEqual(None, errors, errors)

	def testGetCartList(self):
		"""
		Get review with correct ID. Should succeed.
		"""
		cartlistID = models.CartList.objects.all()[0].id
		hasError, cartlist = models.CartList.get_cartlist(cartlistID)
		self.assertFalse(hasError)

	def testGetCartListWrongID(self):
		"""
		Get review with ID too big. Should fail.
		"""
		cartlistID = models.CartList.objects.all()[0].id + 1
		hasError, cartlist = models.CartList.get_cartlist(cartlistID)
		self.assertTrue(hasError)

	def testResolveList(self):
		"""
		Give correct listID and location. Should succeed.
		"""
		cartlistID = models.CartList.objects.all()[0].id
		errors = models.CartList.resolve_list(cartlistID, '94709')
		self.assertEqual(0, len(errors), errors)

	def testResolveListWrongID(self):
		"""
		Give wrong listID and correct location. Should fail and return 1 error.
		"""
		cartlistID = models.CartList.objects.all()[0].id+1
		errors = models.CartList.resolve_list(cartlistID, '94709')
		self.assertEqual(1, len(errors), errors)

	def testResolveListBadLocation(self):
		"""
		Give correct listID and bad location. Should fail and return 1 error.
		"""
		cartlistID = models.CartList.objects.all()[0].id
		errors = models.CartList.resolve_list(cartlistID, '94709ads;lfkjqwoeirjoiajdkfl;jals;dfjoij;lkj;lskdfj')
		self.assertEqual(1, len(errors), errors)

	def testResolveListWrongLocation(self):
		"""
		Give wrong listID and 94030. Should fail and return 1 error.
		"""
		cartlistID = models.CartList.objects.all()[0].id
		errors = models.CartList.resolve_list(cartlistID, '94030')
		self.assertEqual(2, len(errors), errors)

	def testResolveListNoItem(self):
		"""
		Give correct listID and location, but item does not exist. Should fail and return 1 error.
		"""
		cartlist = models.CartList.objects.all()[0]
		listitem = ListItemFactory(cartlist=cartlist, item=None, item_name='peach')
		cartlistID = cartlist.id
		errors = models.CartList.resolve_list(cartlistID, '94709')
		self.assertEqual(1, len(errors), errors)
