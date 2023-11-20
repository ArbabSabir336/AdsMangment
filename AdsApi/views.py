from django.shortcuts import render
from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAdminUser
from .models import AdsModel, AdsLocationModel, RequestCount
from .serializers import AdsSerializer, LocationSerializers, RequestCountSerializer


class AdsViews(APIView):
    # permissions_classes = (IsAdminUser,)

    def get_count(self):
        count_instance, created = RequestCount.objects.get_or_create(pk=1)
        return count_instance

    def check_location(self, location_list, count):
        if "karachi" in location_list and count <= 200:
            return True
        elif "lahore" in location_list and count <= 100:
            return True
        elif "multan" in location_list and count <= 100:
            return True
        else:
            return False

    def get(self, request, pk=None):
        ads = AdsModel.objects.get(id=pk)
        locations = AdsLocationModel.objects.filter(ad_id=ads)
        location_list = [location.location_name for location in locations]
        count_instance = self.get_count()
        location = self.check_location(location_list, count_instance.count)
        if location:
            count_instance.count += 1
            count_instance.save()
            if count_instance.count < 2000:
                if pk is not None:
                    ads = get_object_or_404(AdsModel, id=pk)
                    serializer = AdsSerializer(ads)
                    data = {
                        "success": True,
                        "message": "Ads successfully retrieved",
                        "code": "ads_get_by_id_API",
                        "data": serializer.data,
                        "list": location_list
                    }
                    return Response(data, status=status.HTTP_200_OK)
                else:
                    categories = AdsModel.objects.all()
                    serializer = AdsSerializer(categories, many=True)
                    data = {
                        "success": True,
                        "message": "All Ads successfully retrieved",
                        "code": "All_Ads_get_API",
                        "data": serializer.data
                    }
                    return Response(data, status=status.HTTP_200_OK)
            else:
                data = {
                    "success": False,
                    "message": "Request limit exceeded",
                    "code": "Request_limit_exceeded_API",
                }
                return Response(data, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"success": False, "message": "Request limit exceeded", "code": "Request_limit_exceeded_API"},
                            status=status.HTTP_400_BAD_REQUEST)


class AdsCUD(generics.UpdateAPIView, generics.DestroyAPIView, generics.CreateAPIView):
    queryset = AdsModel.objects.all()
    serializer_class = AdsSerializer
    lookup_field = 'id'

    def post(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            list_data = {"success": True, "message": "Ad created successfully", "code": "Ad_Post_API",
                         "data": serializer.data}
            return Response(list_data, status=status.HTTP_200_OK)
        list_data = {"success": False, "message": serializer.errors, "code": "Ad_Post_API"}
        return Response(list_data, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, *args, **kwargs):
        ad = self.get_object()
        serializer = self.get_serializer(ad, data=request.data)
        if serializer.is_valid():
            serializer.save()
            list_data = {"success": True, "message": "Ad updated successfully", "code": "Ad_Update_API",
                         "data": serializer.data}
            return Response(list_data, status=status.HTTP_200_OK)
        list_data = {"success": False, "message": serializer.errors, "code": "Ad_Update_API"}
        return Response(list_data, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        ad = self.get_object(id)
        ad.delete()
        list_data = {"success": True, "message": "Ad deleted successfully", "code": "Ad_Delete_API"}
        return Response(list_data, status=status.HTTP_204_NO_CONTENT)


class LocationViews(APIView):
    def get(self, request):
        location = AdsLocationModel.objects.all()
        serializer = LocationSerializers(location, many=True)
        data = {
            "success": True,
            "message": "Location successfully retrieved",
            "code": "location_get_API",
            "data": serializer.data
        }
        return Response(data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = LocationSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            list_data = {"success": True, "message": "Location created successfully", "code": "location_Post_API",
                         "data": serializer.data}
            return Response(list_data, status=status.HTTP_200_OK)
        else:
            list_data = {"success": False, "message": serializer.errors, "code": "location_Post_API"}
            return Response(list_data, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        location = self.get_object(pk)
        serializer = LocationSerializers(location, data=request.data)
        if serializer.is_valid():
            serializer.save()
            list_data = {"success": True, "message": "Location updated successfully", "code": "location_Update_API",
                         "data": serializer.data}
            return Response(list_data, status=status.HTTP_200_OK)
        else:
            list_data = {"success": False, "message": serializer.errors, "code": "location_Update_API"}
            return Response(list_data, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        location = self.get_object(pk)
        location.delete()
        list_data = {"success": True, "message": "Location deleted successfully", "code": "location_Delete_API"}
        return Response(list_data, status=status.HTTP_204_NO_CONTENT)


class RecounterView(generics.ListAPIView, generics.CreateAPIView):
    def get(self, request):
        count = RequestCount.objects.all()
        serializer = RequestCountSerializer(count, many=True)
        data = {
            "success": True,
            "message": "Count successfully retrieved",
            "code": "count_get_API",
            "data": serializer.data
        }
        return Response(data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = RequestCountSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            list_data = {"success": True, "message": "Count created successfully", "code": "count_Post_API",
                         "data": serializer.data}
            return Response(list_data, status=status.HTTP_200_OK)
        else:
            list_data = {"success": False, "message": serializer.errors, "code": "count_Post_API"}
            return Response(list_data, status=status.HTTP_400_BAD_REQUEST)
