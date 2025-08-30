from rest_framework import serializers
from .models import Product ,Brand , Category , Review

class ProductSerializer(serializers.ModelSerializer):
    
    review = serializers.SerializerMethodField(method_name='get_reviews' , read_only = True)
    
    brand = serializers.CharField(source='brand.name' , read_only=True)
    category = serializers.CharField(source='category.name' , read_only=True)
    user = serializers.CharField(source='user.username' , read_only=True)
    
    brand_id = serializers.PrimaryKeyRelatedField(
        queryset=Brand.objects.all(), source='brand', write_only=True
    )
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), source='category', write_only=True
    )
    class Meta:
        model = Product
        fields = "__all__"
        # fields = ['name' , 'description' , 'price' , 'brand' , 'category']
        
    def get_reviews(self , obj):
        reviews = obj.reviews.all()
        serializer = ReviewSerializer(reviews,many=True)
        return serializer.data


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = "__all__"