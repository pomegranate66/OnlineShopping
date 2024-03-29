import jsonpickle
from django.http import JsonResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.views import View
from django_redis import get_redis_connection

from apps.goods.models import GoodsSKU


class AddView(View):
    def post(self, request):
        #         判断用户是否登录
        if 'user' not in request.session:
            return JsonResponse({'res': 0, 'errmsg': '请先登录'})
        user = jsonpickle.loads(request.session.get('user', ''))

        #        获取数据
        sku_id = request.POST.get('sku_id')
        count = request.POST.get('count')

        #         数据校验
        if not all([sku_id, count]):
            return JsonResponse({'res': 1, 'errmsg': '数据不完整'})

        #         校验添加的商品书
        try:
            count = int(count)
        except Exception as e:
            #             数目错误
            return JsonResponse({'res': 2, 'errmsg': '商品数目出错'})
        #         检验商品是否存在
        try:
            sku = GoodsSKU.objects.get(id=sku_id)
        except GoodsSKU.DoesNotExist as e:
            return JsonResponse({'res': 3, 'errmsg': '商品不存在'})

        #         业务处理 ：添加购物记录
        connect = get_redis_connection('default')
        cart_key = 'cart_%d' % user.id
        #         先尝试获取sku_id的值 -- 》hget.cart_key属性
        # 如果sku_id在hash中不存在，hget返回None
        cart_count = connect.hget(cart_key, sku_id)
        if cart_count:
            #             累加购物车的商品的数目
            count = int(cart_count)
        #         校验库存
        if count > sku.stock:
            return JsonResponse({'res': 4, 'errmsg': '商品库存不足'})
        #         设置hash中sku_id对应的值
        # hset --> 如果sku_id已经存在，更新数据，如果sku_id不存在，添加数据
        connect.hset(cart_key, sku_id, count)
        #         计算用户购物车商品的条目书
        total_count = connect.hlen(cart_key)
        #         返回应答
        return JsonResponse({'res': 5, 'total_count': total_count, 'message': '添加成功'})


class InfoView(View):
    '''购物车页面'''

    def get(self, request):
        '''显示'''
        #         获取登录的用户
        if 'user' not in request.session:
            return redirect('/user/login/')
        user = jsonpickle.loads(request.session.get('user'))
        #         获取用户购物车中的商品的信息
        conn = get_redis_connection('default')
        cart_key = 'cart_%d' % user.id
        # {'商品id': 商品数量}
        cart_dict = conn.hgetall(cart_key)

        skus = []
        #         保存用户购物车中的总数和总价格
        total_count = 0
        total_price = 0
        #         遍历获取商品的信息
        for sku_id, count in cart_dict.items():
            #             根据商品的id获取商品的信息
            sku = GoodsSKU.objects.get(id=sku_id)
            #             计算商品的小记
            count = int(count)
            amount = sku.price * count
            # 动态给sku对象增加 一个属性amount,保存商品的小计
            sku.amount = amount
            # 动态给sku对象增加一个属性count,保存购物车中对应商品的数量
            sku.count = count
            skus.append(sku)
            #            累加计算商品的总数目和价格
            total_count += int(count)
            total_price += amount
        context = {
            'total_count': total_count,
            'total_price': total_price,
            'skus': skus
        }
        return render(request, 'cart.html', context)


class UpdateView(View):
    '''购物车更新数据'''
    def post(self, request):
        # 判断用户是否登录
        if 'user' not in request.session:
            return JsonResponse({'res': 0, 'errmsg': '请先登录'})

        user = jsonpickle.loads(request.session.get('user', ''))

        # 获取数据
        sku_id = request.POST.get('sku_id')
        count = request.POST.get('count')

        # 数据校验
        if not all([sku_id, count]):
            return JsonResponse({'res': 1, 'errmsg': '数据不完整'})

        # 校验添加的商品数量
        try:
            count = int(count)
        except Exception as e:
            # 数目出错
            return JsonResponse({'res': 2, 'errmsg': '商品数目出错'})

        # 校验商品是否存在
        try:
            sku = GoodsSKU.objects.get(id=sku_id)
        except GoodsSKU.DoesNotExist:
            return JsonResponse({'res': 3, 'errmsg': '商品不存在'})

        # 校验库存
        if count > sku.stock:
            return JsonResponse({'res': 4, 'errmsg': '商品库存不足'})

        # 业务处理：更新购物车记录
        conn = get_redis_connection('default')
        cart_key = 'cart_%d' % user.id
        conn.hset(cart_key, sku_id, count)  # 更新

        # 计算用户购物车总的商品的总件数 {'1':5,'2':3}
        total_count = 0
        vals = conn.hvals(cart_key)
        for val in vals:
            total_count += int(val)

        # 返回应答
        return JsonResponse({'res': 5, 'total_count': total_count, 'message': '更新成功'})


class DeleteView(View):
    '''购物车记录删除'''

    def post(self, request):
        # 判断用户是否登录
        if 'user' not in request.session:
            return JsonResponse({'res': 0, 'errmsg': '请先登录'})
        user = jsonpickle.loads(request.session.get('user', ''))

        # 接收参数
        sku_id = request.POST.get('sku_id')

        # 数据校验
        if not sku_id:
            return JsonResponse({'res': 1, 'error': '无效的商品ID'})

        # 校验商品是否存在
        try:
            sku = GoodsSKU.objects.get(id=sku_id)
        except GoodsSKU.DoesNotExist:
            # 商品不存在
            return JsonResponse({'res': 2, 'errmsg': '商品不存在'})

        # 业务处理：删除购物车记录
        conn = get_redis_connection('default')
        cart_key = 'cart_%d' % user.id

        # 删除 hdel
        conn.hdel(cart_key, sku_id)

        # 计算用户购物车总的商品的总件数 {'1':5,'2':3}
        total_count = 0
        vals = conn.hvals(cart_key)
        for val in vals:
            total_count += int(val)

        # 返回应答
        return JsonResponse({'res': 3, 'total_count': total_count, 'message': '删除成功'})
