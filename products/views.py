from django.shortcuts import render , get_object_or_404 
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework import viewsets , status , mixins
from rest_framework.permissions import IsAuthenticated , IsAdminUser
from rest_framework.decorators import permission_classes
from math import ceil
from django.db.models import Avg

from .models import Product , Category , Brand , Review
from .serializers import ProductSerializer
from .filters import ProductsFilters

# Create your views here.

@api_view(['GET'])
def get_all_products(request):
    if request.method == "GET":
        filterset = ProductsFilters(request.GET , queryset=Product.objects.all().order_by('id'))
        count = filterset.qs.count()
        
            # Pagination
        paginator = PageNumberPagination()
        paginator.page_size = 2
        queryset = paginator.paginate_queryset(filterset.qs , request)
        
        serializer = ProductSerializer(queryset , many=True)
        current_page = int(request.GET.get('page' , 1 ))
        total_pages = ceil(count / paginator.page_size)
        
        return Response({'Products':serializer.data ,
                        'pages': total_pages ,
                        'current_page': current_page,
                        'products':count ,
                        })

@api_view(['GET'])
def get_product_by_id(request , pk):
    if request.method == 'GET':
        product = get_object_or_404(Product , id=pk)
        serializer = ProductSerializer(product)
        return Response({'Product':serializer.data})


@api_view(['POST'])
@permission_classes([IsAuthenticated , IsAdminUser])
def add_product(request):
    serializer = ProductSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=request.user)
        return Response(
            {'Product': serializer.data},
            status=status.HTTP_201_CREATED
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# @api_view(['PUT'])
# @permission_classes([IsAuthenticated])
# def update_product(request , pk):
#     product = get_object_or_404(Product ,id=pk)
#     if product.user != request.user:
#         return Response({f'error':'Sorry {request.user} You Can Not Update This Product'},
#                         status=status.HTTP_403_FORBIDDEN)
#     product.name = request.data['name']
#     product.description = request.data['description']
#     product.price = request.data['price']
    
#     product.brand = Brand.objects.get(pk=request.data['brand_id'])
#     product.category = Category.objects.get(pk=request.data['category_id'])
    
#     product.ratings = request.data['ratings']
#     product.stock = request.data['stock']
#     product.save()
#     serializer = ProductSerializer(product)
#     return Response({'Product':serializer.data})


@api_view(['PUT'])
@permission_classes([IsAuthenticated, IsAdminUser])
def update_product(request, pk):
    product = get_object_or_404(Product, id=pk)

    if product.user != request.user:
        return Response(
            {f'error': f'Sorry {request.user}, You cannot update this product'},
            status=status.HTTP_403_FORBIDDEN
        )

    product.name = request.data['name']
    product.description = request.data['description']
    product.price = request.data['price']
    product.ratings = request.data['ratings']
    product.stock = request.data['stock']

    brand_name = request.data.get('brand')
    if brand_name:
        brand_obj, created = Brand.objects.get_or_create(name=brand_name)
        product.brand = brand_obj

    category_name = request.data.get('category')
    if category_name:
        category_obj, created = Category.objects.get_or_create(name=category_name)
        product.category = category_obj

    product.save()

    serializer = ProductSerializer(product, many=False)
    return Response({'Product': serializer.data})


@api_view(['DELETE'])
@permission_classes([IsAuthenticated , IsAdminUser])
def delete_product(request , pk):
    product = get_object_or_404(Product,id=pk)
    if product.user == request.user:
        product.delete()
        return Response({"Seccess":"Delete Is Successfully"} , status=status.HTTP_204_NO_CONTENT)
    return Response(
        {f'error': f'Sorry {request.user}, You cannot Delete this product'},
        status=status.HTTP_403_FORBIDDEN
    )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_review(request , pk):
    user = request.user
    product = get_object_or_404(Product , id=pk)
    data = request.data
    review = product.reviews.filter(user=user)  
    
    if data['rating'] <= 0 or data['rating'] >= 5 :
        return Response({'error' : 'please select between 1 to 5 only'} , status=status.HTTP_400_BAD_REQUEST)
    elif review.exists() :
        new_review = {'rating' : data['rating'] , 'comment':data['comment']}
        review.update(**new_review)

        rating = product.reviews.aggregate (avg_ratings = Avg('rating'))
        product.ratings = rating['avg_ratings']
        product.save()
        return Response({'details': 'Product review Updated'})
    else:
        Review.objects.create(
            user = user,
            product = product,
            rating = data['rating'],
            comment = data['comment'],
        )
        rating = product.reviews.aggregate (avg_ratings = Avg('rating'))
        product.ratings = rating['avg_ratings']
        product.save()
        return Response({'details': 'Product review Created'})


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_review(request , pk):
    user = request.user
    product = get_object_or_404(Product , id=pk)
    review = product.reviews.filter(user=user)
    if review.exists():
        review.delete()
        rating = product.reviews.aggregate (avg_ratings = Avg('rating'))
        if rating['avg_ratings'] is None :
            rating['avg_ratings'] = 0
            product.ratings = rating['avg_ratings']
            product.save()
            return Response({'details' : 'Product Review deleted'})
        return Response({'error' : 'Review Not found'} , status=status.HTTP_404_NOT_FOUND)


