from rest_framework import generics
from .models import Restaurant
from .serializers import RestaurantSerializer
from math import radians, sin, cos, sqrt, atan2
from rest_framework.response import Response
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser
from torchvision import models, transforms
from PIL import Image
import torch
import requests

def haversine_distance(lat1, lon1, lat2, lon2):
    R = 6371  # Earth's radius in kilometers

    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    distance = R * c

    return distance

class RestaurantDetail(generics.RetrieveAPIView):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer

class RestaurantList(generics.ListAPIView):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    pagination_class = None  # Add custom pagination later

class RestaurantSearch(generics.ListAPIView):
    serializer_class = RestaurantSerializer
    pagination_class = None

    def get_queryset(self):
        lat = float(self.request.query_params.get('lat', 0))
        lng = float(self.request.query_params.get('lng', 0))
        radius = float(self.request.query_params.get('radius', 3))  # Default radius is 3km

        # Get all restaurants
        restaurants = Restaurant.objects.all()
        
        # Filter restaurants within radius
        nearby_restaurants = []
        for restaurant in restaurants:
            distance = haversine_distance(
                lat, lng,
                restaurant.latitude, restaurant.longitude
            )
            # print(distance)
            if distance <= radius:
                nearby_restaurants.append(restaurant)
        return nearby_restaurants

@api_view(['POST'])
@parser_classes([MultiPartParser])
def classify_image(request):
    image = request.FILES.get('image')
    if not image:
        return Response({'error': 'No image uploaded'}, status=400)

    try:
        # Load and preprocess image
        img = Image.open(image).convert('RGB')
        transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
        ])
        input_tensor = transform(img).unsqueeze(0)

        # Load a pretrained model
        model = models.resnet18(pretrained=True)
        model.eval()

        with torch.no_grad():
            outputs = model(input_tensor)
            predicted_idx = torch.argmax(outputs[0]).item()

        # Load ImageNet labels
        LABELS_URL = "https://raw.githubusercontent.com/pytorch/hub/master/imagenet_classes.txt"
        labels = requests.get(LABELS_URL).text.splitlines()
        label = labels[predicted_idx]

        print("Label:")
        print(label)

        # Simple mapping from ImageNet labels to cuisines
        cuisine_keywords = {
            'pizza': 'Pizza',
            'sushi': 'Japanese',
            'ice cream': 'Desserts',
            'burger': 'American',
            'pasta': 'Italian',
            'taco': 'Mexican',
            'noodle': 'Chinese',
            'rice': 'Asian',
            'salad': 'Healthy',
            'sandwich': 'Fast Food',
            'cake': 'Desserts',
            'bread': 'Bakery',
            'coffee': 'Cafe',
            'tea': 'Cafe',
            'chocolate': 'Desserts',
            'cookie': 'Desserts',
            'donut': 'Desserts',
            'french fries': 'Fast Food',
            'hot dog': 'Fast Food',
            'meat': 'BBQ',
            'chicken': 'BBQ',
            'fish': 'Seafood',
            'shrimp': 'Seafood',
            'crab': 'Seafood',
            'lobster': 'Seafood',
            'vegetable': 'Vegetarian',
            'fruit': 'Healthy',
            'apple': 'Healthy',
            'orange': 'Healthy',
            'banana': 'Healthy',
            'strawberry': 'Healthy',
            'grape': 'Healthy',
            'watermelon': 'Healthy',
            'pineapple': 'Healthy',
            'mango': 'Healthy',
            'peach': 'Healthy',
            'pear': 'Healthy',
            'cherry': 'Healthy',
            'lemon': 'Healthy',
            'lime': 'Healthy',
            'coconut': 'Healthy',
            'kiwi': 'Healthy',
            'melon': 'Healthy',
            'blueberry': 'Healthy',
            'raspberry': 'Healthy',
            'blackberry': 'Healthy',
            'cranberry': 'Healthy',
            'pomegranate': 'Healthy',
            'fig': 'Healthy',
            'date': 'Healthy',
            'prune': 'Healthy',
            'raisin': 'Healthy',
            'currant': 'Healthy',
            'apricot': 'Healthy',
            'plum': 'Healthy',
            'nectarine': 'Healthy',
            'persimmon': 'Healthy',
            'guava': 'Healthy',
            'papaya': 'Healthy',
            'passion fruit': 'Healthy',
            'dragon fruit': 'Healthy',
            'star fruit': 'Healthy',
            'jackfruit': 'Healthy',
            'durian': 'Healthy',
            'lychee': 'Healthy',
            'rambutan': 'Healthy',
            'mangosteen': 'Healthy',
            'longan': 'Healthy',
            'loquat': 'Healthy',
            'kumquat': 'Healthy',
            'tangerine': 'Healthy',
            'clementine': 'Healthy',
            'mandarin': 'Healthy',
            'grapefruit': 'Healthy',
            'pomelo': 'Healthy',
            'lime': 'Healthy',
            'lemon': 'Healthy',
            'orange': 'Healthy',
            'tangerine': 'Healthy',
            'clementine': 'Healthy',
            'mandarin': 'Healthy',
            'grapefruit': 'Healthy',
            'pomelo': 'Healthy',
            'lime': 'Healthy',
            'lemon': 'Healthy',
        }

        matched_cuisine = None
        for keyword, cuisine in cuisine_keywords.items():
            if keyword in label.lower():
                matched_cuisine = cuisine
                break

        if not matched_cuisine:
            return Response({
                'error': f'Could not determine cuisine from: {label}',
                'detected_label': label
            }, status=400)

        # Query matching restaurants
        restaurants = Restaurant.objects.filter(cuisines__icontains=matched_cuisine)
        serializer = RestaurantSerializer(restaurants, many=True)
        
        return Response({
            'cuisine': matched_cuisine,
            'detected_label': label,
            'restaurants': serializer.data
        })

    except Exception as e:
        return Response({
            'error': f'Error processing image: {str(e)}'
        }, status=500)
