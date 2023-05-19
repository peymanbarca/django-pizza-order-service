from rest_framework import serializers
from pizza_order_api.models import PizzaOrderModel, PizzaOrderItemsModel
from rest_framework import status
import datetime

# Model Serializers

class PizzaOrderItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PizzaOrderItemsModel
        fields = ['pizza_flavour','pizza_size','pizza_count','pizza_order_id','item_number']


class PizzaOrderSerializer(serializers.ModelSerializer):
    items = PizzaOrderItemsSerializer(read_only=True, many=True)
    class Meta:
        model = PizzaOrderModel
        fields = '__all__'

# Create Order Serializers

class PizzaOrderItemsCreateSerializer(serializers.Serializer):
    pizza_flavour = serializers.CharField(max_length=30, required=True)
    pizza_size = serializers.CharField(max_length=10, required=True)
    pizza_count = serializers.IntegerField(required=True)


class PizzaOrderCreateSerializer(serializers.Serializer):

    order_info = PizzaOrderSerializer(required=True)
    order_items = serializers.ListField(child=PizzaOrderItemsCreateSerializer(),required=True)

    def create(self, validated_data):
        order = PizzaOrderModel(
                        status='new', customer_name=validated_data['order_info']['customer_name'],
                        customer_email = validated_data['order_info']['customer_email']
                                        if 'customer_email' in (validated_data['order_info']).keys() else None,
                        customer_mobile= validated_data['order_info']['customer_mobile']
                                        if 'customer_mobile' in (validated_data['order_info']).keys() else None
                        )
        order.save()

        items = []
        number = 1
        for item in validated_data['order_items']:
            item = PizzaOrderItemsModel(
                pizza_flavour = item['pizza_flavour'],
                pizza_size = item['pizza_size'],
                pizza_count = item['pizza_count'],
                item_number = number,
                pizza_order = order
            )
            item.save()
            number+=1
            items.append(item)

        order.items = items
        return order


# Update Order Serializers

class PizzaOrderItemsUpdateSerializer(serializers.Serializer):
    pizza_flavour = serializers.CharField(max_length=30, required=True)
    pizza_size = serializers.CharField(max_length=10, required=True)
    pizza_count = serializers.IntegerField(required=True)


class PizzaOrderUpdateSerializer(serializers.Serializer):
    status = serializers.CharField(max_length=50, required=False)
    order_items = serializers.ListField(child=PizzaOrderItemsUpdateSerializer(), required=False)

    def update(self, instance:PizzaOrderModel, validated_data):

        if instance.status == 'delivered':
            raise serializers.ValidationError(
                'It should not be possible to update an order for some statutes of delivery (e.g. delivered)'
                , code=status.HTTP_400_BAD_REQUEST)

        if 'status' in validated_data.keys() and validated_data['status']:
            instance.status = validated_data['status']

        if 'order_items' in validated_data.keys() and validated_data['order_items']:
            new_items_requested = validated_data['order_items']

            # remove all old items of the target order
            PizzaOrderItemsModel.objects.filter(pizza_order_id=instance.pk).delete()

            # persist new items for target order
            number = 1
            new_items = []
            for item in new_items_requested:
                item = PizzaOrderItemsModel(
                    pizza_flavour=item['pizza_flavour'],
                    pizza_size=item['pizza_size'],
                    pizza_count=item['pizza_count'],
                    item_number=number,
                    pizza_order=instance
                )
                item.save()
                number += 1
                new_items.append(item)

            instance.updated_at = datetime.datetime.now()
            instance.items = new_items

        instance.save()
        return instance
