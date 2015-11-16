import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

class TodoTest(unittest.TestCase):

	@classmethod
	def setUpClass(cls):
		# create instance of Firefox driver
		cls.driver = webdriver.Firefox()
		self.base_url = "http://todomvc.com/examples/react/"
		#self.base_url = "http://todomvc.com/examples/angularjs"
 		 	
	def setUp(self):
		#wait for firefox to open, set url, load and clear the cache
		self.driver.implicitly_wait(30)
		#clear the local storage
		self.driver.get('javascript:localStorage.clear();')
		
	#Testing add function by add a value to the field and press enter.
	#Assert true if:
	#- Inputted text is match
	#- Todo added to the list (list=1)
	#- Todo count updated
	#Testing edit function by add a value to the field, double click inserted field and edit the value.
	#Assert true if: list updated
	def test_delete(self):
		##arrange: get the web page, insert list to delete
		driver=self.driver
		driver.get(self.base_url)
		
		#insert todo list to delete
		inputElement = driver.find_elements_by_xpath("//input[@placeholder='What needs to be done?']")[0]
		inputElement.send_keys('List delete')
		inputElement.send_keys(Keys.RETURN)
		inputElement.send_keys('List delete 2')
		inputElement.send_keys(Keys.RETURN)			
		
		##act: element is not visible if we don't hover to the text
		#select button delete with class destroy
		deleteButton = driver.find_elements_by_css_selector(".destroy")[0]
		listTodo = driver.find_elements_by_css_selector(".view label")[0]
		#creat an action to hover into it
		ActionChains(driver).move_to_element(listTodo).click(deleteButton).perform()

		##assert: check todolist lenght after delete
		self.assertEqual(len(driver.find_elements_by_css_selector(".view")),1)
		
		#check added item information
		self.assertEqual(driver.find_elements_by_css_selector("footer span strong")[0].text,'1')
	
	def test_add(self):
		##arrange: open web page, wait for element to load and clear the cache
		driver=self.driver
		driver.get(self.base_url)
		# get new-todo element to input a value
		inputElement = driver.find_elements_by_xpath("//input[@placeholder='What needs to be done?']")[0]
		
		## act: input value to the element
		# type value to the element
		inputElement.send_keys('List todo')
		# press enter
		inputElement.send_keys(Keys.RETURN)
		
		listItem = driver.find_elements_by_class_name("view")
		##assert: 
		if listItem:
			#check input text
			self.assertEqual(listItem[0].text,'List todo')
			
			#check list count
			self.assertEqual(len(listItem),1)
			
			#check added item information
			self.assertEqual(driver.find_elements_by_css_selector("footer span strong")[0].text,'1')
		else:
			self.assertFalse(True)
	
	#Testing edit function by add a value to the field, double click inserted field and edit the value.
	#Assert true if: list updated	
	def test_edit(self):
		##arrange: get the web page, add an item
		driver=self.driver
		driver.get(self.base_url)
		
		#insert todo list to edit
		inputElement = driver.find_elements_by_xpath("//input[@placeholder='What needs to be done?']")[0]
		inputElement.send_keys('List Todo')
		inputElement.send_keys(Keys.RETURN)
		
		##act:get edited todo list item		
		#double click the todo list item
		listTodo = driver.find_elements_by_css_selector(".view label")[0]
		ActionChains(driver).move_to_element(listTodo).double_click(listTodo).perform()
		
		#find element label to edit
		editedLabel = driver.find_elements_by_css_selector(".edit")[0]
		#clear and insert new value
		editedLabel.clear()
		editedLabel.send_keys('List Todo Edited')
		editedLabel.send_keys(Keys.RETURN)
		
		##assert: if first todo list equals edited value
		self.assertEqual(listTodo.text,'List Todo Edited')
		
		##act: element is not visible if we don't hover to the text
		#creat an action to hover into it
		deleteButton = driver.find_elements_by_css_selector(".destroy")[0]
		ActionChains(driver).move_to_element(listTodo).click(deleteButton).perform()
		
	#Testing uncheck function by add an item to the list, click checkbox beside the item
	#Assert true if:
	#- List item not selected
	#- Todo count updated (1 item left)
	def test_uncheckTodo(self):
		##arrange: get the web page, add a list
		driver=self.driver
		driver.get(self.base_url)
		
		#input element and checkit
		inputElement = driver.find_elements_by_xpath("//input[@placeholder='What needs to be done?']")[0]
		inputElement.send_keys('List Todo')
		inputElement.send_keys(Keys.RETURN)
		checkBox = driver.find_elements_by_xpath("//input[@type='checkbox']")
		ActionChains(driver).move_to_element(checkBox[1]).click(checkBox[1]).perform()
		
		#get the first list
		listTodo = driver.find_elements_by_css_selector(".view")[0]
		
		##act: click the checkbox
		ActionChains(driver).move_to_element(checkBox[1]).click(checkBox[1]).perform()
		checked = checkBox[1].is_selected()
		
		##assert: checkbox unselected
		self.assertFalse(checked)
		
		#check todolist item information
		self.assertEqual(driver.find_elements_by_css_selector("footer span strong")[0].text,'1')
	
	#Testing checkbox function by add 2 item to the list, click checkbox beside the one of the item
	#Assert true if:
	#- List item checked
	#- Todo count updated (1 item left)
	def test_checkTodo(self):
		##arrange: get the web page, add some list
		driver=self.driver
		driver.get(self.base_url)
		
		#input an element to check
		inputElement = driver.find_elements_by_xpath("//input[@placeholder='What needs to be done?']")[0]
		inputElement.send_keys('List Todo')
		inputElement.send_keys(Keys.RETURN)	
		inputElement.send_keys('List Todo 2')
		inputElement.send_keys(Keys.RETURN)			
		
		##act: check the checkbox
		checkBox = driver.find_elements_by_xpath("//input[@type='checkbox']")[2]
		ActionChains(driver).move_to_element(checkBox).click(checkBox).perform()
		checked = checkBox.is_selected()
		
		##assert: checkbox value checked
		self.assertTrue(checked)	
		
		#check added item information
		self.assertEqual(driver.find_elements_by_css_selector("footer span strong")[0].text,'1')
	
	#Testing checkall function by add 2 item to the list, click checkall
	#Assert true if: all list checked
	def test_checkall(self):		
		##arrange: get the web page, add some list
		driver=self.driver
		driver.get(self.base_url)
		
		#add some list		
		inputElement = driver.find_elements_by_xpath("//input[@placeholder='What needs to be done?']")[0]
		inputElement.send_keys('Item Todo')
		inputElement.send_keys(Keys.RETURN)		
		inputElement.send_keys('Item Todo 2')
		inputElement.send_keys(Keys.RETURN)
		
		##act: get check all element
		listTodoCheckbox = driver.find_elements_by_xpath("//input[@type='checkbox']")
		#click the checkbox
		ActionChains(driver).move_to_element(listTodoCheckbox[0]).click(listTodoCheckbox[0]).perform()
		
		##assert : loop for each chekcbox
		checked = True
		for item in listTodoCheckbox:
			checked = checked & item.is_selected()
		self.assertTrue(checked)
 		
	#Testing uncheck all function by add 2 items to the list, check all of them and click uncheckall
	#Assert true if:
	#- List item not selected
	#- Todo count updated (2 items left)
	def test_uncheckall(self):		
		##arrange: get the web page, add some list, check all checkbox
		driver=self.driver
		driver.get(self.base_url)
		
		#add some list		
		inputElement = driver.find_elements_by_xpath("//input[@placeholder='What needs to be done?']")[0]
		inputElement.send_keys('Item Todo')
		inputElement.send_keys(Keys.RETURN)		
		inputElement.send_keys('Item Todo 2')
		inputElement.send_keys(Keys.RETURN)
		
		#check all checkbox		
		listTodoCheckbox = driver.find_elements_by_xpath("//input[@type='checkbox']")
		ActionChains(driver).move_to_element(listTodoCheckbox[0]).click(listTodoCheckbox[0]).perform()
		
		##act: unchekced all element
		ActionChains(driver).move_to_element(listTodoCheckbox[0]).click(listTodoCheckbox[0]).perform()
		
		##assert : loop for each chekcbox
		checked = True
		for item in listTodoCheckbox:
			checked = checked & item.is_selected()
		self.assertFalse(checked)
		
		#check todolist item information
		self.assertEqual(driver.find_elements_by_css_selector("footer span strong")[0].text,'2')
 		
	#Testing active button function by add 3 items to the list, check 1 of them and click active
	#Assert true if: 
	#- list length is 2
	#- all checkbox in list length is unchecked
	def test_active(self):
		##arrange: get the web page, add some list, check second list
		driver=self.driver
		driver.get(self.base_url)
		
		#add some list		
		inputElement = driver.find_elements_by_xpath("//input[@placeholder='What needs to be done?']")[0]
		inputElement.send_keys('Item Todo')
		inputElement.send_keys(Keys.RETURN)		
		inputElement.send_keys('Item Todo 2')
		inputElement.send_keys(Keys.RETURN)		
		inputElement.send_keys('Item Todo 3')
		inputElement.send_keys(Keys.RETURN)
		
		#check second list		
		checkBox = driver.find_elements_by_xpath("//input[@type='checkbox']")[2]
		ActionChains(driver).move_to_element(checkBox).click(checkBox).perform()
		
		##act: click active
		activeLink = driver.find_element_by_link_text('Active')
		ActionChains(driver).move_to_element(activeLink).click(activeLink).perform()
		
		#check for each checkbox
		listTodoCheckbox = driver.find_elements_by_xpath("//input[@type='checkbox']")
		checked = True
		for item in listTodoCheckbox:
			checked = checked & item.is_selected()
		self.assertFalse(checked)
			
		##assert all listitem unchecked and list items length is 2	
		self.assertEqual(len(driver.find_elements_by_css_selector(".view")),2)
 		
	#Testing completed button function by add 3 items to the list, check 1 of them and click active
	#Assert true if: list length is 2
	def test_completed(self):
		##arrange: get the web, add some list, check second item
		driver=self.driver
		driver.get(self.base_url)
		
		#add some list		
		inputElement = driver.find_elements_by_xpath("//input[@placeholder='What needs to be done?']")[0]
		inputElement.send_keys('Item Todo')
		inputElement.send_keys(Keys.RETURN)		
		inputElement.send_keys('Item Todo 2')
		inputElement.send_keys(Keys.RETURN)		
		inputElement.send_keys('Item Todo 3')
		inputElement.send_keys(Keys.RETURN)
		
		#check second list		
		checkBox = driver.find_elements_by_xpath("//input[@type='checkbox']")[2]
		ActionChains(driver).move_to_element(checkBox).click(checkBox).perform()
		
		##act: click active
		completedLink = driver.find_element_by_link_text('Completed')
		ActionChains(driver).move_to_element(completedLink).click(completedLink).perform()
					
		##assert list items length is 1	
		self.assertEqual(len(driver.find_elements_by_css_selector(".view")),1)
 		
	#Testing all button function by add 3 items to the list, check 1 of them and click active
	#Assert true if: all list displayed (3 list)
	def test_all(self):
		##arrange: get the web page, add list, check second item
		driver=self.driver
		driver.get(self.base_url)
		
		#add some list		
		inputElement = driver.find_elements_by_xpath("//input[@placeholder='What needs to be done?']")[0]
		inputElement.send_keys('Item Todo')
		inputElement.send_keys(Keys.RETURN)		
		inputElement.send_keys('Item Todo 2')
		inputElement.send_keys(Keys.RETURN)		
		inputElement.send_keys('Item Todo 3')
		inputElement.send_keys(Keys.RETURN)
		
		#check second list		
		checkBox = driver.find_elements_by_xpath("//input[@type='checkbox']")[2]
		ActionChains(driver).move_to_element(checkBox).click(checkBox).perform()
		
		##act: click active
		allLink = driver.find_element_by_link_text('All')
		ActionChains(driver).move_to_element(allLink).click(allLink).perform()
		
		##assert: active list length is 3	
		self.assertEqual(len(driver.find_elements_by_css_selector(".view")),3)
 		
	#Testing clearcompleted button function by add 3 items to the list, check 1 of them and click active
	#Assert true if:
	#-list length is 1
	#todo count updated	
	def test_clearCompleted(self):
		##arrange: get the web page, add list and check some checkbox
		driver=self.driver
		driver.get(self.base_url)
		
		#add some list		
		inputElement = driver.find_elements_by_xpath("//input[@placeholder='What needs to be done?']")[0]
		inputElement.send_keys('Item Todo')
		inputElement.send_keys(Keys.RETURN)		
		inputElement.send_keys('Item Todo 2')
		inputElement.send_keys(Keys.RETURN)	
		inputElement.send_keys('Item Todo 3')
		inputElement.send_keys(Keys.RETURN)
		
		#check all checkbox		
		checkBox = driver.find_elements_by_xpath("//input[@type='checkbox']")
		ActionChains(driver).move_to_element(checkBox[1]).click(checkBox[1]).perform()
		ActionChains(driver).move_to_element(checkBox[3]).click(checkBox[3]).perform()
		
		##act: get the element anc clickit
		clearLink = driver.find_element_by_xpath("//button[contains(text(),'Clear')]")
		ActionChains(driver).move_to_element(clearLink).click(clearLink).perform()		
		
		##assert: listed 1 item in teh list
		self.assertEqual(len(driver.find_elements_by_css_selector(".view")),1)	
		#check todolist item information
		self.assertEqual(driver.find_elements_by_css_selector("footer span strong")[0].text,'1')
		
	@classmethod
	def tearDownClass(cls):
		cls.driver.quit()
	
if __name__ == "__main__":
	unittest.main() 