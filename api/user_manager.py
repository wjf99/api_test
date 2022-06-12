# 此类主要实现用户的增删改查
# 导入基础类
from loguru import logger

from api.base import Base
# 继承基础类
class UserManager(Base):
    # 将基础数据定义好,初始化接口路径

    def __init__(self):
        self.add_user_url=self.get_url("/admin/admin/create")
        self.search_user_url=self.get_url("/admin/admin/list?page=1&limit=20&sort=add_time&order=desc")
        self.edit_user_url=self.get_url("/admin/admin/update")
        self.delete_user_url=self.get_url("/admin/admin/delete")

    # 新增用户
    def add_user(self,username,password,**kwargs):
        # 把必填项存储在字典中，选填项存在可变参数中**kwargs
        '''
        请求添加管理员的接口
        :param username:
        :param password:
        :param kwargs:
        :return: 添加管理员接口返回的是json数据
        '''
        user_data={"username":username,"password":password}
        if kwargs:
            logger.info("添加管理员可选参数:{}".format(**kwargs))
            user_data.update(**kwargs)
        return self.post(self.add_user_url,user_data)
     # 查询用户
    def search_user(self):
        '''
        请求的是查询接口
        :return: 查询管理员返回的是json数据
        '''


        return self.get(self.search_user_url)
    # 修改用户
    def edit_user(self,id,username,password,**kwargs):
        '''
        请求的是修改接口
        :return: 修改管理员返回的是json数据
        '''
        user_data={"id":id,"username":username,"password":password}
        if kwargs:
            user_data.update(**kwargs)
        return self.post(self.edit_user_url,user_data)
    # 删除用户
    def delete_user(self,id,username,**kwargs):
        '''
         请求的是删除的接口
         ：:return:删除管理员返回的是json数据
         '''
        user_data={"id":id,"username":username}
        if kwargs:
            user_data.update(**kwargs)
        return  self.post(self.delete_user_url,user_data)

