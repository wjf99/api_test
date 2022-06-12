# 主要实现用户管理中的测试用例
import unittest
from api.user_manager import UserManager




class TestUserManager(unittest.TestCase):
    user_id=0
    # 在测试类中，此类会首先执行，我们把用户管理接口抽取到此类中，以下所有方法都可以用
    @classmethod
    def setUpClass(cls) -> None:
        cls.user=UserManager()
        #cls.user.login()
        # 因为删除中删除的是添加的username所有需要把username定义出来
        cls.username = 'test0ww1'
        cls.new_username="test006"
    # case1-->添加管理员：只输入用户名和密码
    def test01_add_user(self):
        #1、初始化添加管理员的数据
        #self.username='test01'
        self.password='123456'
        #2、调用添加管理员的接口
        actual_result =self.user.add_user(self.username,self.password)
        data=actual_result.get("data")
        if data:
           self.user_id=data.get("id")
           TestUserManager.user_id=self.user_id
        #3、进行断言
        self.assertEqual(0,actual_result['errno'])
        self.assertEqual(self.username,actual_result.get('data').get('username'))

    # case2-->编辑用户：修改的是用户名称
    def test02_edit_username(self):
        # 修改需要添加id、username、password
        # 调用添加的接口

        actual_result=self.user.edit_user(TestUserManager.user_id,self.new_username,password=123456)
        # 3、进行断言
        self.assertEqual(0, actual_result['errno'])
        self.assertEqual(self.new_username, actual_result.get('data').get('username'))

    # case3-->查询用户列表
    def test03_search_user(self):
        # 调用查询的接口

        actual_result = self.user.search_user()
        # 3、进行断言
        self.assertEqual(0, actual_result['errno'])
        self.assertEqual(self.new_username, actual_result.get('data').get('list')[0].get('username'))
    # case3-->删除用户：删除指定id的用户名
    def test04_delete_user(self):
       # 初始化要删除的id,和username
       # 调用删除管理员的接口
       actual_result = self.user.delete_user(TestUserManager.user_id, self.new_username)
       self.assertEqual(0,actual_result['errno'])




if __name__ == '__main__':
    unittest.main()