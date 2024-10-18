from rest_framework import serializers
from apps.shop.models import (
    fashionMallSPU, fashionMallSKU, fashionMallSKUSpecs
)
from .spuimage import fashionMallSPUImageSerializer


class fashionMallSKUSpecsSerializer(serializers.ModelSerializer):

    class Meta:
        model = fashionMallSKUSpecs
        fields = '__all__'


class fashionMallSKUSerializer(serializers.ModelSerializer):

    class Meta:
        model = fashionMallSKU
        fields = '__all__'


class fashionMallSPUSerializer(serializers.ModelSerializer):

    price = serializers.DecimalField(
        max_digits=10, decimal_places=2, read_only=True
    )
    dash_price = serializers.DecimalField(
        max_digits=10, decimal_places=2, read_only=True
    )
    stock = serializers.IntegerField(read_only=True)
    sale = serializers.IntegerField(read_only=True)
    img = serializers.ImageField(
        source='fashionMallspuimage_set.first.image',
        read_only=True
    )

    class Meta:
        model = fashionMallSPU
        fields = '__all__'


class fashionMallSPUDetailSerializer(fashionMallSPUSerializer):
    # 商品详情序列化
    fashionMallspuimage_set = fashionMallSPUImageSerializer(many=True, read_only=True)
    specs = serializers.SerializerMethodField()
    skus = serializers.SerializerMethodField()

    def get_specs(self, obj):
        # 获取规格
        specs = fashionMallSKUSpecs.objects.filter(sku__spu=obj).distinct()
        specs_list = specs.values('value__specs__name', 'value__value', 'value__id')
        return self.merge_dicts(specs_list)
    
    def merge_dicts(self, dicts):
        # 合并字典
        item_dict = {}
        for item in dicts:
            if item['value__specs__name'] not in item_dict:
                item_dict[item['value__specs__name']] = []
                item_dict[item['value__specs__name']].append(item)
            elif item not in item_dict[item['value__specs__name']]:
                item_dict[item['value__specs__name']].append(item)
        return item_dict
    
    def get_skus(self, obj):
        # 获取sku
        skus = obj.fashionMallsku_set.filter(is_sale=True)
        item_dict = {}
        for sku in skus:
            specs = sku.fashionMallskuspecs_set.all()
            if specs.exists():
                for spec in specs:
                    value_ids = tuple(spec.value.order_by('id').values_list('id', flat=True))
                    value_ids = ','.join(str(i) for i in value_ids)
                    item_dict[value_ids] = fashionMallSKUSerializer(spec.sku, many=False).data
            elif skus.count() == 1:
                item_dict['0'] = fashionMallSKUSerializer(sku, many=False).data
        return item_dict