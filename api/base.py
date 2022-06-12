'''

作用：主要用于所有接口的公共功能，使用一个基类（父类）
1、处理url
2、重新封装get方法，post方法
3、处理头信息
4、登录
'''
import requests

from setting import BASE_URL, LOGIN_INFO
from loguru import logger
from cacheout import Cache
cache=Cache()
class Base():
    # 实现url功能
    # 实现思路，返回一个完整的url主要包含baseurl+接口路径+（参数）
    '''
    返回一个完整的url
    :param path:接口路径； 如 /admin/auth/login
    :param params: 参数； 如 page=1&limit=20&sort=add_time&order=desc
    :return: full_url : http://121.196.13.152:8080/admin/auth/login
    注：参数有的有，有的没有，所有提前赋值none
    '''
    def get_url(self,path,params=None):
        if params:
            full_url=BASE_URL + path +params
            return full_url
        return BASE_URL+path

    # 重写get方法
    def get(self,url):
        result=None
        response = requests.get(url, headers=self.get_headers())
        try:

           result=response.json()
           logger.success("请求url：{},返回结果：{}".format(url,result))
           return result
        except Exception as e:
          logger.error("请求get异常，返回结果为{}".format(result))
    # 重写post方法
    '''在原来post方法的基础上，新增日志以及直接返回json格式
    :return json格式
    
    '''
    def post(self,url,data):
       result=None
       response = requests.post(url, json=data, headers=self.get_headers())
       try:

           result=response.json()
           logger.success("请求url：{},请求参数：{},返回结果：{}".format(url,data,result))
           return result
       except Exception as e:
           logger.error("请求post方法异常，返回结果为：{}".format(result))



    # 实现所有头信息处理
    def get_headers(self):
        '''
        处理请求头
        :return: 返回的是字典格式的请求头，包括了Content-Type,X-Litemall-Admin-Token
        '''
        # 先设置一个字典存储请求头中数据，因为Content-Type每个都有，可作为字典中默认存储数据
        headers={'Content-Type':'application/json'}
        # 从缓存中取出token
        token=cache.get('token')
        if token:
            headers.update({'X-Litemall-Admin-Token':token})
            return headers
        return headers
    # 实现登录功能
    def login(self):
      '''

      因为登录后会产生一个token值，而后续所有的操作都是在登录的基础上才能进行，所有我们可以将token放在缓存中，如果缓存中没有取到token
      那么重写请求登录接口。。。。。。

      :return:
      '''
      # 第一步要先登录，先拼接url
      login_path="/admin/auth/login"
      Login_url = self.get_url(login_path)
      result = self.post(Login_url, LOGIN_INFO)
      # 万一登录出错，需要捕获异常
      try:
         if result.get('errno') == 0:
             logger.info("请求登录成功,返回数据：{}".format(result))
             token=result.get('data').get('token')
             cache.set('token',token)

         else:
             logger.error("请求登录异常,返回数据：{}".format(result))
             return None
      except Exception as e:
          logger.error("请求登录接口返回异常，异常数据：{}".format(result))
          logger.error("报错信息：{}".format(e))


if __name__ == '__main__':
    base=Base()
    # 测试get_url()
    #result=base.get_url("/admin/auth/login") #http://121.196.13.152:8080/admin/auth/login
   # result=base.get_url("/admin/admin/list?","page=1&limit=20&sort=add_time&order=desc")
    #print(result) # http://121.196.13.152:8080/admin/admin/list?page=1&limit=20&sort=add_time&order=desc

   # 测试post
   #  login_url=base.get_url("/admin/auth/login")
   #  login_data={"username":"admin123","password":"admin123"}
   #  print(base.post(login_url,login_data)) #2022-06-10 20:35:21.881 | SUCCESS  | __main__:post:45 - 请求url：http://121.196.13.152:8080/admin/auth/login,请求参数：{'username': 'admin123', 'password': 'admin123'},返回结果：{'errno': 0, 'data': {'adminInfo': {'nickName': 'admin123', 'avatar': 'https://wpimg.wallstcn.com/f778738c-e4f8-4870-b634-56703b4acafe.gif'}, 'token': 'd82ccd13-dc07-46de-b6f2-48cd20ebf8d0'}, 'errmsg': '成功'}
