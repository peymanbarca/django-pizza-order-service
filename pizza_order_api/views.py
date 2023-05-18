from rest_framework.response import Response
from rest_framework import status, generics, viewsets
from pizza_order_api.models import PizzaOrderModel
from pizza_order_api.serializers import PizzaOrderSerializer, PizzaOrderUpdateSerializer,  PizzaOrderCreateSerializer
import math
from datetime import datetime


class PizzaOrderViewSet(viewsets.GenericViewSet):

    serializer_class = PizzaOrderCreateSerializer
    queryset = PizzaOrderModel.objects.all()

    def get_order(self, pk):
        try:
            order = PizzaOrderModel.objects.get(pk=pk)
            return self.fetch_order_with_items(order)
        except Exception as e:
            print(e)
            return None

    def fetch_order_with_items(self, order):
        order.items = order.pizza_order_id.all()
        return order

    def create(self, request):
        serializer = PizzaOrderCreateSerializer(data=request.data)

        if serializer.is_valid():
            order = serializer.save()
            return Response({"status": "success", "order": PizzaOrderSerializer(instance=order).data}, status=status.HTTP_201_CREATED)
        else:
            return Response({"status": "fail", "message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk):
        order = self.get_order(pk)
        if order is None:
            return Response({"status": "fail", "message": f"Order with Id: {pk} not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = PizzaOrderUpdateSerializer(order, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.validated_data['updated_at'] = datetime.now()
            order = serializer.save()
            return Response({"status": "success", "order": PizzaOrderSerializer(instance=order).data})
        return Response({"status": "fail", "message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk):
        order = self.get_order(pk=pk)
        if order is None:
            return Response({"status": "fail", "message": f"Order with Id: {pk} not found"}, status=status.HTTP_404_NOT_FOUND)

        print(order)
        serializer = PizzaOrderSerializer(order)
        return Response({"status": "success", "order": serializer.data})

    def list(self, request):
        page_num = int(request.GET.get("page", 1))
        limit_num = int(request.GET.get("limit", 10))
        start_num = (page_num - 1) * limit_num
        end_num = limit_num * page_num
        status_param = request.GET.get("status")
        customer_name_param = request.GET.get("customer_name")
        customer_email_param = request.GET.get("customer_email")
        customer_mobile_param = request.GET.get("customer_mobile")
        need_order_items = request.GET.get("need_order_items")

        orders = PizzaOrderModel.objects.all()
        if status_param:
            orders = orders.filter(status=status_param)
        if customer_name_param:
            orders = orders.filter(customer_name__icontains=customer_name_param)
        if customer_email_param:
            orders = orders.filter(customer_email__icontains=customer_email_param)
        if customer_mobile_param:
            orders = orders.filter(customer_mobile__icontains=customer_mobile_param)

        total_orders = orders.count()

        if need_order_items is not None and need_order_items.lower() == 'true':
            orders = [self.fetch_order_with_items(order) for order in orders]

        serializer = PizzaOrderSerializer(orders[start_num:end_num], many=True)
        return Response({
            "status": "success",
            "total": total_orders,
            "page": page_num,
            "last_page": math.ceil(total_orders / limit_num),
            "orders": serializer.data
        })



    def delete(self, request, pk):
        order = self.get_order(pk)
        if order is None:
            return Response({"status": "fail", "message": f"Order with Id: {pk} not found"}, status=status.HTTP_404_NOT_FOUND)

        order.status = 'deleted'
        order.save()
        return Response({"status": "The order {} has been successfully deleted".format(pk)},status=status.HTTP_200_OK)

pizza_order_list = PizzaOrderViewSet.as_view({'get': 'list'})
pizza_order_create = PizzaOrderViewSet.as_view({'post': 'create'})
pizza_order_single = PizzaOrderViewSet.as_view({'get': 'retrieve','patch': 'partial_update','delete': 'delete'})
