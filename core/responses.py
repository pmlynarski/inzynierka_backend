from rest_framework import status
from rest_framework.response import Response


def response406(data):
    return Response(status=status.HTTP_406_NOT_ACCEPTABLE, data=data)


def response200(data):
    return Response(status=status.HTTP_200_OK, data=data)


def response404(item_name):
    return Response(status=status.HTTP_404_NOT_FOUND, data={'message': '{} could not be found'.format(item_name)})
